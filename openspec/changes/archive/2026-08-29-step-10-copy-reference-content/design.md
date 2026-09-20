## Context

See proposal.md - Why. Step 09 already built `Reference`, `build_reference`, `copy_reference`,
`_set_clipboard_text`, and `copy.js`'s selection-to-line-range resolution. This step extends those
rather than duplicating them — the step file is explicit that "one clipboard-writing helper, not
two" and reusing "the same range-resolution code as `Ctrl+C`" are load-bearing constraints, not
suggestions.

## Goals / Non-Goals

**Goals:**
- `Ctrl+Shift+C` produces the reference line, `---`, the exact raw source lines, `---`.
- Content is always raw source (a rendered `## Title` copies `## Title`, never the rendered text).
- A range extending past the last line clamps rather than raising.
- Both copy actions are reachable via a right-click context menu, matching their shortcuts.
- Exactly one code path writes to the clipboard, for both variants.

**Non-Goals:**
- The visible confirmation toast — step 11.

## Decisions

- **`Reference.content` (already a field since step 09, unused until now) carries the raw text;
  `to_clipboard_text()` branches on whether it's `None`.** Step 09 already gave `Reference` a
  `content: str | None` field for exactly this extension point, so no new dataclass field is
  needed — only the branch in `to_clipboard_text()`.
- **`build_reference_with_content` slices `FileContent.lines`, not the rendered HTML or the
  selection's `textContent`.** The spec's "content is raw, not rendered" requirement means the
  source of truth for copied text is the same `FileContent.lines` list `read_text_lossy` already
  produced — JS only ever supplies line *numbers*, never text, keeping "line numbers always come
  from raw source" and "content is raw" enforced by the same mechanism (Python owns the text).
- **Clamping happens in `build_reference_with_content`, once, not in both bridge methods or in
  JS.** `end = min(end, len(content.lines))` at the one place that slices lines is sufficient;
  `copy_reference` (reference-only, step 09) has no content to slice so it has nothing to clamp —
  an out-of-range end there only affects the printed number, which the spec doesn't forbid (no
  scenario requires clamping the number itself, only the content read).
- **`App.copy_reference_with_content` calls the same `_set_clipboard_text` as `copy_reference`.**
  Both bridge methods build a `Reference` (with or without content) and pass its
  `to_clipboard_text()` to the one clipboard-writing helper — verified by grep per the task list,
  not by construction alone, since it's easy to accidentally inline a second Win32 call.
- **`copy.js` factors range resolution into a function shared by both shortcut handlers**, and the
  context menu's two entries call the same two bridge-method wrappers the shortcuts use, so a
  context-menu click and its shortcut are provably the same code path rather than two
  independently-written call sites that could drift.
- **The context menu is a minimal custom `<ul>` shown on `contextmenu`, not the native OS menu.**
  pywebview's webview surface doesn't expose a way to inject entries into the native right-click
  menu; a small absolutely-positioned custom menu, hidden by default and shown at the cursor
  position on `contextmenu` (with `preventDefault()` to suppress the native one), is the standard
  approach for a custom action list in a webview.

## Risks / Trade-offs

- [Risk] A custom context menu can be dismissed inconsistently across click-outside/`Escape`/
  scroll → Mitigation: acceptable for v1 — the spec only requires the two entries be present and
  reachable, not a full native-menu-parity interaction model.
- [Risk] Clamping silently changes what's copied when a caller passes an out-of-range end
  → Mitigation: this is the explicit acceptance requirement ("clamps to the last line and does not
  raise"), not an accidental side effect.
