# Step 02 — App shell, open folder, raw view

**Previous:** [01](01-project-scaffold.md) · **Next:** [03 — Markdown rendering](03-markdown-rendering.md)

**Specs:** `../specs/md-viewer/app-shell/spec.md`,
`../specs/md-viewer/markdown-rendering/spec.md` (Raw view, File reading is robust)

## Goal

A real window that opens a folder via the native picker and displays one chosen `.md` file as raw text
with line numbers. No tree yet — the file is chosen by a temporary flat dropdown of markdown files
found directly under the root.

## Scope

- `mdview/session.py`: `ViewMode` (`StrEnum`: `RAW`, `RENDERED`, `BOTH`) and
  `SessionState(root, open_file, view_mode, expanded)` with typed mutators.
- `mdview/files.py`: `FileContent(path, text, lines, had_decode_errors)` and
  `read_text_lossy(path: Path) -> FileContent` (UTF-8, `errors="replace"`).
- `mdview/app.py`: `App` class exposed as pywebview's `js_api` — `open_folder()`, `list_markdown()`,
  `load_file(path: str)`, `set_view_mode(mode: str)`. Each returns a payload built by an explicit
  `to_payload()`, never `dataclasses.asdict`.
- `mdview/assets/index.html`, `app.css`, `app.js`: two-pane layout (content left, empty tree pane
  right), a Raw/Rendered/Both toggle (only Raw functional this step), and the raw renderer with a
  1-based line-number gutter in a monospace font.
- Startup check for the WebView2 runtime with an actionable in-window message when absent.
- `__main__.py` wires `App` into `webview.create_window(...)` and `webview.start()`.

Out of scope: markdown-to-HTML, the tree, watching, shortcuts.

## Task breakdown

- [x] 2.1 Implement `session.py`: `ViewMode` `StrEnum` (`RAW`, `RENDERED`, `BOTH`)
- [x] 2.2 Implement `session.py`: `SessionState` dataclass (`root`, `open_file`, `view_mode`, `expanded`) with typed mutators
- [x] 2.3 Implement `files.py`: `FileContent` dataclass (`path`, `text`, `lines`, `had_decode_errors`)
- [x] 2.4 Implement `files.py`: `read_text_lossy(path) -> FileContent` using UTF-8 `errors="replace"`; verify a lossy read of invalid UTF-8 returns replacement chars instead of raising
- [x] 2.5 Implement `app.py`: `App` class skeleton exposed as `js_api`, with a `to_payload()` per dataclass
- [x] 2.6 Implement `App.open_folder()`: native folder picker, updates `SessionState.root`, returns payload
- [x] 2.7 Implement `App.list_markdown()`: flat listing of markdown files directly under root (temporary dropdown data source)
- [x] 2.8 Implement `App.load_file(path)`: reads file via `read_text_lossy`, updates `SessionState.open_file`, returns payload
- [x] 2.9 Implement `App.set_view_mode(mode)`: updates `SessionState.view_mode`, returns payload
- [x] 2.10 Verify each `App` method's return value from the JS console
- [x] 2.11 Build `assets/index.html`: two-pane layout (content left, empty tree pane right) and Raw/Rendered/Both toggle markup
- [x] 2.12 Build `assets/app.css`: layout styling for the two panes and toggle
- [x] 2.13 Build `assets/app.js`: temporary flat dropdown wired to `list_markdown`/`load_file`; Open Folder button wired to `open_folder`
- [x] 2.14 Build `assets/app.js`: raw renderer with 1-based line-number gutter in monospace font; verify a 40-line file shows gutter 1–40 matching the file
- [x] 2.15 Add WebView2-missing detection with an actionable in-window message
- [x] 2.16 Wire `__main__.py`: `webview.create_window(...)` with `App` as `js_api`, `webview.start()`; verify the window opens and closes cleanly with exit 0
- [x] 2.17 Verify the Acceptance list below in full

## Notes

- Raw view must be read-only and byte-faithful — no wrapping that renumbers lines, no tab expansion,
  no trailing-whitespace trimming.
- Design D1: the bridge is pywebview `js_api` + `evaluate_js` only. Do not start an HTTP server.

## Verification

```bash
python -m mdview
```
Then: Open Folder… → pick a folder containing `.md` files → choose a file from the dropdown.

## Acceptance

- [x] The app opens a single window with a left content area, a right (empty) tree pane, and a visible
      Raw / Rendered / Both toggle.
- [x] "Open Folder…" opens the native Windows folder picker.
- [x] Cancelling the picker leaves the root, the open file, and the view unchanged.
- [x] Picking a folder that contains no `.md` file anywhere shows an explicit empty-state message, not
      a blank pane and not an error dialog.
- [x] Opening a known 40-line file shows gutter numbers 1–40, and line N on screen matches line N of
      the file byte-for-byte (spot-check lines 1, 20, 40).
- [x] Typing into the raw pane changes nothing on screen and leaves the file's modification time
      unchanged.
- [x] A file containing invalid UTF-8 bytes still displays, with a replacement character where the bad
      bytes were, and the app does not crash.
- [x] Selecting a second file replaces the first in the content area.
- [x] Closing the window exits the process within 2 seconds with status 0 and no lingering threads.
- [x] Restarting the app reopens nothing — no folder, no file — and the view mode is back to its default.
- [x] `pyright mdview` reports zero errors.
- [x] Every value crossing a function boundary with more than one field is a `@dataclass`; no bare
      tuples or mixed-key dicts are returned.
- [x] Step 01's acceptance list still passes.
