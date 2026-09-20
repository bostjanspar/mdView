## Context

See proposal.md - Why. Design D4 (whole-project design) specifies a single recursive `watchdog`
observer per session root, feeding two logical buckets — "open file modified" and "markdown file
created/deleted anywhere" — each with its own 200 ms `Debouncer`. This step wires only the first
bucket end-to-end; the second is created but unused until step 06.

## Goals / Non-Goals

**Goals:**
- One recursive observer per open root; watchdog callbacks never call `evaluate_js` directly.
- Exactly one reload per debounce window, regardless of how many filesystem events arrive in it.
- Reading position (topmost `data-line` in Rendered, topmost gutter line in Raw) survives a reload.

**Non-Goals:**
- Tree create/delete handling — step 06 wires the second debouncer's bucket into an actual tree
  update; this step only allocates the debouncer so nothing structural is missing later.
- Any UI for watcher status/errors beyond the "file no longer available" message.

## Decisions

- **Watchdog handler methods live on a module-level `_MarkdownEventHandler`, not closures.** The
  project rule against nested function/method definitions applies to event handlers too; a
  module-level class keeps them named, testable in isolation, and out of `FolderWatcher.start()`.
- **Classified events flow through one `queue.Queue`, drained on the main thread.** pywebview's
  `evaluate_js` must run on the same thread as the window; watchdog's observer runs its callbacks
  on a separate thread. A typed dataclass per event (e.g. `ContentChanged(path)`,
  `FileDeleted(path)`) posted to the queue and drained by a pywebview-scheduled callback (or a
  short polling drain tied to `webview.start(..., http_server=False)`'s event loop) keeps all
  webview calls single-threaded. Alternative considered: calling `evaluate_js` directly from the
  watchdog thread — rejected, pywebview's GTK/EdgeChromium backends are not thread-safe for this.
- **One shared `Debouncer` implementation, parameterized by delay, not two bespoke ones.** Content
  and tree buckets have identical coalescing semantics (200 ms window, keep only the latest
  trigger); one class with two instances avoids duplicated timer logic.
- **Position capture/restore is JS-side, not Python-side.** The topmost visible `data-line`/gutter
  line is a property of the DOM's current scroll state, which Python has no direct view into;
  capturing it in `app.js` right before the swap and restoring it right after is the only place
  that has both the old and new DOM available in a single spot.
- **Deleted-file handling reuses the existing content area, not a separate error page.** A
  "file no longer available" message rendered into the same content area the file used to occupy
  keeps the rest of the shell (toolbar, tree) functional, matching the live-reload spec's
  "keeps running" requirement.

## Risks / Trade-offs

- [Risk] Two events for the same logical save (e.g. a temp-file-then-rename pattern some editors
  use) could each reset the debounce timer indefinitely if they keep arriving → Mitigation: the
  debounce window is fixed at 200 ms from the *last* event, per design D4; this is standard
  debounce behavior and matches the spec's 100 ms two-step-save scenario with margin.
- [Risk] `FolderWatcher.stop()` not being called before a new one starts (e.g. opening a second
  folder) would leak an observer thread → Mitigation: `App.open_folder()` must stop the previous
  watcher before starting a new one; verified by the acceptance item "closing the window
  terminates every watcher thread."
