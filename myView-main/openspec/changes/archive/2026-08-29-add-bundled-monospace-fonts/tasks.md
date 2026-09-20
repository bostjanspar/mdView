## 1. Bundle font files

- [x] 1.1 Download JetBrains Mono Regular + Bold (woff2, SIL OFL) and Cascadia Mono Regular + Bold
  (woff2) into `mdview/assets/fonts/`, and verify all four files exist and open as valid woff2
  (e.g. `python -c "import fontTools.ttLib; fontTools.ttLib.TTFont('mdview/assets/fonts/JetBrainsMono-Regular.woff2')"`
  or simply confirm the files load in a browser `@font-face` test page).

## 2. Wire up @font-face and selectors

- [x] 2.1 Add `@font-face` declarations for both families (Regular = `font-weight: 400`, Bold =
  `font-weight: 700`) to `mdview/assets/app.css`, with `src` paths relative to `app.css`
  (`fonts/...woff2`), and verify by running the app from source, opening DevTools (if available)
  or visually confirming the font loads with no 404 in the console/log.
- [x] 2.2 Update `.raw-view` and `.raw-line-number` in `app.css` to use
  `font-family: 'JetBrains Mono', 'Cascadia Mono', Consolas, monospace;`, `font-size: 14px;`, and
  `line-height: 1.5;` (replacing the current `"Cascadia Mono", Consolas, monospace` / `13px`
  values), and verify by opening a `.md` file in Raw view and confirming line height/size visually.
- [x] 2.3 Add rules for `.rendered-view pre` and `.rendered-view code` using the same font stack,
  `font-size: 14px;`, and `line-height: 1.5;`, and verify by opening a `.md` file with a fenced code
  block in Rendered view.
- [x] 2.4 Confirm no other selector in `app.css` (headings, paragraphs, lists, tables under
  `.rendered-view`) picks up the new font stack — the existing sans-serif inheritance from `body`
  should remain unchanged for prose.

## 3. Packaging

- [ ] 3.1 Verify `mdview.spec`'s existing `datas = [("mdview/assets", "mdview/assets")]` entry
  picks up `mdview/assets/fonts/` automatically; if it does not, add an explicit
  `("mdview/assets/fonts", "mdview/assets/fonts")` entry. Verify by building with
  `pyinstaller mdview.spec` and checking the new font files exist under the extracted/output
  `mdview/assets/fonts/` in `dist/`.

## 4. End-to-end verification

- [ ] 4.1 Launch the app from source (`python -m mdview` or the project's documented run command),
  open a folder containing a `.md` file with a fenced code block, and visually confirm the raw pane
  and the rendered code block both use the bundled JetBrains Mono font (distinctive zero/letter
  shapes), not a system fallback.
- [ ] 4.2 Repeat the same visual check against the packaged `dist/mdview.exe` build to confirm the
  bundled fonts render identically when run standalone.
