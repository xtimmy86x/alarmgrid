# ruff: noqa: F401
import importlib.util
import unittest


@unittest.skipUnless(
    importlib.util.find_spec("homeassistant"),
    "Home Assistant is not installed in this environment",
)
class EntityImportTests(unittest.TestCase):
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
