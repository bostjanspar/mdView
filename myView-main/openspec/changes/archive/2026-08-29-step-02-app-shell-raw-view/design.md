## Context

See proposal.md - Why. Target module layout (design D1 from the whole-project design) is
`app.py`, `session.py`, `files.py`, `rendering.py`, `tree.py`, `watching.py`, `reference.py`,
`assets/`. This step adds `session.py`, `files.py`, `app.py`, and the first three asset files;
`rendering.py`, `tree.py`, `watching.py`, `reference.py` remain absent until the steps that need
them.

## Goals / Non-Goals

**Goals:**
- A real, closable pywebview window backed by `App` as `js_api`.
- Raw view is byte-faithful: no wrapping, no tab expansion, no trailing-whitespace trimming.
- Every value crossing the Python/JS boundary is a dataclass with an explicit `to_payload()`.

**Non-Goals:**
- Markdown-to-HTML conversion (step 03).
- Populating the tree pane (step 05) — it stays visually present but empty.
- Any file watching (step 04).

## Decisions

- **Bridge is `js_api` + `evaluate_js` only, no HTTP server.** pywebview's `js_api` mechanism is
  sufficient for a single-process desktop app and avoids the complexity (port, CORS, lifecycle) of
  running a local web server just to serve one page. Alternative considered: a local Flask/FastAPI
  server — rejected, no need for HTTP semantics.
- **Explicit `to_payload()` per dataclass, not `dataclasses.asdict`.** `asdict` recurses
  automatically and silently breaks if a field type changes; a hand-written `to_payload()` makes
  the JS-visible contract for each type visible in one place in the Python source.
- **Temporary flat dropdown for file selection.** The real tree (step 05) doesn't exist yet;
  `App.list_markdown()` does a flat, non-recursive scan of the root only, so this step has an
  observable way to pick a file without building throwaway tree-scanning code that step 05 would
  replace anyway.
- **`read_text_lossy` always decodes as UTF-8 with `errors="replace"`.** Matches the
  "File reading is robust" requirement (undecodable bytes become a replacement character, no
  crash) without adding encoding detection.
- **`SessionState` is in-memory only, never persisted.** Matches app-shell's "State is not
  persisted across runs" requirement — no config file, no serialization needed.

## Risks / Trade-offs

- [Risk] WebView2 absence is only detectable once pywebview tries to create the window, which may
  raise rather than degrade gracefully → Mitigation: wrap window creation and show the actionable
  message in a minimal fallback window (or console message plus non-zero exit) if creation fails.
- [Risk] The flat dropdown built for this step could tempt future steps to keep extending it
  instead of building the real tree → Mitigation: proposal and this design both call it temporary;
  step 05 replaces the dropdown's role entirely.
