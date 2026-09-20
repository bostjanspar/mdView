# Design

## Context

See proposal.md - Why. The user wants a regular "Copy" option on the right-click context menu in the document view that copies the selected text without file name and line numbers.

## Goals / Non-Goals

**Goals:**
- Add a "Copy" menu item to the context menu in `index.html`.
- Implement `copy_plain_text` method on the python backend (`app.py`) using `_set_clipboard_text`.
- Add front-end handler in `copy.js` to extract plain text from the selection and trigger the backend API call with toast notification.

**Non-Goals:**
- Modifying keyboard shortcuts (Ctrl+C remains reference copy).
- Changing reference-only or reference-with-content behaviors.

## Decisions

- **Decision 1: Plain text extraction strategy**: Use `window.getSelection().toString()` when the user selects "Copy" from the context menu, falling back or adapting to get the exact raw lines or rendered text selection. Wait, should plain copy copy the exact selected text (rendered text or raw text depending on where it's selected, or raw text)? The user request says: "add alos regular option on right click called just copy that will copy the text without file name and line". Standard browser copy copies the selected text. However, since the viewer supports selections across raw and rendered panes, using standard `window.getSelection().toString()` gives the text selected by the user. Let's check how `currentRange()` works or how selection works. Actually, standard clipboard copy in browsers copies selected text. But wait, if selected in the rendered view, does plain copy copy rendered text or raw source text? Usually, "just copy that will copy the text without file name and line" means copying the selected text. Let's use `window.getSelection().toString()` directly for plain copy, or retrieve the text from the selected range. Wait, if selected in the raw view, `window.getSelection().toString()` gives the raw lines. If in the rendered view, it gives the rendered text. That is standard and expected for a plain copy option.
  - *Alternatives considered*: Always slicing raw text from source file using line numbers. But if someone selects text in the rendered view, they expect the text they selected (or its raw equivalent). Wait, let's look at `build_reference_with_content` which slices raw source lines. For a plain copy, copying `window.getSelection().toString()` is extremely robust and simple. Let's make sure it handles both panes naturally via browser selection.

## Risks / Trade-offs

- [Risk] Plain text copy might copy formatted text if selected from rendered view. → [Mitigation] That's standard behavior for plain text/HTML copy in browsers, or we can use `selection.toString()` which yields plain text.
