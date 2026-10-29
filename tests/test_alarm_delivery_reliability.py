"""Regression coverage for missing notifications and lifecycle reconciliation."""

import asyncio
import sqlite3
import unittest
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

from custom_components.alarmgrid.alarm_engine import AlarmEngine
from custom_components.alarmgrid.alarm_models import (
    AlarmLifecycleState,
    AlarmRule,
    AlarmRuntimeState,
)
from custom_components.alarmgrid.alarm_notifications import (
    TelegramNotifier,
    async_send_telegram,
    format_telegram_message,
)
from custom_components.alarmgrid.alarm_store import (
    InMemoryHistoryStore,
    MemoryRuleStore,
)
from custom_components.alarmgrid.notification_queue import DeliveryError, TelegramOutbox
from custom_components.alarmgrid.telegram_interactive import TelegramInteractiveManager
from tests.test_notification_queue import Store
from tests.test_notifications import event, options


def make_rule(**changes):
    return AlarmRule.from_dict(
        {
            "id": "fault",
            "name": "Fault",
            "entity_id": "binary_sensor.fault",
            "condition": "is_on",
            "priority": "high",
            **changes,
        }
    )


class AlarmReliabilityTests(unittest.IsolatedAsyncioTestCase):
    async def test_history_failure_does_not_prevent_notification_or_state_persistence(
        self,
    ):
        class BrokenHistory(InMemoryHistoryStore):
            async def add_event(self, item):
                raise sqlite3.OperationalError("database is locked")

        notified, saved = [], []

        async def handle(item):
            notified.append(item.event_type)

        async def persist(states):
            saved.append(states["fault"].is_active)

        engine = AlarmEngine(
            [make_rule()], BrokenHistory(), event_handler=handle, persist_states=persist
        )
        with self.assertLogs(
            "custom_components.alarmgrid.alarm_engine", level="ERROR"
        ) as logs:
            await engine.process_state("binary_sensor.fault", "on")
        self.assertEqual(notified, ["activated"])
        self.assertEqual(saved, [True])
        self.assertIn("rule=fault", str(logs.output))
        self.assertEqual(engine.diagnostics["history_write_failures"], 1)

    async def test_concurrent_pulse_keeps_all_advanced_rule_transitions(self):
        entered, release = asyncio.Event(), asyncio.Event()

        class SlowHistory(InMemoryHistoryStore):
            async def add_event(self, item):
                if not entered.is_set():
                    entered.set()
                    await release.wait()
                await super().add_event(item)

        expression = {
            "type": "group",
            "operator": "and",
            "conditions": [
                {
                    "type": "condition",
                    "entity_id": "binary_sensor.fault",
                    "operator": "is_on",
                },
                {
                    "type": "condition",
                    "entity_id": "binary_sensor.enabled",
                    "operator": "is_on",
                },
            ],
        }
        history = SlowHistory()
        engine = AlarmEngine(
            [
                make_rule(id=identifier, condition_expression=expression)
                for identifier in ("a", "b")
            ],
            history,
        )
        engine.seed_entity_states(
            {"binary_sensor.fault": "off", "binary_sensor.enabled": "on"}
        )
        on = asyncio.create_task(engine.process_state("binary_sensor.fault", "on"))
        await asyncio.wait_for(entered.wait(), 1)
        off = asyncio.create_task(engine.process_state("binary_sensor.fault", "off"))
        await asyncio.sleep(0)
        self.assertFalse(off.done())
        release.set()
        await asyncio.wait_for(asyncio.gather(on, off), 1)
        self.assertEqual(
            [(e.rule_id, e.event_type) for e in history.events],
            [
                ("a", "activated"),
                ("b", "activated"),
                ("a", "cleared"),
                ("b", "cleared"),
            ],
        )

    async def test_state_storage_failure_does_not_drop_later_source_events(self):
        async def broken_persist(states):
            raise OSError("storage unavailable")

        notified = []

        async def handle(item):
            notified.append(item.event_type)

        engine = AlarmEngine(
            [make_rule()], persist_states=broken_persist, event_handler=handle
        )
        with self.assertLogs("custom_components.alarmgrid.alarm_engine", level="ERROR"):
            await engine.process_state("binary_sensor.fault", "on")
            await engine.process_state("binary_sensor.fault", "off")
            await engine.process_state("binary_sensor.fault", "on")
        self.assertEqual(notified, ["activated", "cleared", "activated"])
        self.assertEqual(engine.diagnostics["state_write_failures"], 3)

    async def test_slow_telegram_does_not_block_source_processing(self):
        entered = asyncio.Event()

        async def slow_send(target, message):
            entered.set()
            await asyncio.Event().wait()

        notifier = TelegramNotifier(options(), slow_send)
        outbox = TelegramOutbox(Store(), notifier.async_deliver, notifier.skip_reason)
        notifier.outbox = outbox
        engine = AlarmEngine([make_rule()], event_handler=notifier.notify)
        outbox.start()
        try:
            await asyncio.wait_for(engine.process_state("binary_sensor.fault", "on"), 1)
            await asyncio.wait_for(entered.wait(), 1)
            await asyncio.wait_for(
                engine.process_state("binary_sensor.fault", "off"), 1
            )
            self.assertFalse(engine.states["fault"].is_active)
            self.assertEqual(outbox.diagnostics()["pending"], 2)
        finally:
            await outbox.async_close()

    async def test_existing_alarm_at_setup_is_evaluated_without_duplicate_on_reload(
        self,
    ):
        engine = AlarmEngine([make_rule()])
        await engine.reconcile_states({"binary_sensor.fault": "on"})
        self.assertTrue(engine.states["fault"].is_active)
        restored = AlarmEngine([make_rule()], initial_states=engine.states)
        await restored.reconcile_states({"binary_sensor.fault": "on"})
        self.assertTrue(restored.states["fault"].is_active)
        self.assertEqual(restored.history_store.events, [])

    async def test_stale_restored_state_does_not_hide_next_activation(self):
        engine = AlarmEngine(
            [make_rule()],
            initial_states={
                "fault": AlarmRuntimeState(
                    rule_id="fault",
                    lifecycle_state=AlarmLifecycleState.ACTIVE_UNACK,
                )
            },
        )
        await engine.reconcile_states({"binary_sensor.fault": "off"})
        await engine.process_state("binary_sensor.fault", "on")
        self.assertEqual(
            [e.event_type for e in engine.history_store.events],
            ["cleared", "activated"],
        )

    async def test_startup_does_not_invent_state_changed_events(self):
        engine = AlarmEngine([make_rule(condition="state_changed")])
        await engine.reconcile_states({"binary_sensor.fault": "on"})
        self.assertEqual(engine.history_store.events, [])
        await engine.process_state("binary_sensor.fault", "off")
        self.assertEqual(
            [e.event_type for e in engine.history_store.events], ["activated"]
        )

    async def test_missing_startup_entity_clears_stale_pending_timer(self):
        now = datetime(2026, 10, 29, tzinfo=UTC)
        engine = AlarmEngine(
            [make_rule(delay_on_seconds=5)],
            initial_states={
                "fault": AlarmRuntimeState(
                    rule_id="fault",
                    pending_active_since=now - timedelta(seconds=10),
                    last_state="on",
                )
            },
            now=lambda: now,
        )
        await engine.reconcile_states({"binary_sensor.fault": None})
        self.assertIsNone(engine.next_due_transition_at())
        self.assertEqual(engine.history_store.events, [])
        await engine.process_state("binary_sensor.fault", "on")
        self.assertEqual(engine.next_due_transition_at(), now + timedelta(seconds=5))

    async def test_suspension_expires_without_source_updates(self):
        now = datetime(2026, 10, 29, tzinfo=UTC)
        engine = AlarmEngine([make_rule()], now=lambda: now)
        await engine.process_state("binary_sensor.fault", "on")
        await engine.shelve_alarm("fault", duration_minutes=1)
        self.assertEqual(engine.next_due_transition_at(), now + timedelta(minutes=1))
        now += timedelta(minutes=1)
        await engine.process_due_transitions()
        self.assertTrue(engine.states["fault"].is_active)
        self.assertEqual(
            [e.event_type for e in engine.history_store.events][-2:],
            ["unshelved", "activated"],
        )
        self.assertIsNone(engine.next_due_transition_at())

    async def test_editor_enable_and_disable_follow_runtime_lifecycle(self):
        engine = AlarmEngine([make_rule()])
        await engine.disable_alarm("fault")
        await engine.process_state("binary_sensor.fault", "on")
        await engine.update_rule("fault", {"enabled": True})
        self.assertTrue(engine.states["fault"].is_active)
        await engine.update_rule("fault", {"enabled": False})
        self.assertEqual(
            engine.states["fault"].lifecycle_state, AlarmLifecycleState.DISABLED
        )

    async def test_reenable_and_manual_unshelve_evaluate_current_source(self):
        engine = AlarmEngine([make_rule()])
        await engine.disable_alarm("fault")
        await engine.process_state("binary_sensor.fault", "on")
        await engine.enable_alarm("fault")
        self.assertTrue(engine.states["fault"].is_active)
        await engine.shelve_alarm("fault", duration_minutes=5)
        await engine.unshelve_alarm("fault")
        self.assertTrue(engine.states["fault"].is_active)

    async def test_enable_and_disable_actions_persist_rule_definition_on_reload(self):
        store = MemoryRuleStore([make_rule()])
        engine = await AlarmEngine.from_store(store, InMemoryHistoryStore())
        await engine.disable_alarm("fault")
        restored = await AlarmEngine.from_store(store, InMemoryHistoryStore())
        self.assertFalse(restored.rules["fault"].enabled)
        await restored.process_state("binary_sensor.fault", "on")
        self.assertFalse(restored.states["fault"].is_active)
        await restored.enable_alarm("fault")
        restored_again = await AlarmEngine.from_store(store, InMemoryHistoryStore())
        self.assertTrue(restored_again.rules["fault"].enabled)
        await restored_again.reconcile_states({"binary_sensor.fault": "on"})
        self.assertTrue(restored_again.states["fault"].is_active)
        self.assertEqual(restored_again.history_store.events, [])


