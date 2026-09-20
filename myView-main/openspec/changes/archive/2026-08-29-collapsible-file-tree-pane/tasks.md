## 1. Tree pane styling

- [x] 1.1 Reduce `.tree-row` label font-size in `mdview/assets/app.css` to match toolbar scale
      (~13px) and verify by opening a folder with nested `.md` files and visually comparing row
      text size to the view-mode toggle labels
- [x] 1.2 Fix left alignment of `.tree-toggle`/name groups at every depth in `app.css` (no
      centering, no overflow pushing content off the left edge) and verify with a folder containing
      long filenames and 3+ nesting levels that every row's toggle+name starts flush at its
      indentation level

## 2. Pane visibility toggle

- [x] 2.1 Add a toggle button/control to `#toolbar` in `mdview/assets/index.html` and verify it
      renders alongside "Open Folder…" and the view-mode toggle
- [x] 2.2 Implement show/hide behavior for `#tree-pane` (JS in `tree.js` or `app.js`) that hides the
      pane and lets `#content-area` occupy the freed width, and verify by toggling with a folder
      open and confirming the content area visibly widens
- [x] 2.3 Track pane-visible state in existing session state and verify toggling twice restores the
      pane with the same directory expand/collapse state and open-file selection as before
- [x] 2.4 Verify hiding the pane while a file is open leaves the open file's content unaffected

## 3. Verification pass

- [ ] 3.1 Run the app (`uv run mdview` or equivalent), open a real nested folder, and manually
      confirm: smaller left-aligned tree labels, working show/hide toggle, and no regression to
      file selection or view-mode switching
