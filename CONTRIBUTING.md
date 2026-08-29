# Contributing

Thanks for helping improve AlarmGrid.

This is the official contribution guide for
[`xtimmy86x/alarmgrid`](https://github.com/xtimmy86x/alarmgrid).

## Before You Open A PR

1. Search the [existing issues](https://github.com/xtimmy86x/alarmgrid/issues)
   and [pull requests](https://github.com/xtimmy86x/alarmgrid/pulls).
2. Keep the change focused on one bug, feature, or documentation improvement.
3. Add or update tests when behavior changes.
4. Update `README.md` or `INSTALLATION.md` when the user-facing workflow changes.

## Local Checks

Run the lightweight checks before opening a pull request:

```bash
python3 -m unittest discover -s tests -v
node --check custom_components/alarmgrid/frontend/dist/alarmgrid.js
```

If you have a Home Assistant development environment available, also run the integration in a real Home Assistant instance and verify setup, services, and the `/alarmgrid` panel.

## Pull Request Expectations

- Explain what changed and why.
- Include screenshots for panel or visual changes.
- Include the Home Assistant version used for manual validation.
- Do not include unrelated formatting or generated-file churn.

## Support Scope

GitHub issues are for reproducible bugs, feature requests, and documentation gaps. Installation questions should include the exact HACS/install step that failed and relevant Home Assistant log lines.
