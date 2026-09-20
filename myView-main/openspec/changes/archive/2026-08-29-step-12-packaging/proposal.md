## Why

Every prior step has run from source. The project's whole point is a standalone desktop tool a
user can run without a Python environment, so the final step packages it as one self-contained
Windows `.exe` and proves the full feature set still works once bundled — the point at which
assets most commonly go missing silently.

## What Changes

- Add `mdview.spec` (pyinstaller spec file) for a single-file, windowed build, bundling
  `mdview/assets/` and Pygments' lexer data.
- Change `mdview/__main__.py`'s asset-path resolution to go through `sys._MEIPASS` when frozen
  (`getattr(sys, "frozen", False)`), falling back to the existing source-relative path in dev, so
  the same code runs identically from source and from the bundle.
- Extend `README.md` with the build command, the produced executable's path, and confirmation that
  the WebView2 runtime prerequisite (already documented since step 01) is what a target machine
  needs.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. `openspec/specs/md-viewer/packaging/spec.md` already specifies the single-file executable,
bundled assets, reproducible build command, and windowed launch; this step implements that
already-written spec. `.openspec.yaml` sets `skip_specs: true` accordingly.

## Impact

- New file: `mdview.spec`.
- Modifies `mdview/__main__.py` (frozen-aware asset path) and `README.md` (build/run
  instructions).
- No new runtime dependency — `pyinstaller` was already a dev dependency since step 01.

## Non-goals

- Code signing, an installer, auto-update, or any non-Windows target — explicit non-goals per the
  step file.
