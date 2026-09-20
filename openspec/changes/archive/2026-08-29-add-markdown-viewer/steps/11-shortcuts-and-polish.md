# Step 11 — View-mode shortcuts and shell polish

**Previous:** [10](10-copy-reference-content.md) · **Next:** [12 — Packaging](12-packaging.md)

**Specs:** `../specs/md-viewer/copy-reference/spec.md` (Keyboard shortcuts, Copy is discoverable and
confirmed), `../specs/md-viewer/app-shell/spec.md` (Session state, Startup errors are surfaced)

## Goal

Every shortcut in the spec works, copies are visibly confirmed, and the remaining app-shell error and
empty states are real rather than placeholder.

## Scope

- `assets/app.js`: `Ctrl+1` / `Ctrl+2` / `Ctrl+3` switch to Raw / Rendered / Both, going through the same
  code path as the toggle, and update the toggle's active indicator.
- A brief non-blocking confirmation (toast) after each successful copy, naming which form was copied.
- Confirm and finish `SessionState` behaviour: the last-used view mode applies to newly opened files, and
  nothing persists across runs.
- Finish the app-shell error states: missing WebView2 runtime message, unreadable-file message,
  deleted-open-file message, empty-folder message — all in-window, none as an unhandled traceback.
- A first-run empty state in the content area telling the user to open a folder.

Out of scope: any new capability; this step closes gaps only.

## Task breakdown

- [ ] 11.1 Implement `app.js`: `Ctrl+1`/`Ctrl+2`/`Ctrl+3` handlers routed through the same code path as the toggle
- [ ] 11.2 Verify each shortcut leaves the UI identical to the equivalent toggle click, including the active indicator
- [ ] 11.3 Suppress shortcuts while focus is in a text input; verify
- [ ] 11.4 Implement the non-blocking copy confirmation (toast) naming which form was copied
- [ ] 11.5 Verify the toast appears for both copy actions and dismisses itself
- [ ] 11.6 Confirm/finish `SessionState`: last-used view mode applies to newly opened files
- [ ] 11.7 Confirm nothing persists across restarts (view mode resets to default)
- [ ] 11.8 Finish the WebView2-missing message (actionable, in-window)
- [ ] 11.9 Finish the unreadable-file message (in-window, no traceback)
- [ ] 11.10 Finish the deleted-open-file message
- [ ] 11.11 Finish the empty-folder message
- [ ] 11.12 Add the first-run empty state in the content area
- [ ] 11.13 Verify the Acceptance list below in full, including simulating the WebView2-missing path and documenting how it was simulated

## Notes

- Shortcuts must not fire while focus is in a text input.
- One code path per mode change — the toggle and the shortcut must not diverge.

## Verification

```bash
python -m mdview
```
Exercise each shortcut, then walk the error states deliberately (rename the file, delete it, open an
empty folder).

## Acceptance

- [ ] `Ctrl+1`, `Ctrl+2`, `Ctrl+3` switch to Raw, Rendered, and Both respectively.
- [ ] Each shortcut leaves the UI in exactly the state the equivalent toggle click produces, including the
      active indicator.
- [ ] Shortcuts do not fire while focus is in a text input.
- [ ] `Ctrl+C` and `Ctrl+Shift+C` still behave per steps 09 and 10, including the plain-copy fallback.
- [ ] A successful copy shows a brief confirmation that names which form was copied, and it disappears on
      its own without blocking interaction.
- [ ] Selecting Rendered mode and then opening a different file from the tree opens the new file in
      Rendered mode.
- [ ] Restarting the app reopens no folder or file and resets the view mode to its default.
- [ ] Launching without the WebView2 runtime shows an in-window message naming the runtime and how to
      install it (simulate the failure path if a clean machine is unavailable, and say how you simulated
      it).
- [ ] Opening a folder with no `.md` files shows the empty-state message.
- [ ] Deleting the open file shows the "file no longer available" message with the app still usable.
- [ ] Making the open file unreadable (lock or permission-deny it) shows a readable message, not a
      traceback.
- [ ] On first launch, before any folder is opened, the content area explains how to open a folder.
- [ ] No unhandled Python traceback and no JS console error occurs anywhere in the above walkthrough.
- [ ] `pyright mdview` reports zero errors.
- [ ] Steps 01–10 acceptance lists still pass.
