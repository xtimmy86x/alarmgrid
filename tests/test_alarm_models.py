import unittest
from datetime import UTC, datetime, timedelta

from custom_components.alarmgrid.alarm_models import (
    AlarmPriority,
    AlarmRule,
    AlarmRuntimeState,
    AlarmValidationError,
    TelegramNotificationPolicy,
)


class AlarmModelTests(unittest.TestCase):
    def test_alarm_rule_parses_required_fields_and_defaults(self) -> None:
        rule = AlarmRule.from_dict(
            {
                "id": "inverter_high_temp",
                "entity_id": "sensor.inverter_temperature",
                "name": "Inverter High Temperature",
                "condition": "above",
                "threshold": 75,
                "priority": "critical",
            }
        )

        self.assertEqual(rule.id, "inverter_high_temp")
        self.assertEqual(rule.priority, AlarmPriority.CRITICAL)
        self.assertTrue(rule.enabled)
        self.assertTrue(rule.requires_ack)
        self.assertTrue(rule.audible)
        self.assertEqual(rule.slug, "inverter_high_temp")
        self.assertEqual(
            rule.telegram_notification_policy, TelegramNotificationPolicy.INHERIT
        )

    def test_alarm_rule_accepts_each_telegram_notification_policy(self) -> None:
        for value in ("inherit", "always", "never"):
            with self.subTest(policy=value):
                rule = AlarmRule.from_dict(
                    {
                        "id": f"policy_{value}",
                        "entity_id": "sensor.value",
                        "name": "Policy rule",
                        "condition": "above",
                        "threshold": 10,
                        "telegram_notification_policy": value,
                    }
                )
                self.assertEqual(rule.telegram_notification_policy.value, value)

    def test_alarm_rule_rejects_invalid_telegram_notification_policy(self) -> None:
        with self.assertRaisesRegex(
            AlarmValidationError, "Unsupported Telegram notification policy: sometimes"
        ):
            AlarmRule.from_dict(
                {
                    "id": "bad_policy",
                    "entity_id": "sensor.value",
                    "name": "Bad policy",
                    "condition": "above",
                    "threshold": 10,
                    "telegram_notification_policy": "sometimes",
                }
            )

    def test_alarm_rule_telegram_policy_serialization_round_trip(self) -> None:
        rule = AlarmRule.from_dict(
            {
                "id": "always_notify",
                "entity_id": "sensor.value",
                "name": "Always notify",
                "condition": "above",
                "threshold": 10,
                "telegram_notification_policy": "always",
            }
        )

        serialized = rule.to_dict()
        loaded = AlarmRule.from_dict(serialized)

        self.assertEqual(serialized["telegram_notification_policy"], "always")
        self.assertEqual(loaded.to_dict(), serialized)

    def test_alarm_rule_rejects_invalid_priority(self) -> None:
        with self.assertRaisesRegex(AlarmValidationError, "priority"):
            AlarmRule.from_dict(
                {
                    "id": "bad",
                    "entity_id": "sensor.value",
                    "name": "Bad Rule",
                    "condition": "above",
                    "threshold": 10,
                    "priority": "urgent",
                }
            )

    def test_alarm_rule_requires_threshold_for_numeric_conditions(self) -> None:
        with self.assertRaisesRegex(AlarmValidationError, "threshold"):
            AlarmRule.from_dict(
                {
                    "id": "missing_threshold",
                    "entity_id": "sensor.value",
                    "name": "Missing Threshold",
                    "condition": "above",
                }
            )

    def test_runtime_state_round_trips_pending_transition_timestamps(self) -> None:
        pending_active = datetime(2026, 1, 1, tzinfo=UTC)
        pending_clear = pending_active + timedelta(seconds=5)
        state = AlarmRuntimeState(
            rule_id="pump_fault",
            pending_active_since=pending_active,
            pending_clear_since=pending_clear,
        )

        loaded = AlarmRuntimeState.from_dict(state.to_dict())

        self.assertEqual(loaded.pending_active_since, pending_active)
        self.assertEqual(loaded.pending_clear_since, pending_clear)


if __name__ == "__main__":
    unittest.main()
