"""Tests for AlarmGrid's Lovelace resource registration."""

from __future__ import annotations

import sys
from types import ModuleType, SimpleNamespace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch


class FrontendResourceRegistrationTests(IsolatedAsyncioTestCase):
    async def test_existing_resource_is_updated_without_creating_duplicate(self) -> None:
        """A prior build URL is replaced when its query string changes."""

        homeassistant = ModuleType("homeassistant")
        core = ModuleType("homeassistant.core")
        event = ModuleType("homeassistant.helpers.event")
        helpers = ModuleType("homeassistant.helpers")
        core.HomeAssistant = object
        event.async_call_later = lambda *_args, **_kwargs: None

        modules = {
            "homeassistant": homeassistant,
            "homeassistant.core": core,
            "homeassistant.helpers": helpers,
            "homeassistant.helpers.event": event,
        }
        with patch.dict(sys.modules, modules):
            from custom_components.alarmgrid import frontend_resource

        old_resource = {
            "id": "alarmgrid-resource",
            "res_type": "module",
            "url": "/alarmgrid/frontend/dist/alarmgrid.js?v=2.0.0",
        }
        resources = SimpleNamespace(
            loaded=True,
            async_items=lambda: [old_resource],
            async_update_item=AsyncMock(),
            async_create_item=AsyncMock(),
        )
        hass = SimpleNamespace(
            data={"lovelace": SimpleNamespace(mode="storage", resources=resources)}
        )

        await frontend_resource.async_register_lovelace_resource(hass)

        resources.async_update_item.assert_awaited_once_with(
            "alarmgrid-resource",
            {
                "res_type": "module",
                "url": (
                    "/alarmgrid/frontend/dist/alarmgrid.js"
                    "?v=2.0.0&build=20260829.3"
                ),
            },
        )
        resources.async_create_item.assert_not_awaited()
