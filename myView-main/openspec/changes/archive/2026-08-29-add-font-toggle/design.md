## Context

See proposal.md - Why. Relevant current state:
- Fonts are hardcoded in `mdview/assets/app.css` (`@font-face` for JetBrains Mono / Cascadia Mono, three literal font-stack declarations for `.raw-view`, `.raw-line-number`, `.rendered-view pre/code`).
- The existing view-mode toggle (`mdview/assets/index.html`, `app.css`, `app.js`, backed by `App.set_view_mode` in `mdview/app.py` and `ViewMode` in `mdview/session.py`) is the closest analog: a `<fieldset>` of radio inputs styled as a segmented pill, wired via a JS→Python bridge call.
- `SessionState` (`mdview/session.py`) is explicitly in-memory-only and never persisted. No prefs/settings persistence mechanism exists anywhere in the app today.
- `webview.start()` defaults to `private_mode=True`, under which `localStorage` does not survive a restart, so a browser-storage approach would require also changing that startup flag.

## Goals / Non-Goals

**Goals:**
- Runtime font switch with no perceptible flash of the wrong font on restart.
- Reuse the existing toggle UI pattern and JS↔Python bridge idiom exactly, rather than inventing a new UI paradigm.
- Keep persistence dead simple: one small file, one small module.

**Non-Goals:**
- Persisting any other preference (view mode, tree-pane visibility, window size) — out of scope, no change to `SessionState`'s "never persisted" contract.
- Bundling additional font files.
- A general-purpose settings panel.

## Decisions

**Persistence: a Python-written JSON file at `%APPDATA%\mdview\prefs.json`, not `localStorage`.**
Alternative considered: `localStorage` in the webview. Rejected because pywebview's `private_mode` defaults to `True` (local storage discarded), so it would require also flipping that flag — a second, easy-to-regress behavior change for an internal WebView2 setting, versus one explicit, inspectable JSON file. This also keeps font preference cleanly separate from `SessionState`, whose docstring already commits to "never persisted across app restarts" — extending it would contradict its own contract.

**New dedicated module `mdview/prefs.py`, not an extension of `session.py`.**
Alternative considered: add a `font_choice` field to `SessionState`. Rejected for the same reason above (contract conflict) and because it would force every consumer of `SessionState`/`SessionPayload` to reason about a field with different persistence semantics than every other field.

**Startup ordering: `:root` defaults to the JetBrains Mono stack (today's default), and `app.js` fetches the real persisted choice from the JS↔Python bridge once the `pywebviewready` event fires, then applies it.**
Originally planned: pass the persisted font as a `?font=...` query parameter on the `file://` URL given to `webview.create_window`, read via `window.location.search` in an inline `<head>` script, to apply before `app.css` even loads and avoid any flash. This was implemented and tested, but pywebview/WebView2 does not handle a query string appended to a `file://` URL the way a normal browser does — the window failed to load the page at all ("file not found" / blank white screen) even though the identical URL opened correctly in a real browser. Reverted to a plain `file://` URL with no query string, at the cost of a brief flash when a non-default font is remembered (the window opens with JetBrains Mono applied via the `:root` default, then swaps to the persisted font moments later, once `pywebviewready` fires and `get_font()` resolves). No visible content exists yet at that point anyway (no file is open until the user picks one), so the practical impact is limited to the toggle's initial `checked` state settling a moment after window paint.

**CSS: a single `--font-family-mono` custom property, with `Consolas, monospace` kept as a literal fallback tail in each rule (not inside the variable).**
This lets "System monospace" be implemented by setting the variable to an empty string, letting the browser fall through to the literal tail, without a special-cased branch in JS or CSS.

## Risks / Trade-offs

- [Risk] ~~Passing `?font=...` on the `file://` URL~~ — confirmed broken: pywebview/WebView2 fails to load the page when a query string is appended to a `file://` window URL, even though the same URL works in a standalone browser → Mitigated by reverting to a plain `file://` URL and fetching the font via the JS↔Python bridge after `pywebviewready` instead (see Decisions above).
- [Risk] Brief flash of the JetBrains Mono default before the real persisted font (if different) is fetched and applied via the bridge on startup → Accepted: no file content is visible at that point (nothing is open until the user picks a file), so the only visible effect is the toggle's `checked` state settling a moment after paint.
- [Risk] Corrupt/missing prefs file → Mitigation: `load_font_choice()` catches `OSError`/`ValueError`/`KeyError`/`json.JSONDecodeError` and falls back to the JetBrains Mono default, per the spec's "Corrupt stored preference" scenario.

## Migration Plan

Additive only — no existing data or config to migrate. First run with no `prefs.json` present behaves identically to today's default (JetBrains Mono). No rollback concerns beyond reverting the change.
