## Why

The whole point of this viewer, per the project's motivation, is pasting precise file:line
references into an AI coding agent. This step delivers the core of that: selecting text in either
pane and pressing `Ctrl+C` puts `path:start-end` on the clipboard, while leaving ordinary copy
untouched everywhere else.

## What Changes

- Add `mdview/reference.py`: `Reference(path_text, lines, content)` with `to_clipboard_text()`,
  and `build_reference(path, lines) -> Reference` using `to_forward_slashes` (step 01). Reuses
  `LineRange` from `mdview/rendering.py` (step 03) as the project's one range type.
- Add `App.copy_reference(start: int, end: int) -> str` bridge method: builds the `Reference`,
  writes it to the clipboard, and returns what it wrote so JS can confirm.
- Clipboard write uses the Win32 clipboard API via `ctypes` (no new runtime dependency — the six
  dependencies fixed in step 01 do not include a clipboard library, and this project is Windows-
  only, matching the existing `ctypes`-based WebView2-missing message box in `__main__.py`).
- Add `mdview/assets/copy.js`:
  - Raw pane: map the selection's anchor and focus to gutter line numbers.
  - Rendered pane: walk up from anchor and focus to the nearest `data-line` ancestor and union the
    two ranges.
  - `Ctrl+C` handler: if focus is in the document view and there is a non-empty selection, call
    `copy_reference` and `preventDefault()`; otherwise let native copy run.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. `openspec/specs/md-viewer/copy-reference/spec.md`'s "Reference format", "Line numbers
always come from raw source", and "Plain-copy fallback" requirements already specify this
behavior; this step implements that subset (the with-content variant is step 10; the context menu
and confirmation toast are step 11). `.openspec.yaml` sets `skip_specs: true` accordingly.

## Impact

- New files: `mdview/reference.py`, `mdview/assets/copy.js`.
- Modifies `mdview/app.py` (bridge method + clipboard write) and `mdview/assets/index.html`
  (script include).
- No new pip dependency, no spec text changes.

## Non-goals

- The with-content variant (`Ctrl+Shift+C`) — step 10.
- The right-click context menu and the copy-confirmation toast — step 11.
