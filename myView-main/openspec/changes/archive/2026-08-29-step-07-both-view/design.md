## Context

See proposal.md - Why. `#raw-view` and `#rendered-view` already exist as sibling elements inside
`#content-area` (steps 02-03); `showView()` already toggles their `hidden` attribute based on
`currentMode`. Both mode only needs both visible at once, side by side, instead of exactly one.

## Goals / Non-Goals

**Goals:**
- Both mode shows both existing panes simultaneously, each independently scrollable.
- No new rendering code — `renderRaw()` and `renderRendered()` (steps 02-03) are called exactly as
  they already are; Both mode differs only in which elements are visible and how they're laid out.
- Step 08 can attach scroll listeners to `#raw-view` and `#rendered-view` directly, unchanged.

**Non-Goals:**
- Any scroll synchronization between the panes (step 08).
- A user-draggable/resizable divider — a fixed 50/50 (or CSS-`resize`-based) split satisfies the
  spec; nothing requires persisted or drag-adjustable widths.

## Decisions

- **`showView()` gains a `both` branch that un-hides *both* panes, not a new function.** Both mode
  is a variant of the existing show/hide logic, not a separate rendering path — this is what the
  step's "no third rendering path" instruction is checking for.
- **Layout via CSS `display: flex` on `#content-area` when in Both mode, not a JS-managed split.**
  A `both-mode` class toggled on `#content-area` switches its `display` and gives each pane
  `flex: 1; min-width: 0; overflow: auto`, so panes can never collapse to zero width and the
  window never gains a horizontal scrollbar (each pane scrolls internally). A JS-computed pixel
  split was considered and rejected — pure CSS is simpler and resize-safe by construction.
- **The divider is a static 1px border between panes, not a draggable splitter.** Nothing in the
  spec or acceptance list requires a user-resizable split; adding drag-resize now would be scope
  beyond what step 07 asks for and would need to be revisited once scroll sync (step 08) exists
  anyway.

## Risks / Trade-offs

- [Risk] A fixed 50/50 split could look cramped on narrow windows → Mitigation: acceptance only
  requires neither pane collapses to zero width and no horizontal scrollbar appears; `min-width: 0`
  with internal `overflow: auto` on each pane satisfies that regardless of window width.
