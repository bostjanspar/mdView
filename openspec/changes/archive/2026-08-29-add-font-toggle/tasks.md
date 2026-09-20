## 1. Persistence module

- [x] 1.1 Create `mdview/prefs.py` with `FontChoice(enum.StrEnum)` (`jetbrains-mono`, `cascadia-mono`, `system-mono`) and `load_font_choice()`/`save_font_choice()` reading/writing `%APPDATA%\mdview\prefs.json`; verify by running a throwaway script that saves each enum value and reloads it, and that a missing/corrupt file returns the JetBrains Mono default without raising.

## 2. Backend wiring

- [x] 2.1 In `mdview/app.py`, load the persisted choice in `App.__init__` and add `get_font()`/`set_font(font)` methods that validate via `FontChoice` and persist on change; verify by calling `App().get_font()` and `App().set_font("cascadia-mono")` from a Python shell and confirming `prefs.json` updates.
- [x] 2.2 ~~Pass the loaded font as a `?font=...` query parameter on the window URL~~ — dropped: pywebview/WebView2 fails to load `file://` URLs with a query string appended (confirmed by manual testing: "file not found" / blank white screen, despite the same URL working in a browser). `mdview/__main__.py` keeps the original plain `str(index_html)` URL; the frontend fetches the font via the bridge instead (see 3.1).

## 3. Frontend: apply-before-paint and toggle UI

- [x] 3.1 Revised approach (see design.md Decisions): `:root` in `app.css` defaults `--font-family-mono` to the JetBrains Mono stack; `mdview/assets/app.js` fetches the real persisted choice via `api().get_font()` once `pywebviewready` fires and applies it via `setProperty`; verified by launching with a non-default `prefs.json` value and confirming the toggle/font settle to the persisted choice shortly after window paint, with no visible content to flash beforehand (no file is open yet).
- [x] 3.2 Add the `#font-toggle` fieldset markup to `mdview/assets/index.html`'s toolbar, next to `#view-mode-toggle`; verify the three radio options render and are keyboard-navigable as a single group.
- [x] 3.3 Add `--font-family-mono` to `:root` and replace the three literal font-stacks (`.raw-view`, `.raw-line-number`, `.rendered-view pre, .rendered-view code`) with `var(--font-family-mono), Consolas, monospace` in `mdview/assets/app.css`; comma-extend the existing `.view-mode-input`/`.view-mode-label` pill-styling selectors to also cover `.font-choice-input`/`.font-choice-label`; verify visually that the new toggle matches the existing pill styling.
- [x] 3.4 In `mdview/assets/app.js`, wire the font radio inputs to call `api().set_font(value)` on change, update `--font-family-mono` and the selected radio in the `.then()` callback (mirroring `switchToMode`), and sync initial `checked` state from `window.__mdviewInitialFont` on load; verify by clicking each option and confirming immediate font changes in raw/rendered views with no effect on toolbar font.

## 4. End-to-end verification

- [x] 4.1 Manually ran through the scenarios in `specs/md-viewer/font-preference/spec.md`: toggle visible on launch, switching fonts live updates raw/rendered code without affecting toolbar font (confirmed live by user), persistence across a full app restart (confirmed live by user), default-on-first-run and corrupt/missing-prefs fallback (confirmed via automated script in task 1.1). All throwaway verification scripts were run inline via `python -c` (not saved to disk), so there is nothing to delete.
