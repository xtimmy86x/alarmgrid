"""Side-effect-free rule condition previews."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

from .alarm_models import AlarmRule
from .alarm_rules import evaluate_rule
from .condition_expression import evaluate_condition_expression


def _state_metadata(state: Any) -> tuple[str | None, str | None]:
    attributes = getattr(state, "attributes", {}) or {}
    return attributes.get("friendly_name"), attributes.get("unit_of_measurement")


def _expected(condition: dict[str, Any]) -> Any:
    if condition["operator"] in {"between", "outside_range"}:
        return {"lower": condition["lower"], "upper": condition["upper"]}
    return condition.get("value")


def _expression_leaves(expression: dict[str, Any]) -> list[dict[str, Any]]:
    if expression["type"] == "condition":
        return [expression]
    return [leaf for child in expression["conditions"] for leaf in _expression_leaves(child)]


async def async_preview_rule(
    hass: HomeAssistant,
    engine: Any,
    rule_data: dict[str, Any],
    *,
    rule_id: str | None = None,
) -> dict[str, Any]:
    """Validate and evaluate a draft without touching live engine state."""
    normalized = dict(rule_data)
    if not normalized.get("id"):
        normalized["id"] = "__preview__"
    if not normalized.get("name"):
        normalized["name"] = "Rule preview"
    rule = AlarmRule.from_dict(normalized)

    runtime = engine.states.get(rule_id) if rule_id else None
    currently_active = bool(runtime and runtime.is_active)
    previous_states = getattr(engine, "_previous_entity_states", {})

    if rule.condition_expression is not None:
        entity_ids = rule.source_entity_ids
        current_states = {
            entity_id: state
            for entity_id in entity_ids
            if (state := hass.states.get(entity_id)) is not None
        }
        result = evaluate_condition_expression(
            rule.condition_expression,
            current_states,
            previous_states,
            currently_active=currently_active,
        )
        leaves = _expression_leaves(rule.condition_expression)
        conditions = []
        for detail, condition in zip(result.details["conditions"], leaves, strict=True):
            state = current_states.get(detail["entity_id"])
            friendly_name, unit = _state_metadata(state)
            item = dict(detail)
            item.update(
                friendly_name=friendly_name,
                unit=unit,
                expected=_expected(condition),
                deadband=condition.get("deadband", 0),
            )
            if condition["operator"] == "state_changed" and detail["entity_id"] not in previous_states:
                item.update(matched=False, reason="previous_state_unavailable")
            conditions.append(item)
        # Re-evaluate root semantics after diagnostic overrides (currently only state_changed).
        by_id = iter(item["matched"] for item in conditions)
        def visit(node: dict[str, Any]) -> bool:
            if node["type"] == "condition":
                return next(by_id)
            values = [visit(child) for child in node["conditions"]]
            return all(values) if node["operator"] == "and" else any(values)
        matched = visit(rule.condition_expression)
    else:
        entity_id = rule.entity_id
        state = hass.states.get(entity_id)
        previous = previous_states.get(entity_id)
        if state is None:
            detail = {"entity_id": entity_id, "operator": rule.condition.value, "current_value": None, "matched": False, "reason": "entity_not_found"}
            matched = False
        else:
            evaluation = evaluate_rule(rule, state.state, previous, currently_active=currently_active)
            matched = evaluation.matched
            reason = evaluation.reason
            if state.state == "unavailable" and rule.condition.value != "unavailable":
                reason = "entity_unavailable"
            if rule.condition.value == "state_changed" and entity_id not in previous_states:
                matched, reason = False, "previous_state_unavailable"
            detail = {"entity_id": entity_id, "operator": rule.condition.value, "current_value": state.state, "matched": matched, "reason": reason}
        friendly_name, unit = _state_metadata(state)
        detail.update(friendly_name=friendly_name, unit=unit, expected=rule.threshold, deadband=rule.deadband)
        conditions = [detail]

    matched_count = sum(bool(item["matched"]) for item in conditions)
    total = len(conditions)
    return {
        "matched": matched,
        "condition_mode": "advanced" if rule.condition_expression is not None else "simple",
        "matched_conditions": matched_count,
        "total_conditions": total,
        "summary": f"{matched_count} / {total} conditions matched",
        "conditions": conditions,
        "currently_active": currently_active,
        "delays": {
            "alarm_seconds": rule.delay_on_seconds,
            "clear_seconds": rule.delay_off_seconds,
            "min_active_duration_seconds": rule.min_active_duration_seconds,
            "repeat_alarm_after_seconds": rule.repeat_alarm_after_seconds,
        },
        "timers_simulated": False,
    }
