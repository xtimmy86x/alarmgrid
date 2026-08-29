# AlarmGrid 2.1.0

AlarmGrid 2.1.0 introduces a native Home Assistant visual editor for the
AlarmGrid Lovelace card.

## What's new

### Visual card editor

`custom:alarmgrid-card` can now be configured directly from the Home Assistant
dashboard editor without manually writing YAML.

The visual editor includes configuration for:

- alarm view
- maximum displayed alarms
- light/dark/automatic theme
- card header and icon
- header status and actions
- summary metrics
- alarm metadata
- ACK, shelve, disable and restore actions
- priority filtering
- advanced size and appearance settings

Changes are reflected in the card preview while editing.

### Stable editing experience

The visual editor now preserves its UI state during Home Assistant updates.

This fixes cases where:

- dropdowns closed immediately;
- the advanced appearance section collapsed;
- text fields lost focus;
- the cursor position jumped while typing.

The editor now updates configuration without unnecessarily rebuilding its
complete DOM.

## Compatibility

YAML configuration remains fully supported.

Existing AlarmGrid card configurations continue to work, including compatibility
handling for older card option aliases.

## Card type

```yaml
type: custom:alarmgrid-card
```

## Upgrade

Update AlarmGrid through HACS and refresh the browser after Home Assistant has
restarted.

**Full Changelog:** https://github.com/xtimmy86x/alarmgrid/compare/2.0.0...2.1.0
