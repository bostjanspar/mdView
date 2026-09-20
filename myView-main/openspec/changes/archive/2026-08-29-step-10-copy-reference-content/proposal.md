## Why

Step 09 delivered reference-only copy. The second half of the copy-reference capability — pasting
the actual source lines alongside the reference, and reaching both copy actions without a
keyboard — is what makes this genuinely fast to use when handing a selection to an AI agent.

## What Changes

- Extend `mdview/reference.py`: `build_reference_with_content(content: FileContent, lines:
  LineRange) -> Reference`, slicing raw lines from `FileContent.lines`; extend
  `Reference.to_clipboard_text()` to emit the reference line, `---`, the raw lines, `---` when
  `content` is set.
- Extend `mdview/app.py`: `App.copy_reference_with_content(start, end) -> str`, sharing
  `_set_clipboard_text` with step 09's `copy_reference` — one clipboard-writing helper, not two.
- Extend `mdview/assets/copy.js`: a `Ctrl+Shift+C` handler reusing the same range-resolution code
  as `Ctrl+C`, plus a right-click context menu on the document view offering "Copy Reference" and
  "Copy Reference with Content".
- Clamp an out-of-range end line to the file's last line rather than raising.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. `openspec/specs/md-viewer/copy-reference/spec.md`'s "Reference with content" and part of
"Copy is discoverable and confirmed" (the context-menu scenario; the confirmation toast is step
11) already specify this behavior; this step implements it. `.openspec.yaml` sets
`skip_specs: true` accordingly.

## Impact

- Modifies `mdview/reference.py`, `mdview/app.py`, `mdview/assets/copy.js`, and
  `mdview/assets/index.html` (context-menu markup/wiring). No new files.
- No spec text changes.

## Non-goals

- The visible copy-confirmation toast — step 11 (until then, confirm by pasting, per the step
  file).
