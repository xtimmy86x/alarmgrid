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

        from custom_components.alarmgrid.settings import SETTINGS_SECTIONS

        def form(**integration):
            return {group.key: {} for group in SETTINGS_SECTIONS} | {"integration": integration}

        handler = OptionsFlowHandler(SimpleNamespace(data={}, options={}))
        for enabled in (True, False):
            schema = handler._options_schema({**DEFAULT_OPTIONS, CONF_CREATE_RULE_BUTTONS: enabled})
            self.assertIs(schema(form())["integration"][CONF_CREATE_RULE_BUTTONS], enabled)
            changed = schema(form(**{CONF_CREATE_RULE_BUTTONS: not enabled}))
            self.assertIs(changed["integration"][CONF_CREATE_RULE_BUTTONS], not enabled)
            with self.assertRaises(vol.Invalid):
                schema(form(**{CONF_CREATE_RULE_BUTTONS: "false"}))

    def test_options_form_is_split_into_sections_from_shared_settings(self) -> None:
        from types import SimpleNamespace

        from custom_components.alarmgrid.options_flow import OptionsFlowHandler
        from custom_components.alarmgrid.settings import SETTINGS_SECTIONS

        handler = OptionsFlowHandler(SimpleNamespace(data={}, options={}))
        schema = handler._options_schema({})
        self.assertEqual([str(key) for key in schema.schema], [group.key for group in SETTINGS_SECTIONS])
        flat = handler._flatten({"sound": {"sound_mode": "none"}, "integration": {"panel_title": "X"}})
        self.assertEqual(flat, {"sound_mode": "none", "panel_title": "X"})

if __name__ == "__main__":
    unittest.main()
