"""AlarmGrid integration."""

from __future__ import annotations

import asyncio
import logging
from asyncio import Lock
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .alarm_engine import AlarmEngine
from .alarm_notifications import (
    AlarmNotificationManager,
    TelegramNotifier,
    async_send_telegram,
)
from .alarm_sound import AlarmSoundManager
from .alarm_store import HomeAssistantRuleStore, SQLiteHistoryStore
from .const import (
    CONF_ALARM_FLOOD_THRESHOLD,
    CONF_ALARM_FLOOD_WINDOW_SECONDS,
    CONF_AUTO_SHELVE_FLAPPING,
    CONF_CREATE_RULE_BUTTONS,
    CONF_MEDIA_PLAYERS,
    CONF_REPEAT_INTERVAL_SECONDS,
    CONF_SOUND_MODE,
    CONF_TELEGRAM_CALLBACK_EVENT_ENTITIES,
    CONF_TELEGRAM_INTERACTIVE_ENABLED,
    DEFAULT_OPTIONS,
    DOMAIN,
    PLATFORMS,
    RULE_ENTITY_PLATFORMS,
    RULES_STORAGE_KEY,
    STATE_STORAGE_KEY,
)
from .notification_queue import TelegramOutbox
from .telegram_interactive import TelegramInteractiveManager

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class AlarmGridRuntime:
    """Runtime objects for one config entry."""

    entry_id: str
    rule_store: HomeAssistantRuleStore
    history_store: SQLiteHistoryStore
    sound_manager: AlarmSoundManager
    notification_manager: AlarmNotificationManager
    engine: AlarmEngine
    create_rule_buttons: bool = True
    notification_outbox: TelegramOutbox | None = None
    remove_start_listener: Any | None = None
    remove_transition_listener: Any | None = None
    tasks: set = field(default_factory=set)
    stopping: bool = False
    remove_state_listener: Any | None = None
    remove_delay_timer: Any | None = None
    remove_frontend_update_listener: Any | None = None
    telegram_interactive_manager: TelegramInteractiveManager | None = None
    remove_telegram_callback_listener: Any | None = None
    remove_panel: Any | None = None
    refresh_rule_runtime: Any | None = None
    rule_refresh_lock: Lock = field(default_factory=Lock)

    async def async_refresh_rules(self) -> None:
        """Refresh only runtime resources that depend on the rule collection."""

        if self.refresh_rule_runtime is None:
            raise RuntimeError("AlarmGrid rule refresh is not initialized")
        async with self.rule_refresh_lock:
            await self.refresh_rule_runtime()


AlarmGridConfigEntry = Any


def rule_source_entity_ids(engine: AlarmEngine) -> list[str]:
    """Return the source entities needed by the current rule collection."""

    return sorted(
        {
            entity_id
            for rule in engine.rules.values()
            for entity_id in getattr(
                rule, "source_entity_ids", {rule.entity_id} if rule.entity_id else set()
            )
        }
    )


