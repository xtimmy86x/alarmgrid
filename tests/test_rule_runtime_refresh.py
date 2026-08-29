import ast
import asyncio
import unittest
from pathlib import Path
from types import SimpleNamespace

from custom_components.alarmgrid import AlarmGridRuntime, rule_source_entity_ids
from custom_components.alarmgrid.const import RULE_ENTITY_PLATFORMS, Platform

ROOT = Path(__file__).parents[1]


def _function_calls(path: str, function_name: str) -> list[str]:
    tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
    function = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == function_name
    )
    calls = []
    for node in ast.walk(function):
        if not isinstance(node, ast.Call):
            continue
        name = node.func.attr if isinstance(node.func, ast.Attribute) else None
        if name:
            calls.append(name)
    return calls


class RuleRuntimeRefreshTests(unittest.IsolatedAsyncioTestCase):
    def test_rule_source_listener_entities_follow_create_update_delete(self) -> None:
        engine = SimpleNamespace(
            rules={"a": SimpleNamespace(entity_id="sensor.a")}
        )
        engine.rules["b"] = SimpleNamespace(entity_id="sensor.b")
        self.assertEqual(rule_source_entity_ids(engine), ["sensor.a", "sensor.b"])

        engine.rules["b"].entity_id = "sensor.c"
        self.assertEqual(rule_source_entity_ids(engine), ["sensor.a", "sensor.c"])

        del engine.rules["a"]
        self.assertEqual(rule_source_entity_ids(engine), ["sensor.c"])

    def test_only_rule_entity_platforms_are_refreshed(self) -> None:
        self.assertEqual(
            RULE_ENTITY_PLATFORMS,
            [Platform.BINARY_SENSOR, Platform.BUTTON],
        )
        self.assertTrue(
            set(RULE_ENTITY_PLATFORMS).isdisjoint(
                {Platform.SENSOR, Platform.SWITCH, Platform.SELECT, Platform.NUMBER}
            )
        )
        calls = _function_calls(
            "custom_components/alarmgrid/__init__.py", "_refresh_rule_runtime"
        )
        self.assertEqual(calls.count("async_unload_platforms"), 1)
        self.assertEqual(calls.count("async_forward_entry_setups"), 1)
        self.assertNotIn("async_reload", calls)

    async def test_runtime_serializes_rule_refreshes(self) -> None:
        active = 0
        maximum_active = 0

        async def refresh() -> None:
            nonlocal active, maximum_active
            active += 1
            maximum_active = max(maximum_active, active)
            await asyncio.sleep(0)
            active -= 1

        runtime = AlarmGridRuntime(
            entry_id="entry",
            rule_store=None,
            history_store=None,
            sound_manager=None,
            notification_manager=None,
            engine=None,
            refresh_rule_runtime=refresh,
        )
        await asyncio.gather(
            runtime.async_refresh_rules(), runtime.async_refresh_rules()
        )

        self.assertEqual(maximum_active, 1)

    def test_websocket_mutations_refresh_without_full_reload_or_panel_unload(self) -> None:
        expected_refreshes = {
            "websocket_create_rule": 1,
            "websocket_update_rule": 1,
            "websocket_delete_rule": 1,
            "websocket_import_rules": 1,
            "websocket_create_suggested_rules": 1,
            "websocket_delete_rules": 1,
        }
        for function_name, expected in expected_refreshes.items():
            with self.subTest(function_name=function_name):
                calls = _function_calls(
                    "custom_components/alarmgrid/websocket_api.py", function_name
                )
                self.assertEqual(calls.count("async_refresh_rules"), expected)
                self.assertNotIn("async_reload", calls)
                self.assertNotIn("remove_panel", calls)
                self.assertNotIn("async_unload_entry", calls)

    def test_rule_services_use_shared_runtime_refresh_without_reload(self) -> None:
        source = (ROOT / "custom_components/alarmgrid/services.py").read_text(
            encoding="utf-8"
        )
        self.assertEqual(source.count("await runtime.async_refresh_rules()"), 3)
        self.assertNotIn("async_reload", source)
        self.assertNotIn("_reload_entry", source)


if __name__ == "__main__":
    unittest.main()
