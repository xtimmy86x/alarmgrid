"""Shared settings definition used by the panel and the options flow."""

import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from custom_components.alarmgrid.const import DEFAULT_OPTIONS, DOMAIN
from custom_components.alarmgrid.settings import (
    SETTING_FIELDS,
    current_settings,
    settings_schema,
    validate_settings,
)
from tests.test_operator_identity import ha_adapters


class SettingsValidationTests(unittest.TestCase):
    def test_every_editable_setting_has_a_default(self):
        for key in SETTING_FIELDS:
            with self.subTest(key=key):
                self.assertIn(key, DEFAULT_OPTIONS)

    def test_current_settings_only_exposes_editable_keys_and_normalizes_lists(self):
        values = current_settings({"media_players": "media_player.a, media_player.b", "group_by": "area"})
        self.assertEqual(set(values), set(SETTING_FIELDS))
        self.assertEqual(values["media_players"], ["media_player.a", "media_player.b"])

    def test_schema_lists_sections_in_order(self):
        self.assertEqual(
            [section["key"] for section in settings_schema()],
            ["sound", "alarm_handling", "telegram", "telegram_interactive", "integration"],
        )

    def test_numbers_are_coerced_and_bounded(self):
        values, errors = validate_settings({"repeat_interval_seconds": "45"}, {})
        self.assertEqual((values["repeat_interval_seconds"], errors), (45, {}))
        for raw, code in (("2", "out_of_range"), ("abc", "invalid_number"), (1.5, "invalid_number"), (True, "invalid_number")):
            with self.subTest(raw=raw):
                self.assertEqual(validate_settings({"repeat_interval_seconds": raw}, {})[1], {"repeat_interval_seconds": code})

    def test_types_choices_and_entity_domains_are_enforced(self):
        _, errors = validate_settings(
            {"auto_shelve_flapping_alarms": "yes", "sound_mode": "loud", "media_players": ["light.kitchen"]}, {}
        )
        self.assertEqual(
            errors,
            {"auto_shelve_flapping_alarms": "invalid_boolean", "sound_mode": "invalid_choice", "media_players": "invalid_entity"},
        )

    def test_unknown_and_legacy_keys_are_ignored(self):
        values, errors = validate_settings({"group_by": "area", "nope": 1}, {})
        self.assertEqual(errors, {})
        self.assertNotIn("group_by", values)

    def test_blank_panel_title_falls_back_to_default(self):
        values, _ = validate_settings({"panel_title": "   "}, {})
        self.assertEqual(values["panel_title"], "AlarmGrid")

    def test_telegram_cross_field_rules(self):
        self.assertEqual(
            validate_settings({"telegram_enabled": True}, {})[1],
            {"telegram_targets": "telegram_targets_required"},
        )
        _, errors = validate_settings(
            {
                "telegram_interactive_enabled": True,
                "telegram_interactive_ack": False,
                "telegram_interactive_shelve": False,
                "telegram_interactive_disable": False,
            },
            {},
        )
        self.assertEqual(
            errors,
            {
                "telegram_interactive_enabled": "telegram_required",
                "telegram_callback_event_entities": "telegram_callback_entities_required",
                "telegram_interactive_ack": "telegram_action_required",
            },
        )
        _, errors = validate_settings(
            {
                "telegram_enabled": True,
                "telegram_targets": ["notify.ops"],
                "telegram_interactive_enabled": True,
                "telegram_callback_event_entities": ["event.telegram"],
            },
            {},
        )
        self.assertEqual(errors, {})


class SettingsWebsocketTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.entry = SimpleNamespace(entry_id="entry", data={"instance_name": "AG"}, options={"group_by": "area"})
        self.update_entry = Mock()
        self.hass = SimpleNamespace(
            data={DOMAIN: {"entry": SimpleNamespace(entry_id="entry")}},
            config_entries=SimpleNamespace(
                async_get_entry=lambda entry_id: self.entry if entry_id == "entry" else None,
                async_update_entry=self.update_entry,
            ),
        )

    def connection(self, admin):
        return SimpleNamespace(user=SimpleNamespace(is_admin=admin), send_result=Mock(), send_error=Mock())

    async def test_get_settings_reports_values_layout_and_edit_permission(self):
        with ha_adapters() as (_, ws):
            for admin in (True, False):
                connection = self.connection(admin)
                await ws.websocket_get_settings(self.hass, connection, {"id": 1})
                result = connection.send_result.call_args.args[1]
                self.assertIs(result["can_edit"], admin)
                self.assertEqual(result["values"]["sound_mode"], "browser_only")
                self.assertNotIn("group_by", result["values"])
                self.assertEqual(result["sections"][0]["key"], "sound")

    async def test_update_settings_requires_admin(self):
        with ha_adapters() as (_, ws):
            connection = self.connection(False)
            await ws.websocket_update_settings(self.hass, connection, {"id": 2, "settings": {"sound_mode": "none"}})
        connection.send_error.assert_called_once()
        self.assertEqual(connection.send_error.call_args.args[1], "unauthorized")
        self.update_entry.assert_not_called()

    async def test_update_settings_returns_errors_without_saving(self):
        with ha_adapters() as (_, ws):
            connection = self.connection(True)
            await ws.websocket_update_settings(self.hass, connection, {"id": 3, "settings": {"telegram_enabled": True}})
        self.assertEqual(
            connection.send_result.call_args.args[1],
            {"saved": False, "errors": {"telegram_targets": "telegram_targets_required"}},
        )
        self.update_entry.assert_not_called()

    async def test_update_settings_saves_and_keeps_legacy_options(self):
        with ha_adapters() as (_, ws):
            connection = self.connection(True)
            await ws.websocket_update_settings(
                self.hass, connection, {"id": 4, "settings": {"sound_mode": "none", "repeat_interval_seconds": 60}}
            )
        result = connection.send_result.call_args.args[1]
        self.assertTrue(result["saved"])
        self.assertTrue(result["reloading"])
        saved = self.update_entry.call_args.kwargs["options"]
        self.assertEqual((saved["sound_mode"], saved["repeat_interval_seconds"], saved["group_by"]), ("none", 60, "area"))

    async def test_update_settings_without_changes_does_not_reload(self):
        self.entry.options = current_settings({})
        with ha_adapters() as (_, ws):
            connection = self.connection(True)
            await ws.websocket_update_settings(self.hass, connection, {"id": 5, "settings": {"sound_mode": "browser_only"}})
        self.assertFalse(connection.send_result.call_args.args[1]["reloading"])
        self.update_entry.assert_not_called()


if __name__ == "__main__":
    unittest.main()
