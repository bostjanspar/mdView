## Why

Step 02 gave the app a Raw view; the app-shell toggle already advertises Rendered and Both modes
but only Raw works. This step makes Rendered work: markdown source becomes HTML with the full set
of constructs the markdown-rendering spec requires, and every block carries the raw source line
range later steps (live-reload re-render, scroll sync, copy-reference) depend on.

## What Changes

- Add `mdview/rendering.py`: `LineRange`, `BlockMapping`, `RenderedDocument` dataclasses and
  `render_markdown(content: FileContent) -> RenderedDocument`, built on `markdown-it-py` with the
  `mdit_py_plugins` tasklists and footnotes plugins and `linkify-it-py` autolinking.
- Add a module-level renderer rule that stamps each block-level element's opening tag with
  `data-line="start-end"` (1-based, inclusive) derived from the token's `map`.
- Resolve the whole-project design's Open Question (Pygments vs. highlight.js for fenced code
  blocks) by choosing Pygments, recorded as a one-line comment in `rendering.py`.
- Wire Rendered mode into `assets/app.js`: the toggle now switches between Raw and Rendered by
  rendering `RenderedDocument.html` into the content area.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. `openspec/specs/md-viewer/markdown-rendering/spec.md` already specifies rendered output,
code-block highlighting, source line mapping, and view modes; this step implements a subset of
that already-written spec (Rendered mode; Both mode and scroll sync remain later steps).
`.openspec.yaml` sets `skip_specs: true` accordingly.

## Impact

- New file: `mdview/rendering.py`.
- Modifies `mdview/assets/app.js` (and possibly `app.css`) to wire the Rendered toggle.
- No spec text changes.

## Non-goals

- Both (split) mode and scroll sync — deferred to steps 07 and 08.
- Live re-render on file change — deferred to step 04.
- Highlight.js or any client-side highlighting — Pygments is the chosen approach for this project.
