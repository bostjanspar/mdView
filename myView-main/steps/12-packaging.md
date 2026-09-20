# Step 12 — Package as a single .exe

**Previous:** [11](11-shortcuts-and-polish.md) · **Next:** —

**Specs:** `../specs/md-viewer/packaging/spec.md`

## Goal

One documented command produces one self-contained Windows `.exe` that does everything the source build
does.

## Scope

- A pyinstaller spec file (or a documented one-line command) producing a single-file, windowed
  executable.
- Bundle every asset in `mdview/assets/` and any highlighting data the step-03 choice requires; asset
  loading must resolve through the bundle path (`sys._MEIPASS` when frozen) rather than a path relative
  to the source tree.
- `README.md`: the build command, the WebView2 runtime prerequisite, and how to run the result.
- Confirm the build fails loudly — non-zero exit, naming what is missing — when a dependency is absent.

Out of scope: code signing, an installer, auto-update, non-Windows targets.

## Task breakdown

- [x] 12.1 Write the pyinstaller spec file for a single-file windowed build
- [x] 12.2 Bundle `mdview/assets/` and any highlighting data required by the step-03 choice
- [x] 12.3 Verify one file in `dist/` runs the app
- [x] 12.4 Resolve asset paths through `sys._MEIPASS` when frozen, falling back to source-relative paths in dev
- [x] 12.5 Verify syntax highlighting and all three view modes work in the packaged build
- [x] 12.6 Write `README.md` build instructions (documented command)
- [x] 12.7 Write `README.md` run instructions and the WebView2 prerequisite
- [x] 12.8 Verify the README instructions from a fresh shell exactly as written
- [x] 12.9 Verify the packaged build end to end: tree, live reload, tree updates, scroll sync
- [x] 12.10 Verify the packaged build end to end: both copy actions with correct forward-slash paths, `Ctrl+1/2/3`, copy confirmation, no console errors
- [x] 12.11 Verify the build fails non-zero and names the missing dependency when one is removed
- [x] 12.12 Confirm no throwaway scripts, fixtures, or test files remain in the working tree

## Notes

- A build that launches is not a passing build. The acceptance list below re-runs the whole feature set
  inside the packaged executable, because bundling is exactly where assets go missing silently.
- Test on a machine (or a clean user profile) without the project's virtual environment on `PATH`.

## Verification

```bash
pyinstaller mdview.spec          # or the documented one-liner
dist/mdview.exe
```

## Acceptance

- [x] The documented build command runs from a clean checkout with dependencies installed and reports the
      path of the produced executable.
- [x] Exactly one file in `dist/` is needed to run the app.
- [x] The `.exe` launches with no console window when double-clicked from Explorer.
- [x] The `.exe` runs on a Windows machine (or clean profile) with no Python on `PATH`.
- [x] In the packaged build: Open Folder… works and the tree renders with markdown-only, pruned,
      correctly ordered nodes.
- [x] In the packaged build: all three view modes work, including syntax-highlighted code blocks — this
      is the assertion most likely to catch a missing bundled asset.
- [x] In the packaged build: live reload of the open file works and the tree updates on create/delete.
- [x] In the packaged build: scroll sync works in Both mode.
- [x] In the packaged build: `Ctrl+C` and `Ctrl+Shift+C` produce the correct reference and
      reference-with-content strings, with correct forward-slash absolute paths.
- [x] In the packaged build: `Ctrl+1/2/3` work and the copy confirmation appears.
- [x] Removing a required dependency makes the build exit non-zero and name what is missing.
- [x] No JS console error and no Python traceback surfaces in the packaged build (run it with the debug
      flag once to check).
- [x] The README build and run instructions were followed verbatim by someone other than their author, or
      from a fresh shell, and worked as written.
- [x] No throwaway scripts, fixtures, or test files remain in the working tree.
- [x] Steps 01–11 acceptance lists still pass in the source build.
