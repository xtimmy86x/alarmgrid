"""Single source of truth for the user-editable AlarmGrid settings.

The panel settings page and the options flow both render and validate these
definitions, so a setting is described, bounded and checked in one place.
Only options that the runtime actually reads are listed here; legacy keys that
older versions stored stay untouched in the entry options.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .const import (
    CONF_ALARM_FLOOD_THRESHOLD,
    CONF_ALARM_FLOOD_WINDOW_SECONDS,
    CONF_AUTO_SHELVE_FLAPPING,
    CONF_CREATE_RULE_BUTTONS,
    CONF_FLAPPING_DETECTION_THRESHOLD,
    CONF_MEDIA_PLAYERS,
    CONF_PANEL_TITLE,
    CONF_REPEAT_INTERVAL_SECONDS,
    CONF_SOUND_MODE,
    CONF_TELEGRAM_CALLBACK_EVENT_ENTITIES,
    CONF_TELEGRAM_ENABLED,
    CONF_TELEGRAM_INTERACTIVE_ACK,
    CONF_TELEGRAM_INTERACTIVE_DISABLE,
    CONF_TELEGRAM_INTERACTIVE_ENABLED,
    CONF_TELEGRAM_INTERACTIVE_SHELVE,
    CONF_TELEGRAM_MIN_PRIORITY,
    CONF_TELEGRAM_NOTIFY_ACKNOWLEDGED,
    CONF_TELEGRAM_NOTIFY_ACTIVATED,
    CONF_TELEGRAM_NOTIFY_CLEARED,
    CONF_TELEGRAM_NOTIFY_DISABLED,
    CONF_TELEGRAM_NOTIFY_ENABLED,
    CONF_TELEGRAM_NOTIFY_SHELVED,
    CONF_TELEGRAM_NOTIFY_UNSHELVED,
    CONF_TELEGRAM_TARGETS,
    DEFAULT_OPTIONS,
    PANEL_TITLE,
    SOUND_MODES,
)

PRIORITIES = ["critical", "high", "medium", "low", "info", "status"]

TELEGRAM_INTERACTIVE_ACTIONS = (
    CONF_TELEGRAM_INTERACTIVE_ACK,
    CONF_TELEGRAM_INTERACTIVE_SHELVE,
    CONF_TELEGRAM_INTERACTIVE_DISABLE,
)


@dataclass(frozen=True)
class SettingField:
    """One editable option."""

    key: str
    kind: str  # bool | int | text | select | entities
    minimum: int | None = None
    maximum: int | None = None
    choices: tuple[str, ...] = ()
    domain: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"key": self.key, "kind": self.kind}
        if self.minimum is not None:
            data["min"] = self.minimum
        if self.maximum is not None:
            data["max"] = self.maximum
        if self.choices:
            data["choices"] = list(self.choices)
        if self.domain:
            data["domain"] = self.domain
        return data


@dataclass(frozen=True)
class SettingSection:
    """A group of related options, rendered as one card / form section."""

    key: str
    fields: tuple[SettingField, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {"key": self.key, "fields": [item.to_dict() for item in self.fields]}


SETTINGS_SECTIONS: tuple[SettingSection, ...] = (
    SettingSection(
        "sound",
        (
            SettingField(CONF_SOUND_MODE, "select", choices=tuple(SOUND_MODES)),
            SettingField(CONF_MEDIA_PLAYERS, "entities", domain="media_player"),
            SettingField(CONF_REPEAT_INTERVAL_SECONDS, "int", 5, 3600),
        ),
    ),
    SettingSection(
        "alarm_handling",
        (
            SettingField(CONF_ALARM_FLOOD_THRESHOLD, "int", 1, 10000),
            SettingField(CONF_ALARM_FLOOD_WINDOW_SECONDS, "int", 1, 3600),
            SettingField(CONF_AUTO_SHELVE_FLAPPING, "bool"),
            SettingField(CONF_FLAPPING_DETECTION_THRESHOLD, "int", 2, 1000),
        ),
    ),
    SettingSection(
        "telegram",
        (
            SettingField(CONF_TELEGRAM_ENABLED, "bool"),
            SettingField(CONF_TELEGRAM_TARGETS, "entities", domain="notify"),
            SettingField(CONF_TELEGRAM_MIN_PRIORITY, "select", choices=tuple(PRIORITIES)),
            SettingField(CONF_TELEGRAM_NOTIFY_ACTIVATED, "bool"),
            SettingField(CONF_TELEGRAM_NOTIFY_CLEARED, "bool"),
            SettingField(CONF_TELEGRAM_NOTIFY_ACKNOWLEDGED, "bool"),
            SettingField(CONF_TELEGRAM_NOTIFY_SHELVED, "bool"),
            SettingField(CONF_TELEGRAM_NOTIFY_UNSHELVED, "bool"),
            SettingField(CONF_TELEGRAM_NOTIFY_DISABLED, "bool"),
            SettingField(CONF_TELEGRAM_NOTIFY_ENABLED, "bool"),
        ),
    ),
    SettingSection(
        "telegram_interactive",
        (
            SettingField(CONF_TELEGRAM_INTERACTIVE_ENABLED, "bool"),
            SettingField(CONF_TELEGRAM_CALLBACK_EVENT_ENTITIES, "entities", domain="event"),
            SettingField(CONF_TELEGRAM_INTERACTIVE_ACK, "bool"),
            SettingField(CONF_TELEGRAM_INTERACTIVE_SHELVE, "bool"),
            SettingField(CONF_TELEGRAM_INTERACTIVE_DISABLE, "bool"),
        ),
    ),
    SettingSection(
        "integration",
        (
            SettingField(CONF_PANEL_TITLE, "text"),
            SettingField(CONF_CREATE_RULE_BUTTONS, "bool"),
        ),
    ),
)

SETTING_FIELDS: dict[str, SettingField] = {
    item.key: item for section in SETTINGS_SECTIONS for item in section.fields
}


def current_settings(options: dict[str, Any]) -> dict[str, Any]:
    """Return the effective value of every editable setting."""

    merged = {**DEFAULT_OPTIONS, **options}
    values: dict[str, Any] = {}
    for key, item in SETTING_FIELDS.items():
        value = merged.get(key)
        if item.kind == "entities":
            value = _entity_list(value)
        elif key == CONF_PANEL_TITLE:
            value = str(value or PANEL_TITLE)
        values[key] = value
    return values


def settings_schema() -> list[dict[str, Any]]:
    """Describe the sections for the panel."""

    return [section.to_dict() for section in SETTINGS_SECTIONS]


def _entity_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, (list, tuple)):
        return [str(item).strip() for item in value if str(item).strip()]
    raise ValueError("invalid_entities")


def validate_settings(
    changes: dict[str, Any], current: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, str]]:
    """Coerce ``changes`` on top of ``current`` and check cross-field rules.

    Returns the full set of normalized editable settings and a mapping of
    field key -> error code. Unknown keys are ignored.
    """

    values = current_settings(current)
    errors: dict[str, str] = {}
    for key, raw in changes.items():
        item = SETTING_FIELDS.get(key)
        if item is None:
            continue
        try:
            values[key] = _coerce(item, raw)
        except ValueError as err:
            errors[key] = str(err)

    if values[CONF_TELEGRAM_ENABLED] and not values[CONF_TELEGRAM_TARGETS]:
        errors.setdefault(CONF_TELEGRAM_TARGETS, "telegram_targets_required")
    if values[CONF_TELEGRAM_INTERACTIVE_ENABLED]:
        if not values[CONF_TELEGRAM_ENABLED]:
            errors.setdefault(CONF_TELEGRAM_INTERACTIVE_ENABLED, "telegram_required")
        if not values[CONF_TELEGRAM_CALLBACK_EVENT_ENTITIES]:
            errors.setdefault(
                CONF_TELEGRAM_CALLBACK_EVENT_ENTITIES,
                "telegram_callback_entities_required",
            )
        if not any(values[key] for key in TELEGRAM_INTERACTIVE_ACTIONS):
            errors.setdefault(CONF_TELEGRAM_INTERACTIVE_ACK, "telegram_action_required")
    return values, errors


def _coerce(item: SettingField, raw: Any) -> Any:
    if item.kind == "bool":
        if not isinstance(raw, bool):
            raise ValueError("invalid_boolean")
        return raw
    if item.kind == "int":
        if isinstance(raw, bool):
            raise ValueError("invalid_number")
        try:
            number = float(raw)
        except (TypeError, ValueError):
            raise ValueError("invalid_number") from None
        if not number.is_integer():
            raise ValueError("invalid_number")
        number = int(number)
        if item.minimum is not None and number < item.minimum:
            raise ValueError("out_of_range")
        if item.maximum is not None and number > item.maximum:
            raise ValueError("out_of_range")
        return number
    if item.kind == "select":
        if raw not in item.choices:
            raise ValueError("invalid_choice")
        return raw
    if item.kind == "text":
        text = str(raw if raw is not None else "").strip()
        if len(text) > 64:
            raise ValueError("too_long")
        return text or PANEL_TITLE
    if item.kind == "entities":
        entities = _entity_list(raw)
        prefix = f"{item.domain}."
        if any(not entity.startswith(prefix) for entity in entities):
            raise ValueError("invalid_entity")
        return list(dict.fromkeys(entities))
    raise ValueError("unsupported")
