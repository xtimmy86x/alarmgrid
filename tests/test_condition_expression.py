"""Advanced condition expression tests."""

import unittest

from custom_components.alarmgrid.alarm_models import AlarmRule, AlarmValidationError
from custom_components.alarmgrid.condition_expression import (
    evaluate_condition_expression,
    validate_condition_expression,
)


def condition(entity, operator="equal", **values):
    return {"type": "condition", "entity_id": entity, "operator": operator, **values}


class ConditionExpressionTests(unittest.TestCase):
    def evaluate(self, operator, left, right):
        expression = {
            "type": "group",
            "operator": operator,
            "conditions": [
                condition("sensor.a", value="on"),
                condition("sensor.b", value="on"),
            ],
        }
        return evaluate_condition_expression(
            validate_condition_expression(expression),
            {"sensor.a": left, "sensor.b": right},
            {},
        ).matched

    def test_and_or_truth_tables(self):
        for left, right in (("on", "on"), ("on", "off"), ("off", "on"), ("off", "off")):
            self.assertEqual(self.evaluate("and", left, right), left == right == "on")
            self.assertEqual(
                self.evaluate("or", left, right), left == "on" or right == "on"
            )

    def test_nested_groups(self):
        expression = validate_condition_expression(
            {
                "type": "group",
                "operator": "and",
                "conditions": [
                    condition("a", value="on"),
                    {
                        "type": "group",
                        "operator": "or",
                        "conditions": [
                            condition("b", value="on"),
                            condition("c", value="on"),
                        ],
                    },
                ],
            }
        )
        self.assertTrue(
            evaluate_condition_expression(
                expression, {"a": "on", "b": "off", "c": "on"}, {}
            ).matched
        )
        self.assertFalse(
            evaluate_condition_expression(
                expression, {"a": "off", "b": "on", "c": "on"}, {}
            ).matched
        )

    def test_numeric_boundaries_and_deadband(self):
        cases = [
            ("above", 10, 10, False),
            ("below", 10, 10, False),
            ("greater_or_equal", 10, 10, True),
            ("less_or_equal", 10, 10, True),
        ]
        for operator, value, state, expected in cases:
            result = evaluate_condition_expression(
                condition("x", operator, value=value, deadband=0), {"x": state}, {}
            )
            self.assertEqual(expected, result.matched)
        node = condition("x", "above", value=100, deadband=5)
        self.assertFalse(
            evaluate_condition_expression(
                node, {"x": 99}, {}, currently_active=False
            ).matched
        )
        self.assertTrue(
            evaluate_condition_expression(
                node, {"x": 101}, {}, currently_active=False
            ).matched
        )
        self.assertTrue(
            evaluate_condition_expression(
                node, {"x": 98}, {}, currently_active=True
            ).matched
        )
        self.assertFalse(
            evaluate_condition_expression(
                node, {"x": 94}, {}, currently_active=True
            ).matched
        )

    def test_range_validation_and_missing_entity_details(self):
        with self.assertRaisesRegex(AlarmValidationError, "lower must be less"):
            validate_condition_expression(condition("x", "between", lower=8, upper=2))
        result = evaluate_condition_expression(
            condition("missing", "unavailable"), {}, {}
        )
        self.assertEqual("entity_not_found", result.details["conditions"][0]["reason"])

    def test_advanced_rule_round_trip_and_sources(self):
        data = {
            "id": "multi",
            "name": "Multi",
            "condition_expression": {
                "type": "group",
                "operator": "and",
                "conditions": [
                    condition("sensor.a", value="on"),
                    condition("switch.b", "is_off"),
                ],
            },
        }
        rule = AlarmRule.from_dict(data)
        self.assertEqual({"sensor.a", "switch.b"}, rule.source_entity_ids)
        self.assertEqual(
            rule.condition_expression,
            AlarmRule.from_dict(rule.to_dict()).condition_expression,
        )

    def test_limits_and_validation(self):
        with self.assertRaises(AlarmValidationError):
            validate_condition_expression(
                {
                    "type": "group",
                    "operator": "xor",
                    "conditions": [condition("x", value=1)],
                }
            )
        with self.assertRaises(AlarmValidationError):
            validate_condition_expression(
                {"type": "group", "operator": "and", "conditions": []}
            )
        with self.assertRaises(AlarmValidationError):
            validate_condition_expression(condition("x", "above", value=1, deadband=-1))
