"""Exercise HA setup/unload wiring with fake services, event bus, and storage."""

import asyncio
import copy
import sys
import tempfile
import unittest
from pathlib import Path
from datetime import UTC, datetime, timedelta
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

from custom_components.alarmgrid import async_setup_entry, async_unload_entry
from custom_components.alarmgrid.alarm_models import AlarmLifecycleState
from custom_components.alarmgrid.alarm_store import SQLiteHistoryStore
from tests.test_alarm_delivery_reliability import make_rule
from tests.test_notifications import options


def module(name, **attrs):
    result = ModuleType(name)
    result.__dict__.update(attrs)
    return result


class SetupTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.stored = {"alarmgrid.rules": {"rules": [make_rule().to_dict()]}}
        self.state_listeners = []
        self.timers = []
        self.start_listeners = []
        self.source_states = {
            "binary_sensor.fault": SimpleNamespace(state="on"),
            "notify.telegram_operations": SimpleNamespace(state="unknown"),
        }
        self.sent = []
        self.delivered = asyncio.Event()

        async def no_op(*args, **kwargs):
            return True

        async def send(*args, **kwargs):
            self.sent.append(kwargs)
            self.delivered.set()
            return {"chats": [{"chat_id": 1, "message_id": len(self.sent)}]}

        def track(hass, entities, callback):
            item = (entities, callback)
            self.state_listeners.append(item)
            return lambda: self.state_listeners.remove(item)

        def later(hass, delay, callback):
            item = (delay, callback)
            self.timers.append(item)
            return lambda: self.timers.remove(item) if item in self.timers else None

        def once(event_type, callback):
            self.start_listeners.append(callback)
            return lambda: self.start_listeners.remove(callback)

        stored = self.stored

        class Store:
            def __init__(self, hass, version, key, **kwargs):
                self.key = key

            async def async_load(self):
                return copy.deepcopy(stored.get(self.key))

            async def async_save(self, value):
                stored[self.key] = copy.deepcopy(value)

        class ConfigEntryNotReady(Exception):
            pass

        self.hass = SimpleNamespace(
            data={},
            is_running=True,
            config=SimpleNamespace(
                language="en", path=lambda name: str(Path(self.temp.name) / name)
            ),
            states=SimpleNamespace(get=self.source_states.get),
            services=SimpleNamespace(async_call=send),
            bus=SimpleNamespace(async_fire=lambda *args: None, async_listen_once=once),
            config_entries=SimpleNamespace(
                async_forward_entry_setups=no_op, async_unload_platforms=no_op
            ),
            async_create_task=asyncio.create_task,
            async_create_background_task=asyncio.create_task,
        )
        self.entry = SimpleNamespace(
            entry_id="test",
            data={},
            options=options(),
            add_update_listener=lambda _: lambda: None,
            async_on_unload=lambda _: None,
        )
        replacements = {
            "homeassistant": module("homeassistant"),
            "homeassistant.const": module(
                "const", EVENT_HOMEASSISTANT_STARTED="started"
            ),
            "homeassistant.core": module(
                "core", Event=SimpleNamespace, callback=lambda fn: fn
            ),
            "homeassistant.exceptions": module(
                "exceptions", ConfigEntryNotReady=ConfigEntryNotReady
            ),
            "homeassistant.helpers": module("helpers"),
            "homeassistant.helpers.event": module(
                "event", async_call_later=later, async_track_state_change_event=track
            ),
            "homeassistant.helpers.storage": module("storage", Store=Store),
            "custom_components.alarmgrid.alarm_panel": module(
                "panel", async_register_panel=no_op
            ),
            "custom_components.alarmgrid.frontend_resource": module(
                "resource", async_register_lovelace_resource=no_op
            ),
            "custom_components.alarmgrid.services": module(
                "services", async_setup_services=no_op
            ),
            "custom_components.alarmgrid.websocket_api": module(
                "websocket", async_register_websocket_api=lambda _: None
            ),
        }
        self.patch = patch.dict(sys.modules, replacements)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    async def asyncTearDown(self):
        if getattr(self.entry, "runtime_data", None) is not None:
            self.entry.runtime_data.remove_panel = None
            await async_unload_entry(self.hass, self.entry)

    async def test_running_ha_reconciles_sources_and_starts_outbox(self):
        await async_setup_entry(self.hass, self.entry)
        await asyncio.wait_for(self.delivered.wait(), 1)
        self.assertTrue(self.entry.runtime_data.engine.states["fault"].is_active)
        self.assertEqual(self.sent[0]["service_data"]["parse_mode"], "plain_text")
        self.assertEqual(len(self.state_listeners), 1)

    async def test_initial_history_failure_recovers_without_blocking_telegram(self):
        original_setup = SQLiteHistoryStore.async_setup
        attempts = 0

        async def fail_once(store):
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise OSError("history unavailable")
            await original_setup(store)

        with patch.object(SQLiteHistoryStore, "async_setup", fail_once):
            with self.assertLogs("custom_components.alarmgrid", level="ERROR"):
                await async_setup_entry(self.hass, self.entry)
            await asyncio.wait_for(self.delivered.wait(), 1)
        events = await self.entry.runtime_data.history_store.query_events()
        self.assertEqual([event.event_type for event in events], ["activated"])
        self.assertEqual(attempts, 2)

    async def test_startup_waits_for_ha_ready_before_reconciliation(self):
        self.hass.is_running = False
        await async_setup_entry(self.hass, self.entry)
        runtime = self.entry.runtime_data
        self.assertFalse(runtime.engine.states["fault"].is_active)
        self.assertEqual(self.sent, [])
        self.assertEqual(len(self.start_listeners), 1)
        self.hass.is_running = True
        self.start_listeners.pop()(SimpleNamespace())
        await asyncio.wait_for(self.delivered.wait(), 1)
        self.assertTrue(runtime.engine.states["fault"].is_active)

    async def test_shelving_action_reschedules_timer_without_source_update(self):
        await async_setup_entry(self.hass, self.entry)
        await self.entry.runtime_data.engine.shelve_alarm("fault", duration_minutes=1)
        self.assertEqual(len(self.timers), 1)
        self.assertGreater(self.timers[0][0], 59)

    async def test_rule_refresh_evaluates_new_rule_against_current_ha_state(self):
        await async_setup_entry(self.hass, self.entry)
        runtime = self.entry.runtime_data
        await runtime.engine.create_rule(make_rule(id="new").to_dict())
        await runtime.async_refresh_rules()
        self.assertEqual(
            runtime.engine.states["new"].lifecycle_state,
            AlarmLifecycleState.ACTIVE_UNACK,
        )
        self.assertEqual(len(self.state_listeners), 1)

    async def test_timer_failure_is_logged_and_retried_without_busy_loop(self):
        await async_setup_entry(self.hass, self.entry)
        runtime = self.entry.runtime_data
        await runtime.engine.shelve_alarm("fault", duration_minutes=1)
        runtime.engine.states["fault"].shelve_expiry = datetime.now(UTC) - timedelta(
            seconds=1
        )

        async def fail():
            raise RuntimeError("timer failure")

        with patch.object(runtime.engine, "process_due_transitions", fail):
            with self.assertLogs("custom_components.alarmgrid", level="ERROR") as logs:
                self.timers.pop()[1](datetime.now(UTC))
                await asyncio.gather(*list(runtime.tasks))
        self.assertEqual(len(self.timers), 1)
        self.assertGreater(self.timers[0][0], 4)
        self.assertIn("retry_in=5s", str(logs.output))

    async def test_unload_removes_start_listener_and_all_timers(self):
        self.hass.is_running = False
        await async_setup_entry(self.hass, self.entry)
        self.entry.runtime_data.remove_panel = None
        await async_unload_entry(self.hass, self.entry)
        self.assertEqual(self.state_listeners, [])
        self.assertEqual(self.start_listeners, [])
        self.assertEqual(self.timers, [])
        self.entry.runtime_data = None


if __name__ == "__main__":
    unittest.main()
