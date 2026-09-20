## Context

See proposal.md - Why. `data-line` is load-bearing for steps 04 (reload position preservation), 08
(scroll sync), 09-10 (rendered-pane copy-reference) — an element missing it is a defect even if it
renders correctly visually.

## Goals / Non-Goals

**Goals:**
- Every block-level element in rendered HTML carries `data-line="start-end"`, 1-based inclusive.
- All markdown-rendering scenarios needed for Rendered mode: headings/lists/tables/blockquotes/
  inline code, task lists (non-editable), footnotes, bare-URL autolinking, labelled/unlabelled/
  unknown-language fences.
- Resolve the Pygments-vs-highlight.js open question now, in code, not left open.

**Non-Goals:**
- Both mode and scroll sync (steps 07, 08) — this step only makes the Rendered toggle button work.
- Re-rendering on external file changes (step 04).

## Decisions

- **Pygments (server-side), not highlight.js.** `Pygments` is already a declared runtime
  dependency from step 01, so choosing it adds nothing to the pyinstaller bundle beyond what's
  already there; highlight.js would require bundling and loading an additional JS asset with no
  offsetting benefit for a desktop app with no network dependency. Recorded as a one-line comment
  in `rendering.py` per the task breakdown.
- **`markdown-it-py` renderer rule override, not post-processing the HTML string.** `token.map`
  gives `[start, end)` 0-based line ranges per block token at render time; overriding the
  `renderer.rules` entries for block-opening tags (module-level function, not nested) to inject
  `data-line="start-end"` is the point where that information is available — post-processing HTML
  with a parser to re-attach line numbers would require re-deriving what markdown-it already knows.
- **`LineRange` is the project's one range type, 1-based inclusive everywhere.** Every later
  consumer of a source range (scroll sync, copy-reference) uses the same type and convention, so
  there is exactly one off-by-one-error surface, fixed here.
- **Scratch fixture file lives outside git.** A single fixture exercising every construct
  (headings, nested lists, table, blockquote, inline code, three fence variants, task list,
  footnote, bare URL) is the fastest way to verify all scenarios at once; per project convention it
  is deleted (or left untracked) once verification is done, not committed as a permanent test
  asset.

## Risks / Trade-offs

- [Risk] `mdit_py_plugins` tasklist rendering might make checkboxes interactive `<input>` elements
  by default → Mitigation: verify against the spec's "checked/unchecked, not togglable" scenario
  and force `disabled` on the checkbox if the plugin doesn't already.
- [Risk] Pygments' default CSS class names could collide with app-shell styles → Mitigation: scope
  Pygments' generated `<pre>`/`<span>` styling under a dedicated rendered-content container class.
