# Proposal

## Why

Users frequently want to copy just the selected text without file paths and line numbers when using the right-click context menu. Currently, the context menu only offers "Copy Reference" and "Copy Reference with Content", lacking a plain text copy option. Adding a "Copy" option to the context menu improves usability.

## What Changes

- Add a "Copy" option to the right-click context menu in the document view that copies the selected plain text without file names and line numbers.
- Maintain existing "Copy Reference" and "Copy Reference with Content" options.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `md-viewer/copy-reference`: Add requirement for plain text copy option in the context menu alongside reference copy options.

## Impact

- `mdview/assets/copy.js`: Add event handling and clipboard write for plain text copy.
- `mdview/assets/index.html`: Update context menu markup to include the plain text copy option.
- `mdview/app.py`: Add a Python backend method `copy_plain_text` to write raw selected text to the clipboard.

## Non-goals

- Changing keyboard shortcut behaviors (Ctrl+C remains reference copy).
- Modifying non-context-menu copy interactions.