class TelegramTransportTests(unittest.IsolatedAsyncioTestCase):
    def hass(self, send, state="unknown"):
        return SimpleNamespace(
            config=SimpleNamespace(language="en"),
            states=SimpleNamespace(
                get=lambda _: SimpleNamespace(state=state) if state else None
            ),
            services=SimpleNamespace(async_call=send),
        )

    async def test_plain_text_with_special_characters_is_explicit(self):
        calls = []

        async def send(*args, **kwargs):
            calls.append(kwargs)
            return {"chats": [{"chat_id": -1, "message_id": 20}]}

        await async_send_telegram(
            self.hass(send), "notify.test", "POMPA_1 <backup> [fault]!"
        )
        self.assertEqual(
            calls[0]["service_data"],
            {"message": "POMPA_1 <backup> [fault]!", "parse_mode": "plain_text"},
        )
        self.assertTrue(calls[0]["return_response"])

    async def test_missing_or_unavailable_target_raises_retryable_error(self):
        async def send(*args, **kwargs):
            self.fail("must wait for target")

        for state in (None, "unavailable"):
            with self.assertRaisesRegex(DeliveryError, "target_unavailable"):
                await async_send_telegram(
                    self.hass(send, state), "notify.test", "Alarm"
                )

    async def test_missing_response_is_not_considered_confirmed_delivery(self):
        async def send(*args, **kwargs):
            return {"chats": []}

        with self.assertRaisesRegex(DeliveryError, "missing_message_identifiers"):
            await async_send_telegram(self.hass(send), "notify.test", "Alarm")

    async def test_long_unicode_fields_are_bounded_and_keep_event_time(self):
        item = event(tag="😀" * 5000, area="a" * 5000, message="<x>" * 5000)
        message = format_telegram_message(item)
        self.assertLessEqual(len(message.encode("utf-16-le")) // 2, 4096)
        self.assertIn("…", message)
        self.assertIn("2026-08-29", message)

    async def test_ambiguous_interactive_timeout_does_not_immediately_double_send(self):
        async def send(*args, **kwargs):
            raise TimeoutError("possibly sent")

        plain = []

        async def fallback(target, message):
            plain.append(message)

        engine = AlarmEngine([make_rule(id="temperature")])
        manager = TelegramInteractiveManager(self.hass(send), engine, {})
        notifier = TelegramNotifier(
            options(telegram_interactive_enabled=True), fallback, manager
        )
        await notifier.notify(event())
        self.assertEqual(plain, [])

    async def test_confirmed_keyboard_rejection_falls_back_to_plain(self):
        class InvalidKeyboard(Exception):
            translation_key = "invalid_inline_keyboard"

        async def send(*args, **kwargs):
            raise InvalidKeyboard()

        plain = []

        async def fallback(target, message):
            plain.append(message)

        manager = TelegramInteractiveManager(
            self.hass(send), AlarmEngine([make_rule(id="temperature")]), {}
        )
        await TelegramNotifier(
            options(telegram_interactive_enabled=True), fallback, manager
        ).notify(event())
        self.assertEqual(len(plain), 1)

    async def test_skip_log_explains_priority_filter(self):
        async def send(target, message):
            self.fail("filtered event")

        with self.assertLogs(
            "custom_components.alarmgrid.alarm_notifications", level="DEBUG"
        ) as logs:
            await TelegramNotifier(options(), send).notify(event(priority="medium"))
        self.assertIn("reason=below_minimum_priority", str(logs.output))


if __name__ == "__main__":
    unittest.main()
