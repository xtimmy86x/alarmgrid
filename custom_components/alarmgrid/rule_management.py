"""Pure helpers for suggested rule selection and bulk rule cleanup."""

from __future__ import annotations

import csv
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from io import StringIO
from typing import Any, Protocol

from .alarm_models import AlarmRule, AlarmValidationError
from .const import DOMAIN

RULE_CSV_FIELDS = (
    "id",
    "enabled",
    "entity_id",
    "name",
    "tag",
    "area",
    "system",
    "description",
    "condition",
    "threshold",
    "deadband",
    "priority",
    "telegram_notification_policy",
    "requires_ack",
    "audible",
    "sound_profile",
    "delay_on_seconds",
    "delay_off_seconds",
    "min_active_duration_seconds",
    "repeat_alarm_after_seconds",
    "show_when_cleared",
    "auto_ack_on_clear",
    "shelving_allowed",
    "instructions",
    "duration",
    "template",
)

_BOOLEAN_CSV_FIELDS = {
    "enabled",
    "requires_ack",
    "audible",
    "show_when_cleared",
    "auto_ack_on_clear",
    "shelving_allowed",
}


class _RegistryEntry(Protocol):
    entity_id: str
    unique_id: str
    config_entry_id: str


@dataclass(slots=True)
class RuleDeletionResult:
    """Result of a bulk rule deletion request."""

    deleted_rules: list[AlarmRule] = field(default_factory=list)
    skipped_rule_ids: list[str] = field(default_factory=list)

    @property
    def deleted_rule_ids(self) -> list[str]:
        """Return deleted rule IDs in deletion order."""

        return [rule.id for rule in self.deleted_rules]


def export_rules_csv(rules: Iterable[AlarmRule]) -> str:
    """Serialize alarm rules to a spreadsheet-friendly CSV document."""

    output = StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=RULE_CSV_FIELDS, extrasaction="ignore")
    writer.writeheader()
    for rule in rules:
        writer.writerow(rule.to_dict())
    return output.getvalue()


def import_rules_csv(content: str) -> list[AlarmRule]:
    """Parse and validate every alarm rule in a CSV document."""

    if not content.strip():
        raise AlarmValidationError("CSV file is empty")
    try:
        reader = csv.DictReader(StringIO(content.lstrip("\ufeff")))
        if reader.fieldnames is None:
            raise AlarmValidationError("CSV header is missing")
        missing = {"id", "entity_id", "name", "condition"} - set(reader.fieldnames)
        if missing:
            raise AlarmValidationError(
                f"CSV is missing required columns: {', '.join(sorted(missing))}"
            )

        rules: list[AlarmRule] = []
        seen: set[str] = set()
        for row_number, row in enumerate(reader, start=2):
            if None in row:
                raise AlarmValidationError(f"CSV row {row_number} has extra columns")
            data = {key: value for key, value in row.items() if value != ""}
            for field_name in _BOOLEAN_CSV_FIELDS & data.keys():
                value = data[field_name].strip().lower()
                if value not in {"true", "false", "1", "0", "yes", "no"}:
                    raise AlarmValidationError(
                        f"CSV row {row_number}: {field_name} must be true or false"
                    )
                data[field_name] = value in {"true", "1", "yes"}
            rule = AlarmRule.from_dict(data)
            if rule.id in seen:
                raise AlarmValidationError(
                    f"CSV row {row_number}: duplicate rule id {rule.id}"
                )
            seen.add(rule.id)
            rules.append(rule)
    except csv.Error as exc:
        raise AlarmValidationError(f"Invalid CSV: {exc}") from exc

    if not rules:
        raise AlarmValidationError("CSV contains no rules")
    return rules

def is_generated_rule_id(rule_id: str) -> bool:
    """Return whether a rule ID belongs to generated suggestions."""

    return rule_id.startswith("auto_")


