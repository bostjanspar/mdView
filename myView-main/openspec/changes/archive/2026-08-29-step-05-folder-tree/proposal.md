## Why

File selection has been a temporary flat dropdown since step 02, which does not scale and does not
match the app-shell's advertised right-hand tree pane. This step replaces it with the real,
markdown-only, collapsible folder tree the file-tree spec requires, keeping the window responsive
even on large folders.

## What Changes

- Add `mdview/tree.py`: `TreeNode(name, path, is_dir, children)` and
  `scan_folder(root: Path) -> TreeNode` — recursive, prunes directories with no `.md` at any depth,
  sorts directories before files (case-insensitive) within each group, and tracks visited real
  paths to break symlink cycles.
- Run the scan on a worker thread and deliver the finished `TreeNode` through the step-04 event
  queue, so opening a large folder never blocks the window.
- Extend `mdview/session.py`'s `expanded: set[Path]` to be populated with the ancestors of the
  open file, keyed by path so it survives a re-scan.
- Add `mdview/assets/tree.js`: renders `TreeNode`, per-directory expand/collapse, open-file
  highlight, and directory-click-toggles-without-changing-open-file behavior.
- Remove the step-02 temporary flat dropdown from `index.html` and `app.js`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. `openspec/specs/md-viewer/file-tree/spec.md` already specifies the markdown-only tree,
ordering, collapse/expand, file selection, and bounded/non-blocking scan; this step implements
that already-written spec. `.openspec.yaml` sets `skip_specs: true` accordingly.

## Impact

- New files: `mdview/tree.py`, `mdview/assets/tree.js`.
- Modifies `mdview/session.py` (expanded-set population), `mdview/app.py` (worker-thread scan,
  queue delivery), `mdview/assets/index.html`/`app.js` (dropdown removal, tree pane wiring).
- No spec text changes.

## Non-goals

- Reacting to filesystem create/delete events to keep the tree live — deferred to step 06.
- Any change to Raw/Rendered/Both view-mode behavior.
