## Context

See proposal.md - Why. Step 04 already allocated a second `Debouncer` "even though unused" and
step 05 already classifies non-open-file `.md` events as `MarkdownTreeChanged` but the drain loop
currently does nothing with them (`pass  # tree refresh on create/delete is step 06`). This step
closes that gap: it's wiring, not new architecture.

## Goals / Non-Goals

**Goals:**
- `.md` create/delete/move anywhere under the root triggers exactly one debounced re-scan, on its
  own 200 ms window, independent of the content debouncer.
- A tree refresh never resets the content pane, its scroll position, the open-file selection, or
  collapse state for directories that still exist.
- Pruning is re-applied on every refresh: deleting the last `.md` under a directory removes that
  directory from the tree, cascading to now-empty ancestors.

**Non-Goals:**
- Detecting or special-casing renames as distinct from delete+create — `watchdog`'s move events
  are routed the same as create/delete (both mark the tree dirty); no diffing of old vs. new tree
  structure beyond what `scan_folder` + re-render already does.

## Decisions

- **`MarkdownTreeChanged` events schedule the *existing* `_tree_debouncer`, not a new one.**
  Step 04's `_tree_debouncer` was allocated for exactly this; using it now means step 06 adds zero
  new debouncing primitives, only a call to `self._tree_debouncer.schedule(self._refresh_tree)`
  where the drain loop currently has `pass`.
- **The tree debouncer's callback re-scans and enqueues a fresh `TreeReady`, reusing step 05's
  push path.** `_refresh_tree()` calls `scan_folder(root)` on a worker thread (same pattern as
  `_start_tree_scan`) and puts a `TreeReady` event back onto the watch queue; the existing
  `TreeReady` handler in the drain loop already pushes it to the webview and already discards
  stale results for a since-changed root. No new push mechanism needed.
- **Content and tree debouncers are fully independent instances with independent timers.**
  A `ContentChanged` event and a `MarkdownTreeChanged` event arriving together each schedule their
  own debouncer; neither `cancel()`s the other. This is what step 04's design already committed to
  by creating two separate `Debouncer` instances rather than one shared one.
- **`assets/tree.js`'s refresh path reuses `render()`, not a diffing algorithm.** Since expansion
  state and selection are tracked client-side in `expandedPaths`/`selectedPath` (step 05) rather
  than derived from the DOM, a full rebuild from the new `TreeNode` naturally preserves both —
  `render()` already takes an `expanded` list and `open_file` from the payload rather than reading
  prior DOM state, so no new preservation logic is needed, only calling it again on refresh.
- **Watchdog's recursive observer is verified, not re-implemented, for new subdirectories.**
  `watchdog.observers.Observer.schedule(..., recursive=True)` is documented to pick up newly
  created subdirectories automatically; this step's job is to confirm that experimentally (task
  6.5) rather than add manual re-scheduling logic on directory-create events.

## Risks / Trade-offs

- [Risk] A tree refresh mid-scroll-position-capture (step 04's Raw/Rendered position logic) could
  race if both debouncers fire in the same tick → Mitigation: the two refreshes touch disjoint DOM
  (content pane vs. tree pane) and disjoint JS state (`currentFileContent` vs. `lastTree`), so no
  shared mutable state needs locking.
- [Risk] A burst of many rapid creates could still produce more than one refresh if events span
  more than one 200 ms window → Mitigation: this matches the spec's stated debounce window: only
  events within the *same* window coalesce, matching the acceptance item's "ten files in a burst"
  (fired fast enough to land in one window) rather than an unbounded time span.
