## Context

See proposal.md - Why. The target module layout for the whole project (all 12 steps) is
`mdview/__main__.py`, `app.py`, `session.py`, `paths.py`, `files.py`, `rendering.py`, `tree.py`,
`watching.py`, `reference.py`, and `assets/`. This step creates only the subset that scaffolding
needs: `__init__.py`, `__main__.py`, `paths.py`, `assets/index.html`. Later steps add the rest —
this step must not create placeholder files for capabilities that don't exist yet.

## Goals / Non-Goals

**Goals:**
- An editable install (`pip install -e .`) that resolves all six runtime dependencies.
- A `main() -> int` CLI entry point usable for smoke-testing later steps without a window.
- `to_forward_slashes` and `is_markdown` implemented once, correctly, since copy-reference
  (steps 09-10) depends on `to_forward_slashes` being the sole place display paths are built.

**Non-Goals:**
- Any window, webview content, or file-content reading (step 02+).
- The full module layout (`app.py`, `session.py`, `files.py`, `rendering.py`, `tree.py`,
  `watching.py`, `reference.py`) — those files do not exist until the step that needs them.

## Decisions

- **`--folder` prints instead of acting.** Step 01 has no window and no tree, so `--folder`
  only resolves and prints the absolute path (or errors if missing). This gives an observable,
  scriptable acceptance check now without building throwaway folder-scanning logic that step 05
  would replace anyway.
- **`to_forward_slashes` takes a `Path`, returns `str`.** Uses `Path.resolve().as_posix()` rather
  than a manual `str.replace("\\", "/")`, so it also normalizes `.`/`..` segments and relative
  paths consistently — the copy-reference spec requires absolute, forward-slash paths.
- **`is_markdown` checks suffix case-insensitively** (`path.suffix.lower() == ".md"`) rather than
  a regex, since the acceptance list only requires `.md`/`.MD` accepted and everything else
  rejected.
- **No `tests/` directory.** Per project convention, `paths.py` is verified with a throwaway
  script deleted before the step is marked done, not a committed test file.

## Risks / Trade-offs

- [Risk] Declaring dependencies now that a later step ends up not needing (e.g., `Pygments`
  if syntax highlighting moves client-side) → Mitigation: the proposal's dependency list matches
  the spec's committed tech stack (md-viewer-spec.md), so this is treated as settled, not
  speculative.
- [Risk] `main()`'s argparse surface expands awkwardly once step 02 adds real window-opening
  behavior → Mitigation: keep `--version` and `--folder` as the only two flags in this step;
  step 02 is expected to change `--folder`'s behavior, not its argparse shape.
