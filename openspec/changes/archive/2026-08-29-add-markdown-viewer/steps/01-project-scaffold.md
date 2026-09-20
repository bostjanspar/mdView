# Step 01 — Project scaffold and dependencies

**Previous:** — · **Next:** [02 — App shell, open folder, raw view](02-app-shell-raw-view.md)

## Goal

A runnable, importable, type-checked `mdview` package with all runtime dependencies declared and
installed. No UI yet.

## Scope

- `pyproject.toml`: project metadata, `requires-python`, runtime deps (`pywebview`, `watchdog`,
  `markdown-it-py`, `mdit-py-plugins`, `linkify-it-py`, `Pygments`), dev deps (`pyinstaller`,
  `pyright`), and the existing `integration` pytest marker left intact.
- `mdview/__init__.py` with `__version__`.
- `mdview/__main__.py` with a `main() -> int` entry point that parses `--version` and `--folder <path>`
  and, for now, prints what it would open.
- `mdview/paths.py`: `to_forward_slashes(path: Path) -> str`, `is_markdown(path: Path) -> bool`.
- `mdview/assets/` directory with a placeholder `index.html`.
- `README.md` stub naming the WebView2 runtime prerequisite.

Out of scope: any window, any rendering, any file reading beyond argument handling.

## Task breakdown

- [ ] 1.1 Write `pyproject.toml` project metadata and `requires-python`
- [ ] 1.2 Add runtime dependencies (pywebview, watchdog, markdown-it-py, mdit-py-plugins, linkify-it-py, Pygments); verify `python -m pip install -e .` succeeds
- [ ] 1.3 Add dev dependencies (pyinstaller, pyright) and preserve the existing `integration` pytest marker
- [ ] 1.4 Create `mdview/__init__.py` with `__version__`
- [ ] 1.5 Create `mdview/assets/` with a placeholder `index.html`
- [ ] 1.6 Create `mdview/__main__.py` with `main() -> int` and argparse for `--version` and `--folder`
- [ ] 1.7 Implement `--version`: print `mdview.__version__`, exit 0
- [ ] 1.8 Implement `--folder`: resolve to absolute path, print with forward slashes, exit 0; error naming the missing folder and exit non-zero when it does not exist
- [ ] 1.9 Implement `mdview/paths.py`: `to_forward_slashes(path: Path) -> str`
- [ ] 1.10 Implement `mdview/paths.py`: `is_markdown(path: Path) -> bool` (accepts `.md`/`.MD`, rejects others)
- [ ] 1.11 Verify both `paths.py` functions with a throwaway script covering the acceptance cases, then delete the script
- [ ] 1.12 Write `README.md` stub naming the WebView2 runtime prerequisite
- [ ] 1.13 Verify the Acceptance list below in full

## Notes

- `to_forward_slashes` is the single place path formatting happens (copy-reference spec depends on it);
  no other module may build a display path.
- Design D1 fixes the module layout — create only the files this step lists, not the whole tree.

## Verification

```bash
python -m pip install -e .
python -m mdview --version
python -m mdview --folder .
pyright mdview
```

## Acceptance

- [ ] `python -m pip install -e .` completes without error and installs all six runtime dependencies.
- [ ] `python -m mdview --version` prints the version from `mdview.__version__` and exits 0.
- [ ] `python -m mdview --folder .` prints the absolute folder it would open, with forward slashes,
      and exits 0.
- [ ] `python -m mdview --folder ./does-not-exist` prints an error naming the missing folder and exits
      non-zero.
- [ ] `pyright mdview` reports zero errors.
- [ ] `to_forward_slashes(Path(r"C:\a\b.md"))` returns `C:/a/b.md`; `is_markdown` accepts `.md` and
      `.MD` and rejects `.txt` (verified by a throwaway script, then delete it).
- [ ] No `tests/` directory and no test file are left in the working tree.
- [ ] No function or method is defined inside another function or method.
