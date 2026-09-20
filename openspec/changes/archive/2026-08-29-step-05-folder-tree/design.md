## Context

See proposal.md - Why. Step 04 already built a `queue.Queue[WatchEvent]`-based drain loop and a
worker-thread-safe pattern for pushing updates to the webview (`Debouncer` + `evaluate_js` on the
drain thread, never the watchdog thread). This step reuses that same queue for a different kind of
background result: a folder scan.

## Goals / Non-Goals

**Goals:**
- `scan_folder` prunes markdown-empty branches, orders directories-before-files
  case-insensitively, and terminates on symlink cycles.
- Opening a large folder never blocks the window; the tree appears once the scan completes.
- Expand state is keyed by `Path` and survives a re-scan; the path to the open file starts
  expanded.

**Non-Goals:**
- Reacting to filesystem create/delete anywhere under the root to refresh the tree live — step 06.
- Any change to how a file's content is loaded once selected (reuses `App.load_file`).

## Decisions

- **`scan_folder` runs on a `threading.Thread`, result delivered via a new `TreeReady` event on
  the existing `watching.WatchEvent` queue.** Step 04's drain loop already exists and already
  distinguishes event types with `isinstance`; adding `TreeReady(tree: TreeNode)` to the union is
  less new machinery than a second queue or a callback-based API, and keeps "the window never
  blocks" and "one place drains background results" as a single mechanism.
- **Pruning is bottom-up.** `scan_folder` recurses into subdirectories first, builds each
  directory's `children` list from only the entries that themselves survive pruning (a `.md` file
  always survives; a directory survives only if `is_markdown_anywhere_below(children)` is true),
  then applies directories-before-files, case-insensitive-name ordering to what's left. This
  directly implements "no markdown anywhere below" rather than "no markdown directly inside."
- **Symlink cycle protection via a visited-real-paths set, passed down the recursion.**
  `Path.resolve()` on directory entries, checked against a `set[Path]` threaded through the
  recursive calls; a directory whose resolved path is already visited is treated as empty rather
  than recursed into. Alternative considered: `os.walk` with `followlinks=False` — rejected,
  since it skips walking into symlinked directories entirely rather than allowing controlled
  one-level traversal with cycle detection.
- **`SessionState.expanded` stores `Path`, not tree position.** A path-keyed set is unaffected by
  re-scans producing structurally different `TreeNode` trees (e.g. after step 06 adds a file),
  which is exactly the "survives a refresh" requirement.
- **The step-02 dropdown is deleted outright, not hidden.** Nothing in later steps depends on
  `list_markdown`/the dropdown markup; keeping dead code around after its replacement exists would
  violate the project's no-half-finished-implementations convention.

## Risks / Trade-offs

- [Risk] A worker-thread scan racing with the user opening a second folder before the first scan
  finishes could deliver a stale `TreeReady` for the wrong root → Mitigation: `TreeReady` carries
  the root it was scanned for; the drain handler discards it if it doesn't match the current
  session root.
- [Risk] Very deep directory structures could hit Python's recursion limit → Mitigation: not
  addressed this step (no spec requirement for arbitrary depth); acceptable given the step's
  explicit large-*file-count* (not large-*depth*) performance scenario.
