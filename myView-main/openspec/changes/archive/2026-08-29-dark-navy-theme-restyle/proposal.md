## Why

The app currently uses a plain light theme (white background, gray borders, plain buttons) that
looks unfinished next to modern Windows apps. The user wants a cohesive dark navy blue look, a
rounded "Open Folder…" button, and a more stylish way to pick the view mode.

## What Changes

- Restyle the whole window (toolbar, content area, tree pane, context menu, toast) with a dark
  navy blue color palette instead of the current white/gray theme.
- Round the corners of the "Open Folder…" button.
- Replace the three separate `Raw` / `Rendered` / `Both` `<button>` elements in the view-mode
  toggle with a horizontal set of styled radio buttons (segmented-control look: pill-shaped group,
  highlighted selected option), keeping the same three choices and the same underlying selection
  behavior (including Ctrl+1/2/3 shortcuts and per-session persistence).
- No new capability and no requirement change: this is a visual/markup restyle of the existing
  app-shell UI. The view-mode toggle still offers exactly Raw, Rendered, and Both, and still
  behaves as one mutually-exclusive selection — only its color palette and widget markup change.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. The `md-viewer/app-shell` requirements ("a view-mode toggle offering Raw, Rendered, and
Both") do not mandate a specific widget type or color scheme, so no requirement text changes.

## Impact

- `mdview/assets/app.css`: new dark navy color variables/palette applied across toolbar, content
  area, tree pane, context menu, toast; rounded style for the open-folder button; new styles for
  the radio-button segmented control.
- `mdview/assets/index.html`: view-mode toggle markup changes from three `<button>` elements to a
  `<fieldset>`/`radio input` group (or equivalent radio-based markup) with visible labels.
- `mdview/assets/app.js`: view-mode selection logic updated to read/write the radio inputs instead
  of toggling a `.active` class on buttons; keyboard shortcuts and mode-persistence logic keep the
  same behavior.
- No Python backend changes, no new dependencies, no changes to file-tree, copy-reference,
  scroll-sync, live-reload, markdown-rendering, or packaging capabilities.

## Non-goals

- No new features, view modes, or keyboard shortcuts.
- No light-theme/dark-theme toggle — this replaces the current look with a single dark navy theme.
- No changes to markdown rendering, syntax highlighting, or layout structure (pane sizes, tree
  behavior) beyond color/shape restyling.
