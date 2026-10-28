# AlarmGrid 2.2.0

This release brings the latest panel and card redesigns, more reliable rule
editing, Telegram operator attribution, and optional per-rule button entities.

## Panel and Lovelace card

- Refreshed panel navigation, rule editor, alarm details, and history interface.
- Redesigned the Lovelace card with clearer lifecycle badges, alarm-state colors,
  compact metadata, and summary indicators.
- Fixed entity dropdowns closing during background polling and alarm updates in
  the rule editor, including nested AND/OR condition groups.
- Restored focus to the entity field when editing a rule.
- Updated the frontend cache key so Home Assistant loads the new JavaScript.

## Telegram operator history

- History and CSV exports now show the person who performed a Telegram action,
  for example `Mario Rossi (Telegram)`.
- Applies to acknowledgement, shelving, unshelving, disabling, and enabling.
- Uses the sender of the final action button in shared chats. Falls back to the
  Telegram user ID when the name is missing, or `telegram` when neither is supplied.
- Existing history entries keep their previously recorded operator.

## Optional rule buttons

- Added **Create buttons for each rule** / **Crea pulsanti per ogni regola** in
  **Settings > Devices & services > AlarmGrid > Configure**.
- Enabled by default. Turning it off removes the acknowledge, shelve, and disable
  button entities for each rule; turning it back on recreates them.
- Per-rule binary sensors, global buttons, and panel/card/Telegram/service actions
  remain available. New and imported rules respect the option.
- Panel entity-count estimates now reflect whether rule buttons are enabled.
- Entity-registry customizations on removed buttons are not retained when recreated.

## Updating

Update AlarmGrid through HACS and restart Home Assistant. Reload the browser or
Home Assistant app if it still displays the previous interface.

Existing AlarmGrid configuration, stored rules, alarm state, and history require
no migration. Per-rule buttons remain enabled unless explicitly turned off.

## Validation

- Python suite: 164 tests, with 6 Home Assistant-dependent tests skipped in the
  lightweight environment.
- Frontend runtime regressions: 17 passing tests.
- JavaScript syntax and GitHub CI checks.
- Live Home Assistant validation was not performed in the release environment.

**Full Changelog:** https://github.com/xtimmy86x/alarmgrid/compare/2.1.1...2.2.0
