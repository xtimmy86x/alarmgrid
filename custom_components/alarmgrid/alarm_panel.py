"""Frontend panel registration."""

# ruff: noqa: I001

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components import frontend
from homeassistant.components import panel_custom
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_ENABLE_PANEL,
    CONF_PANEL_TITLE,
    DEFAULT_OPTIONS,
    DOMAIN,
    PANEL_ICON,
    PANEL_TITLE,
    PANEL_URL,
)
from .frontend_version import FRONTEND_DIST, async_get_frontend_module_url

_LOGGER = logging.getLogger(__name__)


async def async_register_panel(hass: HomeAssistant, entry: ConfigEntry) -> Any | None:
    """Register the frontend assets and optional custom sidebar panel."""

    options = {**DEFAULT_OPTIONS, **entry.data, **entry.options}

    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                f"/{DOMAIN}/frontend/dist",
                str(FRONTEND_DIST),
                cache_headers=False,
            )
        ]
    )

    if not options.get(CONF_ENABLE_PANEL, True):
        return None

    await panel_custom.async_register_panel(
        hass,
        frontend_url_path=PANEL_URL,
        webcomponent_name="alarmgrid-panel",
        sidebar_title=options.get(CONF_PANEL_TITLE, PANEL_TITLE),
        sidebar_icon=PANEL_ICON,
        module_url=await async_get_frontend_module_url(hass),
        embed_iframe=False,
        trust_external=False,
        config={
            "entry_id": entry.entry_id,
            "title": options.get(CONF_PANEL_TITLE, PANEL_TITLE),
        },
        require_admin=False,
    )

    def remove_panel() -> None:
        remove = getattr(frontend, "async_remove_panel", None)
        if remove:
            remove(hass, PANEL_URL)
        else:
            _LOGGER.debug("Frontend panel removal API not available")

    return remove_panel
