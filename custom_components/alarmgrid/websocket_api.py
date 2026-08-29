"""WebSocket API for the AlarmGrid frontend."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import voluptuous as vol
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .alarm_models import AlarmPriority
from .const import DOMAIN
from .rule_management import (
    delete_rules,
    export_rules_csv,
    import_rules_csv,
    remove_per_rule_entity_registry_entries,
)
from .rule_preview import async_preview_rule


def async_register_websocket_api(hass: HomeAssistant) -> None:
    """Register websocket commands once."""

    domain_data = hass.data.setdefault(DOMAIN, {})
    if domain_data.get("websocket_registered"):
        return
    websocket_api.async_register_command(hass, websocket_list_alarms)
    websocket_api.async_register_command(hass, websocket_list_history)
    websocket_api.async_register_command(hass, websocket_list_rules)
    websocket_api.async_register_command(hass, websocket_create_rule)
    websocket_api.async_register_command(hass, websocket_update_rule)
    websocket_api.async_register_command(hass, websocket_test_rule)
    websocket_api.async_register_command(hass, websocket_delete_rule)
    websocket_api.async_register_command(hass, websocket_delete_rules)
    websocket_api.async_register_command(hass, websocket_export_rules)
    websocket_api.async_register_command(hass, websocket_import_rules)
    websocket_api.async_register_command(hass, websocket_acknowledge)
    websocket_api.async_register_command(hass, websocket_acknowledge_all)
    websocket_api.async_register_command(hass, websocket_silence)
    websocket_api.async_register_command(hass, websocket_shelve)
    websocket_api.async_register_command(hass, websocket_unshelve)
    websocket_api.async_register_command(hass, websocket_disable)
    websocket_api.async_register_command(hass, websocket_enable)
    websocket_api.async_register_command(hass, websocket_test_sound)
    websocket_api.async_register_command(hass, websocket_export_history)
    domain_data["websocket_registered"] = True


def _runtime(hass: HomeAssistant) -> Any:
    for key, value in hass.data.get(DOMAIN, {}).items():
        if key not in {"services_registered", "websocket_registered"}:
            return value
    raise HomeAssistantError("AlarmGrid is not loaded")


@websocket_api.websocket_command(
    {vol.Required("type"): "alarmgrid/list_alarms"}
)
@websocket_api.async_response
async def websocket_list_alarms(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """List alarms."""

    runtime = _runtime(hass)
    connection.send_result(
        msg["id"],
        {
            "alarms": runtime.engine.list_alarms(include_normal=True),
            "sound": runtime.sound_manager.as_dict(),
        },
    )


@websocket_api.websocket_command(
    {
        vol.Required("type"): "alarmgrid/list_history",
        vol.Optional("limit", default=250): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=5000)
        ),
        vol.Optional("start_time"): str,
        vol.Optional("end_time"): str,
        vol.Optional("priority"): str,
        vol.Optional("area"): str,
        vol.Optional("system"): str,
        vol.Optional("event_type"): str,
    }
)
@websocket_api.async_response
async def websocket_list_history(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """List alarm history."""

    runtime = _runtime(hass)
    events = await runtime.history_store.query_events(
        limit=msg["limit"],
        start_time=_parse_datetime(msg.get("start_time")),
        end_time=_parse_datetime(msg.get("end_time")),
        priority=msg.get("priority"),
        area=msg.get("area"),
        system=msg.get("system"),
        event_type=msg.get("event_type"),
    )
    connection.send_result(msg["id"], {"events": [event.to_dict() for event in events]})


@websocket_api.websocket_command(
    {vol.Required("type"): "alarmgrid/list_rules"}
)
@websocket_api.async_response
async def websocket_list_rules(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """List alarm rules."""

    runtime = _runtime(hass)
    connection.send_result(
        msg["id"],
        {"rules": [rule.to_dict() for rule in runtime.engine.rules.values()]},
    )


@websocket_api.websocket_command(
    {vol.Required("type"): "alarmgrid/export_rules"}
)
@websocket_api.async_response
async def websocket_export_rules(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Export every alarm rule as CSV."""

    runtime = _runtime(hass)
    connection.send_result(
        msg["id"], {"csv": export_rules_csv(runtime.engine.rules.values())}
    )


