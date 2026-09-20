## Why

In Both view mode, the raw source pane is always fixed on the left and the rendered pane on the
right. Some users prefer rendered output on the left (closer to how a preview usually reads) or
want to flip the layout on demand for a given file. There is currently no way to swap the pane
order without editing code.

## What Changes

- Add a "flip panes" button, visible only when Both view mode is active, that swaps which side
  (left/right) shows the raw pane and which shows the rendered pane.
- Clicking it again flips back, so the control acts as a toggle, not a one-way action.
- The flipped/unflipped state is part of session state: it survives switching files and toggling
  away from and back to Both mode within the same run, but is not persisted across app restarts
  (consistent with how view mode itself resets on launch).
- No change to scroll-sync, line mapping, or the Raw/Rendered/Both mode toggle itself.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `md-viewer/markdown-rendering`: the "View modes" requirement gains pane-order behavior for Both
  mode — a flip control that swaps raw/rendered left-right placement and toggles back.

## Impact

- `mdview/assets/index.html`: add a flip button in the toolbar or content area, shown only in Both
  mode.
- `mdview/assets/app.js`: track flipped state, wire the button, apply/remove a CSS class on
  `#content-area` reflecting pane order.
- `mdview/assets/app.css`: add a `flipped` variant of the existing `.both-mode` flex layout that
  reorders `.raw-view` and `.rendered-view` visually (e.g. via `order`) without changing DOM order,
  so scroll-sync and line-mapping logic (which reference the panes by id, not position) are
  unaffected.

## Non-goals

- No change to which pane content is shown in Raw-only or Rendered-only modes.
- No persistence of flip state across application restarts.
- No independent flip-state per file; it is a single session-wide toggle like the view mode itself.
