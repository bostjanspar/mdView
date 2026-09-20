## Why

The app currently only shows a file's content as of the moment it was opened. A user editing the
same file in another program (Kate, VS Code, etc.) has no way to see their changes without closing
and reopening the file. This step adds automatic, debounced reload of the open file with reading
position preserved, and a graceful message if the file is deleted while open.

## What Changes

- Add `mdview/watching.py`: `Debouncer(delay_ms)`, a typed watch-event dataclass, a module-level
  `_MarkdownEventHandler(watchdog.events.FileSystemEventHandler)` whose handlers are methods that
  classify events and push onto a `queue.Queue`, and `FolderWatcher` (`start(root)` / `stop()`)
  owning one recursive `watchdog` observer.
- Add a second, currently-unused tree debouncer (design D4) so step 06 has no structural work left.
- Extend `mdview/app.py` with a main-thread drain loop for the event queue: on an "open file
  modified" event, re-read via `read_text_lossy`, re-render if needed, and push the new content to
  the webview via `evaluate_js` — called only from the main thread, never from a watchdog thread.
- Extend `assets/app.js`: before a content swap, capture the topmost visible `data-line` (Rendered)
  or gutter line number (Raw); after the swap, restore that position, clamped to the last existing
  line if the file got shorter.
- Handle deletion of the open file with a "file no longer available" message; the app keeps
  running.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. `openspec/specs/md-viewer/live-reload/spec.md` already specifies open-file reload,
debouncing, and watcher lifecycle; this step implements the "open file" subset of it (tree
create/delete watching is step 06). `.openspec.yaml` sets `skip_specs: true` accordingly.

## Impact

- New file: `mdview/watching.py`.
- Modifies `mdview/app.py` (queue drain, re-read/re-render/push) and `mdview/assets/app.js`
  (position capture/restore, deleted-file message).
- No spec text changes.

## Non-goals

- Tree refresh on file create/delete anywhere under the root — deferred to step 06.
- Scroll sync between Raw and Rendered panes in Both mode — deferred to step 08.
