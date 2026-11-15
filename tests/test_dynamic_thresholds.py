"""Dynamic operands: dependency tracking, invalid data, timers and persistence."""

import unittest
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

from custom_components.alarmgrid.alarm_engine import AlarmEngine
from custom_components.alarmgrid.alarm_models import AlarmRule, AlarmValidationError
from custom_components.alarmgrid.alarm_notifications import format_telegram_message
from custom_components.alarmgrid.alarm_rules import evaluate_rule
from custom_components.alarmgrid.condition_expression import (
    evaluate_condition_expression, validate_condition_expression,
)
from custom_components.alarmgrid.rule_management import export_rules_csv, import_rules_csv
from custom_components.alarmgrid.rule_preview import async_preview_rule


def rule(**changes):
    return AlarmRule.from_dict({
        "id": "temperature", "name": "Temperature", "entity_id": "sensor.temperature",
        "condition": "above", "threshold_entity": "input_number.limit", **changes,
    })


def expression(operator="above"):
    return {"type": "condition", "entity_id": "sensor.temperature", "operator": operator,
            "value_entity": "input_number.limit"}


class DynamicThresholdTests(unittest.IsolatedAsyncioTestCase):
    async def test_either_entity_update_uses_primary_reading(self):
        engine = AlarmEngine([rule()])
        await engine.process_state("sensor.temperature", "30")
        self.assertFalse(engine.states["temperature"].is_active)
        await engine.process_state("input_number.limit", "25")
        self.assertTrue(engine.states["temperature"].is_active)
        self.assertEqual(engine.states["temperature"].last_value, 30)
        self.assertIn("superiore a 25", format_telegram_message(engine.last_event, "it"))
        await engine.process_state("input_number.limit", "35")
        self.assertFalse(engine.states["temperature"].is_active)
        self.assertEqual(engine.states["temperature"].last_value, 30)
        await engine.process_state("sensor.temperature", "40")
        self.assertTrue(engine.states["temperature"].is_active)

    async def test_invalid_values_hold_state_until_recovery(self):
        for advanced in (False, True):
            with self.subTest(advanced=advanced):
                config = rule(condition_expression=expression()) if advanced else rule()
                engine = AlarmEngine([config])
                await engine.reconcile_states({"sensor.temperature": "30", "input_number.limit": "25"})
                for entity in ("input_number.limit", "sensor.temperature"):
                    for invalid in ("unknown", "unavailable", "bad", "NaN", "inf"):
                        await engine.process_state(entity, invalid)
                        self.assertTrue(engine.states["temperature"].is_active, (advanced, entity, invalid))
                        self.assertIsNone(engine.next_due_transition_at())
                    await engine.process_state(entity, "25" if entity.endswith("limit") else "30")
                await engine.process_state("input_number.limit", "40")
                self.assertFalse(engine.states["temperature"].is_active)

    async def test_hysteresis_and_delay_restart_after_invalid_threshold(self):
        now = datetime(2026, 11, 14, tzinfo=UTC)
        engine = AlarmEngine([rule(deadband=2, delay_on_seconds=10)], now=lambda: now)
        await engine.reconcile_states({"sensor.temperature": "30", "input_number.limit": "25"})
        now += timedelta(seconds=6)
        await engine.process_state("input_number.limit", "unavailable")
        self.assertIsNone(engine.next_due_transition_at())
        now += timedelta(seconds=6)
        await engine.process_state("input_number.limit", "25")
        self.assertFalse(engine.states["temperature"].is_active)
        now += timedelta(seconds=10)
        await engine.process_due_transitions()
        self.assertTrue(engine.states["temperature"].is_active)
        await engine.process_state("input_number.limit", "31")
        self.assertTrue(engine.states["temperature"].is_active)
        await engine.process_state("input_number.limit", "33")
        self.assertFalse(engine.states["temperature"].is_active)

    async def test_invalid_during_clear_delay_does_not_clear(self):
        now = datetime(2026, 11, 14, tzinfo=UTC)
        engine = AlarmEngine([rule(delay_off_seconds=10)], now=lambda: now)
        await engine.reconcile_states({"sensor.temperature": "30", "input_number.limit": "25"})
        await engine.process_state("input_number.limit", "35")
        now += timedelta(seconds=5)
        await engine.process_state("input_number.limit", "unknown")
        now += timedelta(seconds=20)
        await engine.process_due_transitions()
        self.assertTrue(engine.states["temperature"].is_active)
        await engine.process_state("input_number.limit", "35")
        now += timedelta(seconds=10)
        await engine.process_due_transitions()
        self.assertFalse(engine.states["temperature"].is_active)

    async def test_nested_groups_track_references_and_hold_on_invalid_leaf(self):
        group = {"type": "group", "operator": "or", "conditions": [
            expression("greater_or_equal"),
            {"type": "group", "operator": "and", "conditions": [
                {"type": "condition", "entity_id": "binary_sensor.fault", "operator": "is_on"},
                expression("less_or_equal"),
            ]},
        ]}
        config = rule(condition_expression=group)
        self.assertEqual(config.source_entity_ids, {"sensor.temperature", "input_number.limit", "binary_sensor.fault"})
        engine = AlarmEngine([config])
        await engine.reconcile_states({"sensor.temperature": "30", "input_number.limit": "35", "binary_sensor.fault": "off"})
        await engine.process_state("input_number.limit", "30")
        self.assertTrue(engine.states["temperature"].is_active)
        await engine.process_state("input_number.limit", "unknown")
        self.assertTrue(engine.states["temperature"].is_active)

    async def test_reenable_and_unshelve_use_latest_threshold(self):
        engine = AlarmEngine([rule()])
        await engine.reconcile_states({"sensor.temperature": "30", "input_number.limit": "25"})
        await engine.shelve_alarm("temperature", duration_minutes=1)
        await engine.process_state("input_number.limit", "40")
        await engine.unshelve_alarm("temperature")
        self.assertFalse(engine.states["temperature"].is_active)
        await engine.disable_alarm("temperature")
        await engine.process_state("input_number.limit", "20")
        await engine.enable_alarm("temperature")
        self.assertTrue(engine.states["temperature"].is_active)

    def test_numeric_and_text_entity_comparisons(self):
        for condition, left, right, matched in (
            ("equal", "20", "20.0", True), ("not_equal", "20", "20.0", False),
            ("equal", "heating", "heating", True), ("contains", "not ready", "ready", True),
            ("above", "20", "19.5", True), ("below", "20", "21", True),
        ):
            with self.subTest(condition=condition):
                self.assertEqual(evaluate_rule(rule(condition=condition), left,
                    current_states={"input_number.limit": right}).matched, matched)
                config = validate_condition_expression(expression(condition))
                self.assertEqual(evaluate_condition_expression(config,
                    {"sensor.temperature": left, "input_number.limit": right}, {}).matched, matched)

    def test_round_trip_and_reject_invalid_configurations(self):
        for config in (rule(), rule(condition_expression=expression())):
            self.assertEqual(AlarmRule.from_dict(config.to_dict()), config)
            imported = import_rules_csv(export_rules_csv([config]))[0]
            self.assertEqual(imported.source_entity_ids, config.source_entity_ids)
            self.assertEqual(imported.threshold_entity, config.threshold_entity)
            self.assertEqual(imported.condition_expression, config.condition_expression)
        for changes in ({"threshold_entity": "invalid"}, {"condition": "is_on"},
                        {"threshold_source": "entity", "threshold_entity": ""}):
            with self.assertRaises(AlarmValidationError):
                rule(**changes)
        for op in ("is_on", "between", "outside_range"):
            with self.assertRaises(AlarmValidationError):
                validate_condition_expression(expression(op))

    async def test_switching_to_fixed_removes_reference_dependency(self):
        engine = AlarmEngine([rule()])
        await engine.update_rule("temperature", {"threshold_entity": None, "threshold": 25})
        self.assertEqual(engine.rules["temperature"].source_entity_ids, {"sensor.temperature"})
        await engine.process_state("sensor.temperature", "30")
        await engine.process_state("input_number.limit", "50")
        self.assertTrue(engine.states["temperature"].is_active)

    async def test_invalid_or_operand_does_not_activate_even_if_other_branch_matches(self):
        group = {"type": "group", "operator": "or", "conditions": [expression(),
            {"type": "condition", "entity_id": "binary_sensor.fault", "operator": "is_on"}]}
        config = rule(condition_expression=group)
        engine = AlarmEngine([config])
        states = {"sensor.temperature": "30", "input_number.limit": "unavailable", "binary_sensor.fault": "on"}
        await engine.reconcile_states(states)
        self.assertFalse(engine.states["temperature"].is_active)
        hass = SimpleNamespace(states=SimpleNamespace(get=lambda entity: SimpleNamespace(state=states[entity])))
        preview = await async_preview_rule(hass, engine, config.to_dict())
        self.assertFalse(preview["matched"])
        await engine.process_state("input_number.limit", "25")
        self.assertTrue(engine.states["temperature"].is_active)

    async def test_telegram_snapshots_localized_decimal_threshold(self):
        engine = AlarmEngine([rule()])
        await engine.reconcile_states({"sensor.temperature": "30", "input_number.limit": "25.5"})
        event = engine.last_event
        await engine.process_state("input_number.limit", "40")
        self.assertIn("superiore a 25,5", format_telegram_message(event, "it"))

    async def test_preview_shows_reference_and_invalid_reason(self):
        states = {"sensor.temperature": SimpleNamespace(state="30"), "input_number.limit": SimpleNamespace(state="25")}
        hass = SimpleNamespace(states=SimpleNamespace(get=states.get))
        engine = AlarmEngine()
        for config in (rule(), rule(condition_expression=expression())):
            preview = await async_preview_rule(hass, engine, config.to_dict())
            self.assertTrue(preview["matched"])
            self.assertEqual(preview["conditions"][0]["expected"], "25")
            states["input_number.limit"].state = "unavailable"
            preview = await async_preview_rule(hass, engine, config.to_dict())
            self.assertFalse(preview["matched"])
            self.assertEqual(preview["conditions"][0]["reason"], "threshold_entity_unavailable")
            states["input_number.limit"].state = "25"
