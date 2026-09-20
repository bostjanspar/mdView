## Why

The raw/rendered code font is hardcoded to JetBrains Mono, with no way for a user to switch to a font they find more readable. Users should be able to pick the monospace font used for markdown/code content at runtime, and have that choice stick across restarts.

## What Changes

- Add a "code font" segmented toggle to the toolbar (next to the existing Raw/Rendered/Both view-mode toggle), offering JetBrains Mono, Cascadia Mono, and System monospace.
- Changing the toggle immediately re-renders the raw view, line numbers, and rendered code blocks in the chosen font. The toolbar/tree-pane UI font is unaffected.
- The chosen font is written to a new JSON prefs file under `%APPDATA%\mdview\prefs.json` and re-applied automatically the next time the app starts, before the window paints, with no flash of the previous font.
- A corrupt or missing prefs file falls back silently to the JetBrains Mono default rather than crashing startup.

## Capabilities

### New Capabilities
- `md-viewer/font-preference`: lets the user choose the code/raw-view monospace font at runtime via a toolbar toggle, and persists that choice across app restarts (the first user-facing state in this app that survives a restart, distinct from the existing in-memory-only session state).

### Modified Capabilities
(none — `app-shell`'s session state contract and its "not persisted across runs" guarantee are unchanged; font preference is a separate, deliberately-persisted piece of state)

## Impact

- Affected code: `mdview/assets/index.html`, `mdview/assets/app.css`, `mdview/assets/app.js`, `mdview/app.py`, `mdview/__main__.py`.
- New code: `mdview/prefs.py` (JSON prefs read/write, new `FontChoice` enum).
- No new dependencies, no new font files — all three font options already ship in `mdview/assets/fonts/` or are OS defaults.
