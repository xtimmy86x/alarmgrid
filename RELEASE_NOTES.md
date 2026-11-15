# AlarmGrid 2.3.0

This release adds entity-based alarm thresholds, Home Assistant operator attribution, more reliable Telegram delivery, and fully functional settings for history, sound, and panel presentation.

## Settings and panel

- Manage integration settings directly from the sidebar panel, with grouped sections, inline explanations, and validation.
- Administrators can save settings; other users have read-only access.
- The integration's **Configure** dialog uses the same settings and validation.
- Added configurable grouping by area, system, or priority, compact rows, initial tab, cleared-alarm visibility, and displayed alarm limits.
- Custom panel titles now appear in both the sidebar and panel header.
- Display limits do not reduce the number of alarms monitored.
- The global flashing setting now applies to both panel and cards.

## Dynamic thresholds and rule defaults

- Compare a source entity against another entity, such as an `input_number` setpoint, without creating a template sensor.
- Supported in simple rules and advanced AND/OR conditions.
- Changes to either the source or the setpoint trigger evaluation.
- Rule previews and CSV import/export support entity references.
- Invalid or unavailable setpoints preserve the previous alarm state instead of producing a false clear.
- Configured activation delays, clear delays, and deadband now initialize new rules. Existing rules and explicitly supplied values remain unchanged.
- The global acknowledgement-after-clear setting now controls future clear transitions, while preserving per-rule automatic acknowledgement.

## Telegram and operator history

- Home Assistant actions now record the authenticated user's name in history, exports, and Telegram messages.
- Actions without a user context are identified as system/automation actions.
- Shelving and disabling notifications are enabled by default; existing saved notification preferences are preserved.
- Added a persistent delivery queue with automatic retries for temporary failures and rate limits.
- Pending notifications survive integration reloads and Home Assistant restarts.
- Slow Telegram requests no longer block alarm processing.
- Improved message layout, Italian translations, condition descriptions, and handling of special characters.
- Added delivery diagnostics for pending, successful, retried, failed, expired, and cancelled notifications.

## Sound and silencing

- Alarm sounds now repeat at the configured interval, even when the source sensor does not update.
- Disabling repetition plays once per new audible activation.
- Browser playback respects the selected audio output and follows backend sound events.
- Silencing and its expiry are saved with alarm states and restored after settings reloads and Home Assistant restarts.
- Saving settings no longer restarts an already silenced alarm.
- Timed silencing expires automatically; new alarm activations can rearm sound.
- Sound tests are now one-shot and preserve the current alarm and silence state.
- Fixed sound remaining active after rule deletion or restarting immediately after automatic shelving.

## History

- History retention now runs in the background at startup and every hour.
- The configured history row limit now controls panel queries without limiting full exports.
- Optional source-change recording can capture value changes without an alarm lifecycle transition.
- Additional source-change recording is disabled by default; explicitly saved choices are preserved.
- Alarm lifecycle events and operator actions remain recorded independently of these optional settings.

## Lovelace card and frontend updates

- Redesigned the visual card editor.
- Added an optional neutral color scheme, configurable flashing styles, and custom text for the link to the panel.
- Card and panel resources now use a content-based version fingerprint, so even small frontend updates receive a new resource URL.
- Automatically managed Lovelace resources are updated in place.

## Other fixes

- Improved alarm reevaluation after startup, rule enabling, and shelving expiry.
- Fixed opening the Configure dialog with decimal settings that have no upper bound.
- Applied the configured flapping detection threshold and clarified that it counts activations within five minutes.
- Removed duplicate integration reloads when changing history retention through its number entity.
- Added regression coverage and configuration-flow checks against Home Assistant 2026.11.1.

## Updating

Update through HACS, restart Home Assistant, and refresh the browser or reopen the Companion App frontend.

**Review history retention before updating:** it now actively deletes events older than the configured period, including existing history. The default is 90 days. Export older events first if you need to retain them.

Existing rules and saved configuration remain compatible. Changing rule defaults does not overwrite existing rules.

If you manage Lovelace resources manually in YAML, update the resource's version/build query value yourself. Automatic resource fingerprint updates apply to storage-managed resources.

Previously saved Telegram event preferences are preserved. Enable shelving and disabling notifications in Settings if they were previously turned off.

**Full Changelog:** https://github.com/xtimmy86x/alarmgrid/compare/2.2.0...2.3.0
