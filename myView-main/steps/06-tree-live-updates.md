# Step 06 — Live tree updates on create and delete

**Previous:** [05](05-folder-tree.md) · **Next:** [07 — Both view](07-both-view.md)

**Specs:** `../specs/md-viewer/live-reload/spec.md` (tree reflects created and deleted files),
`../specs/md-viewer/file-tree/spec.md` (collapse state survives a refresh)

## Goal

Creating or deleting `.md` files anywhere under the root updates the tree automatically, on its own
debounce, without disturbing collapse state or the open file.

## Scope

- `mdview/watching.py`: route create/delete/move events for `.md` paths into the second debouncer from
  step 04 (200 ms), emitting a "tree dirty" event.
- `mdview/app.py`: on "tree dirty", re-run `scan_folder` on the worker thread and push the new
  `TreeNode` to the webview. Content reload and tree refresh must remain independent — one must never
  suppress or cancel the other.
- `assets/tree.js`: re-render from the new `TreeNode` while restoring expansion state from
  `SessionState.expanded` and keeping the selection highlight on the open file.
- Directory create/delete: newly created subdirectories must be covered by the existing recursive
  observer; confirm rather than assume.

Out of scope: arbitrary directory restructuring beyond create/delete (explicit non-goal for v1).

## Task breakdown

- [x] 6.1 Route `.md` create events into the second debouncer, emitting a "tree dirty" event
- [x] 6.2 Route `.md` delete events into the second debouncer, emitting "tree dirty"
- [x] 6.3 Route `.md` move events into the second debouncer, emitting "tree dirty"
- [x] 6.4 Verify a `.txt` creation produces no event
- [x] 6.5 Confirm newly created subdirectories are covered by the existing recursive observer (do not assume)
- [x] 6.6 On "tree dirty", re-run `scan_folder` on the worker thread in `app.py`
- [x] 6.7 Push the new `TreeNode` to the webview, keeping content reload and tree refresh independent (neither suppresses the other)
- [x] 6.8 Implement `assets/tree.js` re-render from the new `TreeNode` restoring expansion state from `SessionState.expanded`
- [x] 6.9 Keep the selection highlight on the open file across a tree refresh
- [x] 6.10 Verify new file appears, brand-new nested directory path appears, deletion removes node and cascades pruning of markdown-free parents
- [x] 6.11 Verify a simultaneous edit + create produces both a content refresh and a tree refresh
- [x] 6.12 Verify a burst of ten creations produces one tree refresh (temporary counter, then remove it)
- [x] 6.13 Verify the Acceptance list below in full

## Notes

- Pruning applies to refreshes too: deleting the last `.md` under a directory must make that directory
  disappear, cascading upward.
- The tree refresh must not reset the content pane or the scroll position.

## Verification

```bash
python -m mdview        # open the step-05 scratch folder, then create/delete files from Explorer
```

## Acceptance

- [x] Creating `root/alpha/new.md` makes it appear in the tree within ~1 second, with no reopen.
- [x] Creating `root/brand-new/deep/x.md` (a directory tree that did not exist when the folder was
      opened) makes the whole path appear.
- [x] Deleting a `.md` file removes its node.
- [x] Deleting the last `.md` under `alpha/` removes `alpha/` as well, cascading to any parent that is
      now markdown-free.
- [x] Creating `root/notes.txt` produces no visible tree change.
- [x] `alpha/` expanded before a refresh is still expanded after it.
- [x] The open file stays open and its scroll position is unchanged across a tree refresh.
- [x] Editing the open file and creating a new file at nearly the same moment produces both a content
      refresh and a tree refresh — neither cancels the other.
- [x] Creating ten files in a burst produces a single tree refresh (temporary counter log confirms the
      count, then remove the log).
- [x] Closing the window still terminates every watcher thread.
- [x] `pyright mdview` reports zero errors.
- [x] Steps 01–05 acceptance lists still pass.
