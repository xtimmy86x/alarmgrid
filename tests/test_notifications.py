import unittest
from datetime import UTC, datetime

from custom_components.industrial_alarm_panel.alarm_engine import AlarmEngine
from custom_components.industrial_alarm_panel.alarm_models import (
    AlarmEvent,
    AlarmRule,
    AlarmRuntimeState,
)
from custom_components.industrial_alarm_panel.alarm_notifications import (
    AlarmNotificationManager,
    TelegramNotifier,
    format_telegram_message,
)
from custom_components.industrial_alarm_panel.alarm_store import InMemoryHistoryStore
from custom_components.industrial_alarm_panel.const import DEFAULT_OPTIONS


def event(event_type: str = "activated", priority: str = "critical", **values):
    return AlarmEvent(
        rule_id="temperature",
        entity_id="sensor.temperature",
        event_type=event_type,
        timestamp=datetime(2026, 8, 29, 8, 42, tzinfo=UTC),
        name="Inverter temperature high",
        priority=priority,
        **values,
    )


def options(**overrides):
    return {
        **DEFAULT_OPTIONS,
        "telegram_enabled": True,
        "telegram_targets": ["notify.telegram_operations"],
        **overrides,
    }


class TelegramNotifierTests(unittest.IsolatedAsyncioTestCase):
    async def test_disabled_and_empty_targets_do_not_send(self):
        calls = []

        async def send(target, message):
            calls.append((target, message))

        await TelegramNotifier(options(telegram_enabled=False), send).notify(event())
        await TelegramNotifier(options(telegram_targets=[]), send).notify(event())
        self.assertEqual(calls, [])

    async def test_activated_and_enabled_cleared_send(self):
        calls = []

        async def send(target, message):
            calls.append((target, message))

        notifier = TelegramNotifier(options(), send)
        await notifier.notify(event())
        await notifier.notify(event("cleared"))
        self.assertEqual(len(calls), 2)
        self.assertIn("ACTIVATED", calls[0][1])
        self.assertIn("CLEARED", calls[1][1])

    async def test_each_optional_lifecycle_flag(self):
        cases = {
            "acknowledged": "telegram_notify_acknowledged",
            "shelved": "telegram_notify_shelved",
            "unshelved": "telegram_notify_unshelved",
            "disabled": "telegram_notify_disabled",
            "enabled": "telegram_notify_enabled",
        }
        for event_type, option in cases.items():
            with self.subTest(event_type=event_type):
                calls = []

                async def send(target, message, captured=calls):
                    captured.append((target, message))

                await TelegramNotifier(options(), send).notify(event(event_type))
                self.assertEqual(calls, [])
                await TelegramNotifier(options(**{option: True}), send).notify(
                    event(event_type)
                )
                self.assertEqual(len(calls), 1)

    async def test_cleared_can_be_disabled(self):
        calls = []

        async def send(target, message):
            calls.append((target, message))

        await TelegramNotifier(options(telegram_notify_cleared=False), send).notify(
            event("cleared")
        )
        self.assertEqual(calls, [])

    async def test_minimum_high_allows_critical_but_not_medium(self):
        calls = []

        async def send(target, message):
            calls.append((target, message))

        notifier = TelegramNotifier(options(telegram_min_priority="high"), send)
        await notifier.notify(event(priority="critical"))
        await notifier.notify(event(priority="high"))
        await notifier.notify(event(priority="medium"))
        self.assertEqual(len(calls), 2)

    async def test_multiple_targets_continue_after_one_failure(self):
        calls = []

        async def send(target, message):
            calls.append(target)
            if target == "notify.missing":
                raise RuntimeError("not found")

        notifier = TelegramNotifier(
            options(
                telegram_targets=[
                    "notify.missing",
                    "notify.telegram_operations",
                ]
            ),
            send,
        )
        await notifier.notify(event())
        self.assertEqual(calls, ["notify.missing", "notify.telegram_operations"])

    async def test_message_omits_empty_optional_fields(self):
        message = format_telegram_message(event())
        self.assertNotIn("Area:", message)
        self.assertNotIn("System:", message)
        self.assertNotIn("Tag:", message)
        self.assertIn("Priority: CRITICAL", message)
        self.assertIn("Time: 08:42", message)

    async def test_manager_isolates_provider_failure(self):
        class BrokenProvider:
            async def notify(self, alarm_event):
                raise RuntimeError("Telegram unavailable")

        await AlarmNotificationManager([BrokenProvider()]).notify(event())


class NotificationLifecycleTests(unittest.IsolatedAsyncioTestCase):
    async def test_failure_does_not_interrupt_activation_or_history(self):
        async def broken_handler(alarm_event):
            raise RuntimeError("Telegram unavailable")

        history = InMemoryHistoryStore()
        rule = AlarmRule.from_dict(
            {
                "id": "temperature",
                "entity_id": "sensor.temperature",
                "name": "Temperature high",
                "condition": "above",
                "threshold": 80,
                "priority": "critical",
            }
        )
        engine = AlarmEngine([rule], history, event_handler=broken_handler)
        await engine.process_state("sensor.temperature", "87.4")
        self.assertEqual(len(history.events), 1)
        self.assertEqual(history.events[0].event_type, "activated")

    async def test_repeated_state_does_not_duplicate_activation(self):
        delivered = []

        async def handler(alarm_event):
            delivered.append(alarm_event)

        rule = AlarmRule.from_dict(
            {
                "id": "fault",
                "entity_id": "binary_sensor.fault",
                "name": "Fault",
                "condition": "is_on",
                "priority": "high",
            }
        )
        engine = AlarmEngine([rule], event_handler=handler)
        await engine.process_state("binary_sensor.fault", "on")
        await engine.process_state("binary_sensor.fault", "on")
        self.assertEqual([item.event_type for item in delivered], ["activated"])

    async def test_initial_persisted_state_is_not_notified(self):
        delivered = []

        async def handler(alarm_event):
            delivered.append(alarm_event)

        rule = AlarmRule.from_dict(
            {
                "id": "fault",
                "entity_id": "binary_sensor.fault",
                "name": "Fault",
                "condition": "is_on",
                "priority": "high",
            }
        )
        AlarmEngine(
            [rule],
            initial_states={
                "fault": AlarmRuntimeState.from_dict(
                    {"rule_id": "fault", "lifecycle_state": "ACTIVE_UNACK"}
                )
            },
            event_handler=handler,
        )
        self.assertEqual(delivered, [])
