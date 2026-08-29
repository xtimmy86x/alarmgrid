# Industrial Alarm Panel

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://www.hacs.xyz/)
[![GitHub release](https://img.shields.io/github/v/release/xtimmy86x/industrial-alarm-panel?display_name=tag)](https://github.com/xtimmy86x/industrial-alarm-panel/releases)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2025.1%2B-41BDF5.svg)](https://www.home-assistant.io/)
[![License](https://img.shields.io/github/license/xtimmy86x/industrial-alarm-panel)](LICENSE)

Industrial Alarm Panel is an independently maintained Home Assistant custom
integration that provides a DCS-style alarm annunciator for industrial, energy,
and equipment monitoring. Its official repository is
[`xtimmy86x/industrial-alarm-panel`](https://github.com/xtimmy86x/industrial-alarm-panel).

It creates Home Assistant entities, exposes services and a websocket API, persists alarm rules and runtime state, stores alarm history in SQLite, and serves a dedicated sidebar panel at `/industrial-alarms`.

![Industrial Alarm Panel preview](docs/images/industrial-alarm-panel-preview.png)

## Highlights

- Dedicated Home Assistant sidebar panel at `/industrial-alarms`
- DCS-style alarm lifecycle: active, acknowledged, cleared, shelved, disabled
- Dedicated active, unacknowledged, disabled, shelved, and history views
- Priority levels with horn behavior: `critical`, `high`, `medium`, `low`, `info`, `status`
- Per-rule binary sensors and operator action buttons
- Rule storage, runtime state persistence, and SQLite alarm history
- Browser horn and optional media-player sound output
- Suggested alarm rule generator for PowerTag/electrical/solar-water sensors
- Rules editor with CSV import and export
- Compact, configurable Lovelace alarm summary card
- Optional Telegram notifications with per-rule policy, interactive actions, and
  English/Italian messages
- Downloadable diagnostics for troubleshooting
- Event-driven panel refresh with a polling fallback
- HACS-ready repository layout with local Home Assistant brand images

## What's New in v1.1.0

- Industrial Alarm Panel is now independently maintained as a standalone project.
- Updated repository ownership, documentation, HACS links, issue tracking, and
  project metadata.
- Preserved compatibility with existing Home Assistant installations, alarm rules,
  entities, history, Lovelace cards, and Telegram configuration.
- Retained attribution to the original `AlRiachi/industrial-alarm-panel` project
  under the Apache-2.0 license.

This is a non-breaking maintenance release. Existing installations require no
migration and can upgrade normally through HACS.

## What's New in v1.0.24

- Fixed Home Assistant Telegram inline keyboard formatting so interactive buttons
  display and callback correctly.
- Added full English/Italian localization for Telegram alarm messages and actions.
- Hardened callbacks for multiple Telegram bots and stale alarm lifecycle states.
- Added lifecycle tests for ACK, shelving, disable/enable, keyboard payloads, and localization.

## What's New in v1.0.23

- Added opt-in interactive Telegram actions for ACK, temporary shelving, disable,
  unshelve, and enable using Home Assistant's native `telegram_bot` actions.
- Added Telegram callback event entity configuration, inline keyboards, bounded
  runtime sessions, and strict callback validation.
- Kept the outbound-only v1 notification path unchanged when interactivity is off.

## What's New in v1.0.22

- Added per-rule Telegram notification policies: inherit global settings, always notify, or never notify.
- Added Telegram policy controls to the Rules editor and Rules table.
- Preserved backward compatibility for existing rules, which default to global Telegram settings.

## What's New in v1.0.21

- Added opt-in, outbound-only Telegram alarm notifications through Home Assistant
  `notify` entities, without storing Telegram bot tokens, chat IDs, or credentials.
- Added minimum-priority filtering, per-lifecycle-event controls, multiple notification
  targets, and best-effort failure isolation.
- Added English and Italian options-flow labels, privacy-conscious diagnostics, tests,
  and setup documentation for the Telegram notification V1.

## What's New in v1.0.18

- Fixed the Lovelace alarm item's per-alarm action trigger so the 44 px three-dot button remains visible beside ACK in active and unacknowledged views.
- Prevented the Suspend/Disable popup from being clipped by the alarm item while preserving its rounded accent styling.
- Added outside-click, Escape, and single-open-menu behavior, and bumped the frontend cache key.

## What's New in v1.0.16

- Redesigned the Lovelace card as a standalone, responsive alarm summary while retaining the sidebar panel as the complete DCS console.
- Added compact alarm items, summary chips, card-local view and priority filters, configurable metadata/actions, and client-side navigation to the full panel.
- Preserved legacy `tab`, `hide_tabs`, `hide_header`, and `min_height` card configuration compatibility and bumped the frontend cache key.

## What's New in v1.0.15

- Bumped the frontend cache-busting version so the light/dark theme bundle is reloaded by browsers and Lovelace instead of the cached pre-theme build.
- Fixed unreadable `Silence`, `Ack All`, and secondary action buttons in the light theme by using white text and dedicated hover colors on colored buttons.
- Added entity autocomplete to the rule form: the **Entity id** field now suggests all available Home Assistant entities (with friendly names) while typing.
- Added Italian localization: the panel and card UI follow the Home Assistant user language (English and Italian), and the config flow ships an `it.json` translation.
- Localized alarm priorities and lifecycle states in the alarm and history tables (for example `ACTIVE_UNACK` renders as "Active, unacknowledged" / "Attivo, non riconosciuto").
- Added an **Edit** button to each rule row: the rule form switches to edit mode with Save/Cancel and updates the rule through the existing `update_rule` WebSocket command.
- Fixed the "Industrial Alarm Panel is not configured" traceback logged when the panel refreshed during the config entry reload that follows a rule change; the frontend now silently retries while the reload completes.
- Auto-filled the rule **area** from the Home Assistant area of the source entity (entity or device registry) when creating or saving a rule from the panel.
- Added an editable **System** field to the rule form and Area/System columns to the rules table.

## What's New in v1.0.13

- Fixed alarm timing fields so `delay_on_seconds`, `delay_off_seconds`, and `min_active_duration_seconds` now drive the alarm state machine instead of only being stored.
- Added Home Assistant timer scheduling so delayed alarm activations and clears complete even when the source entity does not change again.
- Persisted pending timing state so debounce windows survive Home Assistant storage round-trips.
- Clarified how to use `delay_on_seconds: 5` for alarms that should activate only after the condition lasts longer than 5 seconds.

## What's New in v1.0.12

- Added panel presets for shelving alarms for 1 hour, 4 hours, 8 hours, 1 day, 3 days, or 7 days.
- Added a **Shelved Until** alarm table column so operators can see the current `shelve_expiry`.
- Kept the Home Assistant `shelve_alarm` service duration-based with `duration_minutes`; use `1440` for 1 day, `4320` for 3 days, or `10080` for 7 days.
- Bumped the frontend cache-busting version and package metadata for the new release.

## What's New in v1.0.11

- Added **Select All** and **Deselect All** controls to Suggested Rules previews.
- Added a mobile panel menu button so operators can open the Home Assistant sidebar when edge-swipe is blocked by the panel.
- Preserved horizontal table scroll during alarm, history, rules, and suggested-rule refreshes so wide tables stay on the inspected columns.
- Bumped the frontend cache-busting version and package metadata for the new release.

## What's New in v1.0.9

- Added resizable columns to the alarm, history, rules, and suggested-rule listings.
- Added a 2-second delay before new unacknowledged alarms receive full DCS row coloring, reducing transient visual noise.
- Throttled browser and media-player horn output so repeated Home Assistant refreshes or alarm floods do not stack noisy tones.
- Bumped the frontend cache-busting version and package metadata for the new release.

## What's New in v1.0.8

- Added **Suggested Rules** in the panel Rules tab.
- Suggested rules can create high-consumption, low-voltage, high-voltage, high solar-water temperature, and unavailable-sensor alarms.
- Added full-row DCS-style alarm colors, with acknowledged alarms shown in neutral gray.
- Added event-driven alarm refresh so new alarms appear faster than the polling fallback.
- Fixed Rules tab form inputs being cleared by automatic refresh while an operator is typing.
- Bumped the frontend cache-busting version to force Home Assistant browsers to load the new panel bundle.

## Installation

[![Open your Home Assistant instance and open this repository inside HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=xtimmy86x&repository=industrial-alarm-panel&category=integration)

### HACS

1. Add this repository as a HACS custom repository with category `Integration`:

   ```text
   https://github.com/xtimmy86x/industrial-alarm-panel
   ```

2. Install **Industrial Alarm Panel** from HACS.
3. Restart Home Assistant.
4. Go to **Settings > Devices & services > Add integration** and search for **Industrial Alarm Panel**.

After upgrading through HACS, restart Home Assistant again. If the sidebar panel was already open, hard refresh the browser with `Ctrl+Shift+R`.

The repository follows HACS integration layout rules: all runtime files are under `custom_components/industrial_alarm_panel`, with a root `hacs.json`, GitHub releases, and one integration directory under `custom_components`.

See [INSTALLATION.md](INSTALLATION.md) for manual installation, media-player sound setup, and a test rule.

## Brand Assets

This repository includes local Home Assistant brand assets in `custom_components/industrial_alarm_panel/brand/`:

- `icon.png` and `dark_icon.png`
- `logo.png` and `dark_logo.png`

Home Assistant 2026.3 and newer can serve local brand assets for custom integrations. Older Home Assistant versions still run the integration, but may not show the local icon/logo in all UI surfaces.

## Lovelace Card

The two frontend surfaces now have deliberately different roles: the sidebar panel is the complete DCS alarm console (tables, history, rules, shelving, sound, and settings), while the Lovelace card is a compact, dashboard-first alarm summary. In normal Home Assistant storage-mode dashboards, the integration automatically registers this JavaScript module resource and keeps it versioned:

```yaml
url: /industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js?v=1.1.0
type: module
```

If you use Lovelace YAML mode, add the resource above to `ui-lovelace.yaml` manually. Then add the card to a dashboard:

```yaml
type: custom:industrial-alarm-panel-card
title: Industrial Alarms
view: active
max_alarms: 5
show_summary: true
show_header_status: true
show_header_actions: true
show_actions: true
show_shelve_action: true
show_disable_action: true
show_open_panel: true
theme: auto
```

The same dashboard-first card can also provide focused suppression views:

```yaml
# Temporarily shelved alarms
type: custom:industrial-alarm-panel-card
title: Shelved Alarms
view: shelved
max_alarms: 10
show_restore_actions: true
```

```yaml
# Alarms disabled until manually enabled
type: custom:industrial-alarm-panel-card
title: Disabled Alarms
view: disabled
max_alarms: 10
show_restore_actions: true
```

```yaml
# Both categories, kept visually distinct
type: custom:industrial-alarm-panel-card
title: Suppressed Alarms
view: inactive
max_alarms: 10
show_restore_actions: true
```

**Shelved** means temporary suppression with automatic expiry. **Disabled** means
persistent suppression until the alarm is manually enabled again.

Card options:

- `title`: card heading shown above its metrics and compact actions.
- `view`: alarm list to show: `active` (default), `unacknowledged`, `shelved`, `disabled`, or `inactive` (shelved and disabled together). The card has no tab bar; history, rules, and settings remain in the full sidebar console.
- `max_alarms`: maximum alarm items shown before the “more alarms” link (default `5`). Items retain severity-then-timestamp ordering.
- `show_summary` and `show_open_panel`: toggle the metric chips and full-panel link respectively (both default to `true`).
- `show_header_status`: shows or hides the active/unacknowledged/horn status line under the card title (default `true`).
- `show_header_actions`: shows or hides global header actions such as **Silence horn** and **Ack All** (default `true`). When omitted, it inherits `show_actions` so existing configurations with `show_actions: false` continue to hide all actions.
- `show_actions`: controls only the actions on individual alarms, such as **ACK** and the more-actions menu (default `true`).
- `show_shelve_action` and `show_disable_action`: independently control the temporary-shelve and persistent-disable entries in active/unacknowledged alarm menus (both default to `true`).
- `show_restore_actions`: controls **Unshelve now** and **Enable alarm** in the shelved, disabled, and inactive views (default `true`).
- `show_value`, `show_area`, `show_system`, and `show_tag`: toggle optional alarm item metadata (all default to `true`). Empty values are always omitted.
- `show_shelve` remains accepted for compatibility; setting it to `false` hides the shelving action. New configurations should use `show_shelve_action`.
- `header_icon` selects the Home Assistant MDI icon in the heading (default `mdi:alarm-light`); `show_header_icon` shows or hides it (default `true`).
- `priorities`: optional card-local priority filter. For example:

  ```yaml
  priorities:
    - critical
    - high
  ```

All visual customization options are optional. The existing icon and type sizes
remain the defaults when these options are omitted:

| Option | Default | Affects |
| --- | --- | --- |
| `header_icon` | `mdi:alarm-light` | Header icon |
| `show_header_icon` | `true` | Header icon visibility |
| `show_header_status` | `true` | Active/unacknowledged/horn status line under the title |
| `show_header_actions` | `true` | Global Silence horn and Ack All actions |
| `header_icon_size` | `24px` | Header icon dimensions |
| `title_font_size` | `1.15rem` | Main card title |
| `subtitle_font_size` | `0.85rem` | Active/unacknowledged subtitle |
| `summary_font_size` | `0.78rem` | Summary chips |
| `alarm_name_font_size` | `1rem` | Alarm name |
| `alarm_meta_font_size` | `0.78rem` | Timestamp, tag, context, value, state, and remaining shelf time |
| `priority_font_size` | `0.7rem` | Priority badge |
| `action_font_size` | `0.78rem` | Textual alarm-item actions (not icon-only actions) |

Size options accept non-negative numeric values using `px`, `rem`, `em`, or `%`.
Invalid values are ignored and replaced with the defaults above. For example:

```yaml
type: custom:industrial-alarm-panel-card
title: Allarmi
view: active

header_icon: mdi:shield-alert
header_icon_size: 30px

title_font_size: 20px
subtitle_font_size: 13px
summary_font_size: 12px

alarm_name_font_size: 17px
alarm_meta_font_size: 13px
priority_font_size: 11px
action_font_size: 12px
```

A minimal icon override only needs:

```yaml
type: custom:industrial-alarm-panel-card
view: active
header_icon: mdi:shield-alert
```

To omit the icon without leaving an empty header slot:

```yaml
type: custom:industrial-alarm-panel-card
view: active
show_header_icon: false
```

To keep per-alarm actions while showing only the icon and title in the header:

```yaml
type: custom:industrial-alarm-panel-card
title: Allarmi
view: active

show_header_icon: true
show_header_status: false
show_header_actions: false

show_actions: true
```

This keeps **ACK** and the more-actions menu on each alarm, while removing the
active/unacknowledged/horn status line and the global header controls.

- `theme`: `auto`, `light`, or `dark`; `auto` follows the active Home Assistant light/dark theme. The sidebar panel also follows Home Assistant automatically.
- `hide_header`: set to `true` to hide the complete header (icon, title, status line, and global actions), regardless of the individual header visibility options.
- `min_height`: optional CSS height such as `420px`; defaults to dashboard card sizing instead of the full sidebar height.

Existing configurations remain valid: legacy `tab: active` and `tab: unacknowledged` are treated as aliases for `view`, and `hide_tabs` is accepted as a deprecated no-op because the summary card never renders tabs. Legacy full-console values such as `tab: history` safely fall back to the active alarm summary; open the sidebar panel for those workflows.

The integration registers the static frontend path even when the sidebar panel option is disabled, and it persists the Lovelace resource in storage-mode dashboards so the card is still loaded after a browser refresh.


## Entities

Global entities include:

- `sensor.industrial_alarm_panel_active_count`
- `sensor.industrial_alarm_panel_unacknowledged_count`
- `sensor.industrial_alarm_panel_critical_count`
- `sensor.industrial_alarm_panel_high_count`
- `sensor.industrial_alarm_panel_last_alarm`
- `sensor.industrial_alarm_panel_last_event`
- `binary_sensor.industrial_alarm_panel_any_active`
- `binary_sensor.industrial_alarm_panel_any_unacknowledged`
- `binary_sensor.industrial_alarm_panel_horn_active`
- `switch.industrial_alarm_panel_sound_enabled`
- `button.industrial_alarm_panel_acknowledge_all`
- `button.industrial_alarm_panel_silence_horn`
- `button.industrial_alarm_panel_unsilence_horn`
- `button.industrial_alarm_panel_test_sound`
- `select.industrial_alarm_panel_filter_priority`
- `number.industrial_alarm_panel_history_retention_days`

Every stored rule also gets a binary alarm sensor and action buttons after the integration reloads.

## Rule Creation

Create and manage rules from **Developer Tools > Services**, automations, scripts, or the panel's rule editor.

Rules use stable Home Assistant `entity_id` values. For numeric range alarms, create two rules: one `below` rule and one `above` rule.

### Suggested Rules

Open **Industrial Alarms > Rules > Suggested Rules** and click **Preview Suggested Rules** to scan current Home Assistant `sensor.*` entities before creating anything. Select the suggestions you want, then click **Create Selected**. **Create All** is still available after preview, but it asks for confirmation and shows the estimated Home Assistant entity count.

Default suggested thresholds:

- `High W`: `2000 W` for power/high-consumption sensors
- `Low V`: `207 V`
- `High V`: `253 V`
- `Solar C`: `75 C` for solar water/tank/boiler temperature sensors

The generator detects candidates from `device_class`, unit of measurement, entity ID, and friendly name. It skips generated rule IDs that already exist so repeated previews or creates do not duplicate rules. Generated suggested rules use IDs beginning with `auto_`.

If too many suggested rules were created, use **Remove Auto-Generated Rules** in the same section. It removes stored `auto_` rules and the per-rule alarm/button entities created by this integration, but it does not remove the original source sensors. For manual cleanup, select rows in the Rules table and click **Delete Selected**.

### Rule Fields

Common fields:

- `id`: stable rule ID. Keep it lowercase and unique.
- `entity_id`: source entity to monitor.
- `name`: operator-facing alarm name.
- `tag`: short DCS-style tag.
- `area`: room, plant area, or system area.
- `system`: equipment group, such as `SOFAR Inverter`, `Grid`, or `Electric Heater`.
- `condition`: one of `above`, `below`, `equal`, `not_equal`, `contains`, `is_on`, `is_off`, `state_changed`, `unavailable`, `unavailable_for`, `unknown_for`, `manual`.
- `threshold`: numeric value for `above` and `below`, or expected text for text conditions.
- `deadband`: hysteresis for numeric alarms.
- `priority`: `critical`, `high`, `medium`, `low`, `info`, or `status`.
- `instructions`: short operator guidance shown in the panel.

Optional fields include `requires_ack`, `audible`, `delay_on_seconds`, `delay_off_seconds`, `min_active_duration_seconds`, `repeat_alarm_after_seconds`, `show_when_cleared`, and `shelving_allowed`.

Timing fields are in seconds:

- `delay_on_seconds`: the source condition must remain true for this long before the alarm activates. Use `5` for "alarm only if this condition lasts longer than 5 seconds".
- `delay_off_seconds`: the source condition must remain clear for this long before an active alarm clears.
- `min_active_duration_seconds`: once activated, keep the alarm active for at least this long even if the source clears sooner.

### High Temperature Rule

Create a rule from Developer Tools > Services:

```yaml
service: industrial_alarm_panel.create_rule
data:
  rule:
    id: inverter_high_temp
    entity_id: sensor.inverter_temperature
    name: Inverter High Temperature
    tag: INV-TEMP-HH
    area: Solar Inverter
    system: PV
    condition: above
    threshold: 75
    deadband: 2
    priority: critical
    requires_ack: true
    audible: true
    delay_on_seconds: 5
    delay_off_seconds: 10
    instructions: Check inverter ventilation, fans, ambient temperature, and loading.
```

### Voltage Range Rules

```yaml
service: industrial_alarm_panel.create_rule
data:
  rule:
    id: grid_phase_a_voltage_low
    entity_id: sensor.shellyem3_e8db84d68e3c_channel_a_voltage
    name: Grid Phase A Voltage Low
    tag: GRID-A-V-LOW
    area: Electrical
    system: Grid Meter
    condition: below
    threshold: 207
    deadband: 3
    priority: high
    instructions: Check Phase A supply voltage and upstream breaker or utility condition.
```

```yaml
service: industrial_alarm_panel.create_rule
data:
  rule:
    id: grid_phase_a_voltage_high
    entity_id: sensor.shellyem3_e8db84d68e3c_channel_a_voltage
    name: Grid Phase A Voltage High
    tag: GRID-A-V-HIGH
    area: Electrical
    system: Grid Meter
    condition: above
    threshold: 253
    deadband: 3
    priority: high
    instructions: Check Phase A supply voltage and utility condition.
```

### Binary Problem Rule

```yaml
service: industrial_alarm_panel.create_rule
data:
  rule:
    id: electric_heater_overheating
    entity_id: binary_sensor.shellyplus1pm_c4d8d55505a0_switch_0_overheating
    name: Electric Heater Overheating
    tag: EHEATER-OVERTEMP
    area: Electrical
    system: Electric Heater
    condition: is_on
    priority: critical
    instructions: Turn off heater circuit if safe and inspect the load before re-enabling.
```

### Starter Alarm Ideas

Good first rules usually monitor:

- inverter native fault words, for example SOFAR fault registers `> 0`
- grid voltage low/high, for example `< 207 V` and `> 253 V` on 230 V nominal systems
- grid frequency low/high, for example `< 49.5 Hz` and `> 50.5 Hz`
- inverter heatsink or cabinet temperature high
- PV insulation resistance low
- solar heater water temperature high
- built-in problem binary sensors such as overheating, overcurrent, overpower, or overvoltage
- Home Assistant host power problem sensors
- internet connectivity loss if cloud/mobile notification delivery matters

## Services

The integration registers:

- `industrial_alarm_panel.acknowledge_alarm`
- `industrial_alarm_panel.acknowledge_all`
- `industrial_alarm_panel.silence_horn`
- `industrial_alarm_panel.unsilence_horn`
- `industrial_alarm_panel.shelve_alarm`
- `industrial_alarm_panel.unshelve_alarm`
- `industrial_alarm_panel.disable_alarm`
- `industrial_alarm_panel.enable_alarm`
- `industrial_alarm_panel.create_rule`
- `industrial_alarm_panel.update_rule`
- `industrial_alarm_panel.delete_rule`
- `industrial_alarm_panel.test_sound`
- `industrial_alarm_panel.export_history`

Silence only stops horn output. Acknowledgement changes the alarm lifecycle state.
Shelving is temporary. In the panel, choose a **Shelve for** preset before clicking a row's **Shelve** button. In service calls, set `duration_minutes`; day-based shelves use minute values such as `1440` for 1 day and `10080` for 7 days.

## Sound

Browser sound is generated in the panel with Web Audio after the operator clicks **Enable Alarm Sound**. Media-player output uses Home Assistant `media_player.play_media` with files expected at:

```text
/config/www/industrial_alarm_panel/sounds/
```

Default filenames are `critical.mp3`, `high.mp3`, `medium.mp3`, `low.mp3`, and `info.mp3`.

## Storage

Rules are stored in Home Assistant storage with key `industrial_alarm_panel.rules`.
Runtime alarm states are stored with key `industrial_alarm_panel.state`.
History is stored in `/config/industrial_alarm_panel_history.db`.

## Troubleshooting

- If `/industrial-alarms` is blank after an update, restart Home Assistant and hard refresh the browser with `Ctrl+Shift+R`.
- If a newly created rule does not show as an entity yet, wait for the integration reload to finish or restart Home Assistant.
- If the horn does not play in the browser, click **Enable Alarm Sound** in the panel. Browsers block audio until a user gesture.
- If media-player sound does not play, confirm your MP3 files exist under `/config/www/industrial_alarm_panel/sounds/`.
- Check **Settings > System > Logs** for `industrial_alarm_panel` errors.

## Reporting Issues

Before opening an issue:

1. Update to the latest release.
2. Restart Home Assistant.
3. Reproduce the problem.
4. Check Home Assistant logs for `industrial_alarm_panel`.

Open a GitHub issue here:

```text
https://github.com/xtimmy86x/industrial-alarm-panel/issues/new/choose
```

Please include:

- Home Assistant version
- Industrial Alarm Panel version
- install method, usually HACS custom repository
- browser and device if the issue is panel-related
- exact rule YAML or service data if the issue is rule-related
- relevant log lines and screenshots

Security issues should not be reported in public issues. See [SECURITY.md](SECURITY.md).

## Contributing

Pull requests are welcome. Keep changes focused, include tests for behavioral changes, and run:

```bash
python3 -m unittest discover -s tests -v
node --check custom_components/industrial_alarm_panel/frontend/dist/industrial-alarm-panel.js
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for repository workflow and support expectations.

## Development

Runtime dependencies are provided by Home Assistant. The root `requirements.txt` documents that there are no extra runtime Python packages.

Run the pure core tests without Home Assistant installed:

```bash
python3 -m unittest discover -s tests -v
```

For full Home Assistant integration tests, install `requirements_test.txt` in a virtual environment and run pytest.

## Telegram notifications

Industrial Alarm Panel can send **outbound-only, plain-text** alarm lifecycle
notifications through one or more Home Assistant `notify` entities. The feature is
fully opt-in and has a default minimum priority of `high`.

1. Configure the [Telegram Bot integration](https://www.home-assistant.io/integrations/telegram_bot/)
   in Home Assistant first.
2. Verify that Home Assistant exposes a working `notify` entity for that Telegram
   configuration.
3. Open **Settings → Devices & services → Industrial Alarm Panel → Configure**.
4. Enable **Telegram notifications**.
5. Select one or more Telegram-backed `notify` entities.
6. Choose the minimum priority and the lifecycle event types to send.

The selector intentionally lists all entities in the `notify` domain because Home
Assistant does not expose a stable, universal way for an options selector to limit
these entities to Telegram providers. Choose only notify entities created for your
Telegram Bot configuration.

Each alarm rule can refine the global minimum-priority behavior with
`telegram_notification_policy`:

- `inherit` (default) uses the global Telegram minimum-priority and lifecycle-event settings.
- `always` bypasses **only** the global minimum-priority filter. Telegram must still be
  globally enabled, have at least one target, and enable the event type being delivered.
- `never` suppresses all Telegram notifications for that rule.

Existing and legacy-imported rules without the field automatically use `inherit`. For example:

```yaml
rule:
  id: inverter_temperature_high
  entity_id: sensor.inverter_temperature
  name: Inverter Temperature High
  condition: above
  threshold: 80
  priority: medium
  telegram_notification_policy: always
```

Industrial Alarm Panel does not store or manage Telegram bot tokens. Telegram
configuration remains owned by Home Assistant.

Telegram alarm messages and interactive action labels currently support English
and Italian and follow the language configured in Home Assistant. Other languages
fall back to English.

### Interactive Telegram actions

Interactive actions extend the existing V1 setup and are disabled by default. The
Telegram bot must use **Polling** or **Webhooks**; **Broadcast** bots are send-only and
continue to receive ordinary outbound notifications but cannot deliver callbacks.
In the integration options, enable interactive actions, select the Telegram Bot
`event` entity that reports callbacks, and choose whether to allow ACK, shelving,
and disable. The event selector shows all `event.*` entities, so select the entity
created by the Telegram Bot integration rather than relying on its name.

The equivalent internal option names are illustrated below (normal configuration is
through the UI):

```yaml
telegram_enabled: true
telegram_interactive_enabled: true
telegram_targets:
  - notify.telegram_operations
telegram_callback_event_entities:
  - event.telegram_bot_update
telegram_interactive_ack: true
telegram_interactive_shelve: true
telegram_interactive_disable: true
```

Activation messages use Home Assistant's native `telegram_bot.send_message` action.
Callbacks arrive through the selected event entities and execute the existing alarm
engine actions; no raw Telegram HTTP API, credentials, or user identity is handled.
If an interactive send definitely fails, the integration attempts one plain V1
notification without buttons. A successful send with incomplete response data is
not retried, preventing duplicate messages.

Interactive Telegram action sessions are currently stored in memory, bounded to
1,000 entries with a seven-day TTL. Buttons on messages created before a Home
Assistant restart may expire gracefully. This limitation is intentional in v1.1.0.

## Upgrade compatibility

Repository ownership changes do not alter the Home Assistant integration domain,
config entries, entity or unique IDs, services, stored alarm rules, runtime state,
SQLite history, Lovelace configuration, or Telegram configuration. Existing users
can upgrade normally through HACS; no migration or reinstallation is required.

## Origins and attribution

Industrial Alarm Panel was originally based on
[`AlRiachi/industrial-alarm-panel`](https://github.com/AlRiachi/industrial-alarm-panel).

The project is now independently maintained and has significantly diverged from
the original implementation. The original project and its contributors remain
credited through the Git history and the Apache-2.0 license.
