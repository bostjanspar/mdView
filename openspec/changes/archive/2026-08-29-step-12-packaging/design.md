## Context

See proposal.md - Why. Every other step ran `python -m mdview` from an editable install. This
step is the first point at which `mdview/assets/*` and Pygments' lexer data must be located inside
a bundled, single-file executable rather than on a normal filesystem path relative to the source
tree.

## Goals / Non-Goals

**Goals:**
- One documented command produces one `.exe`; running it does everything the source build does.
- Asset loading works identically in dev and frozen, via one small `sys.frozen` branch, not two
  divergent code paths.
- The build fails loudly (non-zero exit, names what's missing) if a dependency required at bundle
  time is absent.

**Non-Goals:**
- Code signing, an installer, auto-update, non-Windows targets.
- Reducing executable size or startup time beyond what pyinstaller's defaults produce.

## Decisions

- **`mdview/__main__.py` resolves its assets directory via `getattr(sys, "frozen", False)`, not a
  try/except around a source-relative path.** PyInstaller sets `sys.frozen = True` and
  `sys._MEIPASS` to the extraction directory at runtime; checking the flag directly is the
  documented, unambiguous way to branch, rather than inferring "frozen" from whether a path
  happens to exist (which could mask a genuinely missing asset as "must be frozen").
- **`mdview.spec` bundles `mdview/assets` at the same relative path (`mdview/assets`) inside the
  bundle**, so the frozen path is `Path(sys._MEIPASS) / "mdview" / "assets"` — mirroring
  `Path(__file__).parent / "assets"` in dev. Keeping the same relative layout in both cases means
  the only difference between dev and frozen is which root directory to join against.
- **Pygments' lexer package is collected wholesale (`collect_all` / `--collect-all pygments` in
  the spec), not cherry-picked lexer-by-lexer.** Pygments discovers built-in lexers by scanning
  `pygments.lexers._mapping` at import time; PyInstaller's static import analysis does not reliably
  follow that scan, and the acceptance list explicitly calls syntax highlighting "the assertion
  most likely to catch a missing bundled asset" — collecting the whole package removes that
  failure mode rather than chasing individual missing lexers one crash at a time.
- **pywebview's backend (`pythonnet`/`clr`, used for EdgeChromium on Windows) is also collected
  wholesale for the same reason** — its runtime dependency on the .NET bridge is not something
  PyInstaller's import scanner can fully see through static analysis alone.
- **The build command is `pyinstaller mdview.spec`, documented verbatim in `README.md`**, not a
  wrapper script — the spec file is already declarative and the acceptance list requires the
  README's instructions to work "followed verbatim ... from a fresh shell," which a spec-file
  invocation satisfies directly.
- **Verifying "the build fails loudly when a dependency is missing" is done by temporarily
  uninstalling one dev/runtime dependency in a scratch virtual environment, not by editing the
  spec to inject a fake failure.** This exercises the real failure path (pyinstaller's own
  dependency resolution erroring out) rather than a simulated one.

## Risks / Trade-offs

- [Risk] `--collect-all` for `pygments` and `pywebview` bloats the executable and slows the build
  → Mitigation: acceptable — this project's non-goals explicitly exclude optimizing build size or
  startup time; correctness (every asset present) matters more than a lean bundle here.
- [Risk] A one-file pyinstaller build extracts to a temp directory on every launch, adding a
  startup delay → Mitigation: not addressed this step; the spec's "Single-file executable"
  requirement is about deployment simplicity, not launch latency, and no acceptance item measures
  startup time.
