## Context

See proposal.md - Why. Design D5 (whole-project design) already settled the split:
`Ctrl+C` interception and selection resolution live in JS (only JS can see focus and DOM
selection); the clipboard write lives in Python, reading the authoritative raw source. This step
implements that split for the reference-only variant.

## Goals / Non-Goals

**Goals:**
- `Ctrl+C` over a non-empty document-view selection writes `path:start-end` to the clipboard and
  prevents the native copy.
- Every other `Ctrl+C` (no selection, focus outside the document view, no file open) is a no-op
  for our handler and falls through to native copy untouched.
- Line numbers are always raw source lines, regardless of which pane the selection was made in.

**Non-Goals:**
- Copy-with-content (`Ctrl+Shift+C}`) — step 10 adds a second bridge method sharing this step's
  clipboard-writing helper, not duplicating it.
- Any visible confirmation UI — step 11.

## Decisions

- **Clipboard write via `ctypes` calls into `user32`/`kernel32`, not a new pip dependency.**
  Step 01 fixed the six runtime dependencies as settled (pywebview, watchdog, markdown-it-py,
  mdit-py-plugins, linkify-it-py, Pygments); none is a clipboard library, and `md-viewer-spec.md`
  doesn't name one either. This app is Windows-only, and `__main__.py` already uses `ctypes` for
  the WebView2-missing message box, so the same low-level approach (`GlobalAlloc` +
  `SetClipboardData` with `CF_UNICODETEXT`) keeps the dependency count at six rather than adding a
  library (e.g. `pyperclip`) for one function's worth of functionality.
- **`Reference.lines` reuses `LineRange` from `mdview/rendering.py`, not a new range type.**
  Design D2 (whole-project) already commits to one range type project-wide; `reference.py`
  imports it rather than defining a second one.
- **JS resolves and orders the range before calling `copy_reference`; Python still defensively
  `min`/`max`s.** The union-of-endpoints and backwards-selection normalization happen in
  `copy.js` where the DOM selection lives, but `App.copy_reference(start, end)` also normalizes
  its two arguments — cheap, and it means the bridge method's contract (`start <= end` always) is
  self-enforcing rather than trusting the caller.
- **Selection-to-line-range resolution is two independent code paths in `copy.js`** (raw:
  `.raw-line` ancestor index; rendered: nearest `[data-line]` ancestor), not a shared abstraction.
  The two panes have structurally different DOM (one line-per-element vs. block-per-element), so a
  shared helper would need a branch internally anyway; two small named functions are clearer than
  one parameterized one for this.
- **Pane detection is "which container does `selection.anchorNode` fall under."** `rawView`/
  `renderedView` are checked via `Element.contains()`; if neither contains the anchor (e.g.,
  selection is inside a form control, where `document.getSelection()` is collapsed by browser
  behavior anyway, or there is no file open), the handler is a no-op and native copy proceeds.

## Risks / Trade-offs

- [Risk] Direct Win32 clipboard calls can fail if another process holds the clipboard open
  momentarily → Mitigation: not handled defensively this step; acceptable for a desktop app where
  clipboard contention is rare and the failure mode (silently not writing) does not corrupt state.
- [Risk] `ctypes` clipboard code is Windows-specific, so this module cannot be reused if the app
  ever targets another OS → Mitigation: acceptable — the whole app is scoped to Windows/WebView2
  per `md-viewer-spec.md`.