async def async_setup_entry(
    hass: HomeAssistant, entry: AlarmGridConfigEntry
) -> bool:
    """Set up AlarmGrid from a config entry."""

    from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
    from homeassistant.core import Event, callback
    from homeassistant.exceptions import ConfigEntryNotReady
    from homeassistant.helpers.storage import Store
    from homeassistant.helpers.event import (
        async_call_later,
        async_track_state_change_event,
    )

    from .alarm_panel import async_register_panel
    from .frontend_events import attach_alarm_update_event_listener
    from .frontend_resource import async_register_lovelace_resource
    from .services import async_setup_services
    from .websocket_api import async_register_websocket_api

    options = {**DEFAULT_OPTIONS, **entry.data, **entry.options}
    rule_store = HomeAssistantRuleStore(hass, RULES_STORAGE_KEY, STATE_STORAGE_KEY)
    history_path = Path(hass.config.path("alarmgrid_history.db"))
    history_store = SQLiteHistoryStore(history_path)
    try:
        await history_store.async_setup()
    except Exception as err:
        _LOGGER.error(
            "Alarm history initialization failed: error=%s; alarms will continue and history setup will be retried on the next event",
            type(err).__name__,
        )

    async def _media_call(rule_id: str, priority: Any) -> None:
        media_players = options.get(CONF_MEDIA_PLAYERS) or []
        if not media_players:
            return
        media_content_id = f"/local/alarmgrid/sounds/{priority.value}.mp3"
        await hass.services.async_call(
            "media_player",
            "play_media",
            target={"entity_id": media_players},
            service_data={
                "media_content_id": media_content_id,
                "media_content_type": "music",
            },
            blocking=False,
        )

    sound_manager = AlarmSoundManager(
        sound_mode=options.get(CONF_SOUND_MODE, DEFAULT_OPTIONS[CONF_SOUND_MODE]),
        repeat_interval_seconds=int(
            options.get(
                CONF_REPEAT_INTERVAL_SECONDS,
                DEFAULT_OPTIONS[CONF_REPEAT_INTERVAL_SECONDS],
            )
        ),
        media_players=list(options.get(CONF_MEDIA_PLAYERS, [])),
        media_call=_media_call,
    )

    async def _notify_call(target: str, message: str) -> None:
        await async_send_telegram(hass, target, message)

    notification_manager = AlarmNotificationManager()
    engine = await AlarmEngine.from_store(
        rule_store,
        history_store,
        sound_manager=sound_manager,
        event_handler=notification_manager.notify,
    )
    engine.alarm_flood_threshold = int(
        options.get(
            CONF_ALARM_FLOOD_THRESHOLD, DEFAULT_OPTIONS[CONF_ALARM_FLOOD_THRESHOLD]
        )
    )
    engine.alarm_flood_window_seconds = int(
        options.get(
            CONF_ALARM_FLOOD_WINDOW_SECONDS,
            DEFAULT_OPTIONS[CONF_ALARM_FLOOD_WINDOW_SECONDS],
        )
    )
    engine.auto_shelve_flapping = bool(
        options.get(
            CONF_AUTO_SHELVE_FLAPPING, DEFAULT_OPTIONS[CONF_AUTO_SHELVE_FLAPPING]
        )
    )
    interactive_manager = None
    if options.get(CONF_TELEGRAM_INTERACTIVE_ENABLED, False):
        interactive_manager = TelegramInteractiveManager(hass, engine, options)
    notifier = TelegramNotifier(
        options,
        _notify_call,
        interactive_manager,
        hass.config.language,
        rule_lookup=engine.rules.get,
    )
    outbox = TelegramOutbox(
        Store(hass, 1, f"{DOMAIN}.{entry.entry_id}.telegram_outbox"),
        notifier.async_deliver,
        notifier.skip_reason,
    )
    try:
        await outbox.async_load()
    except Exception as err:
        raise ConfigEntryNotReady("Unable to load AlarmGrid Telegram outbox") from err
    notifier.outbox = outbox
    notification_manager.providers.append(notifier)

    runtime = AlarmGridRuntime(
        entry_id=entry.entry_id,
        create_rule_buttons=options[CONF_CREATE_RULE_BUTTONS],
        rule_store=rule_store,
        history_store=history_store,
        sound_manager=sound_manager,
        notification_manager=notification_manager,
        notification_outbox=outbox,
        engine=engine,
        telegram_interactive_manager=interactive_manager,
    )
    entry.runtime_data = runtime
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = runtime
    runtime.remove_frontend_update_listener = attach_alarm_update_event_listener(
        hass, entry.entry_id, engine
    )

    ready = False
    timer_retry_at: datetime | None = None

    def _create_task(coro: Any) -> None:
        task = hass.async_create_task(coro)
        runtime.tasks.add(task)
        task.add_done_callback(runtime.tasks.discard)

    callback_entities = list(options.get(CONF_TELEGRAM_CALLBACK_EVENT_ENTITIES) or [])
    if interactive_manager is not None and callback_entities:

        @callback
        def _telegram_event_changed(event: Event) -> None:
            new_state = event.data.get("new_state")
            if (
                new_state is None
                or new_state.attributes.get("event_type") != "telegram_callback"
            ):
                return
            _create_task(
                interactive_manager.handle_callback(dict(new_state.attributes))
            )

        runtime.remove_telegram_callback_listener = async_track_state_change_event(
            hass, callback_entities, _telegram_event_changed
        )

    def _reschedule_delay_timer() -> None:
        if runtime.remove_delay_timer:
            runtime.remove_delay_timer()
            runtime.remove_delay_timer = None

        if runtime.stopping or not ready:
            return
        due_at = engine.next_due_transition_at()
        if due_at is None:
            return
        if timer_retry_at is not None:
            due_at = max(due_at, timer_retry_at)

        delay_seconds = max(0.0, (due_at - datetime.now(UTC)).total_seconds())
        runtime.remove_delay_timer = async_call_later(
            hass, delay_seconds, _delay_timer_due
        )

    async def _process_delay_timer() -> None:
        nonlocal timer_retry_at
        try:
            await engine.process_due_transitions()
        except Exception as err:
            timer_retry_at = datetime.now(UTC) + timedelta(seconds=5)
            _LOGGER.error(
                "Alarm timer processing failed: error=%s retry_in=5s",
                type(err).__name__,
            )
        else:
            timer_retry_at = None
        finally:
            _reschedule_delay_timer()

    @callback
    def _delay_timer_due(_now: datetime) -> None:
        runtime.remove_delay_timer = None
        _create_task(_process_delay_timer())

    async def _process_state_change(entity_id: str, state: Any) -> None:
        try:
            await engine.process_state(entity_id, state)
        except Exception as err:
            _LOGGER.error(
                "Alarm source processing failed: entity=%s error=%s",
                entity_id,
                type(err).__name__,
            )
        finally:
            _reschedule_delay_timer()

    @callback
    def _state_changed(event: Event) -> None:
        new_state = event.data.get("new_state")
        if new_state is None or not ready or runtime.stopping:
            return
        _create_task(_process_state_change(new_state.entity_id, new_state.state))

    def _refresh_state_listener() -> None:
        if runtime.remove_state_listener:
            runtime.remove_state_listener()
            runtime.remove_state_listener = None

        tracked_entities = rule_source_entity_ids(engine)
        if not tracked_entities:
            return
        runtime.remove_state_listener = async_track_state_change_event(
            hass, tracked_entities, _state_changed
        )

    async def _reconcile_current_states() -> None:
        await engine.reconcile_states(
            {
                entity_id: hass.states.get(entity_id)
                for entity_id in rule_source_entity_ids(engine)
            }
        )
        _reschedule_delay_timer()

    async def _refresh_rule_runtime() -> None:
        _refresh_state_listener()
        if ready:
            await _reconcile_current_states()
        _reschedule_delay_timer()
        unloaded = await hass.config_entries.async_unload_platforms(
            entry, RULE_ENTITY_PLATFORMS
        )
        if not unloaded:
            raise RuntimeError("Unable to unload AlarmGrid rule entity platforms")
        await hass.config_entries.async_forward_entry_setups(
            entry, RULE_ENTITY_PLATFORMS
        )

    runtime.refresh_rule_runtime = _refresh_rule_runtime
    runtime.remove_transition_listener = engine.add_listener(_reschedule_delay_timer)
    _refresh_state_listener()
    _reschedule_delay_timer()

    await async_setup_services(hass)
    async_register_websocket_api(hass)
    runtime.remove_panel = await async_register_panel(hass, entry)
    await async_register_lovelace_resource(hass)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    entry.async_on_unload(lambda: hass.data[DOMAIN].pop(entry.entry_id, None))

    async def _start_monitoring() -> None:
        nonlocal ready
        if runtime.stopping:
            return
        ready = True
        await _reconcile_current_states()
        outbox.start(hass.async_create_background_task)

    @callback
    def _started(_event: Event) -> None:
        runtime.remove_start_listener = None
        _create_task(_start_monitoring())

    if hass.is_running:
        await _start_monitoring()
    else:
        runtime.remove_start_listener = hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STARTED, _started
        )
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: AlarmGridConfigEntry
) -> bool:
    """Unload a config entry."""

    runtime = entry.runtime_data
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        runtime.stopping = True
        if runtime.remove_start_listener:
            runtime.remove_start_listener()
        if runtime.remove_transition_listener:
            runtime.remove_transition_listener()
        if runtime.remove_state_listener:
            runtime.remove_state_listener()
        if runtime.remove_delay_timer:
            runtime.remove_delay_timer()
        if runtime.remove_frontend_update_listener:
            runtime.remove_frontend_update_listener()
        if runtime.remove_telegram_callback_listener:
            runtime.remove_telegram_callback_listener()
        if runtime.remove_panel:
            try:
                runtime.remove_panel()
            except Exception:  # pragma: no cover - HA frontend API compatibility
                _LOGGER.debug("Panel unregister callback failed", exc_info=True)
        if runtime.tasks:
            await asyncio.gather(*list(runtime.tasks), return_exceptions=True)
        await runtime.engine.async_shutdown()
        if runtime.notification_outbox:
            await runtime.notification_outbox.async_close()
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return unload_ok


async def _async_update_listener(
    hass: HomeAssistant, entry: AlarmGridConfigEntry
) -> None:
    """Reload entry when options change."""

    await hass.config_entries.async_reload(entry.entry_id)