def select_suggested_rules(
    suggested_rules: Sequence[dict[str, Any]], rule_ids: Sequence[str] | None
) -> tuple[list[dict[str, Any]], list[str]]:
    """Select suggested rules by ID while preserving request order."""

    if rule_ids is None:
        return list(suggested_rules), []

    suggested_by_id = {str(rule["id"]): rule for rule in suggested_rules}
    selected: list[dict[str, Any]] = []
    skipped: list[str] = []
    seen: set[str] = set()

    for rule_id in rule_ids:
        if rule_id in seen:
            continue
        seen.add(rule_id)

        rule = suggested_by_id.get(rule_id)
        if rule is None:
            skipped.append(rule_id)
            continue
        selected.append(rule)

    return selected, skipped


async def delete_rules(
    engine: Any,
    *,
    generated_only: bool = False,
    rule_ids: Sequence[str] | None = None,
) -> RuleDeletionResult:
    """Delete selected rules from an alarm engine."""

    if not generated_only and rule_ids is None:
        raise AlarmValidationError(
            "delete_rules requires rule_ids or generated_only=True"
        )

    requested_rule_ids = _deduplicate(rule_ids) if rule_ids is not None else None
    skipped_rule_ids: list[str] = []

    if requested_rule_ids is None:
        target_rule_ids = [
            rule_id for rule_id in engine.rules if is_generated_rule_id(rule_id)
        ]
    else:
        target_rule_ids = []
        for rule_id in requested_rule_ids:
            rule = engine.rules.get(rule_id)
            if rule is None or (generated_only and not is_generated_rule_id(rule_id)):
                skipped_rule_ids.append(rule_id)
                continue
            target_rule_ids.append(rule_id)

    deleted_rules: list[AlarmRule] = []
    for rule_id in target_rule_ids:
        rule = engine.rules[rule_id]
        await engine.delete_rule(rule_id)
        deleted_rules.append(rule)

    return RuleDeletionResult(deleted_rules, skipped_rule_ids)


def per_rule_entity_unique_ids(entry_id: str, rule: AlarmRule) -> set[str]:
    """Return unique IDs used by per-rule entities for a rule."""

    return {
        f"{DOMAIN}_{entry_id}_alarm_{rule.id}",
        f"{DOMAIN}_{entry_id}_ack_{rule.slug}_{rule.id}",
        f"{DOMAIN}_{entry_id}_shelve_{rule.slug}_{rule.id}",
        f"{DOMAIN}_{entry_id}_disable_{rule.slug}_{rule.id}",
    }


def matching_per_rule_entity_entries(
    entry_id: str, rules: Iterable[AlarmRule], entries: Iterable[_RegistryEntry]
) -> list[_RegistryEntry]:
    """Return registry entries for current per-rule entities in one config entry."""

    unique_ids = {
        unique_id
        for rule in rules
        for unique_id in per_rule_entity_unique_ids(entry_id, rule)
    }

    return [
        entry
        for entry in entries
        if entry.config_entry_id == entry_id and entry.unique_id in unique_ids
    ]


def remove_per_rule_entity_registry_entries(
    hass: Any, entry_id: str, rules: Iterable[AlarmRule]
) -> list[str]:
    """Remove registry entries belonging to deleted per-rule entities."""

    from homeassistant.helpers import entity_registry as er

    entity_registry = er.async_get(hass)
    entries_for_config_entry = getattr(er, "async_entries_for_config_entry", None)
    if entries_for_config_entry is not None:
        entries = entries_for_config_entry(entity_registry, entry_id)
    else:
        entries = entity_registry.entities.values()

    matches = matching_per_rule_entity_entries(entry_id, rules, entries)
    removed_entity_ids = [entry.entity_id for entry in matches]
    for entity_id in removed_entity_ids:
        entity_registry.async_remove(entity_id)

    return removed_entity_ids


def _deduplicate(rule_ids: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    deduplicated: list[str] = []
    for rule_id in rule_ids:
        if rule_id in seen:
            continue
        seen.add(rule_id)
        deduplicated.append(rule_id)
    return deduplicated
