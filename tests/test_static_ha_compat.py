import json
import re
import tomllib
import unittest
from pathlib import Path


class StaticHomeAssistantCompatibilityTests(unittest.TestCase):
    def test_options_flow_does_not_assign_read_only_config_entry_property(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/options_flow.py"
        ).read_text()

        self.assertNotIn("self.config_entry =", source)

    def test_options_flow_uses_supported_voluptuous_list_validator(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/options_flow.py"
        ).read_text()

        self.assertNotIn("vol.EnsureList", source)

    def test_frontend_registers_panel_custom_element_name(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn('customElements.define("industrial-alarm-panel"', source)

    def test_frontend_edits_and_displays_telegram_rule_policy(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn('data-new="telegram_notification_policy"', source)
        self.assertIn('telegram_notification_policy: "inherit"', source)
        self.assertIn(
            'rule.telegram_notification_policy || "inherit"', source
        )
        self.assertIn('telegram_table_${rule.telegram_notification_policy', source)
        self.assertIn('telegram_policy_always: "Always notify"', source)
        self.assertIn('telegram_policy_never: "Non notificare mai"', source)

    def test_frontend_registration_is_safe_to_import_more_than_once(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn('customElements.get("industrial-alarm-panel")', source)

    def test_frontend_registers_lovelace_card(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn('customElements.define("industrial-alarm-panel-card"', source)
        self.assertIn("window.customCards", source)
        self.assertIn("setConfig(config = {})", source)
        self.assertIn("getStubConfig()", source)

    def test_lovelace_card_is_a_standalone_summary_not_the_sidebar_table(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()
        card_source = source[source.index("class IndustrialAlarmPanelCard") :]

        self.assertIn("class IndustrialAlarmPanelCard extends HTMLElement", card_source)
        self.assertNotIn("extends IndustrialAlarmPanel", card_source)
        self.assertIn('class="alarm-list"', card_source)
        self.assertNotIn("<table", card_source)
        self.assertIn('window.setInterval(() => this._load(), 5000)', card_source)
        self.assertIn("ALARMS_UPDATED_EVENT", card_source)

    def test_lovelace_card_supports_summary_configuration_and_legacy_tab(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()
        card_source = source[source.index("class IndustrialAlarmPanelCard") :]

        self.assertIn("config.view ?? config.tab", card_source)
        self.assertIn("max_alarms", card_source)
        self.assertIn("config.priorities", card_source)
        self.assertIn("show_open_panel", card_source)
        self.assertIn('history.pushState(null, "", "/industrial-alarms")', card_source)
        self.assertIn('new Event("location-changed")', card_source)
        self.assertIn("prefers-reduced-motion:reduce", card_source)

    def test_lovelace_card_supports_safe_visual_customization(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()
        card_source = source[source.index("class IndustrialAlarmPanelCard") :]

        self.assertIn('header_icon: typeof config.header_icon === "string"', card_source)
        self.assertIn(': "mdi:alarm-light"', card_source)
        self.assertIn("show_header_icon: config.show_header_icon !== false", card_source)
        self.assertIn("this._config.show_header_icon ? `<ha-icon", card_source)
        self.assertIn('icon="${this._escape(this._config.header_icon)}"', card_source)
        self.assertIn("_normalizeCssSize(value, fallback)", card_source)
        self.assertIn("(?:px|rem|em|%)$", card_source)

        defaults = {
            "header_icon_size": "24px",
            "title_font_size": "1.15rem",
            "subtitle_font_size": ".85rem",
            "summary_font_size": ".78rem",
            "alarm_name_font_size": "1rem",
            "alarm_meta_font_size": ".78rem",
            "priority_font_size": ".7rem",
            "action_font_size": ".78rem",
        }
        for option, default in defaults.items():
            with self.subTest(option=option):
                self.assertIn(
                    f'{option}: this._normalizeCssSize(config.{option}, "{default}")',
                    card_source,
                )
                css_property = option.replace("_", "-")
                self.assertIn(f'"--iap-{css_property}"', card_source)
                self.assertIn(f"var(--iap-{css_property}, {default})", card_source)

        # The existing min-width and wrapping guards keep larger valid values usable
        # at the card's mobile breakpoint without introducing horizontal overflow.
        self.assertIn(".heading { display:flex; min-width:0", card_source)
        self.assertIn(".alarm-name { margin:5px 0 2px; min-width:0", card_source)
        self.assertIn("overflow-wrap:anywhere", card_source)
        self.assertIn("@media (max-width:420px)", card_source)

    def test_lovelace_card_splits_header_and_item_action_visibility(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()
        card = source[source.index("class IndustrialAlarmPanelCard") :]

        self.assertIn("const showActions = config.show_actions !== false", card)
        self.assertIn("show_actions: showActions", card)
        self.assertIn("show_header_status: config.show_header_status !== false", card)
        self.assertIn(
            "show_header_actions: config.show_header_actions !== undefined ? config.show_header_actions !== false : showActions",
            card,
        )
        self.assertIn("this._config.show_header_status ? `<p>", card)
        self.assertIn("this._config.show_header_actions ? `<div class=\"header-actions\">", card)
        self.assertIn("this._config.show_actions ? `<div class=\"item-actions\">", card)
        self.assertIn('this._config.hide_header ? "" : `<header>', card)
        self.assertNotIn("this._config.show_actions ? `<div class=\"header-actions\">", card)

    def test_frontend_assets_register_even_when_sidebar_panel_disabled(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/alarm_panel.py"
        ).read_text()

        static_path_index = source.index("async_register_static_paths")
        panel_option_index = source.index("if not options.get(CONF_ENABLE_PANEL, True)")
        self.assertLess(static_path_index, panel_option_index)

    def test_integration_auto_registers_lovelace_resource(self) -> None:
        init_source = Path(
            "custom_components/industrial_alarm_panel/__init__.py"
        ).read_text()
        resource_source = Path(
            "custom_components/industrial_alarm_panel/frontend_resource.py"
        ).read_text()
        manifest = json.loads(
            Path("custom_components/industrial_alarm_panel/manifest.json").read_text()
        )

        self.assertIn("async_register_lovelace_resource", init_source)
        self.assertIn("resources.async_create_item", resource_source)
        self.assertIn("resources.async_update_item", resource_source)
        self.assertIn("FRONTEND_MODULE", resource_source)
        self.assertIn("frontend", manifest["dependencies"])
        self.assertIn("http", manifest["dependencies"])
        self.assertIn("lovelace", manifest["dependencies"])

    def test_panel_registration_uses_home_assistant_panel_custom_api(self) -> None:
        source = Path("custom_components/industrial_alarm_panel/alarm_panel.py").read_text()

        self.assertIn("from homeassistant.components import panel_custom", source)
        self.assertIn("await panel_custom.async_register_panel(", source)
        self.assertIn("trust_external=False", source)
        self.assertNotIn('"trust_external_script"', source)

    def test_frontend_module_url_is_versioned_for_browser_cache_busting(self) -> None:
        source = Path("custom_components/industrial_alarm_panel/const.py").read_text()

        self.assertIn("?v={VERSION}", source)

    def test_integration_schedules_due_alarm_timing_transitions(self) -> None:
        source = Path("custom_components/industrial_alarm_panel/__init__.py").read_text()

        self.assertIn("async_call_later", source)
        self.assertIn("next_due_transition_at", source)
        self.assertIn("process_due_transitions", source)
        self.assertIn("remove_delay_timer", source)

    def test_frontend_subscribes_to_alarm_update_events(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn("subscribeEvents", source)
        self.assertIn("industrial_alarm_panel_alarms_updated", source)
        self.assertIn("_unsubscribeUpdates", source)

    def test_frontend_uses_full_row_alarm_colors_and_neutral_acknowledged_rows(
        self,
    ) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn("alarm-row", source)
        self.assertIn("state-active-unack", source)
        self.assertIn("state-active-ack", source)
        self.assertIn("background: #f3f4f6", source)
        self.assertIn(".alarm-row.priority-critical.state-active-unack", source)

    def test_frontend_supports_light_and_dark_themes_for_panel_and_card(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()
        readme_source = Path("README.md").read_text()

        self.assertIn("_syncTheme", source)
        self.assertIn("theme-${this._effectiveTheme}", source)
        self.assertIn(".theme-light", source)
        self.assertIn(".theme-dark", source)
        self.assertIn("config.theme", source)
        self.assertIn("_hassUsesDarkTheme", source)
        self.assertIn("typeof darkMode === \"boolean\"", source)
        self.assertIn("typeof darkMode === \"string\"", source)
        self.assertIn("prefers-color-scheme: dark", source)
        self.assertIn("theme: \"auto\"", source)
        self.assertNotIn("      heme: \"auto\"", source)
        self.assertIn("theme: auto", readme_source)
        
    def test_frontend_can_create_suggested_alarm_rules(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn("Suggested Rules", source)
        self.assertIn("create_suggested_rules", source)
        self.assertIn("High W", source)
        self.assertIn("Low V", source)
        self.assertIn("Solar C", source)

    def test_frontend_preserves_rule_forms_while_refreshing(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn("_ruleDraft", source)
        self.assertIn("_suggestionDraft", source)
        self.assertIn("_isEditingRulesForm", source)
        self.assertIn("if (!this._isEditingRulesForm()) this._render();", source)

    def test_frontend_has_resizable_listing_columns(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn("_wireColumnResizers", source)
        self.assertIn("_columnWidths", source)
        self.assertIn("col-resizer", source)
        self.assertIn("pointerdown", source)
        self.assertIn("colgroup", source)
        self.assertIn("data-table-id", source)

    def test_frontend_downloads_history_for_a_selected_time_range(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn('type="datetime-local" data-history-range="start"', source)
        self.assertIn('type="datetime-local" data-history-range="end"', source)
        self.assertIn('type: "industrial_alarm_panel/export_history"', source)
        self.assertIn("start_time: start.toISOString()", source)
        self.assertIn("end_time: end.toISOString()", source)
        self.assertIn("industrial-alarm-history-", source)
        
    def test_frontend_delays_alarm_color_and_throttles_browser_horn(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn("_alarmVisualDelayMs = 2000", source)
        self.assertIn("state-pending-color", source)
        self.assertIn("_browserHornCooldownMs = 2000", source)
        self.assertIn("_maybePlayBrowserHorn", source)

    def test_release_version_metadata_is_bumped(self) -> None:
        const_source = Path("custom_components/industrial_alarm_panel/const.py").read_text()
        manifest_source = Path(
            "custom_components/industrial_alarm_panel/manifest.json"
        ).read_text()
        pyproject_source = Path("pyproject.toml").read_text()
        readme_source = Path("README.md").read_text()

        expected_version = "1.0.22"
        const_version_match = re.search(r'^VERSION = "([^"]+)"$', const_source, re.MULTILINE)

        self.assertIsNotNone(const_version_match)
        self.assertNotIn("Current release:", readme_source)
        self.assertIn(f"## What's New in v{expected_version}", readme_source)

        const_version = const_version_match.group(1)
        manifest_version = json.loads(manifest_source)["version"]
        pyproject_version = tomllib.loads(pyproject_source)["project"]["version"]

        self.assertEqual(expected_version, const_version)
        self.assertEqual(
            {expected_version},
            {const_version, manifest_version, pyproject_version},
        )

    def test_websocket_registers_suggested_rule_management_commands(self) -> None:
        source = Path("custom_components/industrial_alarm_panel/websocket_api.py").read_text()

        self.assertIn("websocket_list_suggested_rules", source)
        self.assertIn("websocket_create_suggested_rules", source)
        self.assertIn("websocket_delete_rules", source)
        self.assertIn("select_suggested_rules", source)
        self.assertIn("delete_rules(", source)
        self.assertIn("generated_only", source)
        self.assertIn("rule_ids", source)
        self.assertIn("remove_per_rule_entity_registry_entries", source)

    def test_frontend_previews_and_selects_suggested_rules(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn("list_suggested_rules", source)
        self.assertIn("_previewSuggestedRules", source)
        self.assertIn("_selectedSuggestedRuleIds", source)
        self.assertIn("Create Selected", source)
        self.assertIn("Create All", source)
        self.assertIn("data-suggested-select", source)
        self.assertIn("_clearSuggestedPreview", source)
        self.assertIn("Select All", source)
        self.assertIn("Deselect All", source)
        self.assertIn("_selectAllSuggestedRules", source)
        self.assertIn("_deselectAllSuggestedRules", source)

    def test_frontend_can_bulk_delete_rules(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn("delete_rules", source)
        self.assertIn("_selectedRuleIds", source)
        self.assertIn("_deleteSelectedRules", source)
        self.assertIn("_removeAutoGeneratedRules", source)
        self.assertIn("Remove Auto-Generated Rules", source)
        self.assertIn("data-rule-select", source)

    def test_frontend_preserves_table_horizontal_scroll_on_refresh(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn("_tableScrollLeft", source)
        self.assertIn("_captureTableScroll", source)
        self.assertIn("_restoreTableScroll", source)
        self.assertIn("scrollLeft", source)
        self.assertIn("table[data-table-id]", source)

    def test_frontend_has_mobile_sidebar_toggle_button(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn("_toggleSidebar", source)
        self.assertIn("hass-toggle-menu", source)
        self.assertIn("open: true", source)
        self.assertIn("data-action=\"toggle-menu\"", source)
        self.assertIn("menu-button", source)

    def test_frontend_allows_operator_to_choose_shelve_duration(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn("_shelveDurationMinutes", source)
        self.assertIn("_shelveDurationOptions", source)
        self.assertIn("data-field=\"shelve-duration\"", source)
        self.assertIn("1 day", source)
        self.assertIn("3 days", source)
        self.assertIn("7 days", source)
        self.assertIn("duration_minutes: this._shelveDurationMinutes", source)

    def test_frontend_displays_shelve_expiry(self) -> None:
        source = Path(
            "custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js"
        ).read_text()

        self.assertIn("Shelved Until", source)
        self.assertIn("shelve_expiry", source)

    def test_suppression_websocket_commands_delegate_to_engine(self) -> None:
        source = Path("custom_components/industrial_alarm_panel/websocket_api.py").read_text()

        for command in ("unshelve", "disable", "enable"):
            self.assertIn(f'"industrial_alarm_panel/{command}"', source)
            self.assertIn(f"websocket_{command}", source)
            self.assertIn(f"engine.{command}_alarm(", source)
        self.assertGreaterEqual(source.count("operator=connection.user.id"), 7)
        self.assertIn('comment=msg.get("comment")', source)
        self.assertIn('{"unshelved": True}', source)
        self.assertIn('{"disabled": True}', source)
        self.assertIn('{"enabled": True}', source)

    def test_lovelace_card_supports_suppression_views_and_actions(self) -> None:
        source = Path("custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js").read_text()
        card = source[source.index("class IndustrialAlarmPanelCard") :]

        self.assertIn('["active", "unacknowledged", "shelved", "disabled", "inactive"]', card)
        self.assertIn('inactive: ["SHELVED", "DISABLED"]', card)
        self.assertIn('data-open-shelve', card)
        self.assertIn('data-open-disable', card)
        self.assertIn('data-unshelve', card)
        self.assertIn('data-enable', card)
        self.assertIn('show_shelve_action', card)
        self.assertIn('show_disable_action', card)
        self.assertIn('show_restore_actions', card)
        self.assertIn('duration_minutes', card)
        for minutes in ("15", "60", "240", "480", "1440", "4320", "10080"):
            self.assertIn(f'<option value="{minutes}">', card)
        self.assertIn('Number.isFinite(minutes) && minutes > 0', card)
        self.assertIn('Math.ceil(minutes)', card)
        self.assertIn('mdi:dots-vertical', card)
        self.assertIn('aria-label=', card)
        self.assertIn('dialog::backdrop', card)
        self.assertIn('@media (max-width:420px)', card)
        self.assertIn('force-light', card)
        self.assertIn('force-dark', card)

    def test_lovelace_item_action_menu_is_visible_and_not_clipped(self) -> None:
        source = Path("custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js").read_text()
        card = source[source.index("class IndustrialAlarmPanelCard") :]

        self.assertIn('const showActions = config.show_actions !== false', card)
        self.assertIn('show_actions: showActions', card)
        self.assertIn('show_shelve_action: config.show_shelve_action !== false', card)
        self.assertIn('show_disable_action: config.show_disable_action !== false', card)
        self.assertIn('activeActions && (this._config.show_shelve_action || this._config.show_disable_action)', card)
        self.assertIn('alarm.acknowledged ? "disabled" : ""', card)
        self.assertIn('.icon-button { display:grid; place-items:center; width:44px; height:44px;', card)
        self.assertIn('.action-menu summary ha-icon { display:block; width:24px; height:24px; color:var(--primary-text-color);', card)
        self.assertIn('.alarm-item { --priority:var(--iap-status); position:relative; display:flex; min-width:0;', card)
        self.assertIn('overflow:visible;', card)
        self.assertNotIn('background:color-mix(in srgb, var(--ha-card-background, var(--card-background-color)) 96%, var(--priority)); overflow:hidden;', card)

    def test_lovelace_item_action_menu_closes_cleanly(self) -> None:
        source = Path("custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js").read_text()
        card = source[source.index("class IndustrialAlarmPanelCard") :]

        self.assertIn('event.key !== "Escape"', card)
        self.assertIn('document.addEventListener("pointerdown", this._closeActionMenus)', card)
        self.assertIn('document.removeEventListener("pointerdown", this._closeActionMenus)', card)
        self.assertIn('details.action-menu[open]', card)
        self.assertIn('if (other !== menu) other.open = false', card)


if __name__ == "__main__":
    unittest.main()
