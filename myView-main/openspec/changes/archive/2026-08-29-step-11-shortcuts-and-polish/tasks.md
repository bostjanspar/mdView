## 1. View-mode shortcuts

- [x] 1.1 Extract the toggle's mode-switch body into a shared `switchToMode(mode)` function in
      `assets/app.js`
- [x] 1.2 Implement `Ctrl+1`/`Ctrl+2`/`Ctrl+3` handlers calling `switchToMode`
- [x] 1.3 Verify each shortcut leaves the UI identical to the equivalent toggle click, including
      the active indicator
- [x] 1.4 Suppress shortcuts while focus is in a text input (`isTextInputFocused()` check); verify

## 2. Copy confirmation toast

- [x] 2.1 Add a toast element to `index.html` and styling to `app.css`
- [x] 2.2 Implement the non-blocking copy confirmation in `assets/copy.js`, naming which form was
      copied, shown after both the shortcut and the context-menu code paths
- [x] 2.3 Verify the toast appears for both copy actions and dismisses itself without blocking
      interaction

## 3. Session-state confirmation

- [x] 3.1 Confirm the last-used view mode already applies to a newly opened file (no code change
      expected; verify by inspection and by running the app)
- [x] 3.2 Confirm nothing persists across restarts (view mode resets to default; verify by running
      the app twice)

## 4. Unreadable-file and reload-error handling

- [x] 4.1 Extend `FileContentPayload` with an `error: str | None` field
- [x] 4.2 Catch `OSError` in `App.load_file`; return an error payload instead of propagating
- [x] 4.3 Catch `OSError` in `App._reload_open_file`; push an error payload instead of raising in
      the drain-loop thread
- [x] 4.4 Update `assets/app.js`'s `applyLoadedFile`/`onFileReloaded` to show `fileContent.error`
      in the content pane instead of rendering when it is set
- [x] 4.5 Verify by simulating an unreadable file (document the simulation method used) that a
      readable message appears with no traceback

## 5. Empty and first-run states

- [x] 5.1 Add a distinct first-run content-pane message ("open a folder to get started"), shown
      until a folder is opened
- [x] 5.2 Set the content pane's message to "No file open." once a folder is chosen, distinct
      from the first-run message
- [x] 5.3 Add a distinct tree-pane message ("no markdown files found") shown once a folder has
      been scanned and has no markdown, distinct from the first-run "no folder open" message
- [x] 5.4 Verify all three tree/content empty-state variants (first-run, no-file-open,
      no-markdown-found) appear in their correct situations

## 6. Final verification

- [x] 6.1 Run `pyright mdview` and confirm zero errors
- [x] 6.2 Hand off to the user to run `python -m mdview` and walk every acceptance item: all three
      shortcuts, shortcut suppression, both copy confirmations, view-mode carry-over across a file
      switch, a restart resetting state, the WebView2-missing path (document how simulated), an
      empty folder, a deleted open file, an unreadable file (document how simulated), the
      first-run state, and confirm no unhandled Python traceback or JS console error occurs
      anywhere, and that steps 01-10's acceptance lists still pass
