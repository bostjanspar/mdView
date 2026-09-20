# Step 04 — Live reload of the open file

**Previous:** [03](03-markdown-rendering.md) · **Next:** [05 — Folder tree](05-folder-tree.md)

**Specs:** `../specs/md-viewer/live-reload/spec.md` (open file reload, reading position, debouncing,
watcher lifecycle)

## Goal

Editing the open file in another program updates the view within a second, without losing the reading
position, and without double-refreshing on two-step editor saves.

## Scope

- `mdview/watching.py`:
  - `Debouncer(delay_ms: int)` with a typed `schedule(...)` — one shared implementation, 200 ms default.
  - Module-level `_MarkdownEventHandler(watchdog.events.FileSystemEventHandler)` whose handlers are
    methods, classifying events and pushing a typed event dataclass onto a `queue.Queue`.
  - `FolderWatcher` with `start(root: Path) -> None` and `stop() -> None`, owning one recursive observer.
- `mdview/app.py`: main-thread drain of the event queue; on an "open file modified" event, re-read via
  `read_text_lossy`, re-render if needed, and push the new content to the webview through
  `evaluate_js`. Only the main thread may call `evaluate_js` (design D4).
- `assets/app.js`: content replacement that captures the topmost visible `data-line` (Rendered) or
  gutter line number (Raw) before the swap and restores it after, clamping to the last existing line
  when the file got shorter.
- Handle deletion of the open file: show a "file no longer available" message, keep running.

Out of scope: tree refresh on create/delete (step 06).

## Task breakdown

- [ ] 4.1 Implement `watching.py`: `Debouncer(delay_ms)` with typed `schedule(...)`, 200 ms default
- [ ] 4.2 Implement `watching.py`: typed event dataclass(es) for queue items (e.g. content-changed, file-deleted)
- [ ] 4.3 Implement `watching.py`: module-level `_MarkdownEventHandler(FileSystemEventHandler)` with methods classifying events and pushing onto a `queue.Queue`
- [ ] 4.4 Implement `watching.py`: `FolderWatcher.start(root)` / `stop()` owning one recursive observer
- [ ] 4.5 Verify events arrive for an external save
- [ ] 4.6 Implement `app.py`: main-thread queue drain loop
- [ ] 4.7 Implement `app.py`: on "open file modified" event, re-read via `read_text_lossy` and re-render if needed
- [ ] 4.8 Implement `app.py`: push new content to the webview via `evaluate_js` from the main thread only
- [ ] 4.9 Verify an external save updates the view within 1 second in both Raw and Rendered mode
- [ ] 4.10 Implement `assets/app.js`: capture the topmost visible `data-line` (Rendered) or gutter line number (Raw) before a content swap
- [ ] 4.11 Implement `assets/app.js`: restore the captured position after the swap, clamping to the last existing line when the file got shorter
- [ ] 4.12 Verify appending a line keeps the viewport; verify truncating scrolls to the nearest existing position
- [ ] 4.13 Handle deletion of the open file: show "file no longer available" message, keep app running
- [ ] 4.14 Create the second debouncer (tree, 200 ms) now even though unused this step, per design D4
- [ ] 4.15 Verify debouncing with a temporary two-writes-in-100ms script and a temporary refresh counter — exactly 1 refresh; two saves a second apart give 2; delete script and counter afterward
- [ ] 4.16 Verify the Acceptance list below in full

## Notes

- Two separate debouncers (content vs tree) are specified in design D4; create both now even though
  only the content one is wired up, so step 06 has nothing structural to add.
- Do not poll. If watchdog reports nothing on the target folder, fix the observer, don't add a timer.

## Verification

```bash
python -m mdview        # open a scratch folder, open a file, then edit it from another editor
```

## Acceptance

- [ ] Saving the open file from an external editor updates the content area within 1 second, with no
      click or keypress in the app.
- [ ] The update works in Raw mode and in Rendered mode; in Rendered mode the new `data-line` values
      match the new source.
- [ ] Scrolled to the middle of a long file, appending a line at the end leaves the viewport showing the
      same region.
- [ ] Truncating the file so the visible region no longer exists scrolls to the nearest existing
      position instead of erroring or jumping to the top.
- [ ] Writing the open file twice within 100 ms (simulate with a two-write script, then delete the
      script) produces exactly one visible refresh — instrument with a temporary counter log to confirm
      the count is 1.
- [ ] Two saves one second apart produce two refreshes.
- [ ] Deleting the open file shows a "file no longer available" message and the app keeps running.
- [ ] Opening a second folder stops all updates from the first folder.
- [ ] Closing the window terminates every watcher thread; the process exits and does not linger in Task
      Manager.
- [ ] `evaluate_js` is never called from a watchdog thread (grep the call sites and confirm they are on
      the queue-drain path).
- [ ] Watchdog event handlers are methods on a module-level class, not nested functions.
- [ ] `pyright mdview` reports zero errors.
- [ ] Steps 01–03 acceptance lists still pass.
