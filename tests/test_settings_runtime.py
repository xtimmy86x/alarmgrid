"""Behavioural coverage for the settings exposed by both configuration UIs."""

import unittest
from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

from custom_components.alarmgrid.alarm_engine import AlarmEngine
from custom_components.alarmgrid.alarm_models import AlarmLifecycleState, AlarmPriority, AlarmRule
from custom_components.alarmgrid.alarm_sound import AlarmSoundManager
from custom_components.alarmgrid.const import DOMAIN
from custom_components.alarmgrid.settings import current_settings, validate_settings
from tests.test_alarm_engine import Clock
from tests.test_operator_identity import ha_adapters


def rule(**changes):
    return AlarmRule.from_dict({"id": "temp", "name": "Temp", "entity_id": "sensor.temp", "condition": "above", "threshold": 10, **changes})


class SettingsRuntimeTests(unittest.IsolatedAsyncioTestCase):
    async def test_defaults_apply_only_to_new_omitted_fields(self):
        engine = AlarmEngine([rule()])
        engine.options.update(default_delay_on_seconds=8, default_delay_off_seconds=4, default_deadband=1.5)
        data = {"name": "New", "entity_id": "sensor.new", "condition": "above", "threshold": 10}
        new = await engine.create_rule({"id": "new", **data})
        self.assertEqual((new.delay_on_seconds, new.delay_off_seconds, new.deadband), (8, 4, 1.5))
        explicit = await engine.create_rule({"id": "explicit", **data, "deadband": 0, "delay_on_seconds": 0})
        self.assertEqual((explicit.delay_on_seconds, explicit.deadband), (0, 0))
        await engine.update_rule("temp", {"name": "Renamed"})
        self.assertEqual(engine.rules["temp"].delay_on_seconds, 0)
        expression = {"type": "condition", "entity_id": "sensor.temp", "operator": "above", "value": 10}
        advanced = await engine.create_rule({"id": "advanced", **data, "condition_expression": expression})
        self.assertEqual(advanced.condition_expression["deadband"], 1.5)
        self.assertNotIn("deadband", expression, "Defaults must not mutate caller data")

    async def test_global_clear_acknowledgement_and_per_rule_override(self):
        for global_ack, auto_ack, expected in ((True, False, "CLEARED_UNACK"), (False, False, "CLEARED_ACK"), (True, True, "CLEARED_ACK")):
            with self.subTest(global_ack=global_ack, auto_ack=auto_ack):
                engine = AlarmEngine([rule(auto_ack_on_clear=auto_ack)])
                engine.options["require_acknowledgement_for_cleared"] = global_ack
                await engine.process_state("sensor.temp", "20")
                await engine.process_state("sensor.temp", "5")
                self.assertEqual(engine.states["temp"].lifecycle_state, expected)

    async def test_source_logging_flags_do_not_suppress_lifecycle_or_notifications(self):
        for changes, normal, count in ((False, False, 0), (False, True, 0), (True, False, 1), (True, True, 2)):
            notify = AsyncMock()
            engine = AlarmEngine([rule()], event_handler=notify)
            engine.options.update(store_status_changes=changes, store_normal_events=normal)
            for state in ("1", "2", "20", "21", "0"):
                await engine.process_state("sensor.temp", state)
            events = await engine.history_store.query_events()
            types = [event.event_type for event in events]
            self.assertEqual(types.count("status_changed"), count)
            self.assertEqual(types.count("activated"), 1)
            self.assertEqual(types.count("cleared"), 1)
            notified = [call.args[0].event_type for call in notify.await_args_list]
            self.assertIn("activated", notified)
            self.assertIn("cleared", notified)

    async def test_history_limit_is_applied_but_export_is_complete(self):
        engine = AlarmEngine([rule()])
        engine.options["max_history_rows"] = 10
        engine.flapping_threshold = 100
        for i in range(15):
            await engine.process_state("sensor.temp", "20" if i % 2 else "0")
        runtime = SimpleNamespace(engine=engine, history_store=engine.history_store)
        hass = SimpleNamespace(data={DOMAIN: {"entry": runtime}})
        conn = SimpleNamespace(send_result=Mock())
        with ha_adapters() as (_, ws):
            for requested, expected in (({}, 10), ({"limit": 5000}, 10), ({"limit": 3}, 3)):
                await ws.websocket_list_history(hass, conn, {"id": 1, **requested})
                self.assertEqual(len(conn.send_result.call_args.args[1]["events"]), expected)
            await ws.websocket_export_history(hass, conn, {"id": 2, "format": "json"})
        self.assertEqual(len(conn.send_result.call_args.args[1]["rows"]), 14)

    async def test_display_limit_never_limits_engine_or_public_alarm_list(self):
        engine = AlarmEngine([rule(id=f"rule_{i}") for i in range(12)])
        engine.options["max_active_alarms"] = 10
        await engine.process_state("sensor.temp", "20")
        self.assertEqual(engine.active_count(), 12)
        hass = SimpleNamespace(data={DOMAIN: {"entry": SimpleNamespace(engine=engine, sound_manager=AlarmSoundManager())}})
        conn = SimpleNamespace(send_result=Mock())
        with ha_adapters() as (_, ws):
            await ws.websocket_list_alarms(hass, conn, {"id": 1})
        payload = conn.send_result.call_args.args[1]
        self.assertEqual(len(payload["alarms"]), 12)
        self.assertEqual(payload["settings"]["max_active_alarms"], 10)
        self.assertNotIn("telegram_targets", payload["settings"])

    def test_finite_deadband_validation_and_legacy_sound_setup(self):
        values, errors = validate_settings({"default_deadband": "0.25"}, {})
        self.assertEqual((values["default_deadband"], errors), (0.25, {}))
        for invalid in ("nan", "inf", -1, True):
            self.assertIn("default_deadband", validate_settings({"default_deadband": invalid}, {})[1])
        for browser, media, mode in ((True, True, "browser_and_media_player"), (False, True, "media_player_only"), (False, False, "none")):
            stored = {"enable_browser_sound": browser, "enable_media_player_sound": media}
            self.assertEqual(current_settings(stored)["sound_mode"], mode)
            self.assertEqual(current_settings({**stored, "sound_mode": "browser_only"})["sound_mode"], "browser_only")


class SoundSchedulingTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.clock = Clock()
        self.media = AsyncMock()
        self.sound = AlarmSoundManager(sound_mode="browser_and_media_player", repeat_interval_seconds=15, now=self.clock.now, media_call=self.media)
        self.engine = AlarmEngine([rule()], sound_manager=self.sound, now=self.clock.now)

    async def test_repeats_are_scheduled_without_source_updates_then_stop_on_ack(self):
        await self.engine.process_state("sensor.temp", "20")
        first = self.sound.last_sound_at
        self.assertEqual(self.engine.next_due_transition_at(), first + timedelta(seconds=15))
        self.clock.advance(14)
        await self.engine.process_due_transitions()
        self.assertEqual(self.media.await_count, 1)
        self.clock.advance(1)
        await self.engine.process_due_transitions()
        self.assertEqual(self.media.await_count, 2)
        self.assertGreater(self.sound.last_sound_at, first)
        await self.engine.acknowledge_alarm("temp")
        self.assertIsNone(self.engine.next_due_transition_at())
        self.clock.advance(100)
        await self.engine.process_due_transitions()
        self.assertEqual(self.media.await_count, 2)

    async def test_repeat_disabled_and_timed_silence(self):
        self.sound.repeat_until_silenced = False
        await self.engine.process_state("sensor.temp", "20")
        self.assertIsNone(self.engine.next_due_transition_at())
        await self.engine.silence_horn(10)
        self.assertEqual(self.engine.next_due_transition_at(), self.clock.now() + timedelta(seconds=10))
        self.clock.advance(10)
        await self.engine.process_due_transitions()
        self.assertFalse(self.sound.silenced)
        self.assertEqual(self.media.await_count, 2)
        self.assertIsNone(self.engine.next_due_transition_at())
        await self.engine.silence_horn()
        self.assertIsNone(self.engine.next_due_transition_at())

    async def test_reactivation_resounds_when_repeat_is_disabled(self):
        self.sound.repeat_until_silenced = False
        await self.engine.process_state("sensor.temp", "20")
        await self.engine.silence_horn()
        await self.engine.process_state("sensor.temp", "0")
        self.clock.advance(1)
        await self.engine.process_state("sensor.temp", "20")
        self.assertEqual(self.media.await_count, 2)
        self.assertFalse(self.sound.silenced)
        self.assertIsNone(self.sound.next_due_at())

    async def test_suppression_and_deletion_cancel_sound(self):
        for action in ("shelve", "disable", "delete"):
            sound = AlarmSoundManager(now=self.clock.now)
            engine = AlarmEngine([rule()], sound_manager=sound, now=self.clock.now)
            await engine.process_state("sensor.temp", "20")
            if action == "shelve":
                await engine.shelve_alarm("temp", duration_minutes=5)
            elif action == "disable":
                await engine.disable_alarm("temp")
            else:
                await engine.delete_rule("temp")
            self.assertIsNone(sound.next_due_at())
            self.assertFalse(sound.horn_active)

    async def test_test_sound_does_not_latch_horn_or_change_silence(self):
        await self.sound.test_sound()
        self.assertFalse(self.sound.horn_active)
        self.assertIsNone(self.sound.next_due_at())
        await self.engine.process_state("sensor.temp", "20")
        await self.engine.silence_horn()
        await self.sound.test_sound()
        self.assertTrue(self.sound.silenced)
        self.assertFalse(self.sound.horn_active)

    async def test_reconcile_restores_unacknowledged_sound_but_not_acked(self):
        await self.engine.process_state("sensor.temp", "20")
        restored = AlarmEngine([rule()], initial_states=self.engine.states, sound_manager=AlarmSoundManager(now=self.clock.now), now=self.clock.now)
        await restored.reconcile_states({"sensor.temp": "20"})
        self.assertTrue(restored.sound_manager.horn_active)
        await restored.acknowledge_alarm("temp")
        await restored.reconcile_states({"sensor.temp": "20"})
        self.assertFalse(restored.sound_manager.horn_active)

    async def test_auto_shelving_does_not_restart_sound(self):
        self.engine.flapping_threshold = 2
        self.engine.auto_shelve_flapping = True
        for state in ("20", "0", "20"):
            await self.engine.process_state("sensor.temp", state)
        self.assertEqual(self.engine.states["temp"].lifecycle_state, AlarmLifecycleState.SHELVED)
        self.assertFalse(self.sound.horn_active)
        self.assertIsNone(self.sound.next_due_at())


