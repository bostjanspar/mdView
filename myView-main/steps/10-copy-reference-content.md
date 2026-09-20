# Step 10 — Copy reference with content

**Previous:** [09](09-copy-reference.md) · **Next:** [11 — Shortcuts and polish](11-shortcuts-and-polish.md)

**Specs:** `../specs/md-viewer/copy-reference/spec.md` (Reference with content, Copy is discoverable
and confirmed)

## Goal

`Ctrl+Shift+C` copies the reference plus the exact raw source lines, fenced by `---` before and after.
Both copy actions are also reachable from a context action.

## Scope

- `mdview/reference.py`: `build_reference_with_content(content: FileContent, lines: LineRange) ->
  Reference`, slicing raw lines from `FileContent.lines`; `to_clipboard_text()` emits

  ```
  C:/path/to/file.md:12-18
  ---
  <raw lines 12-18>
  ---
  ```

- `mdview/app.py`: `copy_reference_with_content(start: int, end: int) -> str`, sharing the range and
  clipboard path with step 09 — one clipboard-writing helper, not two.
- `assets/copy.js`: `Ctrl+Shift+C` handler reusing the same range-resolution code as `Ctrl+C`; a context
  menu on the document view offering "Copy Reference" and "Copy Reference with Content".
- Out-of-range clamping: a computed range beyond the file's last line clamps to the last line rather than
  raising.

Out of scope: the confirmation toast (step 11) — until then, confirm by pasting.

## Task breakdown

- [x] 10.1 Implement `reference.py`: `build_reference_with_content(content, lines) -> Reference` slicing raw lines from `FileContent.lines`
- [x] 10.2 Implement the with-content `to_clipboard_text()` form: reference line, `---`, raw lines, `---`; verify a paste matches the source lines byte-for-byte
- [x] 10.3 Implement `app.py`: `copy_reference_with_content(start, end) -> str` sharing the clipboard-writing helper with `copy_reference`
- [x] 10.4 Verify by grep that only one code path writes the clipboard
- [x] 10.5 Implement `copy.js`: `Ctrl+Shift+C` handler reusing step 09's range-resolution code
- [x] 10.6 Implement the context menu on the document view offering "Copy Reference" and "Copy Reference with Content"
- [x] 10.7 Verify each context menu entry matches its shortcut's output
- [x] 10.8 Implement out-of-range clamping to the last line in reference building
- [x] 10.9 Verify an over-long range clamps instead of raising
- [x] 10.10 Verify the Acceptance list below in full, including `## Title` copying as raw source and blank lines preserved across a multi-block selection

## Notes

- Content is *raw source*, so a rendered-pane selection over `## Title` copies `## Title`. This is the
  requirement, not a rough edge.
- Line endings inside the copied content follow the source file; do not normalise them.

## Verification

```bash
python -m mdview   # select, press Ctrl+Shift+C, paste into a text editor and compare against the file
```

## Acceptance

- [x] `Ctrl+Shift+C` over raw lines 12–13 produces: the reference line, then `---`, then exactly lines 12
      and 13 of the file, then `---`.
- [x] The copied content matches the file byte-for-byte over that range (diff a paste against the source
      lines).
- [x] A rendered-pane selection over a heading written `## Title` copies `## Title`, not `Title`.
- [x] A rendered-pane selection spanning several blocks copies every raw line in the unioned range,
      including blank lines between the blocks.
- [x] A single-line selection produces the `:12-12` reference form followed by that one line.
- [x] The reference line in the with-content form is identical to what step 09's `Ctrl+C` produces for the
      same selection.
- [x] A range extending past the last line clamps to the last line and does not raise.
- [x] The context menu on the document view offers both "Copy Reference" and "Copy Reference with
      Content", and each produces the same result as its shortcut.
- [x] With no file open, both context entries are unavailable and neither throws.
- [x] `Ctrl+Shift+C` in a plain text input does not produce a reference.
- [x] Exactly one code path writes to the clipboard (grep to confirm).
- [x] `pyright mdview` reports zero errors.
- [x] Steps 01–09 acceptance lists still pass.
