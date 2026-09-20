# Tasks

## 1. Backend Implementation

- [x] 1.1 Add `copy_plain_text(self, text: str) -> str` method to `Api` class in `mdview/app.py` utilizing `_set_clipboard_text` and verify with a quick python check.

## 2. Frontend and Context Menu Implementation

- [x] 2.1 Add "Copy" context menu item to `copy-context-menu` in `mdview/assets/index.html`.
- [x] 2.2 Add handler in `mdview/assets/copy.js` for the plain text copy action, using `window.getSelection().toString()` and calling `api().copy_plain_text(text)`, then verify behavior.
