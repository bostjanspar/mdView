## 1. Reference with content

- [x] 1.1 Implement `mdview/reference.py`: `build_reference_with_content(content, lines) ->
      Reference` slicing raw lines from `FileContent.lines`, clamping `end` to the file's last
      line
- [x] 1.2 Implement the with-content `to_clipboard_text()` form: reference line, `---`, raw
      lines, `---`; verify with a throwaway script that a paste-equivalent read matches the source
      lines byte-for-byte, then delete the script
- [x] 1.3 Verify an over-long range clamps instead of raising

## 2. Bridge method

- [x] 2.1 Implement `mdview/app.py`: `App.copy_reference_with_content(start, end) -> str` sharing
      `_set_clipboard_text` with `copy_reference`
- [x] 2.2 Verify by grep that only one code path (`_set_clipboard_text`) writes the clipboard

## 3. Shortcut and context menu

- [x] 3.1 Implement `assets/copy.js`: `Ctrl+Shift+C` handler reusing step 09's range-resolution
      code
- [x] 3.2 Implement a context menu on the document view offering "Copy Reference" and "Copy
      Reference with Content", wired to the same two code paths as the shortcuts
- [x] 3.3 Verify each context menu entry matches its shortcut's output
- [x] 3.4 Verify with no file open, both context entries are unavailable and neither throws

## 4. Final verification

- [x] 4.1 Run `pyright mdview` and confirm zero errors
- [x] 4.2 Hand off to the user to run `python -m mdview`, exercise `Ctrl+Shift+C` and the context
      menu (raw and rendered selections, a `## Title` heading, a multi-block selection, an
      over-long range, no file open, and a plain text input), and confirm every item in the
      step's Acceptance list passes, including that steps 01-09's acceptance lists still pass
