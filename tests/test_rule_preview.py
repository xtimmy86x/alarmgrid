"""Tests for the pure rule preview helper."""

import unittest
from pathlib import Path
from types import SimpleNamespace

from custom_components.alarmgrid.rule_preview import async_preview_rule


class States:
    def __init__(self, values):
        self.values = values

    def get(self, entity_id):
        return self.values.get(entity_id)


def state(value, name=None, unit=None):
    return SimpleNamespace(
        state=str(value),
        attributes={"friendly_name": name, "unit_of_measurement": unit},
    )


class RulePreviewTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.engine = SimpleNamespace(
            rules={"active": object()},
            states={"active": SimpleNamespace(is_active=True)},
            _previous_entity_states={},
        )

    async def preview(self, values, rule, rule_id=None):
        hass = SimpleNamespace(states=States(values))
        return await async_preview_rule(hass, self.engine, rule, rule_id=rule_id)

    async def test_simple_uses_real_evaluator_and_metadata(self):
        result = await self.preview(
            {"sensor.temperature": state(90, "Temperature", "°C")},
            {"entity_id": "sensor.temperature", "condition": "above", "threshold": 80},
        )
        self.assertTrue(result["matched"])
        self.assertEqual("simple", result["condition_mode"])
        self.assertEqual("Temperature", result["conditions"][0]["friendly_name"])
        self.assertEqual("°C", result["conditions"][0]["unit"])

    async def test_advanced_and_partial_and_or(self):
        leaves = [
            {"type": "condition", "entity_id": "sensor.temperature", "operator": "above", "value": 180},
            {"type": "condition", "entity_id": "switch.fan", "operator": "is_off"},
        ]
        rule = {"condition_expression": {"type": "group", "operator": "and", "conditions": leaves}}
        result = await self.preview({"sensor.temperature": state(190), "switch.fan": state("off")}, rule)
        self.assertTrue(result["matched"])
        self.assertEqual((2, 2), (result["matched_conditions"], result["total_conditions"]))
        partial = await self.preview({"sensor.temperature": state(190), "switch.fan": state("on")}, rule)
        self.assertFalse(partial["matched"])
        self.assertEqual(1, partial["matched_conditions"])
        rule["condition_expression"]["operator"] = "or"
        self.assertTrue((await self.preview({"sensor.temperature": state(100), "switch.fan": state("off")}, rule))["matched"])

    async def test_missing_and_unavailable_diagnostics(self):
        missing = await self.preview({}, {"entity_id": "sensor.missing", "condition": "above", "threshold": 1})
        self.assertEqual("entity_not_found", missing["conditions"][0]["reason"])
        unavailable = await self.preview({"sensor.test": state("unavailable")}, {"entity_id": "sensor.test", "condition": "above", "threshold": 1})
        self.assertEqual("entity_unavailable", unavailable["conditions"][0]["reason"])
        matches = await self.preview({"sensor.test": state("unavailable")}, {"entity_id": "sensor.test", "condition": "unavailable"})
        self.assertTrue(matches["matched"])

    async def test_existing_active_rule_deadband_uses_draft_without_mutation(self):
        rules_before = dict(self.engine.rules)
        states_before = dict(self.engine.states)
        result = await self.preview(
            {"sensor.temperature": state(76)},
            {"entity_id": "sensor.temperature", "condition": "above", "threshold": 80, "deadband": 5},
            "active",
        )
        self.assertTrue(result["matched"])
        self.assertTrue(result["currently_active"])
        self.assertEqual(rules_before, self.engine.rules)
        self.assertEqual(states_before, self.engine.states)
        self.assertFalse(result["timers_simulated"])

    async def test_state_changed_never_invents_previous_state(self):
        result = await self.preview({"sensor.test": state("on")}, {"entity_id": "sensor.test", "condition": "state_changed"})
        self.assertFalse(result["matched"])
        self.assertEqual("previous_state_unavailable", result["conditions"][0]["reason"])


class RulePreviewFrontendTests(unittest.TestCase):
    def test_frontend_contract_and_dom_flush(self):
        source = Path("custom_components/alarmgrid/frontend/dist/alarmgrid.js").read_text()
        self.assertIn('data-action="test-rule"', source)
        self.assertIn('type:"alarmgrid/test_rule"', source)
        method = source[source.index("async _testRule()") : source.index("async _createRule()") if source.index("async _createRule()") > source.index("async _testRule()") else len(source)]
        self.assertLess(method.index("_syncConditionBuilderFromDom()"), method.index("_callWS"))
        self.assertIn("_rulePreviewLoading", source)
        self.assertIn("preview.error", source)
