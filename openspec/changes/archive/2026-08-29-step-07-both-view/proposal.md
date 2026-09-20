## Why

The view-mode toggle has advertised Raw/Rendered/Both since step 02, but Both has never been
wired up. This step makes the third mode work: raw and rendered side-by-side over the same file,
each independently scrollable, with no new rendering logic — just a layout for panes that already
exist.

## What Changes

- Extend `mdview/assets/app.css`/`app.js`: a split layout for `ViewMode.BOTH` — raw pane left,
  rendered pane right, each its own scroll container, with a divider that keeps neither pane at
  zero width and never forces the whole window to scroll horizontally.
- Reuse the existing raw renderer (step 02) and rendered renderer (step 03) as-is for Both mode;
  no third rendering path.
- Extend the view-mode toggle so it visibly indicates the active mode across all three states.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. `openspec/specs/md-viewer/markdown-rendering/spec.md`'s "View modes" requirement already
specifies Both mode; this step implements that already-written spec. `.openspec.yaml` sets
`skip_specs: true` accordingly.

## Impact

- Modifies `mdview/assets/index.html`, `app.css`, `app.js` only. No Python changes expected —
  `showView()`'s mode-based hide/show logic already runs on every reload and file switch, so Both
  mode inherits step 04's live-reload and step 06's file-switch behavior for free once wired.
- No spec text changes.

## Non-goals

- Scroll sync between the two panes — deferred to step 08.
- Keyboard shortcuts for switching modes — deferred to step 11.
