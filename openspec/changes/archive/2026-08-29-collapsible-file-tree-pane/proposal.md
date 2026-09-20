## Why

The file-tree pane's row text renders at the browser's default font size, noticeably larger than
the raw/rendered content, and long filenames get visually pushed off the row's left edge instead
of staying flush with the toggle/name group. There is also no way to hide the pane, so on a narrow
window or when a folder has deeply nested names, the tree pane permanently eats width the user may
want back for reading content.

## What Changes

- Reduce the font size of file-tree row labels (directories and files) so they sit closer to the
  UI chrome scale (toolbar labels, ~13px) instead of the browser default.
- Ensure tree rows are consistently left-aligned: the toggle arrow and name stay flush to the
  pane's left edge at every nesting depth, with only indentation (not centering or wrapping)
  separating levels.
- Add a toolbar toggle button that shows or hides the entire file-tree pane. When hidden, the
  content area expands to fill the freed width. The toggle state is part of in-session state (not
  persisted across app restarts, consistent with existing session-state behavior).

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `md-viewer/file-tree`: tree-pane row font size and left-alignment, and a new
  show/hide affordance for the whole pane.
- `md-viewer/app-shell`: toolbar gains a tree-pane visibility toggle; session state tracks
  whether the tree pane is currently shown or hidden.

## Impact

- `mdview/assets/app.css`: `.tree-row`, `.tree-toggle`, `#tree-pane` styles (font-size, alignment,
  hidden/collapsed width state); `#content-area` width recalculation when the pane is hidden.
- `mdview/assets/index.html`: new toggle button in `#toolbar`.
- `mdview/assets/tree.js` and/or `mdview/assets/app.js`: wire the toggle button to show/hide
  `#tree-pane` and update its pressed/state indicator.

## Non-goals

- Persisting the pane's shown/hidden state across application restarts.
- Resizing the pane by dragging (width stays fixed; only visibility changes).
- Changing tree behavior (sorting, collapse/expand per directory, file selection).
