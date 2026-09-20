## Why

Reviewing markdown docs while working with Claude Code means constantly switching between an
editor and a preview, then hand-typing `path:line` references into chat. No existing preview tool
gives a folder-scoped `.md` tree, side-by-side raw/rendered panes, and a one-keystroke
"copy this selection as a file:line reference" action. This change builds that tool.

## What Changes

- New standalone Windows desktop app (Python + pywebview) that opens a folder and previews its
  markdown files.
- Right-hand collapsible tree scoped to the opened folder, filtered to `.md` files, with empty
  branches excluded.
- Three view modes for the open file — Raw (monospace, line numbers), Rendered (HTML), Both
  (split) — switchable via toolbar and `Ctrl+1/2/3`, last mode persisted for the session.
- Live reload: `watchdog` re-reads and re-renders the open file on modification (debounced
  150–300 ms) and refreshes the tree when `.md` files appear or disappear.
- Scroll sync in Both mode, driven by `data-line="start-end"` attributes emitted from
  markdown-it's `token.map`.
- Smart select → copy reference: `Ctrl+C` copies `C:/path/to/file.md:12-18`, `Ctrl+Shift+C` copies
  the same reference plus the raw lines fenced by `---`. Line numbers are always raw source lines,
  paths always use forward slashes, single-line selections use range form (`:12-12`).
- Packaged with pyinstaller into a single `.exe`.
- Work is decomposed into small, independently verifiable step packages under
  `openspec/changes/add-markdown-viewer/steps/`, with `steps/overview.md` listing them in
  implementation order and each step file carrying its own acceptance checklist that must pass
  before the next step starts.

## Capabilities

### New Capabilities
- `md-viewer/app-shell`: pywebview window, Python↔JS bridge, open-folder picker, session state.
- `md-viewer/markdown-rendering`: markdown-it-py pipeline, plugins, syntax highlighting,
  `data-line` source mapping, and the Raw / Rendered / Both view modes.
- `md-viewer/file-tree`: recursive `.md` scan, tree model, filtering of empty branches,
  collapse/expand state, file selection.
- `md-viewer/live-reload`: watchdog observers, debouncing, in-place content refresh preserving
  scroll position, live tree updates on create/delete.
- `md-viewer/scroll-sync`: nearest-block bidirectional scroll sync between raw and rendered panes
  in Both mode.
- `md-viewer/copy-reference`: selection → raw line range resolution (from either pane), reference
  and reference+content clipboard formats, keyboard shortcuts with plain-copy fallback.
- `md-viewer/packaging`: pyinstaller single-file build.

### Modified Capabilities
None — this is a greenfield app.

## Non-goals

- Editing markdown (view-only).
- Syncing scroll position with an external editor such as Kate.
- Multi-window, multi-folder tabs, or more than one open file at a time.
- A permanent test suite; verification is by runnable command with observable output.

## Impact

- New Python package plus injected HTML/CSS/JS assets; no existing code is touched.
- New runtime dependencies: `pywebview`, `watchdog`, `markdown-it-py`, `mdit-py-plugins`,
  `linkify-it-py`, `Pygments`. New dev dependency: `pyinstaller`.
- Windows-only target (WebView2 runtime required).
