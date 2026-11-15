"""Options flow for AlarmGrid.

The same settings are editable, with live hints, from the AlarmGrid panel
(Settings). This flow stays as a fallback for installs without the panel and
is generated from :mod:`.settings` so both stay in sync.
"""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult, section
from homeassistant.helpers import selector

from .settings import SETTINGS_SECTIONS, SettingField, current_settings, validate_settings


def _selector(item: SettingField) -> Any:
    if item.kind == "bool":
        return bool
    if item.kind in {"int", "float"}:
        return vol.All(
            selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=item.minimum,
                    max=item.maximum,
                    step=1 if item.kind == "int" else 0.01,
                    mode=selector.NumberSelectorMode.BOX,
                )
            ),
            vol.Coerce(int if item.kind == "int" else float),
        )
    if item.kind == "select":
        return selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=list(item.choices),
                translation_key=item.key,
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        )
    if item.kind == "entities":
        return selector.EntitySelector(
            selector.EntitySelectorConfig(domain=item.domain, multiple=True)
        )
    return selector.TextSelector()


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle AlarmGrid options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    def _stored(self) -> dict[str, Any]:
        return {**self._config_entry.data, **self._config_entry.options}

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage integration options."""

        stored = self._stored()
        if user_input is None:
            return self.async_show_form(
                step_id="init", data_schema=self._options_schema(current_settings(stored))
            )

        flat = self._flatten(user_input)
        values, errors = validate_settings(flat, stored)
        if errors:
            return self.async_show_form(
                step_id="init",
                data_schema=self._options_schema({**values, **flat}),
                errors={"base": next(iter(errors.values()))},
            )
        # Keep legacy keys that are no longer editable so downgrades still work.
        return self.async_create_entry(
            title="", data={**self._config_entry.options, **values}
        )

    @staticmethod
    def _flatten(user_input: dict[str, Any]) -> dict[str, Any]:
        flat: dict[str, Any] = {}
        for key, value in user_input.items():
            if isinstance(value, dict):
                flat.update(value)
            else:
                flat[key] = value
        return flat

    def _options_schema(self, options: dict[str, Any]) -> vol.Schema:
        """Build the sectioned options form from the shared settings definition."""

        values = {**current_settings(self._stored()), **options}
        schema: dict[Any, Any] = {}
        for index, group in enumerate(SETTINGS_SECTIONS):
            fields = {
                vol.Optional(item.key, default=values[item.key]): _selector(item)
                for item in group.fields
            }
            schema[vol.Required(group.key)] = section(
                vol.Schema(fields), {"collapsed": index > 0}
            )
        return vol.Schema(schema)
