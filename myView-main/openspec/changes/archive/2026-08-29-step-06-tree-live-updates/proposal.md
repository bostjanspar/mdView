## Why

The tree built in step 05 only reflects the folder's shape at the moment it was opened. Creating
or deleting markdown files elsewhere in the project — the normal case when a user is editing docs
alongside the viewer — currently requires reopening the folder. This step makes the tree
self-updating, using the second debouncer step 04 already allocated for exactly this purpose.

## What Changes

- Extend `mdview/watching.py`: route `.md` create/delete/move events (previously classified as
  `MarkdownTreeChanged` but unused) through the tree `Debouncer` (200 ms), coalescing into a
  single "tree dirty" trigger.
- Extend `mdview/app.py`'s drain loop: on a debounced tree-dirty trigger, re-run `scan_folder` on
  a worker thread and push the new `TreeNode` to the webview — independently of content reload, so
  neither suppresses the other.
- Extend `mdview/assets/tree.js`: re-render from a refreshed `TreeNode` while restoring expansion
  state and keeping the open-file selection highlight, without disturbing the content pane or its
  scroll position.
- Confirm (not assume) that newly created subdirectories are covered by the existing recursive
  `watchdog` observer from step 04.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. `openspec/specs/md-viewer/live-reload/spec.md` ("Tree reflects created and deleted files")
and `openspec/specs/md-viewer/file-tree/spec.md` ("Collapse and expand" — survives a refresh)
already specify this behavior; this step implements it. `.openspec.yaml` sets `skip_specs: true`
accordingly.

## Impact

- Modifies `mdview/watching.py` (event routing into the tree debouncer),
  `mdview/app.py` (tree-dirty handling, re-scan, push), `mdview/assets/tree.js` (refresh-preserving
  re-render).
- No new files; no spec text changes.

## Non-goals

- Arbitrary directory restructuring beyond create/delete/move (explicit non-goal for v1, per the
  step file).
- Any change to content reload behavior — it must keep working exactly as step 04 left it,
  independently of tree refreshes.
