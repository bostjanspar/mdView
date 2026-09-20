## 1. Session state

- [x] 1.1 Implement `mdview/session.py`: `ViewMode` `StrEnum` (`RAW`, `RENDERED`, `BOTH`)
- [x] 1.2 Implement `mdview/session.py`: `SessionState` dataclass (`root`, `open_file`,
      `view_mode`, `expanded`) with typed mutators

## 2. File reading

- [x] 2.1 Implement `mdview/files.py`: `FileContent` dataclass (`path`, `text`, `lines`,
      `had_decode_errors`)
- [x] 2.2 Implement `mdview/files.py`: `read_text_lossy(path) -> FileContent` using UTF-8
      `errors="replace"`; verify with a throwaway script that a lossy read of invalid UTF-8 bytes
      returns replacement characters instead of raising, then delete the script

## 3. App bridge

- [x] 3.1 Implement `mdview/app.py`: `App` class skeleton exposed as `js_api`, with a
      `to_payload()` per dataclass
- [x] 3.2 Implement `App.open_folder()`: native folder picker, updates `SessionState.root`,
      returns payload
- [x] 3.3 Implement `App.list_markdown()`: flat listing of markdown files directly under root
      (temporary dropdown data source)
- [x] 3.4 Implement `App.load_file(path)`: reads file via `read_text_lossy`, updates
      `SessionState.open_file`, returns payload
- [x] 3.5 Implement `App.set_view_mode(mode)`: updates `SessionState.view_mode`, returns payload

## 4. Assets and window wiring

- [x] 4.1 Build `assets/index.html`: two-pane layout (content left, empty tree pane right) and
      Raw/Rendered/Both toggle markup
- [x] 4.2 Build `assets/app.css`: layout styling for the two panes and toggle
- [x] 4.3 Build `assets/app.js`: temporary flat dropdown wired to `list_markdown`/`load_file`;
      Open Folder button wired to `open_folder`
- [x] 4.4 Build `assets/app.js`: raw renderer with 1-based line-number gutter in monospace font
- [x] 4.5 Add WebView2-missing detection with an actionable in-window message
- [x] 4.6 Wire `mdview/__main__.py`: `webview.create_window(...)` with `App` as `js_api`,
      `webview.start()`

## 5. Verification

- [x] 5.1 Run `pyright mdview` and confirm zero errors
- [x] 5.2 Hand off to the user to run `python -m mdview`, exercise Open Folder, file selection,
      the raw line-number gutter, invalid-UTF-8 handling, and clean shutdown, and confirm every
      item in the step's Acceptance list passes, including that step 01's acceptance list still
      passes
