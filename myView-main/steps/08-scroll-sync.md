# Step 08 — Scroll sync in Both view

**Previous:** [07](07-both-view.md) · **Next:** [09 — Copy reference](09-copy-reference.md)

**Specs:** `../specs/md-viewer/scroll-sync/spec.md`

## Goal

In Both mode, scrolling either pane moves the other to the same place in the document — nearest-block
accurate, no jitter, no feedback loop.

## Scope

- `assets/sync.js`:
  - Rendered → raw: find the topmost visible element carrying `data-line`, read its start line, scroll
    the raw pane so that line is at/near the top.
  - Raw → rendered: compute the raw pane's topmost visible line number, find the rendered element whose
    `data-line` range contains it, else the nearest preceding one, and scroll it into view.
  - A module-level `syncing` guard set before a programmatic scroll and cleared on the next animation
    frame, so the induced scroll event is ignored (design D6).
  - Listeners attached only in Both mode and detached on mode change; re-attached and re-aligned on
    re-entry.
  - Re-bind after a live reload so sync works against the new `data-line` values.

Out of scope: pixel-perfect or line-perfect alignment; sync in Raw or Rendered mode.

## Task breakdown

- [x] 8.1 Implement `sync.js`: find the topmost visible `data-line` element in the rendered pane
- [x] 8.2 Implement `sync.js` rendered→raw: scroll the raw pane so that line is at/near the top; verify aligning the block at line 120 puts line 120 near the raw pane's top
- [x] 8.3 Implement `sync.js`: compute the raw pane's topmost visible line number
- [x] 8.4 Implement `sync.js` raw→rendered: find the rendered element whose `data-line` range contains it, else the nearest preceding one, scroll it into view; verify a top line inside a 50-line fence shows that block aligned to its start
- [x] 8.5 Implement the module-level `syncing` guard, set before a programmatic scroll
- [x] 8.6 Clear the `syncing` guard on the next animation frame so the induced scroll event is ignored
- [x] 8.7 Verify one gesture settles both panes with no oscillation and fast scrolling never makes panes fight
- [x] 8.8 Attach sync listeners only on Both-mode entry
- [x] 8.9 Detach sync listeners on Both-mode exit; verify sync is inert in Raw and Rendered mode
- [x] 8.10 Re-bind listeners and re-align on Both-mode re-entry
- [x] 8.11 Re-bind after a live reload so sync works against new `data-line` values; verify after an external edit and a file switch
- [x] 8.12 Verify the Acceptance list below in full, including no console errors at either scroll extreme

## Notes

- Throttle to animation frames rather than debouncing — sync must feel immediate.
- A selection inside a long code block aligns to the block start; that is correct, not a bug.

## Verification

```bash
python -m mdview   # open a 300+ line file with mixed blocks including a 50-line fenced block, Both mode
```

## Acceptance

- [x] Scrolling the rendered pane so the block starting at source line 120 is at the top scrolls the raw
      pane so line 120 is at or near the top (within one block).
- [x] Scrolling the raw pane so line 120 is at the top scrolls the rendered pane to the block containing
      or most closely preceding line 120.
- [x] With the raw pane's top line in the middle of a 50-line fenced block, the rendered pane shows that
      code block aligned to its start.
- [x] One scroll gesture settles both panes at one final position each — no oscillation, no continuous
      drift, no visible jitter.
- [x] Fast repeated scrolling in one pane never causes the panes to fight each other.
- [x] Scrolling in Raw mode and in Rendered mode has no sync side effects.
- [x] Leaving Both mode and returning re-aligns the panes and sync still works.
- [x] Editing the file externally in Both mode and then scrolling either pane syncs correctly against
      the updated line numbers.
- [x] Sync still works after switching to a different file from the tree while in Both mode.
- [x] Scrolling to the very top and the very bottom of either pane does not throw a console error.
- [x] No console errors appear during any of the above.
- [x] Steps 01–07 acceptance lists still pass.