@websocket_api.websocket_command(
    {
        vol.Required("type"): "alarmgrid/import_rules",
        vol.Required("csv"): str,
    }
)
@websocket_api.async_response
async def websocket_import_rules(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Import rules from CSV, updating rules whose IDs already exist."""

    runtime = _runtime(hass)
    rules = import_rules_csv(msg["csv"])
    created_ids: list[str] = []
    updated_ids: list[str] = []
    for rule in rules:
        rule_data = rule.to_dict()
        if rule.id in runtime.engine.rules:
            await runtime.engine.update_rule(rule.id, rule_data)
            updated_ids.append(rule.id)
        else:
            await runtime.engine.create_rule(rule_data)
            created_ids.append(rule.id)

    await runtime.rule_store.async_save_rules(runtime.engine.rules.values())
    await runtime.async_refresh_rules()
    connection.send_result(
        msg["id"],
        {
            "imported_count": len(rules),
            "created_ids": created_ids,
            "updated_ids": updated_ids,
        },
    )


@websocket_api.websocket_command(
    {
        vol.Required("type"): "alarmgrid/create_rule",
        vol.Required("rule"): dict,
    }
)
@websocket_api.async_response
async def websocket_create_rule(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Create an alarm rule."""

    runtime = _runtime(hass)
    rule = await runtime.engine.create_rule(msg["rule"])
    await runtime.rule_store.async_save_rules(runtime.engine.rules.values())
    await runtime.async_refresh_rules()
    connection.send_result(msg["id"], {"rule": rule.to_dict()})


@websocket_api.websocket_command(
    {
        vol.Required("type"): "alarmgrid/test_rule",
        vol.Required("rule"): dict,
        vol.Optional("rule_id"): str,
    }
)
@websocket_api.async_response
async def websocket_test_rule(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Evaluate the submitted draft without saving or changing runtime state."""
    runtime = _runtime(hass)
    try:
        preview = await async_preview_rule(
            hass, runtime.engine, msg["rule"], rule_id=msg.get("rule_id")
        )
    except (TypeError, ValueError) as err:
        connection.send_error(msg["id"], "invalid_rule", str(err))
        return
    connection.send_result(msg["id"], preview)


@websocket_api.websocket_command(
    {
        vol.Required("type"): "alarmgrid/update_rule",
        vol.Required("rule_id"): str,
        vol.Required("changes"): dict,
    }
)
@websocket_api.async_response
async def websocket_update_rule(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Update an alarm rule."""

    runtime = _runtime(hass)
    rule = await runtime.engine.update_rule(msg["rule_id"], msg["changes"])
    await runtime.rule_store.async_save_rules(runtime.engine.rules.values())
    await runtime.async_refresh_rules()
    connection.send_result(msg["id"], {"rule": rule.to_dict()})


@websocket_api.websocket_command(
    {
        vol.Required("type"): "alarmgrid/delete_rule",
        vol.Required("rule_id"): str,
    }
)
@websocket_api.async_response
async def websocket_delete_rule(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Delete an alarm rule."""

    runtime = _runtime(hass)
    rule = runtime.engine.rules[msg["rule_id"]]
    await runtime.engine.delete_rule(msg["rule_id"])
    remove_per_rule_entity_registry_entries(hass, runtime.entry_id, [rule])
    await runtime.rule_store.async_save_rules(runtime.engine.rules.values())
    await runtime.async_refresh_rules()
    connection.send_result(msg["id"], {"deleted": True})


@websocket_api.websocket_command(
    {
        vol.Required("type"): "alarmgrid/delete_rules",
        vol.Required("rule_ids"): [str],
    }
)
@websocket_api.async_response
async def websocket_delete_rules(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Delete selected alarm rules."""

    runtime = _runtime(hass)
    result = await delete_rules(runtime.engine, rule_ids=msg["rule_ids"])
    removed_entity_ids = remove_per_rule_entity_registry_entries(
        hass, runtime.entry_id, result.deleted_rules
    )

    if result.deleted_rules:
        await runtime.rule_store.async_save_rules(runtime.engine.rules.values())
        await runtime.async_refresh_rules()

    connection.send_result(
        msg["id"],
        {
            "deleted_rule_ids": result.deleted_rule_ids,
            "deleted_count": len(result.deleted_rules),
            "skipped_rule_ids": result.skipped_rule_ids,
            "removed_entity_ids": removed_entity_ids,
            "removed_entity_count": len(removed_entity_ids),
        },
    )


@websocket_api.websocket_command(
    {
        vol.Required("type"): "alarmgrid/acknowledge",
        vol.Required("rule_id"): str,
        vol.Optional("comment"): str,
    }
)
@websocket_api.async_response
async def websocket_acknowledge(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Acknowledge one alarm."""

    await _runtime(hass).engine.acknowledge_alarm(
        msg["rule_id"], operator=connection.user.id, comment=msg.get("comment")
    )
    connection.send_result(msg["id"], {"acknowledged": True})


@websocket_api.websocket_command(
    {
        vol.Required("type"): "alarmgrid/acknowledge_all",
        vol.Optional("priority"): str,
        vol.Optional("area"): str,
        vol.Optional("comment"): str,
    }
)
@websocket_api.async_response
async def websocket_acknowledge_all(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Acknowledge all matching alarms."""

    count = await _runtime(hass).engine.acknowledge_all(
        priority=msg.get("priority"),
        area=msg.get("area"),
        operator=connection.user.id,
        comment=msg.get("comment"),
    )
    connection.send_result(msg["id"], {"acknowledged": count})


@websocket_api.websocket_command(
    {
        vol.Required("type"): "alarmgrid/silence",
        vol.Optional("duration_seconds"): vol.All(vol.Coerce(int), vol.Range(min=1)),
    }
)
@websocket_api.async_response
async def websocket_silence(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Silence horn."""

    await _runtime(hass).engine.silence_horn(
        msg.get("duration_seconds"), operator=connection.user.id
    )
    connection.send_result(msg["id"], {"silenced": True})


@websocket_api.websocket_command(
    {
        vol.Required("type"): "alarmgrid/shelve",
        vol.Required("rule_id"): str,
        vol.Required("duration_minutes"): vol.All(vol.Coerce(int), vol.Range(min=1)),
        vol.Optional("comment"): str,
    }
)
@websocket_api.async_response
async def websocket_shelve(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Shelve alarm."""

    await _runtime(hass).engine.shelve_alarm(
        msg["rule_id"],
        duration_minutes=msg["duration_minutes"],
        operator=connection.user.id,
        comment=msg.get("comment"),
    )
    connection.send_result(msg["id"], {"shelved": True})


@websocket_api.websocket_command(
    {
        vol.Required("type"): "alarmgrid/unshelve",
        vol.Required("rule_id"): str,
    }
)
@websocket_api.async_response
async def websocket_unshelve(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Restore a temporarily shelved alarm."""

    await _runtime(hass).engine.unshelve_alarm(
        msg["rule_id"], operator=connection.user.id
    )
    connection.send_result(msg["id"], {"unshelved": True})


@websocket_api.websocket_command(
    {
        vol.Required("type"): "alarmgrid/disable",
        vol.Required("rule_id"): str,
        vol.Optional("comment"): str,
    }
)
@websocket_api.async_response
async def websocket_disable(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Disable an alarm until it is manually enabled."""

    await _runtime(hass).engine.disable_alarm(
        msg["rule_id"], operator=connection.user.id, comment=msg.get("comment")
    )
    connection.send_result(msg["id"], {"disabled": True})


@websocket_api.websocket_command(
    {
        vol.Required("type"): "alarmgrid/enable",
        vol.Required("rule_id"): str,
    }
)
@websocket_api.async_response
async def websocket_enable(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Re-enable a disabled alarm."""

    await _runtime(hass).engine.enable_alarm(
        msg["rule_id"], operator=connection.user.id
    )
    connection.send_result(msg["id"], {"enabled": True})


@websocket_api.websocket_command(
    {
        vol.Required("type"): "alarmgrid/test_sound",
        vol.Optional("priority", default=AlarmPriority.CRITICAL.value): vol.In(
            [priority.value for priority in AlarmPriority]
        ),
    }
)
@websocket_api.async_response
async def websocket_test_sound(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Test sound."""

    await _runtime(hass).sound_manager.test_sound(AlarmPriority(msg["priority"]))
    connection.send_result(msg["id"], {"played": True})


@websocket_api.websocket_command(
    {
        vol.Required("type"): "alarmgrid/export_history",
        vol.Optional("start_time"): str,
        vol.Optional("end_time"): str,
        vol.Optional("format", default="csv"): vol.In(["csv", "json"]),
    }
)
@websocket_api.async_response
async def websocket_export_history(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Export history rows."""

    runtime = _runtime(hass)
    events = await runtime.history_store.query_events(
        start_time=_parse_datetime(msg.get("start_time")),
        end_time=_parse_datetime(msg.get("end_time")),
    )
    connection.send_result(
        msg["id"],
        {"format": msg["format"], "rows": [event.to_dict() for event in events]},
    )


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value)
