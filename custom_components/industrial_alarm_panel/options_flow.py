"""Options flow for Industrial Alarm Panel."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    CONF_ALARM_FLOOD_THRESHOLD,
    CONF_ALARM_FLOOD_WINDOW_SECONDS,
    CONF_AUTO_HIDE_CLEARED_ACK,
    CONF_AUTO_SHELVE_FLAPPING,
    CONF_COMPACT_MODE,
    CONF_DEFAULT_DEADBAND,
    CONF_DEFAULT_DELAY_OFF,
    CONF_DEFAULT_DELAY_ON,
    CONF_DEFAULT_TAB,
    CONF_ENABLE_FLASHING,
    CONF_FLAPPING_DETECTION_THRESHOLD,
    CONF_GROUP_BY,
    CONF_HISTORY_RETENTION_DAYS,
    CONF_MAX_ACTIVE_ALARMS,
    CONF_MAX_HISTORY_ROWS,
    CONF_MEDIA_PLAYERS,
    CONF_PANEL_TITLE,
    CONF_REPEAT_INTERVAL_SECONDS,
    CONF_REPEAT_UNTIL_SILENCED,
    CONF_REQUIRE_ACK_CLEARED,
    CONF_SHOW_CLEARED_UNACK,
    CONF_SOUND_MODE,
    CONF_STORE_NORMAL_EVENTS,
    CONF_STORE_STATUS_CHANGES,
    CONF_TELEGRAM_ENABLED,
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


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Industrial Alarm Panel options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage integration options."""

        if user_input is not None:
            media_players = user_input.get(CONF_MEDIA_PLAYERS)
            if isinstance(media_players, str):
                user_input[CONF_MEDIA_PLAYERS] = [
                    item.strip() for item in media_players.split(",") if item.strip()
                ]
            if user_input.get(CONF_TELEGRAM_ENABLED) and not user_input.get(
                CONF_TELEGRAM_TARGETS
            ):
                return self.async_show_form(
                    step_id="init",
                    data_schema=self._options_schema(
                        {
                            **DEFAULT_OPTIONS,
                            **self._config_entry.data,
                            **self._config_entry.options,
                            **user_input,
                        }
                    ),
                    errors={CONF_TELEGRAM_TARGETS: "telegram_targets_required"},
                )
            return self.async_create_entry(title="", data=user_input)

        options = {
            **DEFAULT_OPTIONS,
            **self._config_entry.data,
            **self._config_entry.options,
        }
        return self.async_show_form(
            step_id="init",
            data_schema=self._options_schema(options),
        )

    def _options_schema(self, options: dict[str, Any]) -> vol.Schema:
        """Build the options form, including opt-in Telegram delivery."""

        return vol.Schema(
            {
                vol.Optional(
                    CONF_MAX_ACTIVE_ALARMS,
                    default=options[CONF_MAX_ACTIVE_ALARMS],
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=5000)),
                vol.Optional(
                    CONF_MAX_HISTORY_ROWS,
                    default=options[CONF_MAX_HISTORY_ROWS],
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=50000)),
                vol.Optional(
                    CONF_HISTORY_RETENTION_DAYS,
                    default=options[CONF_HISTORY_RETENTION_DAYS],
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=3650)),
                vol.Optional(
                    CONF_STORE_STATUS_CHANGES,
                    default=options[CONF_STORE_STATUS_CHANGES],
                ): bool,
                vol.Optional(
                    CONF_STORE_NORMAL_EVENTS,
                    default=options[CONF_STORE_NORMAL_EVENTS],
                ): bool,
                vol.Optional(
                    CONF_AUTO_HIDE_CLEARED_ACK,
                    default=options[CONF_AUTO_HIDE_CLEARED_ACK],
                ): bool,
                vol.Optional(
                    CONF_SHOW_CLEARED_UNACK,
                    default=options[CONF_SHOW_CLEARED_UNACK],
                ): bool,
                vol.Optional(
                    CONF_REQUIRE_ACK_CLEARED,
                    default=options[CONF_REQUIRE_ACK_CLEARED],
                ): bool,
                vol.Optional(
                    CONF_SOUND_MODE,
                    default=options[CONF_SOUND_MODE],
                ): vol.In(SOUND_MODES),
                vol.Optional(
                    CONF_MEDIA_PLAYERS,
                    default=",".join(options[CONF_MEDIA_PLAYERS]),
                ): str,
                vol.Optional(
                    CONF_REPEAT_UNTIL_SILENCED,
                    default=options[CONF_REPEAT_UNTIL_SILENCED],
                ): bool,
                vol.Optional(
                    CONF_REPEAT_INTERVAL_SECONDS,
                    default=options[CONF_REPEAT_INTERVAL_SECONDS],
                ): vol.All(vol.Coerce(int), vol.Range(min=5, max=3600)),
                vol.Optional(
                    CONF_DEFAULT_DELAY_ON,
                    default=options[CONF_DEFAULT_DELAY_ON],
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=86400)),
                vol.Optional(
                    CONF_DEFAULT_DELAY_OFF,
                    default=options[CONF_DEFAULT_DELAY_OFF],
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=86400)),
                vol.Optional(
                    CONF_DEFAULT_DEADBAND,
                    default=options[CONF_DEFAULT_DEADBAND],
                ): vol.All(vol.Coerce(float), vol.Range(min=0)),
                vol.Optional(
                    CONF_ALARM_FLOOD_THRESHOLD,
                    default=options[CONF_ALARM_FLOOD_THRESHOLD],
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=10000)),
                vol.Optional(
                    CONF_ALARM_FLOOD_WINDOW_SECONDS,
                    default=options[CONF_ALARM_FLOOD_WINDOW_SECONDS],
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=3600)),
                vol.Optional(
                    CONF_AUTO_SHELVE_FLAPPING,
                    default=options[CONF_AUTO_SHELVE_FLAPPING],
                ): bool,
                vol.Optional(
                    CONF_FLAPPING_DETECTION_THRESHOLD,
                    default=options[CONF_FLAPPING_DETECTION_THRESHOLD],
                ): vol.All(vol.Coerce(int), vol.Range(min=2, max=1000)),
                vol.Optional(
                    CONF_PANEL_TITLE,
                    default=options.get(CONF_PANEL_TITLE, PANEL_TITLE),
                ): str,
                vol.Optional(
                    CONF_DEFAULT_TAB,
                    default=options[CONF_DEFAULT_TAB],
                ): vol.In(
                    [
                        "active",
                        "unacknowledged",
                        "history",
                        "shelved",
                        "disabled",
                        "rules",
                        "settings",
                    ]
                ),
                vol.Optional(
                    CONF_ENABLE_FLASHING,
                    default=options[CONF_ENABLE_FLASHING],
                ): bool,
                vol.Optional(
                    CONF_COMPACT_MODE,
                    default=options[CONF_COMPACT_MODE],
                ): bool,
                vol.Optional(
                    CONF_GROUP_BY,
                    default=options[CONF_GROUP_BY],
                ): vol.In(["area", "system", "priority", "none"]),
                vol.Optional(
                    CONF_TELEGRAM_ENABLED,
                    default=options[CONF_TELEGRAM_ENABLED],
                ): bool,
                vol.Optional(
                    CONF_TELEGRAM_TARGETS,
                    default=options[CONF_TELEGRAM_TARGETS],
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="notify", multiple=True)
                ),
                vol.Optional(
                    CONF_TELEGRAM_MIN_PRIORITY,
                    default=options[CONF_TELEGRAM_MIN_PRIORITY],
                ): vol.In(["critical", "high", "medium", "low", "info", "status"]),
                vol.Optional(
                    CONF_TELEGRAM_NOTIFY_ACTIVATED,
                    default=options[CONF_TELEGRAM_NOTIFY_ACTIVATED],
                ): bool,
                vol.Optional(
                    CONF_TELEGRAM_NOTIFY_CLEARED,
                    default=options[CONF_TELEGRAM_NOTIFY_CLEARED],
                ): bool,
                vol.Optional(
                    CONF_TELEGRAM_NOTIFY_ACKNOWLEDGED,
                    default=options[CONF_TELEGRAM_NOTIFY_ACKNOWLEDGED],
                ): bool,
                vol.Optional(
                    CONF_TELEGRAM_NOTIFY_SHELVED,
                    default=options[CONF_TELEGRAM_NOTIFY_SHELVED],
                ): bool,
                vol.Optional(
                    CONF_TELEGRAM_NOTIFY_UNSHELVED,
                    default=options[CONF_TELEGRAM_NOTIFY_UNSHELVED],
                ): bool,
                vol.Optional(
                    CONF_TELEGRAM_NOTIFY_DISABLED,
                    default=options[CONF_TELEGRAM_NOTIFY_DISABLED],
                ): bool,
                vol.Optional(
                    CONF_TELEGRAM_NOTIFY_ENABLED,
                    default=options[CONF_TELEGRAM_NOTIFY_ENABLED],
                ): bool,
            }
        )
