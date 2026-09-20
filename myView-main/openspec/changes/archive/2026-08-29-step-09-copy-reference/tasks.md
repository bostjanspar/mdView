## 1. Reference data model

- [x] 1.1 Implement `mdview/reference.py`: `Reference(path_text, lines, content)` dataclass with
      `to_clipboard_text()`
- [x] 1.2 Implement `mdview/reference.py`: `build_reference(path, lines) -> Reference` using
      `to_forward_slashes`; verify with a throwaway script that a single-line selection yields
      `:12-12`, never `:12`, then delete the script

## 2. Clipboard write and bridge method

- [x] 2.1 Implement a Win32 clipboard-write helper in `mdview/app.py` using `ctypes`
      (`CF_UNICODETEXT` via `GlobalAlloc`/`SetClipboardData`)
- [x] 2.2 Implement `App.copy_reference(start, end) -> str`: builds the `Reference`, writes the
      clipboard, returns what it wrote
- [x] 2.3 Verify `copy_reference` by pasting into a text editor

## 3. Selection resolution in JS

- [x] 3.1 Implement `assets/copy.js`: raw-pane selection -> gutter line numbers mapping
- [x] 3.2 Implement `assets/copy.js`: rendered-pane selection -> nearest `data-line` ancestor walk
      from anchor and focus
- [x] 3.3 Union the two endpoint ranges (handles backwards selections); verify a rendered
      selection from source 30-34 yields `30-34` and a multi-block selection yields the union

## 4. Ctrl+C handler and fallback

- [x] 4.1 Implement the `Ctrl+C` handler: `preventDefault` + call `copy_reference` only when focus
      is in the document view and selection is non-empty
- [x] 4.2 Implement the plain-copy fallback: no `preventDefault` outside the document view or with
      no selection; verify a text input copies normally and an empty selection leaves the
      clipboard untouched

## 5. Final verification

- [x] 5.1 Run `pyright mdview` and confirm zero errors
- [x] 5.2 Hand off to the user to run `python -m mdview`, select in each pane (including Both
      mode, backwards selections, and multi-block selections), press `Ctrl+C`, paste into a text
      editor, and confirm every item in the step's Acceptance list passes, including the
      no-file-open and no-selection cases and that steps 01-08's acceptance lists still pass
