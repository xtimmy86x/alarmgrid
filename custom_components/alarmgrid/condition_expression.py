"""Validated, structured condition expressions for advanced alarm rules."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .alarm_models import AlarmValidationError

MAX_EXPRESSION_DEPTH = 4
MAX_EXPRESSION_NODES = 64
GROUP_OPERATORS = {"and", "or"}
CONDITION_OPERATORS = {
    "above",
    "below",
    "greater_or_equal",
    "less_or_equal",
    "between",
    "outside_range",
    "equal",
    "not_equal",
    "contains",
    "is_on",
    "is_off",
    "state_changed",
    "unavailable",
}
NUMERIC_OPERATORS = {
    "above",
    "below",
    "greater_or_equal",
    "less_or_equal",
    "between",
    "outside_range",
}
RANGE_OPERATORS = {"between", "outside_range"}
VALUE_OPERATORS = {
    "above",
    "below",
    "greater_or_equal",
    "less_or_equal",
    "equal",
    "not_equal",
    "contains",
}


def _number(value: Any, field: str) -> float:
    if isinstance(value, bool):
        raise AlarmValidationError(f"{field} must be numeric")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise AlarmValidationError(f"{field} must be numeric") from exc


def validate_condition_expression(expression: Any) -> dict[str, Any]:
    """Validate and return a JSON-native copy of an expression tree."""

    count = 0

    def visit(node: Any, depth: int) -> dict[str, Any]:
        nonlocal count
        if not isinstance(node, dict):
            raise AlarmValidationError("condition expression nodes must be objects")
        count += 1
        if count > MAX_EXPRESSION_NODES:
            raise AlarmValidationError(
                f"condition expression exceeds {MAX_EXPRESSION_NODES} nodes"
            )
        node_type = node.get("type")
        if node_type == "group":
            if depth > MAX_EXPRESSION_DEPTH:
                raise AlarmValidationError(
                    f"condition expression nesting exceeds depth {MAX_EXPRESSION_DEPTH}"
                )
            operator = str(node.get("operator", "")).lower()
            if operator not in GROUP_OPERATORS:
                raise AlarmValidationError(
                    f"unknown group operator: {operator or '<missing>'}"
                )
            children = node.get("conditions")
            if not isinstance(children, list) or not children:
                raise AlarmValidationError(
                    "condition group must contain at least one node"
                )
            return {
                "type": "group",
                "operator": operator,
                "conditions": [visit(child, depth + 1) for child in children],
            }
        if node_type != "condition":
            raise AlarmValidationError(
                f"unknown condition expression node type: {node_type or '<missing>'}"
            )
        entity_id = str(node.get("entity_id") or "").strip()
        if not entity_id:
            raise AlarmValidationError("entity_id is required for a condition")
        operator = str(node.get("operator") or "").lower()
        if operator not in CONDITION_OPERATORS:
            raise AlarmValidationError(
                f"unknown condition operator: {operator or '<missing>'}"
            )
        result: dict[str, Any] = {
            "type": "condition",
            "entity_id": entity_id,
            "operator": operator,
        }
        if operator in RANGE_OPERATORS:
            lower, upper = (
                _number(node.get("lower"), "lower"),
                _number(node.get("upper"), "upper"),
            )
            if lower >= upper:
                raise AlarmValidationError("lower must be less than upper")
            result.update(lower=lower, upper=upper)
        elif operator in VALUE_OPERATORS:
            if "value" not in node:
                raise AlarmValidationError(f"value is required for {operator}")
            result["value"] = (
                _number(node["value"], "value")
                if operator in NUMERIC_OPERATORS
                else node["value"]
            )
        if operator in NUMERIC_OPERATORS:
            deadband = _number(node.get("deadband", 0), "deadband")
            if deadband < 0:
                raise AlarmValidationError("deadband cannot be negative")
            result["deadband"] = deadband
        return result

    return visit(expression, 1)


def expression_entity_ids(expression: Mapping[str, Any]) -> set[str]:
    """Return every source entity referenced by an expression."""
    if expression.get("type") == "condition":
        return {str(expression["entity_id"])}
    result: set[str] = set()
    for child in expression.get("conditions", []):
        result.update(expression_entity_ids(child))
    return result


@dataclass(slots=True)
class ExpressionEvaluationResult:
    """Pure expression evaluation result."""

    matched: bool
    details: dict[str, Any]


def evaluate_condition_expression(
    expression: Mapping[str, Any],
    current_states: Mapping[str, Any],
    previous_states: Mapping[str, Any],
    *,
    currently_active: bool = False,
) -> ExpressionEvaluationResult:
    """Evaluate a validated expression without Home Assistant dependencies."""
    leaves: list[dict[str, Any]] = []

    def leaf(node: Mapping[str, Any]) -> bool:
        entity_id, operator = str(node["entity_id"]), str(node["operator"])
        if entity_id not in current_states:
            leaves.append(
                {
                    "entity_id": entity_id,
                    "operator": operator,
                    "matched": False,
                    "current_value": None,
                    "reason": "entity_not_found",
                }
            )
            return False
        raw = current_states[entity_id]
        state = "" if raw is None else str(getattr(raw, "state", raw))
        normalized = state.strip().lower()
        matched, reason = False, None
        if operator == "unavailable":
            matched = normalized == "unavailable"
        elif normalized == "unavailable":
            reason = "entity_unavailable"
        elif operator == "state_changed":
            matched = (
                entity_id in previous_states
                and str(previous_states[entity_id]) != state
            )
        elif operator == "is_on":
            matched = normalized == "on"
        elif operator == "is_off":
            matched = normalized == "off"
        elif operator == "contains":
            matched = str(node["value"]) in state
        elif operator == "equal":
            matched = state == str(node["value"])
        elif operator == "not_equal":
            matched = state != str(node["value"])
        else:
            try:
                value = float(state)
            except (TypeError, ValueError):
                reason = "not_numeric"
            else:
                db = float(node.get("deadband", 0))
                if operator == "above":
                    matched = value > float(node["value"]) - (
                        db if currently_active else 0
                    )
                elif operator == "greater_or_equal":
                    matched = value >= float(node["value"]) - (
                        db if currently_active else 0
                    )
                elif operator == "below":
                    matched = value < float(node["value"]) + (
                        db if currently_active else 0
                    )
                elif operator == "less_or_equal":
                    matched = value <= float(node["value"]) + (
                        db if currently_active else 0
                    )
                elif operator == "between":
                    low, high = float(node["lower"]), float(node["upper"])
                    matched = (
                        low - (db if currently_active else 0)
                        <= value
                        <= high + (db if currently_active else 0)
                    )
                elif operator == "outside_range":
                    low, high = float(node["lower"]), float(node["upper"])
                    matched = value < low + (
                        db if currently_active else 0
                    ) or value > high - (db if currently_active else 0)
        item = {
            "entity_id": entity_id,
            "operator": operator,
            "matched": matched,
            "current_value": state,
        }
        if reason:
            item["reason"] = reason
        leaves.append(item)
        return matched

    def visit(node: Mapping[str, Any]) -> bool:
        if node["type"] == "condition":
            return leaf(node)
        values = [visit(child) for child in node["conditions"]]
        return all(values) if node["operator"] == "and" else any(values)

    matched = visit(expression)
    matched_count = sum(item["matched"] for item in leaves)
    return ExpressionEvaluationResult(
        matched,
        {
            "matched": matched,
            "matched_conditions": matched_count,
            "total_conditions": len(leaves),
            "conditions": leaves,
        },
    )