class PersistedSilenceTests(unittest.IsolatedAsyncioTestCase):
    async def test_reload_preserves_indefinite_and_timed_silence(self):
        from custom_components.alarmgrid.alarm_store import MemoryRuleStore, InMemoryHistoryStore

        for seconds in (None, 60):
            with self.subTest(seconds=seconds):
                clock = Clock()
                store = MemoryRuleStore([rule()])
                media = AsyncMock()
                sound = AlarmSoundManager(sound_mode="browser_and_media_player", now=clock.now, media_call=media)
                engine = await AlarmEngine.from_store(store, InMemoryHistoryStore(), sound_manager=sound, now=clock.now)
                await engine.process_state("sensor.temp", "20")
                await engine.silence_horn(seconds)
                deadline = sound.silenced_until
                # No shutdown required: silence must already have been persisted.
                restored_sound = AlarmSoundManager(sound_mode="browser_and_media_player", now=clock.now, media_call=media)
                restored = await AlarmEngine.from_store(store, InMemoryHistoryStore(), sound_manager=restored_sound, now=clock.now)
                media.reset_mock()
                await restored.reconcile_states({"sensor.temp": "20"})
                self.assertTrue(restored_sound.silenced)
                self.assertFalse(restored_sound.horn_active)
                self.assertEqual(restored_sound.silenced_until, deadline)
                self.assertEqual(restored.next_due_transition_at(), deadline)
                media.assert_not_awaited()
                clock.advance(60)
                await restored.process_due_transitions()
                if seconds is None:
                    self.assertTrue(restored_sound.silenced)
                    media.assert_not_awaited()
                else:
                    self.assertFalse(restored_sound.silenced)
                    media.assert_awaited_once()
                    self.assertFalse((await store.async_load_sound())["silenced"])

    async def test_silence_expired_during_downtime_resumes_once_after_restore(self):
        from custom_components.alarmgrid.alarm_store import MemoryRuleStore, InMemoryHistoryStore

        clock = Clock()
        store = MemoryRuleStore([rule()])
        sound = AlarmSoundManager(now=clock.now)
        engine = await AlarmEngine.from_store(store, InMemoryHistoryStore(), sound_manager=sound, now=clock.now)
        await engine.process_state("sensor.temp", "20")
        await engine.silence_horn(30)
        clock.advance(40)
        media = AsyncMock()
        restored_sound = AlarmSoundManager(sound_mode="media_player_only", now=clock.now, media_call=media)
        restored = await AlarmEngine.from_store(store, InMemoryHistoryStore(), sound_manager=restored_sound, now=clock.now)
        await restored.reconcile_states({"sensor.temp": "20"})
        media.assert_not_awaited()
        await restored.process_due_transitions()
        await restored.process_due_transitions()
        media.assert_awaited_once()
        self.assertFalse(restored_sound.silenced)

    async def test_new_alarm_rearms_and_explicit_unsilence_is_persisted(self):
        from custom_components.alarmgrid.alarm_store import MemoryRuleStore, InMemoryHistoryStore

        store = MemoryRuleStore([rule(), rule(id="second", entity_id="sensor.second")])
        engine = await AlarmEngine.from_store(store, InMemoryHistoryStore(), sound_manager=AlarmSoundManager())
        await engine.process_state("sensor.temp", "20")
        await engine.silence_horn()
        sound = AlarmSoundManager()
        restored = await AlarmEngine.from_store(store, InMemoryHistoryStore(), sound_manager=sound)
        await restored.reconcile_states({"sensor.temp": "20", "sensor.second": "0"})
        self.assertTrue(sound.silenced)
        await restored.process_state("sensor.second", "20")
        self.assertFalse(sound.silenced)
        self.assertFalse((await store.async_load_sound())["silenced"])
        await restored.silence_horn()
        await restored.unsilence_horn()
        self.assertFalse((await store.async_load_sound())["silenced"])

    async def test_old_state_snapshots_without_sound_still_load(self):
        from custom_components.alarmgrid.alarm_store import MemoryRuleStore, InMemoryHistoryStore

        original = AlarmEngine([rule()])
        await original.process_state("sensor.temp", "20")
        store = MemoryRuleStore([rule()], original.states.values())
        self.assertIsNone(await store.async_load_sound())
        sound = AlarmSoundManager()
        restored = await AlarmEngine.from_store(store, InMemoryHistoryStore(), sound_manager=sound)
        await restored.reconcile_states({"sensor.temp": "20"})
        self.assertTrue(sound.horn_active)

    async def test_raw_numeric_updates_do_not_fill_history_by_default(self):
        engine = AlarmEngine([rule()])
        self.assertFalse(engine.options["store_status_changes"])
        await engine.process_state("sensor.temp", "20")
        for value in range(21, 121):
            await engine.process_state("sensor.temp", str(value))
        await engine.process_state("sensor.temp", "0")
        events = await engine.history_store.query_events()
        self.assertEqual([event.event_type for event in events], ["cleared", "activated"])
        self.assertTrue(current_settings({"store_status_changes": True})["store_status_changes"])
