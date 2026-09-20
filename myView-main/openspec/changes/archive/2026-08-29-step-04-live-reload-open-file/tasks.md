## 1. Watching primitives

- [x] 1.1 Implement `mdview/watching.py`: `Debouncer(delay_ms)` with typed `schedule(...)`, 200 ms
      default
- [x] 1.2 Implement `mdview/watching.py`: typed event dataclass(es) for queue items (e.g.
      content-changed, file-deleted)
- [x] 1.3 Implement `mdview/watching.py`: module-level `_MarkdownEventHandler` (subclass of
      `watchdog.events.FileSystemEventHandler`) whose methods classify events and push onto a
      `queue.Queue`
- [x] 1.4 Implement `mdview/watching.py`: `FolderWatcher.start(root)` / `stop()` owning one
      recursive observer
- [x] 1.5 Verify with a throwaway script that events arrive for an external save, then delete the
      script

## 2. Main-thread queue drain

- [x] 2.1 Implement `mdview/app.py`: main-thread queue drain loop
- [x] 2.2 Implement `mdview/app.py`: on an "open file modified" event, re-read via
      `read_text_lossy` and re-render if needed
- [x] 2.3 Implement `mdview/app.py`: push new content to the webview via `evaluate_js`, called
      only from the main thread
- [x] 2.4 Verify an external save updates the view within 1 second in both Raw and Rendered mode

## 3. Reading-position preservation

- [x] 3.1 Implement `assets/app.js`: capture the topmost visible `data-line` (Rendered) or gutter
      line number (Raw) before a content swap
- [x] 3.2 Implement `assets/app.js`: restore the captured position after the swap, clamping to the
      last existing line when the file got shorter
- [x] 3.3 Verify appending a line keeps the viewport; verify truncating scrolls to the nearest
      existing position

## 4. Deleted-file handling and the second debouncer

- [x] 4.1 Handle deletion of the open file: show "file no longer available" message, keep the app
      running
- [x] 4.2 Create the second debouncer (tree, 200 ms) now even though unused this step, per design
      D4

## 5. Debounce verification and final checks

- [x] 5.1 Verify debouncing with a temporary two-writes-in-100ms script and a temporary refresh
      counter: exactly 1 refresh; two saves a second apart give 2; delete the script and counter
      afterward
- [x] 5.2 Run `pyright mdview` and confirm zero errors; grep call sites to confirm `evaluate_js`
      is only ever called on the queue-drain path
- [x] 5.3 Hand off to the user to run `python -m mdview`, edit the open file externally, delete
      it, open a second folder, and close the window, confirming every item in the step's
      Acceptance list passes, including that steps 01-03's acceptance lists still pass
