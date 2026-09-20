## Why

Every prior step built one capability at a time and deliberately deferred a handful of loose ends:
no keyboard shortcuts for view modes, no visible copy confirmation, and several app-shell error/
empty states that were either placeholder text or would surface as a raw exception instead of a
readable message. This step closes those gaps so the spec's remaining requirements are fully met,
without adding any new capability.

## What Changes

- `mdview/assets/app.js`: `Ctrl+1`/`Ctrl+2`/`Ctrl+3` switch to Raw/Rendered/Both through the same
  `switchToMode()` function the toggle buttons already call, suppressed while focus is in a text
  input.
- `mdview/assets/copy.js`: a brief non-blocking toast after each successful copy, naming which
  form was copied (reference vs. reference-with-content).
- `mdview/app.py`: `load_file` and the live-reload path catch `OSError` from an unreadable file
  and return/push a readable error message instead of letting the exception propagate; the
  content pane shows that message rather than crashing or leaving a raw traceback.
- `mdview/assets/app.js` / `index.html`: a distinct first-run empty state ("open a folder to get
  started") shown before any folder has been opened, separate from "no file open" (folder opened,
  nothing selected yet) and "file no longer available" (step 04).
- `mdview/assets/tree.js`: a distinct "no markdown files found" tree message once a folder has
  been scanned and has none, separate from the "no folder open" first-run state.
- Confirm (not re-implement) that the last-used view mode already carries over to a newly opened
  file, and that nothing persists across app restarts.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. `openspec/specs/md-viewer/copy-reference/spec.md` ("Keyboard shortcuts", "Copy is
discoverable and confirmed") and `openspec/specs/md-viewer/app-shell/spec.md` ("Session state",
"Startup errors are surfaced") already specify this behavior; this step closes the remaining gaps
against already-written specs. `.openspec.yaml` sets `skip_specs: true` accordingly.

## Impact

- Modifies `mdview/app.py` (error handling on file read), `mdview/assets/app.js`,
  `mdview/assets/copy.js`, `mdview/assets/tree.js`, `mdview/assets/index.html`, `app.css` (toast
  styling). No new files, no new spec text.

## Non-goals

- Any new capability beyond what steps 01-10 and the still-open spec requirements already define.
- Packaging — step 12.
