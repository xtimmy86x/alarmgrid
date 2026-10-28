import importlib.util
import unittest


@unittest.skipUnless(
    importlib.util.find_spec("homeassistant"),
    "Home Assistant is not installed in this environment",
)
class OptionsFlowImportTests(unittest.TestCase):
    def test_options_flow_module_imports(self) -> None:
        import custom_components.alarmgrid.options_flow as options_flow

        self.assertTrue(hasattr(options_flow, "OptionsFlowHandler"))

    def test_rule_button_option_is_boolean_and_keeps_the_saved_value(self) -> None:
        import voluptuous as vol
        from types import SimpleNamespace

        from custom_components.alarmgrid.const import CONF_CREATE_RULE_BUTTONS, DEFAULT_OPTIONS
        from custom_components.alarmgrid.options_flow import OptionsFlowHandler

        handler = OptionsFlowHandler(SimpleNamespace(data={}, options={}))
        for enabled in (True, False):
            schema = handler._options_schema({**DEFAULT_OPTIONS, CONF_CREATE_RULE_BUTTONS: enabled})
            self.assertIs(schema({})[CONF_CREATE_RULE_BUTTONS], enabled)
            self.assertIs(schema({CONF_CREATE_RULE_BUTTONS: not enabled})[CONF_CREATE_RULE_BUTTONS], not enabled)
            with self.assertRaises(vol.Invalid):
                schema({CONF_CREATE_RULE_BUTTONS: "false"})


if __name__ == "__main__":
    unittest.main()
