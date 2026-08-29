# ruff: noqa: F401
import importlib.util
import unittest
from types import SimpleNamespace


@unittest.skipUnless(
    importlib.util.find_spec("homeassistant"),
    "Home Assistant is not installed in this environment",
)
class EntityImportTests(unittest.TestCase):
    def test_alarmgrid_entity_uses_alarmgrid_suggested_object_id_prefix(self) -> None:
        from custom_components.alarmgrid.entity_base import AlarmGridEntity

        runtime = SimpleNamespace(engine=object(), entry_id="test-entry")
        entity = AlarmGridEntity(runtime, "active_count", "Active Count")

        self.assertEqual("alarmgrid_active_count", entity._attr_suggested_object_id)
        self.assertNotEqual(
            "industrial_alarm_active_count", entity._attr_suggested_object_id
        )

    def test_entity_modules_import(self) -> None:
        import custom_components.alarmgrid.binary_sensor
        import custom_components.alarmgrid.button
        import custom_components.alarmgrid.number
        import custom_components.alarmgrid.select
        import custom_components.alarmgrid.sensor
        import custom_components.alarmgrid.switch

        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
