## Why

Every later step (app shell, rendering, live-reload, tree, packaging) needs an installable,
importable `mdview` package with its runtime dependencies declared and a path-formatting utility
that later capabilities (notably copy-reference) will depend on for consistent forward-slash
paths. Nothing can be built until this scaffold exists and type-checks cleanly.

## What Changes

- Add `pyproject.toml` with project metadata, `requires-python`, the six runtime dependencies
  (`pywebview`, `watchdog`, `markdown-it-py`, `mdit-py-plugins`, `linkify-it-py`, `Pygments`), dev
  dependencies (`pyinstaller`, `pyright`), and the existing `integration` pytest marker.
- Add `mdview/__init__.py` exposing `__version__`.
- Add `mdview/__main__.py` with a `main() -> int` entry point that parses `--version` and
  `--folder <path>` and prints what it would do (no window, no file reading yet).
- Add `mdview/paths.py` with `to_forward_slashes(path: Path) -> str` and
  `is_markdown(path: Path) -> bool` — the single place path display formatting happens, since
  copy-reference will depend on it later.
- Add `mdview/assets/index.html` as a placeholder for the future webview shell.
- Add a `README.md` stub naming the WebView2 runtime prerequisite.

## Capabilities

### New Capabilities

None. This step is pure project scaffolding — no window, no rendering, no file-content reading.
`.openspec.yaml` sets `skip_specs: true` accordingly.

### Modified Capabilities

None.

## Impact

- New files only: `pyproject.toml`, `mdview/__init__.py`, `mdview/__main__.py`,
  `mdview/paths.py`, `mdview/assets/index.html`, `README.md`.
- Establishes the module layout (design D1) that every later step builds on; later steps must not
  restructure it.
- No behavior visible to an end user yet — verified via CLI (`--version`, `--folder`) and
  `pyright`.

## Non-goals

- Any window, UI, or webview content.
- Reading or rendering markdown file contents.
- Any persistent test suite (verification is by throwaway script, deleted after use).
