## Why

The raw pane and rendered code blocks currently fall back to whatever monospace font the OS
happens to have installed (`Consolas` or a generic `monospace`), so the viewer looks different
machine to machine and can't guarantee a code-friendly font on a clean Windows install. Bundling
JetBrains Mono and Cascadia Mono guarantees a consistent, code-legible look everywhere the app runs,
including the packaged `.exe` on a machine with neither font installed.

## What Changes

- Add JetBrains Mono (Regular + Bold, woff2, SIL OFL) and Cascadia Mono (Regular + Bold, woff2) to
  `mdview/assets/fonts/`.
- Add `@font-face` declarations for both families in `app.css`, referencing the bundled files with
  relative paths.
- Apply `font-family: 'JetBrains Mono', 'Cascadia Mono', Consolas, monospace;`, `font-size: 14px`,
  and `line-height: 1.5` to the raw pane (`.raw-view`, including the `.raw-line-number` gutter) and
  to rendered code blocks (`.rendered-view pre`, `.rendered-view code`), replacing the current
  `"Cascadia Mono", Consolas, monospace` / `13px` raw-view styling.
- Leave rendered prose (headings, paragraphs, lists, tables, etc.) on its existing sans-serif stack
  — no monospace bleed into prose.
- Bundle `assets/fonts/` into the PyInstaller build (`mdview.spec`) so the packaged `.exe` carries
  the fonts too.
- No change to window creation: `mdview/__main__.py` already loads the UI via
  `webview.create_window(..., str(index_html), ...)` (a real file, not an inline `html=` string), so
  relative font paths from `app.css` already resolve correctly.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `md-viewer/markdown-rendering`: the Raw view requirement now specifies the bundled monospace font
  stack, size, and line-height instead of an unspecified/system monospace font, and the
  syntax-highlighted code block requirement now specifies the same stack for rendered `<pre>`/`<code>`.
- `md-viewer/packaging`: the "Bundled assets" requirement now explicitly covers the bundled font
  files as an asset the packaged executable must include.

## Impact

- `mdview/assets/fonts/` (new): 4 woff2 font files.
- `mdview/assets/app.css`: new `@font-face` rules; updated `.raw-view`, `.raw-line-number`,
  `.rendered-view pre`, `.rendered-view code` rules.
- `mdview.spec`: add `mdview/assets/fonts` to `datas` (already covered by the existing
  `("mdview/assets", "mdview/assets")` glob entry — verify during implementation whether an explicit
  entry is still needed).
- No changes to `mdview/app.py`, `mdview/__main__.py`, or any Python module — this is a static-asset
  and stylesheet change only.

## Non-goals

- No font selection UI or user-configurable font preference.
- No change to which elements are monospace vs. prose (only the font stack/sizing applied to the
  already-monospace elements).
- No change to the window-creation mechanism (already file-based, not inline HTML).
- No new fonts beyond JetBrains Mono and Cascadia Mono.
