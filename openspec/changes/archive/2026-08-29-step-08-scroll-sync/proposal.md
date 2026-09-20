## Why

Both mode (step 07) gives raw and rendered panes side by side, but scrolling one leaves the other
in place, forcing the user to manually re-align them. This step synchronizes the two panes so they
always show the corresponding part of the document, using the `data-line` mapping step 03 already
stamps onto every rendered block.

## What Changes

- Add `mdview/assets/sync.js`:
  - Rendered → raw: find the topmost visible element carrying `data-line`, read its start line,
    scroll the raw pane so that line is at/near the top.
  - Raw → rendered: compute the raw pane's topmost visible line number, find the rendered element
    whose `data-line` range contains it (else the nearest preceding one), and scroll it into view.
  - A module-level `syncing` guard, set before a programmatic scroll and cleared on the next
    animation frame, so the scroll event the programmatic scroll itself fires is not mistaken for
    user input and bounced back (design D6, no feedback loop).
  - Listeners attached only while Both mode is active, detached on mode change, and re-attached
    (with a re-alignment) on re-entry.
  - Re-bound after a live reload so sync works against the file's current `data-line` values.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. `openspec/specs/md-viewer/scroll-sync/spec.md` already specifies bidirectional sync,
nearest-block accuracy, no feedback loop, Both-mode scoping, and reload survival; this step
implements that already-written spec. `.openspec.yaml` sets `skip_specs: true` accordingly.

## Impact

- New file: `mdview/assets/sync.js`.
- Modifies `mdview/assets/index.html` (script include) and possibly `app.js` (hooking sync
  attach/detach into the existing mode-switch and reload code paths already built in steps 04 and
  07).
- No spec text changes; no Python changes.

## Non-goals

- Pixel-perfect or line-perfect alignment — nearest-block accuracy is the spec's own bar.
- Any sync behavior in Raw or Rendered mode — sync is Both-mode-only by design.
