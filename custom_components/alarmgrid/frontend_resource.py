"""Lovelace resource registration for the AlarmGrid card."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_call_later

from .const import DOMAIN, FRONTEND_MODULE

_LOGGER = logging.getLogger(__name__)
_LOVELACE_RESOURCE_REGISTERED = f"{DOMAIN}_lovelace_resource_registered"
_LOVELACE_RESOURCE_URL = FRONTEND_MODULE
_LOVELACE_RESOURCE_PATH = FRONTEND_MODULE.split("?", 1)[0]


def _lovelace_mode(lovelace: Any) -> str:
    """Return the configured Lovelace resource mode."""

    return str(getattr(lovelace, "mode", getattr(lovelace, "resource_mode", "yaml")))


def _schedule_lovelace_resource_retry(hass: HomeAssistant) -> None:
    """Retry Lovelace resource registration after HA finishes loading resources."""

    async_call_later(
        hass,
        5,
        lambda _now: hass.add_job(async_register_lovelace_resource, hass),
    )


async def async_register_lovelace_resource(hass: HomeAssistant) -> None:
    """Persist the custom card module in Lovelace resources when possible.

    Lovelace only auto-loads custom card JavaScript after a browser refresh when the
    module is present in its resources list. The sidebar panel can load this bundle
    during the current session, but dashboard refreshes need a persisted resource.
    """

    if hass.data.get(_LOVELACE_RESOURCE_REGISTERED):
        return

    lovelace = hass.data.get("lovelace")
    if lovelace is None:
        _LOGGER.debug("Lovelace data is not ready; retrying resource registration")
        _schedule_lovelace_resource_retry(hass)
        return

    if _lovelace_mode(lovelace) != "storage":
        _LOGGER.debug(
            "Lovelace resource auto-registration skipped because mode is not storage"
        )
        hass.data[_LOVELACE_RESOURCE_REGISTERED] = True
        return

    resources = getattr(lovelace, "resources", None)
    if resources is None:
        _LOGGER.debug("Lovelace resources are not ready; retrying registration")
        _schedule_lovelace_resource_retry(hass)
        return

    if not getattr(resources, "loaded", True):
        _LOGGER.debug("Lovelace resources are not loaded; retrying registration")
        _schedule_lovelace_resource_retry(hass)
        return

    existing = [
        resource
        for resource in resources.async_items()
        if str(resource.get("url", "")).split("?", 1)[0] == _LOVELACE_RESOURCE_PATH
    ]
    if existing:
        resource = existing[0]
        if resource.get("url") != _LOVELACE_RESOURCE_URL:
            await resources.async_update_item(
                resource["id"],
                {"res_type": "module", "url": _LOVELACE_RESOURCE_URL},
            )
        hass.data[_LOVELACE_RESOURCE_REGISTERED] = True
        return

    await resources.async_create_item(
        {"res_type": "module", "url": _LOVELACE_RESOURCE_URL}
    )
    hass.data[_LOVELACE_RESOURCE_REGISTERED] = True