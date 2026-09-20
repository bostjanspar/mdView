## Context

See proposal.md - Why. The app already loads its UI via `webview.create_window("Markdown Viewer",
str(index_html), ...)` in `mdview/__main__.py`, where `index_html` is a real file path resolved by
`_assets_dir()` (source tree in dev, `sys._MEIPASS / "mdview" / "assets"` when frozen). This means
relative paths in `app.css` (e.g. `url("fonts/JetBrainsMono-Regular.woff2")`) already resolve
correctly in both dev and packaged runs — no change needed to window creation.

`mdview.spec` already bundles the whole `mdview/assets` tree via
`datas = [("mdview/assets", "mdview/assets")]`, so any new file placed under
`mdview/assets/fonts/` is picked up by that existing glob without a spec change.

## Goals / Non-Goals

**Goals:**
- Bundle JetBrains Mono and Cascadia Mono (Regular + Bold, woff2) as static assets.
- Make the raw pane, its line-number gutter, and rendered code blocks use those fonts via
  `@font-face`, at 14px / 1.5 line-height.
- Keep rendered prose unaffected.

**Non-Goals:**
- No build tooling for font conversion/subsetting — fonts are used as downloaded, already woff2.
- No runtime font-loading fallback logic (JS) — plain CSS `@font-face` + font stack is sufficient
  since woff2 loading failure already falls through to `'Cascadia Mono', Consolas, monospace`.
- No change to `mdview.spec` unless verification shows the existing glob misses the new files.

## Decisions

- **Font source and license**: Both JetBrains Mono and Cascadia Mono are open-license
  (SIL OFL 1.1 and MIT respectively) and redistributable. Regular + Bold weights only are bundled
  (matching what `<pre>`/`<code>`/raw view actually need — no italic is used anywhere in the UI).
- **Where the files live**: `mdview/assets/fonts/{JetBrainsMono,CascadiaMono}-{Regular,Bold}.woff2`.
  Kept under `mdview/assets/` (not a new top-level `assets/`) so the existing `_assets_dir()` /
  PyInstaller `datas` glob covers them with zero code changes.
- **`@font-face` placement**: added to `mdview/assets/app.css` (the app's only stylesheet), each
  declaration using `font-weight: 400` / `700` on the two files per family rather than shipping
  separate "Bold" family names — this lets `font-weight: bold` in existing/future CSS resolve to
  the bundled bold file automatically.
- **Selector scope**: apply the font stack/size/line-height to `.raw-view`, `.raw-line-number`,
  `.rendered-view pre`, and `.rendered-view code` specifically (not a blanket `pre, code` at the
  `html`/`body` level), so prose selectors are untouched by construction rather than by careful
  exclusion.
- **No JS/window changes**: confirmed `__main__.py` already uses a file URL, not `html=`; this was
  a pre-existing correct state, not something this change needs to fix.

## Risks / Trade-offs

- [Bundled woff2 files increase repo/exe size by roughly a few hundred KB] → acceptable; no
  subsetting attempted since this is a desktop app, not a web page sensitive to payload size.
- [`@font-face src` path is wrong for the packaged build if `_assets_dir()` behavior changes later]
  → mitigated by the verification step (launch packaged exe, open a file with a code block, confirm
  visually) rather than relying solely on code inspection.
- [Font file licensing/attribution] → both fonts ship under permissive open licenses (SIL OFL /
  MIT) that permit bundling and redistribution; no attribution file is required by either license
  but the design keeps the original font file names, which retain the license notice for JetBrains
  Mono conventionally distributed alongside a LICENSE.txt — include that file if the repo wants
  explicit attribution on disk (optional, not spec-required).
