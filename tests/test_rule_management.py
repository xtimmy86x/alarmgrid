import unittest

from custom_components.alarmgrid.alarm_engine import AlarmEngine
from custom_components.alarmgrid.alarm_models import (
    AlarmRule,
    AlarmValidationError,
)
from custom_components.alarmgrid.alarm_store import InMemoryHistoryStore
from custom_components.alarmgrid.rule_management import (
    delete_rules,
    export_rules_csv,
    import_rules_csv,
    matching_per_rule_entity_entries,
    per_rule_entity_unique_ids,
)


class FakeRegistryEntry:
    def __init__(self, entity_id: str, unique_id: str, config_entry_id: str) -> None:
        self.entity_id = entity_id
        self.unique_id = unique_id
        self.config_entry_id = config_entry_id


class FakeEngine:
    def __init__(self, rules: list[AlarmRule]) -> None:
        self.rules = {rule.id: rule for rule in rules}
        self.delete_rule_calls: list[str] = []

    async def delete_rule(self, rule_id: str) -> None:
        self.delete_rule_calls.append(rule_id)
        self.rules.pop(rule_id)


def make_rule(rule_id: str, entity_id: str = "sensor.source") -> AlarmRule:
    return AlarmRule.from_dict(
        {
            "id": rule_id,
            "entity_id": entity_id,
            "name": rule_id.replace("_", " ").title(),
            "condition": "above",
            "threshold": 10,
            "priority": "medium",
        }
    )


class RuleManagementTests(unittest.IsolatedAsyncioTestCase):
    def test_rules_csv_round_trip_preserves_values_and_escaping(self) -> None:
        rule = AlarmRule.from_dict(
            {
                "id": "temperature_high",
                "entity_id": "sensor.temperature",
                "name": 'Temperature, "high"',
                "description": "Line one\nLine two",
                "condition": "above",
                "threshold": 42.5,
                "priority": "high",
                "enabled": False,
                "audible": False,
                "telegram_notification_policy": "always",
            }
        )

        imported = import_rules_csv(export_rules_csv([rule]))

        self.assertEqual(len(imported), 1)
        self.assertEqual(imported[0].to_dict(), rule.to_dict())

    def test_legacy_and_empty_policy_csv_default_to_inherit(self) -> None:
        legacy = (
            "id,entity_id,name,condition,threshold\n"
            "legacy,sensor.one,Legacy,above,1\n"
        )
        empty = (
            "id,entity_id,name,condition,threshold,telegram_notification_policy\n"
            "empty,sensor.two,Empty,above,2,\n"
        )

        self.assertEqual(
            import_rules_csv(legacy)[0].telegram_notification_policy.value, "inherit"
        )
        self.assertEqual(
            import_rules_csv(empty)[0].telegram_notification_policy.value, "inherit"
        )

    def test_rules_csv_rejects_invalid_policy(self) -> None:
        content = (
            "id,entity_id,name,condition,threshold,telegram_notification_policy\n"
            "bad,sensor.one,Bad,above,1,sometimes\n"
        )
        with self.assertRaisesRegex(
            AlarmValidationError, "Unsupported Telegram notification policy"
        ):
            import_rules_csv(content)

    def test_rules_csv_rejects_missing_columns(self) -> None:
        with self.assertRaisesRegex(AlarmValidationError, "missing required columns"):
            import_rules_csv("id,name,condition\nr1,Rule,above\n")

    def test_rules_csv_rejects_duplicate_ids(self) -> None:
        content = (
            "id,entity_id,name,condition,threshold\n"
            "r1,sensor.one,One,above,1\n"
            "r1,sensor.two,Two,below,2\n"
        )

        with self.assertRaisesRegex(AlarmValidationError, "duplicate rule id r1"):
            import_rules_csv(content)

    async def test_delete_selected_rules_deduplicates_and_treats_auto_ids_normally(self) -> None:
        engine = AlarmEngine(
            [make_rule("a"), make_rule("b"), make_rule("c"), make_rule("auto_legacy")],
            InMemoryHistoryStore(),
        )

        result = await delete_rules(
            engine, rule_ids=["a", "c", "a", "missing", "auto_legacy"]
        )

        self.assertEqual(result.deleted_rule_ids, ["a", "c", "auto_legacy"])
        self.assertEqual(result.skipped_rule_ids, ["missing"])
        self.assertEqual(list(engine.rules), ["b"])

    async def test_delete_explicit_rules_skips_unknown_ids(self) -> None:
        engine = AlarmEngine(
            [make_rule("rule_a"), make_rule("rule_b")], InMemoryHistoryStore()
        )

        result = await delete_rules(engine, rule_ids=["missing", "rule_b"])

        self.assertEqual(result.deleted_rule_ids, ["rule_b"])
        self.assertEqual(result.skipped_rule_ids, ["missing"])
        self.assertIn("rule_a", engine.rules)
        self.assertNotIn("rule_b", engine.rules)

    async def test_delete_rules_delegates_to_engine_delete_rule(self) -> None:
        engine = FakeEngine([make_rule("rule_a"), make_rule("rule_b")])

        result = await delete_rules(engine, rule_ids=["rule_b"])

        self.assertEqual(engine.delete_rule_calls, ["rule_b"])
        self.assertEqual(result.deleted_rule_ids, ["rule_b"])
        self.assertIn("rule_a", engine.rules)
        self.assertNotIn("rule_b", engine.rules)

    def test_per_rule_entity_unique_ids_match_existing_entity_classes(self) -> None:
        rule = make_rule("auto_sensor_powertag_main_power_high_consumption")

        self.assertEqual(
            per_rule_entity_unique_ids("entry-1", rule),
            {
                "alarmgrid_entry-1_alarm_auto_sensor_powertag_main_power_high_consumption",
                "alarmgrid_entry-1_ack_auto_sensor_powertag_main_power_high_consumption_auto_sensor_powertag_main_power_high_consumption",
                "alarmgrid_entry-1_shelve_auto_sensor_powertag_main_power_high_consumption_auto_sensor_powertag_main_power_high_consumption",
                "alarmgrid_entry-1_disable_auto_sensor_powertag_main_power_high_consumption_auto_sensor_powertag_main_power_high_consumption",
            },
        )

    def test_matching_registry_entries_returns_only_current_entry_per_rule_entities(
        self,
    ) -> None:
        rule = make_rule("auto_sensor_power_high_consumption")
        expected_unique_id = (
            "alarmgrid_entry-1_alarm_auto_sensor_power_high_consumption"
        )
        entries = [
            FakeRegistryEntry("binary_sensor.match", expected_unique_id, "entry-1"),
            FakeRegistryEntry(
                "binary_sensor.other_entry", expected_unique_id, "entry-2"
            ),
            FakeRegistryEntry("sensor.source", "sensor.source_unique", "entry-1"),
        ]

        matches = matching_per_rule_entity_entries("entry-1", [rule], entries)

        self.assertEqual(
            [entry.entity_id for entry in matches], ["binary_sensor.match"]
        )


if __name__ == "__main__":
    unittest.main()
