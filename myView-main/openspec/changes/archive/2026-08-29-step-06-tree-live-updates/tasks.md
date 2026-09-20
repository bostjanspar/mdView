## 1. Event routing

- [x] 1.1 Route `.md` create events into the tree debouncer (`mdview/app.py`'s drain loop,
      `MarkdownTreeChanged` branch)
- [x] 1.2 Route `.md` delete events into the tree debouncer
- [x] 1.3 Route `.md` move events into the tree debouncer (watchdog reports these as classified
      create/delete pairs via `_MarkdownEventHandler`; confirm both sides land as
      `MarkdownTreeChanged`)
- [x] 1.4 Verify a `.txt` creation produces no queued event
- [x] 1.5 Confirm newly created subdirectories are covered by the existing recursive observer with
      a throwaway script (create a nested dir + file, verify a `MarkdownTreeChanged` arrives),
      then delete the script

## 2. Debounced re-scan and push

- [x] 2.1 Implement `_refresh_tree()` in `mdview/app.py`: re-run `scan_folder` on a worker thread
      when the tree debouncer fires
- [x] 2.2 Push the resulting `TreeReady` through the existing watch-event queue and push path,
      confirming content reload and tree refresh remain independent (neither cancels the other)

## 3. Tree re-render behavior

- [x] 3.1 Verify `assets/tree.js`'s existing `render()` correctly restores expansion state and
      keeps the open-file selection highlight when called again with a refreshed `TreeNode`
- [x] 3.2 Verify a tree refresh does not reset the content pane or its scroll position

## 4. End-to-end verification

- [x] 4.1 Verify a new file appears in the tree, a brand-new nested directory path appears, and a
      deletion removes its node and cascades pruning of now markdown-free parents
- [x] 4.2 Verify a simultaneous content edit and file creation produce both a content refresh and
      a tree refresh
- [x] 4.3 Verify a burst of ten creations produces one tree refresh, using a temporary counter,
      then remove the counter
- [x] 4.4 Run `pyright mdview` and confirm zero errors
- [x] 4.5 Hand off to the user to run `python -m mdview`, create/delete/move `.md` files under an
      open folder, and confirm every item in the step's Acceptance list passes, including that
      steps 01-05's acceptance lists still pass
