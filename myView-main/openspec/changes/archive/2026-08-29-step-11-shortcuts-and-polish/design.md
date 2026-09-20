## Context

See proposal.md - Why. This step touches no new module — it closes gaps left open by steps 02
(app-shell error states, empty states), 07 (view-mode switching), and 09/10 (copy confirmation).

## Goals / Non-Goals

**Goals:**
- One code path per mode change: `Ctrl+1/2/3` and the toggle buttons both call `switchToMode()`;
  neither can leave the UI in a state the other wouldn't also produce.
- Every app-shell error/empty state named in the spec is a readable in-window message, never an
  unhandled Python traceback or a JS console error.
- Copy actions are visibly confirmed without blocking interaction.

**Non-Goals:**
- Any new capability. Every change here closes a gap in already-written specs from steps 01-10.

## Decisions

- **Shortcut handler and toggle buttons both call one `switchToMode(mode)` function.** The task
  list is explicit that "one code path per mode change" is a requirement, not a suggestion —
  extracting the existing toggle-click body (already written in step 07/08) into a named function
  and having both call sites use it is the only way to guarantee they can't diverge.
- **Shortcuts are suppressed via a small `isTextInputFocused()` check** (`document.activeElement`
  is `INPUT`/`TEXTAREA`/`contentEditable`), not by scoping the `keydown` listener to a specific
  container. The document view has no text inputs of its own today, but the check is cheap and
  correct regardless of what gains focus later (e.g. a future filter box), matching the spec's
  "Plain-copy fallback"-style focus check already used for `Ctrl+C`.
- **Unreadable files are handled by catching `OSError` at the two read call sites
  (`App.load_file`, `App._reload_open_file`), not by pre-checking readability.** A pre-check
  (`os.access`) is inherently racy (the file can become unreadable between the check and the
  read); catching the actual `read_bytes()` failure and turning it into an error payload is the
  only race-free approach, and both bridge/reload call sites already funnel through
  `read_text_lossy`, so there are exactly two places to add the guard.
- **The error state reuses the existing content-pane empty-state element**, carrying a message
  string in the payload (`FileContentPayload.error`), rather than a new DOM element or a modal.
  This matches design D2's principle: extend the existing dataclass field, don't invent parallel
  state for what is still fundamentally "nothing valid to show in the content area."
- **First-run vs. "no file open" vs. "no markdown files" are distinguished by which lifecycle
  event last touched the empty-state text**, not by a separate boolean flag. `openFolderBtn`'s
  success handler sets the content pane's text to "No file open." the moment a folder is chosen;
  `tree.js`'s `render()` sets the tree pane's text to "No markdown files found." only when it has
  actually received a scanned (non-null) tree with zero children. Until either of those fires, the
  HTML's original first-run text stands unmodified.
- **The copy toast lives in `copy.js`, not `app.js`.** Only copy actions need to show it, and
  `copy.js` already owns every call site that succeeds or fails at copying; a shared toast
  primitive in `app.js` would create a dependency in the wrong direction (copy-specific behavior
  driving shell-level code).
- **Verifying the unreadable-file and WebView2-missing paths uses simulated rather than literal
  failures, and the simulation method is recorded in tasks.md/acceptance notes** — per the step
  file's own instruction ("simulate the failure path ... and say how you simulated it"). Real ACL
  manipulation or a clean machine without the runtime are both impractical to set up reliably in
  this environment.

## Risks / Trade-offs

- [Risk] Catching `OSError` broadly in `load_file`/`_reload_open_file` could also swallow a
  genuinely unexpected error (e.g. a bug) and misreport it as "file unreadable" → Mitigation:
  `OSError` is the correct, narrow exception family for filesystem access failures in Python;
  anything else (a `TypeError` from a real bug) still propagates and is not silently hidden.
- [Risk] The `Ctrl+1/2/3` `keydown` listener could conflict with a browser-reserved shortcut on
  some platforms → Mitigation: none of `1`/`2`/`3` with `Ctrl` are reserved by Chromium/WebView2,
  and `event.preventDefault()` is only called once we've confirmed we're handling it.
