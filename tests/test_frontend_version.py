"""Regression tests for content-based frontend cache invalidation."""

from __future__ import annotations

import importlib
import os
import sys
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType, SimpleNamespace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock, patch

from custom_components.alarmgrid import frontend_version
from custom_components.alarmgrid.const import FRONTEND_MODULE, VERSION


class FrontendVersionTests(IsolatedAsyncioTestCase):
    async def test_content_changes_url_even_with_same_size_and_mtime(self) -> None:
        with TemporaryDirectory() as directory:
            bundle = Path(directory) / "alarmgrid.js"
            bundle.write_bytes(b"first")
            mtime = bundle.stat().st_mtime
            hass = SimpleNamespace(async_add_executor_job=AsyncMock(side_effect=lambda fn: fn()))
            with patch.object(frontend_version, "FRONTEND_DIST", Path(directory)):
                first = await frontend_version.async_get_frontend_module_url(hass)
                self.assertEqual(first, await frontend_version.async_get_frontend_module_url(hass))
                self.assertEqual(
                    f"{FRONTEND_MODULE}?v={VERSION}&build={sha256(b'first').hexdigest()[:16]}", first,
                )
                bundle.write_bytes(b"other")
                os.utime(bundle, (mtime, mtime))
                self.assertNotEqual(first, await frontend_version.async_get_frontend_module_url(hass))
            self.assertEqual(hass.async_add_executor_job.await_count, 3)


class FrontendRegistrationTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        modules = {name: ModuleType(name) for name in (
            "homeassistant", "homeassistant.core", "homeassistant.helpers",
            "homeassistant.helpers.event", "homeassistant.components",
            "homeassistant.components.frontend", "homeassistant.components.panel_custom",
            "homeassistant.components.http", "homeassistant.config_entries",
        )}
        modules["homeassistant.core"].HomeAssistant = object
        modules["homeassistant.config_entries"].ConfigEntry = object
        modules["homeassistant.helpers.event"].async_call_later = Mock()
        modules["homeassistant.components.http"].StaticPathConfig = lambda *args, **kwargs: (args, kwargs)
        modules["homeassistant.components.panel_custom"].async_register_panel = AsyncMock()
        with patch.dict(sys.modules, modules):
            self.resource = importlib.import_module("custom_components.alarmgrid.frontend_resource")
            self.panel = importlib.import_module("custom_components.alarmgrid.alarm_panel")
        self.items = []
        self.resources = SimpleNamespace(
            loaded=True, async_items=lambda: self.items,
            async_update_item=AsyncMock(), async_create_item=AsyncMock(),
        )
        self.hass = SimpleNamespace(
            data={"lovelace": SimpleNamespace(mode="storage", resources=self.resources)},
            async_add_executor_job=AsyncMock(side_effect=lambda fn: fn()),
            http=SimpleNamespace(async_register_static_paths=AsyncMock()),
        )
        self.url = frontend_version._frontend_module_url()

    async def test_current_resource_is_not_rewritten(self) -> None:
        self.items[:] = [{"id": "current", "type": "module", "url": self.url}]
        await self.resource.async_register_lovelace_resource(self.hass)
        self.resources.async_update_item.assert_not_awaited()
        self.resources.async_create_item.assert_not_awaited()

    async def test_new_resource_is_created_once(self) -> None:
        await self.resource.async_register_lovelace_resource(self.hass)
        await self.resource.async_register_lovelace_resource(self.hass)
        self.resources.async_create_item.assert_awaited_once_with({"res_type": "module", "url": self.url})

    async def test_changed_bundle_is_registered_again_in_same_session(self) -> None:
        self.items[:] = [{"id": "current", "type": "module", "url": self.url}]
        await self.resource.async_register_lovelace_resource(self.hass)
        with patch.object(self.resource, "async_get_frontend_module_url", AsyncMock(return_value="new-build")):
            await self.resource.async_register_lovelace_resource(self.hass)
        self.resources.async_update_item.assert_awaited_once_with(
            "current", {"res_type": "module", "url": "new-build"},
        )

    async def test_yaml_resources_are_not_modified(self) -> None:
        self.hass.data["lovelace"].mode = "yaml"
        await self.resource.async_register_lovelace_resource(self.hass)
        self.resources.async_create_item.assert_not_awaited()
        self.resources.async_update_item.assert_not_awaited()

    async def test_unloaded_resources_retry_before_registering(self) -> None:
        self.resources.loaded = False
        with patch.object(self.resource, "_schedule_lovelace_resource_retry") as retry:
            await self.resource.async_register_lovelace_resource(self.hass)
            retry.assert_called_once_with(self.hass)
        self.resources.async_create_item.assert_not_awaited()
        self.resources.loaded = True
        await self.resource.async_register_lovelace_resource(self.hass)
        self.resources.async_create_item.assert_awaited_once()

    async def test_panel_and_card_use_identical_versioned_url(self) -> None:
        entry = SimpleNamespace(data={}, options={}, entry_id="test")
        with patch.object(self.panel.panel_custom, "async_register_panel", AsyncMock()) as register:
            await self.panel.async_register_panel(self.hass, entry)
            await self.resource.async_register_lovelace_resource(self.hass)
        self.assertEqual(register.await_args.kwargs["module_url"], self.url)
        self.assertEqual(self.resources.async_create_item.await_args.args[0]["url"], self.url)

    async def test_card_resources_are_served_with_panel_disabled(self) -> None:
        entry = SimpleNamespace(data={}, options={"enable_panel": False}, entry_id="test")
        with patch.object(self.panel.panel_custom, "async_register_panel", AsyncMock()) as register:
            self.assertIsNone(await self.panel.async_register_panel(self.hass, entry))
            register.assert_not_awaited()
        self.hass.http.async_register_static_paths.assert_awaited_once()
