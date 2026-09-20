## 1. Package metadata and dependencies

- [x] 1.1 Write `pyproject.toml` project metadata and `requires-python`
- [x] 1.2 Add runtime dependencies (`pywebview`, `watchdog`, `markdown-it-py`, `mdit-py-plugins`,
      `linkify-it-py`, `Pygments`) and verify `python -m pip install -e .` succeeds
- [x] 1.3 Add dev dependencies (`pyinstaller`, `pyright`) and preserve the existing `integration`
      pytest marker

## 2. Package skeleton

- [x] 2.1 Create `mdview/__init__.py` with `__version__`
- [x] 2.2 Create `mdview/assets/` with a placeholder `index.html`

## 3. CLI entry point

- [x] 3.1 Create `mdview/__main__.py` with `main() -> int` and argparse for `--version` and
      `--folder`
- [x] 3.2 Implement `--version`: print `mdview.__version__`, exit 0
- [x] 3.3 Implement `--folder`: resolve to absolute path, print with forward slashes, exit 0; on
      a missing folder print an error naming it and exit non-zero

## 4. Path utilities

- [x] 4.1 Implement `mdview/paths.py`: `to_forward_slashes(path: Path) -> str`
- [x] 4.2 Implement `mdview/paths.py`: `is_markdown(path: Path) -> bool` (accepts `.md`/`.MD`,
      rejects other suffixes)
- [x] 4.3 Verify both functions with a throwaway script covering the acceptance cases below, then
      delete the script

## 5. Docs and final verification

- [x] 5.1 Write `README.md` stub naming the WebView2 runtime prerequisite
- [x] 5.2 Run `python -m pip install -e .`, `python -m mdview --version`,
      `python -m mdview --folder .`, `python -m mdview --folder ./does-not-exist`, and
      `pyright mdview`; confirm every item in the step's Acceptance list passes and that no
      `tests/` directory or test file remains in the working tree
