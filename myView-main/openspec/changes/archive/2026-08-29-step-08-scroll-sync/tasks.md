## 1. Rendered to raw sync

- [x] 1.1 Implement `assets/sync.js`: find the topmost visible `data-line` element in the rendered
      pane
- [x] 1.2 Implement rendered->raw: scroll the raw pane so that line is at/near the top; verify
      aligning the block at line 120 puts line 120 near the raw pane's top

## 2. Raw to rendered sync

- [x] 2.1 Implement `assets/sync.js`: compute the raw pane's topmost visible line number
- [x] 2.2 Implement raw->rendered: find the rendered element whose `data-line` range contains it,
      else the nearest preceding one, scroll it into view; verify a top line inside a 50-line
      fence shows that block aligned to its start

## 3. Feedback-loop guard

- [x] 3.1 Implement the module-level `syncing` guard, set before a programmatic scroll
- [x] 3.2 Clear the `syncing` guard on the next animation frame so the induced scroll event is
      ignored
- [x] 3.3 Verify one gesture settles both panes with no oscillation and fast scrolling never makes
      panes fight

## 4. Lifecycle wiring

- [x] 4.1 Attach sync listeners only on Both-mode entry (wire into `app.js`'s mode-switch handler)
- [x] 4.2 Detach sync listeners on Both-mode exit; verify sync is inert in Raw and Rendered mode
- [x] 4.3 Re-bind listeners and re-align on Both-mode re-entry
- [x] 4.4 Re-bind after a live reload so sync works against new `data-line` values; verify after
      an external edit and a file switch

## 5. Final verification

- [x] 5.1 Run `pyright mdview` and confirm zero errors (no Python changes expected, but confirm
      nothing regressed)
- [x] 5.2 Hand off to the user to run `python -m mdview` against a 300+ line file with a 50-line
      fenced block in Both mode, exercising both scroll directions, mode re-entry, reload, and
      file switch, confirming every item in the step's Acceptance list passes (including no
      console errors at either scroll extreme) and that steps 01-07's acceptance lists still pass
