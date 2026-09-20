# Step 03 — Markdown rendering and the Rendered view

**Previous:** [02](02-app-shell-raw-view.md) · **Next:** [04 — Live reload](04-live-reload-open-file.md)

**Specs:** `../specs/md-viewer/markdown-rendering/spec.md`

## Goal

The Rendered view works: markdown becomes HTML with tables, task lists, footnotes, autolinks, and
highlighted code blocks — and every block-level element carries its raw source line range.

## Scope

- `mdview/rendering.py`:
  - `LineRange(start: int, end: int)` — 1-based, inclusive. This is the project's only range type.
  - `BlockMapping(tag: str, lines: LineRange)`
  - `RenderedDocument(html: str, blocks: list[BlockMapping])`
  - `render_markdown(content: FileContent) -> RenderedDocument`, built on `markdown-it-py` with
    `mdit_py_plugins` tasklists + footnotes and `linkify-it-py`.
  - A module-level renderer rule (not a nested function) that converts each block token's `map`
    (`[start, end)`, 0-based) into `data-line="start-end"` (1-based, inclusive) on the opening tag.
- Code-block highlighting — resolve design.md's Open Question here: pick Pygments (server-side) or
  highlight.js (client-side), whichever is simpler to bundle under pyinstaller, and record the choice
  in a one-line comment in `rendering.py`.
- `assets/app.js`: Rendered mode renders `RenderedDocument.html` into the content area; the toggle now
  switches between Raw and Rendered.
- A fixture file in a scratch folder exercising every construct (headings, nested lists, table,
  blockquote, inline code, labelled fence, unlabelled fence, unknown-language fence, task list,
  footnote, bare URL). Keep it out of git.

Out of scope: Both mode, scroll sync, watching.

## Task breakdown

- [ ] 3.1 Implement `rendering.py`: `LineRange(start, end)` dataclass, 1-based inclusive
- [ ] 3.2 Implement `rendering.py`: `BlockMapping(tag, lines)` dataclass
- [ ] 3.3 Implement `rendering.py`: `RenderedDocument(html, blocks)` dataclass
- [ ] 3.4 Implement `rendering.py`: `render_markdown(content) -> RenderedDocument` using the base `markdown-it-py` pipeline
- [ ] 3.5 Add `mdit_py_plugins` tasklists plugin
- [ ] 3.6 Add `mdit_py_plugins` footnotes plugin
- [ ] 3.7 Add `linkify-it-py` autolinking
- [ ] 3.8 Build the scratch fixture file exercising every construct (headings, nested lists, table, blockquote, inline code, labelled fence, unlabelled fence, unknown-language fence, task list, footnote, bare URL); verify each construct renders; keep out of git
- [ ] 3.9 Implement the module-level renderer rule converting each block token's `map` (`[start, end)` 0-based) into `data-line="start-end"` (1-based inclusive) on the opening tag
- [ ] 3.10 Verify in devtools that a paragraph on source lines 12–14 carries `data-line="12-14"`
- [ ] 3.11 Resolve the Pygments-vs-highlight.js Open Question and record the choice in a one-line comment in `rendering.py`
- [ ] 3.12 Implement the chosen highlighting approach for fenced code blocks
- [ ] 3.13 Verify a `python` fence highlights and an unknown-language fence degrades to plain `<pre>` with no error
- [ ] 3.14 Wire Rendered mode into the toggle in `app.js`: render `RenderedDocument.html` into the content area
- [ ] 3.15 Verify switching Raw ↔ Rendered shows the same file
- [ ] 3.16 Verify the Acceptance list below in full; delete the scratch fixture

## Notes

- `data-line` is load-bearing for steps 04, 08, 09 and 10 (design D3). Get it right here — an element
  without it is a bug even if it looks fine.
- Unknown-language fences must degrade to plain `<pre>`, never raise.

## Verification

```bash
python -m mdview
```
Open the fixture folder, select the fixture file, switch to Rendered, and inspect the DOM in the
WebView2 devtools (`webview.start(debug=True)` during development).

## Acceptance

- [ ] Headings, nested lists, tables, blockquotes, and inline code each render as their proper HTML
      element.
- [ ] `- [ ]` / `- [x]` render as unchecked/checked checkboxes and cannot be toggled by clicking.
- [ ] A footnote reference renders as a link to a footnote block at the end of the document.
- [ ] A bare `https://example.com` renders as a clickable link.
- [ ] A fence labelled `python` shows visually distinct keywords, strings, and comments.
- [ ] A fence labelled with an unknown language renders as plain preformatted text with no error in the
      console.
- [ ] An unlabelled fence renders as plain preformatted text.
- [ ] Every block-level element in the rendered DOM has a `data-line="start-end"` attribute; a
      paragraph known to occupy source lines 12–14 carries `data-line="12-14"`.
- [ ] Ranges are 1-based and inclusive — the first line of the file maps to `1`, not `0`.
- [ ] Re-selecting the file after editing it externally produces `data-line` values matching the new
      line numbers.
- [ ] `render_markdown` returns a `RenderedDocument`, not a tuple or a dict.
- [ ] The highlighting choice is made and recorded in a comment; design.md's Open Question is resolved.
- [ ] `pyright mdview` reports zero errors.
- [ ] The scratch fixture is not committed.
- [ ] Steps 01–02 acceptance lists still pass.
