"""Operator attribution through HA adapters, history, and Telegram delivery."""

import importlib.util
import sys
import unittest
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from custom_components.alarmgrid.alarm_engine import AlarmEngine
from custom_components.alarmgrid.alarm_notifications import TelegramNotifier
from custom_components.alarmgrid.const import DOMAIN
from custom_components.alarmgrid.operator_identity import (
    SYSTEM_OPERATOR,
    async_context_operator,
    user_operator,
)
from custom_components.alarmgrid.rule_management import delete_rules, export_rules_csv
from tests.test_alarm_delivery_reliability import make_rule
from tests.test_notifications import options


@contextmanager
def ha_adapters():
    """Load actual handlers; only HA registration/schema plumbing is stubbed."""
    names = (
        "voluptuous", "homeassistant", "homeassistant.components",
        "homeassistant.components.websocket_api", "homeassistant.core",
        "homeassistant.exceptions", "homeassistant.helpers",
        "homeassistant.helpers.config_validation",
    )
    modules = {name: ModuleType(name) for name in names}
    vol = modules["voluptuous"]
    for name in ("Required", "Optional", "Schema", "All", "Coerce", "In", "Range"):
        setattr(vol, name, lambda value=None, *args, **kwargs: value)
    ws = modules["homeassistant.components.websocket_api"]
    ws.websocket_command = lambda schema: lambda fn: fn
    ws.async_response = lambda fn: fn
    modules["homeassistant.components"].websocket_api = ws
    modules["homeassistant.core"].HomeAssistant = object
    modules["homeassistant.core"].ServiceCall = object
    modules["homeassistant.exceptions"].HomeAssistantError = RuntimeError
    modules["homeassistant.helpers.config_validation"].string = str
    root = Path(__file__).resolve().parents[1] / "custom_components/alarmgrid"
    with patch.dict(sys.modules, modules):
        loaded = []
        for filename in ("services", "websocket_api"):
            name = f"custom_components.alarmgrid.{filename}"
            spec = importlib.util.spec_from_file_location(name, root / f"{filename}.py")
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            loaded.append(module)
        yield loaded


class OperatorIdentityTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.user = SimpleNamespace(id="ha-user-id", name="Alessandro")
        self.actor = "Alessandro (Home Assistant)"
        self.send = AsyncMock()
        self.notifier = TelegramNotifier(options(), self.send, language="it")
        self.engine = AlarmEngine([make_rule()], event_handler=self.notifier.notify)
        self.notifier._rule_lookup = self.engine.rules.get
        self.runtime = SimpleNamespace(
            engine=self.engine, entry_id="entry",
            rule_store=SimpleNamespace(async_save_rules=AsyncMock()),
            async_refresh_rules=AsyncMock(),
            history_store=self.engine.history_store,
        )
        self.registered = {}
        self.hass = SimpleNamespace(
            data={DOMAIN: {"entry": self.runtime}},
            auth=SimpleNamespace(async_get_user=AsyncMock(return_value=self.user)),
            services=SimpleNamespace(async_register=lambda domain, name, fn, **kw: self.registered.update({name: fn})),
        )
        self.connection = SimpleNamespace(user=self.user, send_result=Mock())

    async def test_context_resolves_display_name_and_falls_back_to_id(self):
        context = SimpleNamespace(user_id=self.user.id)
        self.assertEqual(await async_context_operator(self.hass, context), self.actor)
        self.hass.auth.async_get_user.assert_awaited_once_with(self.user.id)
        self.user.name = " "
        self.assertEqual(user_operator(self.user), "Home Assistant (ID ha-user-id)")
        self.hass.auth.async_get_user.return_value = None
        self.assertEqual(await async_context_operator(self.hass, context), "Home Assistant (ID ha-user-id)")
        self.hass.auth.async_get_user.side_effect = RuntimeError("unavailable")
        with self.assertLogs("custom_components.alarmgrid.operator_identity", level="WARNING"):
            self.assertEqual(await async_context_operator(self.hass, context), "Home Assistant (ID ha-user-id)")

    async def test_automation_does_not_guess_user_from_parent_context(self):
        for context in (None, SimpleNamespace(user_id=None, parent_id="someone-elses-context")):
            self.assertEqual(await async_context_operator(self.hass, context), SYSTEM_OPERATOR)
        self.hass.auth.async_get_user.assert_not_awaited()

    async def test_panel_shelve_disable_and_history_export_share_actor(self):
        with ha_adapters() as (_, ws):
            await ws.websocket_shelve(self.hass, self.connection, {
                "id": 1, "rule_id": "fault", "duration_minutes": 15,
                "comment": "Manutenzione", "operator": "forged",
            })
            await ws.websocket_disable(self.hass, self.connection, {
                "id": 2, "rule_id": "fault", "comment": "Manutenzione",
            })
            await ws.websocket_export_history(self.hass, self.connection, {"id": 3, "format": "csv"})
        events = self.engine.history_store.events
        self.assertEqual([e.event_type for e in events], ["shelved", "disabled"])
        self.assertEqual([e.operator for e in events], [self.actor, self.actor])
        rows = self.connection.send_result.call_args.args[1]["rows"]
        self.assertTrue(all(row["operator"] == self.actor for row in rows))
        self.assertEqual(self.send.await_count, 2)
        for call, status in zip(self.send.await_args_list, ("SOSPESO", "DISABILITATO")):
            self.assertIn(status, call.args[1])
            self.assertIn(f"Operatore: {self.actor}", call.args[1])
            self.assertIn("Motivo: Manutenzione", call.args[1])
        self.user.name = "Renamed"
        self.assertTrue(all(e.operator == self.actor for e in events))

    async def test_service_actions_resolve_context_for_history_and_telegram(self):
        with ha_adapters() as (services, _):
            await services.async_setup_services(self.hass)
            for service in ("shelve_alarm", "disable_alarm"):
                await self.registered[service](SimpleNamespace(
                    service=service, context=SimpleNamespace(user_id=self.user.id),
                    data={"rule_id": "fault", "duration_minutes": 5},
                ))
        self.assertEqual(self.send.await_count, 2)
        self.assertTrue(all(e.operator == self.actor for e in self.engine.history_store.events))

    async def test_editor_disabling_keeps_actor_on_both_events(self):
        with ha_adapters() as (_, ws):
            await ws.websocket_update_rule(self.hass, self.connection, {
                "id": 1, "rule_id": "fault", "changes": {"enabled": False},
            })
        self.assertEqual([e.event_type for e in self.engine.history_store.events], ["disabled", "rule_updated"])
        self.assertTrue(all(e.operator == self.actor for e in self.engine.history_store.events))
        self.send.assert_awaited_once()
        self.assertIn(self.actor, self.send.await_args.args[1])

    async def test_service_rule_edit_and_creation_record_actor(self):
        with ha_adapters() as (services, _):
            await services.async_setup_services(self.hass)
            for service, data in (
                ("create_rule", {"rule": make_rule(id="second").to_dict()}),
                ("update_rule", {"rule_id": "second", "changes": {"enabled": False}}),
            ):
                await self.registered[service](SimpleNamespace(
                    service=service, context=SimpleNamespace(user_id=self.user.id), data=data,
                ))
        self.assertEqual([e.event_type for e in self.engine.history_store.events], ["rule_created", "disabled", "rule_updated"])
        self.assertTrue(all(e.operator == self.actor for e in self.engine.history_store.events))

    async def test_csv_import_and_bulk_delete_record_actor(self):
        with ha_adapters() as (_, ws):
            await ws.websocket_import_rules(self.hass, self.connection, {
                "id": 1, "csv": export_rules_csv([make_rule(enabled=False), make_rule(id="second")]),
            })
        await delete_rules(self.engine, rule_ids=["fault", "second"], operator=self.actor)
        self.assertEqual([e.event_type for e in self.engine.history_store.events], ["disabled", "rule_updated", "rule_created", "rule_deleted", "rule_deleted"])
        self.assertTrue(all(e.operator == self.actor for e in self.engine.history_store.events))

    async def test_other_panel_actions_record_authenticated_actor(self):
        await self.engine.process_state("binary_sensor.fault", "on")
        with ha_adapters() as (_, ws):
            for action in ("acknowledge", "silence", "shelve", "unshelve", "disable", "enable"):
                await getattr(ws, f"websocket_{action}")(self.hass, self.connection, {
                    "id": 1, "rule_id": "fault", "duration_minutes": 5,
                })
                if action in ("unshelve", "enable"):
                    recorded = self.engine.history_store.events[-2]
                else:
                    recorded = self.engine.history_store.events[-1]
                self.assertEqual(recorded.operator, self.actor, action)

    async def test_explicit_notification_preferences_and_priority_are_preserved(self):
        for overrides in (
            {"telegram_notify_shelved": False, "telegram_notify_disabled": False},
            {"telegram_enabled": False},
            {"telegram_min_priority": "critical"},
        ):
            self.notifier._options = options(**overrides)
            await self.engine.shelve_alarm("fault", duration_minutes=5, operator=self.actor)
            await self.engine.disable_alarm("fault", operator=self.actor)
        self.send.assert_not_awaited()
        self.assertEqual(len(self.engine.history_store.events), 6)


if __name__ == "__main__":
    unittest.main()
