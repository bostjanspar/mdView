## Why

Step 01 produced an importable package with no UI. This step gives the app an actual window so a
user can open a folder and read one file's raw content — the smallest slice of the app-shell and
markdown-rendering capabilities that is independently observable and testable before rendering,
the tree, or live-reload are added.

## What Changes

- Add `mdview/session.py`: `ViewMode` (`StrEnum` of `RAW`, `RENDERED`, `BOTH`) and `SessionState`
  (root, open file, view mode, expanded set) with typed mutators.
- Add `mdview/files.py`: `FileContent` dataclass and `read_text_lossy(path) -> FileContent`
  (UTF-8, `errors="replace"`).
- Add `mdview/app.py`: an `App` class exposed to the webview as `js_api`, with `open_folder()`,
  `list_markdown()`, `load_file(path)`, `set_view_mode(mode)` — each returning a payload built by
  an explicit `to_payload()`.
- Add `mdview/assets/index.html`, `app.css`, `app.js`: two-pane layout, a Raw/Rendered/Both toggle
  (only Raw functional), and a raw renderer with a 1-based line-number gutter.
- Add a WebView2-missing startup check with an actionable in-window message.
- Wire `mdview/__main__.py` to create and start the pywebview window with `App` as `js_api`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. `openspec/specs/md-viewer/app-shell/spec.md` and
`openspec/specs/md-viewer/markdown-rendering/spec.md` already describe the target behavior this
step implements (Application window, Open folder, Session state, Startup errors; Raw view, File
reading is robust) — this step catches the implementation up to specs written up front, it does
not change what either spec requires. `.openspec.yaml` sets `skip_specs: true` accordingly.

## Impact

- New files: `mdview/session.py`, `mdview/files.py`, `mdview/app.py`,
  `mdview/assets/{index.html,app.css,app.js}`.
- Modifies `mdview/__main__.py` to open a real window instead of only printing.
- No spec text changes.

## Non-goals

- Markdown-to-HTML rendering, the folder tree, file watching, and keyboard shortcuts — all
  deferred to later steps.
- Rendered and Both view modes are present in the toggle markup but not functional this step.
