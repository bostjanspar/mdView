# Step 09 — Copy reference, reference only

**Previous:** [08](08-scroll-sync.md) · **Next:** [10 — Copy reference with content](10-copy-reference-content.md)

**Specs:** `../specs/md-viewer/copy-reference/spec.md` (Reference format, Line numbers always come from
raw source, `Ctrl+C` binding, Plain-copy fallback)

## Goal

`Ctrl+C` over a selection in the document view puts `C:/path/to/file.md:12-18` on the clipboard — from
either pane — while ordinary copy still works everywhere else.

## Scope

- `mdview/reference.py`:
  - `Reference(path_text: str, lines: LineRange, content: str | None)` with
    `to_clipboard_text() -> str`.
  - `build_reference(path: Path, lines: LineRange) -> Reference` using `to_forward_slashes` from
    step 01. Single-line selections keep range form (`:12-12`).
- `mdview/app.py`: `copy_reference(start: int, end: int) -> str` bridge method that builds the
  `Reference`, writes it to the clipboard, and returns what it wrote so JS can confirm.
- `assets/copy.js`:
  - Raw pane: map the selection's anchor and focus to gutter line numbers.
  - Rendered pane: walk up from anchor and focus to the nearest `data-line` ancestor and union the two
    ranges (design D3/D5).
  - `Ctrl+C` handler: if focus is in the document view **and** there is a non-empty selection, call
    `copy_reference` and `preventDefault()`. Otherwise do not `preventDefault()` — native copy runs.
- Clipboard write happens on the Python side, reading line numbers only; the raw text of record stays in
  Python.

Out of scope: the with-content variant, the context menu, the toast (step 10 and 11).

## Task breakdown

- [x] 9.1 Implement `reference.py`: `Reference(path_text, lines, content)` dataclass with `to_clipboard_text()`
- [x] 9.2 Implement `reference.py`: `build_reference(path, lines) -> Reference` using `to_forward_slashes`; verify a single-line selection yields `:12-12`, never `:12`
- [x] 9.3 Implement `app.py`: `copy_reference(start, end) -> str` bridge method building the `Reference`, writing the clipboard, returning what it wrote
- [x] 9.4 Verify `copy_reference` by pasting into a text editor
- [x] 9.5 Implement `copy.js`: raw-pane selection → gutter line numbers mapping
- [x] 9.6 Implement `copy.js`: rendered-pane selection → nearest `data-line` ancestor walk from anchor and focus
- [x] 9.7 Implement `copy.js`: union the two endpoint ranges (handles backwards selections); verify a rendered selection from source 30–34 yields `30-34` and a multi-block selection yields the union
- [x] 9.8 Implement the `Ctrl+C` handler: `preventDefault` + call `copy_reference` only when focus is in the document view and selection is non-empty
- [x] 9.9 Implement the plain-copy fallback: no `preventDefault` outside the document view or with no selection; verify a text input copies normally and an empty selection leaves the clipboard untouched
- [x] 9.10 Verify the Acceptance list below in full, including backwards selections and the no-file-open case

## Notes

- The range is a union of the two endpoints, so a backwards selection (dragged upward) must produce the
  same range as the equivalent forward one.
- Never emit `path:12`. Always `path:12-12`.

## Verification

```bash
python -m mdview   # select in each pane, press Ctrl+C, paste into a text editor to inspect
```

## Acceptance

- [x] Selecting raw lines 12–18 and pressing `Ctrl+C` puts exactly `C:/…/notes.md:12-18` on the
      clipboard — forward slashes, absolute path, no quotes, no trailing newline beyond one.
- [x] A selection entirely within line 12 yields `…:12-12`, never `…:12`.
- [x] A selection dragged upward from line 18 to line 12 yields `12-18`, the same as dragging downward.
- [x] Selecting rendered text that came from source lines 30–34 yields `30-34`.
- [x] A rendered selection starting in a block mapped to 10–12 and ending in a block mapped to 20–22
      yields `10-22`.
- [x] Selecting rendered heading text produced by `## Title` yields the heading's source range, not a
      guess based on the visible text.
- [x] Both panes work in Both mode; the pane that holds the selection is the one that determines the
      range.
- [x] With focus in a plain text input (add a temporary input to confirm, then keep or remove it as the
      UI requires), `Ctrl+C` copies that field's selected text and produces no reference.
- [x] With the document view focused but nothing selected, `Ctrl+C` writes nothing to the clipboard — the
      previous clipboard contents survive.
- [x] With no file open, `Ctrl+C` writes nothing and does not throw.
- [x] The reported line numbers are raw source lines in every case, verified by cross-checking against
      the raw pane's gutter.
- [x] `build_reference` returns a `Reference`, not a tuple or a formatted string.
- [x] `pyright mdview` reports zero errors.
- [x] Steps 01–08 acceptance lists still pass.
