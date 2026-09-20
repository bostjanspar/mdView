# Step 05 — Folder tree and file selection

**Previous:** [04](04-live-reload-open-file.md) · **Next:** [06 — Live tree updates](06-tree-live-updates.md)

**Specs:** `../specs/md-viewer/file-tree/spec.md`

## Goal

The right pane is a real tree: markdown-only, empty branches pruned, deterministic order, per-directory
collapse, click-to-open. The temporary dropdown from step 02 is removed.

## Scope

- `mdview/tree.py`:
  - `TreeNode(name: str, path: Path, is_dir: bool, children: list["TreeNode"])`
  - `scan_folder(root: Path) -> TreeNode` — recursive, prunes directories with no `.md` at any depth,
    sorts directories before files with case-insensitive names within each group, and tracks visited
    real paths to break symlink cycles.
  - Scan runs on a worker thread and delivers the finished `TreeNode` through the step-04 event queue,
    so the window stays responsive.
- `mdview/session.py`: `expanded: set[Path]` populated with the ancestors of the open file; collapse
  state keyed by path so it survives a re-scan.
- `assets/tree.js`: renders `TreeNode`, per-directory expand/collapse toggles, selection highlight on
  the open file, click on a directory toggles it without changing the open file.
- Remove the step-02 dropdown.

Out of scope: reacting to filesystem create/delete (step 06).

## Task breakdown

- [x] 5.1 Implement `tree.py`: `TreeNode(name, path, is_dir, children)` dataclass
- [x] 5.2 Implement `tree.py`: `scan_folder(root) -> TreeNode` with empty-branch pruning (no `.md` at any depth)
- [x] 5.3 Implement `tree.py`: dirs-before-files case-insensitive ordering within `scan_folder`
- [x] 5.4 Implement `tree.py`: symlink-cycle protection via visited real paths
- [x] 5.5 Build the step-05 scratch folder shape and verify `scan_folder` output against it
- [x] 5.6 Run the scan on a worker thread, deliver the finished `TreeNode` through the step-04 event queue
- [x] 5.7 Verify the window stays responsive while scanning a folder with several thousand files
- [x] 5.8 Implement `assets/tree.js`: render `TreeNode` into the tree pane
- [x] 5.9 Implement `assets/tree.js`: per-directory expand/collapse toggle
- [x] 5.10 Implement `assets/tree.js`: open-file highlight
- [x] 5.11 Implement `assets/tree.js`: directory click toggles expand state without changing the open file
- [x] 5.12 Verify each `tree.js` interaction individually
- [x] 5.13 Populate `SessionState.expanded` with the open file's ancestors on load
- [x] 5.14 Key collapse state by `Path` so it survives a re-scan; verify expansion survives a re-scan
- [x] 5.15 Remove the step-02 dropdown from `index.html`/`app.js`
- [x] 5.16 Verify the Acceptance list below in full; delete the scratch folder

## Notes

- The pruning rule is "no `.md` anywhere below", not "no `.md` directly inside" — an intermediate
  directory whose only markdown is three levels down must still appear.
- Expansion state is keyed by `Path`, not by tree position, so step 06's refresh can restore it.

## Verification

Build a scratch folder shaped like:
```
root/ a.md  b.txt  A.md
  alpha/ note.md
  Zebra/ deep/ deeper/ x.md
  assets/ img.png  sub/ img2.png
```
then `python -m mdview` and open `root/`.

## Acceptance

- [x] `b.txt` and `img.png` do not appear anywhere in the tree.
- [x] `assets/` does not appear at all (no markdown at any depth below it).
- [x] `Zebra/`, `deep/`, and `deeper/` all appear, because `x.md` is below them.
- [x] Order at the root level is `alpha/`, `Zebra/`, `A.md`, `a.md` — directories first, then files, each
      group case-insensitively sorted.
- [x] With no file open, every directory node is collapsed.
- [x] Opening `Zebra/deep/deeper/x.md` leaves `Zebra`, `deep`, and `deeper` expanded and marks `x.md` as
      the open file.
- [x] Expanding `alpha/` and then re-scanning (reopen the same folder) leaves `alpha/` expanded.
- [x] Clicking a `.md` node loads it into the content area in the current view mode and marks it selected.
- [x] Clicking a directory node only toggles that directory; the open file does not change.
- [x] A symlink pointing at one of its own ancestors does not cause infinite recursion — the scan
      finishes.
- [x] Opening a folder with several thousand files keeps the window responsive (the window can be moved
      and the toggle clicked while scanning) and the tree appears when the scan finishes.
- [x] The step-02 file dropdown is gone from the UI and the code.
- [x] `scan_folder` returns a `TreeNode`, not a nested `list[dict]`.
- [x] `pyright mdview` reports zero errors.
- [x] The scratch folder is not committed.
- [x] Steps 01–04 acceptance lists still pass.
