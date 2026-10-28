# AlarmGrid 2.1.1

This patch release fixes the **Suspend alarm** and **Disable alarm** dialogs in the AlarmGrid Lovelace card.

## Fixed

- Confirmation dialogs no longer disappear when the alarm list refreshes or a WebSocket update arrives.
- The selected suspension duration and any operator comment remain in place while the alarm list refreshes.
- Modal listeners remain attached exactly once, avoiding duplicated actions after repeated refreshes.
- Refresh the frontend asset cache key so Home Assistant loads the corrected JavaScript.

## Compatibility

- Existing AlarmGrid configuration, alarm rules and persisted alarm state do not require migration.
- No changes to the alarm engine or the underlying services.

## Validation

- Python test suite, JavaScript syntax checks and HACS validation.

**Full Changelog:** https://github.com/xtimmy86x/alarmgrid/compare/2.1.0...2.1.1
