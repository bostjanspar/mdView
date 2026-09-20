## 1. Tree scanning

- [x] 1.1 Implement `mdview/tree.py`: `TreeNode(name, path, is_dir, children)` dataclass
- [x] 1.2 Implement `mdview/tree.py`: `scan_folder(root) -> TreeNode` with empty-branch pruning
      (no `.md` at any depth)
- [x] 1.3 Implement `mdview/tree.py`: dirs-before-files case-insensitive ordering within
      `scan_folder`
- [x] 1.4 Implement `mdview/tree.py`: symlink-cycle protection via visited real paths
- [x] 1.5 Build a scratch folder (outside git) shaped like the step's example and verify
      `scan_folder`'s output against it, then delete the scratch folder

## 2. Non-blocking scan delivery

- [x] 2.1 Add a `TreeReady(root, tree)` event to `mdview/watching.py`'s `WatchEvent` union
- [x] 2.2 Run `scan_folder` on a worker thread from `App.open_folder()`, pushing `TreeReady` onto
      the existing watch-event queue when done
- [x] 2.3 Handle `TreeReady` in the drain loop: push the tree to the webview via `evaluate_js`,
      discarding it if the root no longer matches the current session root
- [x] 2.4 Verify the window stays responsive while scanning a folder with several thousand files

## 3. Tree rendering and interaction

- [x] 3.1 Implement `assets/tree.js`: render `TreeNode` into the tree pane
- [x] 3.2 Implement `assets/tree.js`: per-directory expand/collapse toggle
- [x] 3.3 Implement `assets/tree.js`: open-file highlight
- [x] 3.4 Implement `assets/tree.js`: directory click toggles expand state without changing the
      open file
- [x] 3.5 Verify each `tree.js` interaction individually

## 4. Expand-state persistence

- [x] 4.1 Populate `SessionState.expanded` with the open file's ancestors on load
- [x] 4.2 Key collapse state by `Path` so it survives a re-scan; verify expansion survives a
      re-scan

## 5. Remove the temporary dropdown

- [x] 5.1 Remove the step-02 dropdown from `index.html` and `app.js`

## 6. Final verification

- [x] 6.1 Run `pyright mdview` and confirm zero errors
- [x] 6.2 Hand off to the user to run `python -m mdview` against a real folder, exercise tree
      ordering/pruning/collapse/expand/selection, a symlink cycle, and a large folder, confirming
      every item in the step's Acceptance list passes, including that steps 01-04's acceptance
      lists still pass
