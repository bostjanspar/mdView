## 1. Rendering data model

- [x] 1.1 Implement `mdview/rendering.py`: `LineRange(start, end)` dataclass, 1-based inclusive
- [x] 1.2 Implement `mdview/rendering.py`: `BlockMapping(tag, lines)` dataclass
- [x] 1.3 Implement `mdview/rendering.py`: `RenderedDocument(html, blocks)` dataclass

## 2. Base rendering pipeline

- [x] 2.1 Implement `render_markdown(content) -> RenderedDocument` using the base
      `markdown-it-py` pipeline
- [x] 2.2 Add `mdit_py_plugins` tasklists plugin
- [x] 2.3 Add `mdit_py_plugins` footnotes plugin
- [x] 2.4 Add `linkify-it-py` autolinking
- [x] 2.5 Build a scratch fixture file (outside git) exercising headings, nested lists, table,
      blockquote, inline code, labelled fence, unlabelled fence, unknown-language fence, task
      list, footnote, and bare URL; verify each construct renders

## 3. Source line mapping

- [x] 3.1 Implement the module-level renderer rule converting each block token's `map`
      (`[start, end)` 0-based) into `data-line="start-end"` (1-based inclusive) on the opening tag
- [x] 3.2 Verify in devtools that a paragraph on source lines 12-14 carries `data-line="12-14"`

## 4. Code-block highlighting

- [x] 4.1 Resolve the Pygments-vs-highlight.js open question by choosing Pygments; record the
      choice in a one-line comment in `rendering.py`
- [x] 4.2 Implement Pygments-based highlighting for fenced code blocks
- [x] 4.3 Verify a `python` fence highlights and an unknown-language fence degrades to plain
      `<pre>` with no error

## 5. Wire Rendered mode into the UI

- [x] 5.1 Wire Rendered mode into the toggle in `app.js`: render `RenderedDocument.html` into the
      content area
- [x] 5.2 Verify switching Raw <-> Rendered shows the same file

## 6. Final verification

- [x] 6.1 Run `pyright mdview` and confirm zero errors; delete the scratch fixture
- [x] 6.2 Hand off to the user to run `python -m mdview`, exercise the Rendered view against a
      real markdown file, inspect `data-line` attributes in devtools, and confirm every item in
      the step's Acceptance list passes, including that steps 01-02's acceptance lists still pass
