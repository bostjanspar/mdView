## Context

See proposal.md - Why. Design D6 (whole-project design) already specifies the feedback-loop fix:
a module-level `syncing` flag, set before a programmatic scroll and cleared on the next animation
frame. Step 03 already stamps `data-line="start-end"` on every rendered block; step 07 already
keeps `#raw-view` and `#rendered-view` as two independent scroll containers. This step only adds
the sync logic itself.

## Goals / Non-Goals

**Goals:**
- Scrolling either pane in Both mode moves the other to the corresponding block, within one block
  of accuracy.
- No oscillation: a programmatic scroll never re-triggers the opposite sync direction.
- Sync attaches only in Both mode, detaches on mode exit, and re-attaches (re-aligned) on re-entry.
- Sync keeps working after a live reload or a file switch, without a manual mode toggle.

**Non-Goals:**
- Pixel- or line-exact alignment.
- Any sync behavior while Raw or Rendered mode is active alone.

## Decisions

- **Rendered → raw uses the topmost visible `data-line` element's start line directly.** Every
  block-level element already carries `data-line="start-end"` (step 03); finding the first element
  whose bounding position is at/past the rendered pane's scroll top and reading its `start` is a
  direct application of that mapping — no separate line-mapping table needed.
- **Raw → rendered walks `data-line` ranges to find the containing (or nearest-preceding) block.**
  The raw pane's topmost visible line number is computed the same way step 04's position-capture
  logic already does (`topmostRawLine()`); reusing that function (not duplicating it) means both
  scroll-position-preservation and scroll-sync agree on what "topmost visible line" means.
- **The `syncing` guard is a plain module-level boolean in `sync.js`, cleared via
  `requestAnimationFrame`, not a timeout.** A fixed-delay timeout could fire before or after the
  browser's own scroll-event dispatch for the programmatic scroll, either not suppressing it or
  suppressing a later legitimate user scroll; `requestAnimationFrame` ties the guard's lifetime to
  the actual render/layout cycle the programmatic scroll causes.
- **Sync listeners are attached/detached from the same places `app.js` already toggles mode and
  handles reload** (`showView()`'s both-mode branch, `onFileReloaded`, `applyLoadedFile`) rather
  than `sync.js` polling for mode changes on its own. This keeps "sync is scoped to Both mode" and
  "sync survives a reload" as call sites into `sync.js`'s public `attach()`/`detach()`/`realign()`
  functions, not new state `sync.js` has to independently track and get out of sync with `app.js`.
- **`sync.js` exposes `attach(rawView, renderedView)`, `detach()`, and `realign()` — no internal
  polling, no MutationObserver.** Scroll listeners are the only event source; re-binding happens
  explicitly at the known call sites (mode switch, reload, file switch), which is simpler and
  cheaper than watching the DOM for changes.

## Risks / Trade-offs

- [Risk] Extremely fast scrolling could fire many scroll events before the animation-frame guard
  clears, each re-triggering a sync computation → Mitigation: each sync computation is O(number of
  `data-line` elements currently in the DOM), which is small enough per frame that this is a
  performance non-issue, and the guard still prevents any single programmatic scroll from causing
  a bounce-back regardless of frequency.
- [Risk] Detaching/reattaching listeners on every mode switch could leak old listeners if `detach()`
  is missed on one code path → Mitigation: `attach()` unconditionally calls `detach()` first, so a
  missed explicit detach is self-correcting on the next attach.
