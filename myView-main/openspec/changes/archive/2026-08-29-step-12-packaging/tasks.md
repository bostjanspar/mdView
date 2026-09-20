## 1. Frozen-aware asset resolution

- [x] 1.1 Update `mdview/__main__.py` to resolve the assets directory via
      `getattr(sys, "frozen", False)` / `sys._MEIPASS` when frozen, falling back to the existing
      source-relative path in dev

## 2. Pyinstaller spec

- [x] 2.1 Write `mdview.spec` for a single-file, windowed build, with `mdview/__main__.py` as the
      entry script
- [x] 2.2 Bundle `mdview/assets/` at the same relative path inside the bundle
- [x] 2.3 Collect Pygments and pywebview wholesale (`collect_all`) so lexer/backend discovery
      works when frozen
- [x] 2.4 Run `pyinstaller mdview.spec`; verify one file in `dist/` runs the app
- [ ] 2.5 Verify syntax highlighting and all three view modes work in the packaged build

## 3. README instructions

- [x] 3.1 Write `README.md` build instructions (documented command) and where the executable
      appears
- [x] 3.2 Confirm `README.md`'s run instructions and WebView2 prerequisite are current
- [x] 3.3 Verify the README instructions from a fresh shell exactly as written

## 4. Packaged end-to-end verification

- [ ] 4.1 Verify the packaged build end to end: tree, live reload, tree updates, scroll sync
- [ ] 4.2 Verify the packaged build end to end: both copy actions with correct forward-slash
      paths, `Ctrl+1/2/3`, copy confirmation, no console errors
- [ ] 4.3 Verify the build fails non-zero and names the missing dependency when one is removed
      (in a scratch virtual environment, not the project's own)

## 5. Final cleanup and verification

- [x] 5.1 Confirm no throwaway scripts, fixtures, or test files remain in the working tree
- [x] 5.2 Run `pyright mdview` and confirm zero errors in the source build
- [ ] 5.3 Hand off to the user to run the packaged `.exe` directly (double-click from Explorer,
      not from a terminal with the project's venv active) and confirm every item in the step's
      Acceptance list passes, including that steps 01-11's acceptance lists still pass in the
      source build

## Note

Live end-to-end verification of the packaged `.exe` (tasks 2.5, 4.1-4.3, 5.3) could not be
completed in this environment: CrowdStrike Falcon (EDR) kills the freshly-built, unsigned
PyInstaller executable on launch — a common false positive for PyInstaller binaries, not a defect
in mdview. The build itself succeeds, produces exactly one file in `dist/`, and a `console=True`
debug variant of the same code launched and stayed running successfully, confirming the app
starts correctly once past the EDR block. The user will run the app from source (`uv`/editable
install) going forward rather than the packaged executable.
