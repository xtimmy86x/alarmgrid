import unittest
from datetime import UTC, datetime
from types import SimpleNamespace

from custom_components.alarmgrid.alarm_engine import AlarmEngine
from custom_components.alarmgrid.alarm_models import (
    AlarmEvent,
    AlarmRule,
    AlarmRuntimeState,
)
from custom_components.alarmgrid.alarm_notifications import (
    AlarmNotificationManager,
    TelegramNotifier,
    format_telegram_message,
)
from custom_components.alarmgrid.alarm_store import InMemoryHistoryStore
from custom_components.alarmgrid.const import DEFAULT_OPTIONS
from custom_components.alarmgrid.telegram_interactive import (
    TelegramInteractiveManager,
)


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


def policy_event(policy: str, **values):
    return event(
        metadata={"telegram_notification_policy": policy},
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
    async def test_italian_message_is_fully_localized(self):
        message = format_telegram_message(
            event(source_state="on", source_value="on", priority="high"), "it"
        )
        for expected in ("ALLARME ATTIVO", "Priorità: ALTA", "Stato: on", "Valore: on", "Ora:"):
            self.assertIn(expected, message)
        for english in ("ACTIVATED", "Priority:", "State:", "Value:", "Time:"):
            self.assertNotIn(english, message)

    async def test_unknown_language_falls_back_to_english(self):
        message = format_telegram_message(event(), "de")
        self.assertIn("ACTIVATED", message)
        self.assertIn("Priority: CRITICAL", message)

    async def test_interactive_send_payload_and_response_create_session(self):
        rule = AlarmRule.from_dict({"id": "temperature", "entity_id": "sensor.temperature", "name": "Temperature", "condition": "equal", "threshold": 1, "priority": "critical"})
        engine = SimpleNamespace(
            rules={rule.id: rule},
            states={rule.id: AlarmRuntimeState(rule_id=rule.id, lifecycle_state="active_unack")},
        )

        class Services:
            def __init__(self):
                self.calls = []

            async def async_call(self, domain, service, **kwargs):
                self.calls.append((domain, service, kwargs))
                return {"chats": [{"chat_id": 10, "message_id": 20}]}

        services = Services()
        hass = SimpleNamespace(config=SimpleNamespace(language="en"), services=services)
        manager = TelegramInteractiveManager(hass, engine, {})
        plain = []

        async def send(target, message):
            plain.append((target, message))

        notifier = TelegramNotifier(
            options(telegram_interactive_enabled=True), send, manager
        )
        await notifier.notify(event())
        domain, service, call = services.calls[0]
        self.assertEqual((domain, service), ("telegram_bot", "send_message"))
        self.assertIn("ACTIVATED", call["service_data"]["message"])
        self.assertIsInstance(call["service_data"]["inline_keyboard"][0][0], list)
        self.assertEqual(call["target"], {"entity_id": "notify.telegram_operations"})
        self.assertTrue(call["blocking"])
        self.assertTrue(call["return_response"])
        self.assertEqual(len(manager.sessions), 1)
        self.assertEqual(plain, [])

    async def test_success_without_identifiers_does_not_double_send(self):
        rule = AlarmRule.from_dict({"id": "temperature", "entity_id": "sensor.temperature", "name": "Temperature", "condition": "equal", "threshold": 1})
        engine = SimpleNamespace(rules={rule.id: rule}, states={rule.id: AlarmRuntimeState(rule_id=rule.id, lifecycle_state="active_unack")})

        class Services:
            async def async_call(self, *args, **kwargs):
                return {}

        manager = TelegramInteractiveManager(SimpleNamespace(config=SimpleNamespace(language="en"), services=Services()), engine, {})
        plain = []

        async def send(target, message):
            plain.append((target, message))

        await TelegramNotifier(options(telegram_interactive_enabled=True), send, manager).notify(event())
        self.assertEqual(plain, [])
        self.assertEqual(manager.sessions, {})

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

    async def test_per_rule_policy_controls_priority_filter_only(self):
        calls = []

        async def send(target, message):
            calls.append((target, message))

        notifier = TelegramNotifier(options(telegram_min_priority="high"), send)
        await notifier.notify(policy_event("inherit", priority="medium"))
        await notifier.notify(policy_event("always", priority="medium"))
        await notifier.notify(policy_event("never", priority="critical"))
        self.assertEqual(len(calls), 1)

    async def test_always_still_respects_global_and_event_switches(self):
        calls = []

        async def send(target, message):
            calls.append((target, message))

        alarm_event = policy_event("always", priority="medium")
        await TelegramNotifier(options(telegram_enabled=False), send).notify(alarm_event)
        await TelegramNotifier(
            options(telegram_notify_activated=False), send
        ).notify(alarm_event)
        self.assertEqual(calls, [])

    async def test_never_suppresses_when_all_global_settings_allow(self):
        calls = []

        async def send(target, message):
            calls.append((target, message))

        await TelegramNotifier(
            options(telegram_min_priority="status"), send
        ).notify(policy_event("never", priority="critical"))
        self.assertEqual(calls, [])

    async def test_missing_policy_metadata_inherits_global_threshold(self):
        calls = []

        async def send(target, message):
            calls.append((target, message))

        await TelegramNotifier(
            options(telegram_min_priority="high"), send
        ).notify(event(priority="medium"))
        self.assertEqual(calls, [])

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
    async def test_rule_policy_reaches_notification_flow(self):
        delivered = []

        async def handler(alarm_event):
            delivered.append(alarm_event)

        for policy in ("always", "never"):
            rule = AlarmRule.from_dict(
                {
                    "id": policy,
                    "entity_id": f"binary_sensor.{policy}",
                    "name": policy.title(),
                    "condition": "is_on",
                    "telegram_notification_policy": policy,
                }
            )
            engine = AlarmEngine([rule], event_handler=handler)
            await engine.process_state(rule.entity_id, "on")

        self.assertEqual(
            [item.metadata["telegram_notification_policy"] for item in delivered],
            ["always", "never"],
        )

        calls = []

        async def send(target, message):
            calls.append((target, message))

        notifier = TelegramNotifier(options(telegram_min_priority="critical"), send)
        for alarm_event in delivered:
            await notifier.notify(alarm_event)
        self.assertEqual(len(calls), 1)
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
