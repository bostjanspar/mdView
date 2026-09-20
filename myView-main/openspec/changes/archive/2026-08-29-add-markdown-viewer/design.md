## Context

Greenfield: the repository holds only the spec and OpenSpec scaffolding. See `proposal.md` — Why for
motivation and `specs/md-viewer/**` for the behaviour contracts.

Constraints that shape everything below:

- Windows-only target; `pywebview` uses the WebView2 runtime, so the UI is a web page and all UI code
  is HTML/CSS/JS with no framework.
- The app is therefore two processes-in-one: a Python side (filesystem, rendering, clipboard,
  watching) and a JS side (DOM, selection, scrolling), bridged by pywebview's `js_api` /
  `evaluate_js`. Every feature has to pick a side of that line.
- Project rules: no nested function or method definitions, no complicated return types (a
  `@dataclass` for anything with more than one meaningful field), type annotations on public
  functions and dataclass fields, pyright as the only static check.
- No permanent test suite. Each step must be verifiable by a runnable command with observable
  output, which is why the work is decomposed into `steps/` packages with explicit acceptance lists.

## Goals / Non-Goals

**Goals:**

- Keep markdown parsing, file I/O, and watching in Python; keep selection, scrolling, and layout in
  JS. Cross the bridge with small, named payloads.
- Make source line mapping a first-class output of the render step, since three separate capabilities
  (scroll sync, copy-reference from rendered pane, reload-preserving-position) all depend on it.
- Decompose into steps that each end in a state a human can observe by running the app.

**Non-Goals:**

- No HTTP server, no local web port. Content reaches the webview through the pywebview bridge only.
- No persistence layer. Session state lives in memory and dies with the process.
- No abstraction over the renderer or the watcher for hypothetical future backends.

## Decisions

### D1: Layered package, one module per concern

```
mdview/
  __main__.py        entry point: parse args, build App, start window
  app.py             App: owns Session, wires bridge; the js_api object
  session.py         SessionState dataclass + mutators
  paths.py           to_forward_slashes, is_markdown, path helpers
  files.py           read_text_lossy -> FileContent
  rendering.py       render_markdown -> RenderedDocument (html + line map)
  tree.py            scan_folder -> TreeNode
  watching.py        FolderWatcher, Debouncer
  reference.py       build_reference / build_reference_with_content -> Reference
  assets/            index.html, app.css, app.js, tree.js, sync.js, copy.js
```

Rationale: each capability in `specs/` maps to one or two modules, so a step package touches a small,
named set of files. Alternative — a single `main.py` — was rejected because the copy-reference and
scroll-sync logic is the part most likely to be revisited, and it needs to be findable.

### D2: Dataclasses at every boundary

Every value crossing a function boundary with more than one field is a `@dataclass`:

- `FileContent(path: Path, text: str, lines: list[str], had_decode_errors: bool)`
- `LineRange(start: int, end: int)` — 1-based, inclusive, used everywhere a range is meant
- `RenderedDocument(html: str, blocks: list[BlockMapping])`, `BlockMapping(tag: str, lines: LineRange)`
- `TreeNode(name: str, path: Path, is_dir: bool, children: list["TreeNode"])`
- `Reference(path_text: str, lines: LineRange, content: str | None)` with a `to_clipboard_text()` method
- `SessionState(root: Path | None, open_file: Path | None, view_mode: ViewMode, expanded: set[Path])`
- `ViewMode` as a `enum.StrEnum` — `RAW`, `RENDERED`, `BOTH` — so the JS side receives a stable string

The bridge serialises these with a small explicit `to_payload()` per dataclass rather than
`dataclasses.asdict`, so the JS contract is written down in one place per type.

### D3: Line mapping from `token.map`, emitted as `data-line`

`markdown-it-py` gives every block token a `map` of `[start, end)` 0-based lines. A custom renderer
rule wraps block-level opens with `data-line="start-end"` converted to 1-based inclusive. This single
mechanism serves scroll sync (read `data-line` of topmost visible element), rendered-pane
copy-reference (walk up from the selection anchor/focus to the nearest `data-line` ancestor, union the
ranges), and reload position preservation (remember the topmost `data-line`, restore after re-render).

Alternative considered: a separate source-map side table keyed by DOM path. Rejected — it duplicates
what the DOM can carry directly and goes stale on re-render.

### D4: Watching — one recursive observer, two debouncers

A single `watchdog` recursive observer on the session root. Its handler classifies events into two
buckets: "open file modified" and "markdown file created/deleted anywhere". Each bucket has its own
`Debouncer` (200 ms, inside the spec's 150–300 ms window) so a tree refresh never suppresses a content
reload. Because watchdog callbacks run on an observer thread and `evaluate_js` must be called from the
main thread, the handler pushes a typed event onto a `queue.Queue` that the main thread drains.
Handlers are methods on a module-level `_MarkdownEventHandler` class — no nested definitions.

Alternative considered: watching only the open file plus a separate tree observer. Rejected — two
observers on overlapping paths double the event volume for no benefit.

### D5: `Ctrl+C` interception lives in JS, clipboard write lives in Python

The JS side owns the decision (is focus in the document view? is there a selection?) because only it
can see focus and selection. It calls back into Python with the resolved `LineRange` and a flag for
with/without content; Python reads the authoritative raw lines from disk state and writes the
clipboard. This keeps the "line numbers always come from raw source" requirement enforced on the
Python side, where the source text actually is.

Fallback: if focus is in an `input`/`textarea` or there is no document selection, the JS handler does
not `preventDefault()`, so the browser's native copy runs.

### D6: Scroll sync guarded by a suppression flag

A module-level `syncing` flag in `sync.js` is set before a programmatic scroll and cleared on the next
animation frame, so the scroll event caused by syncing is ignored. This is the standard cure for the
feedback loop the spec forbids.

### D7: Step packages under `steps/`

`steps/overview.md` is the ordered index; `steps/NN-<slug>.md` are the packages. Each package states
its scope, the files it touches, the capabilities it advances, a runnable verification command, and an
**Acceptance** checklist that must be fully checked before the next step begins. `tasks.md` is the
short checklist that points at these files, so there is one ordering, not two.

## Risks / Trade-offs

- **`Ctrl+C` hijacking surprises users** → Fallback rules are specified and tested by hand in step 8;
  the confirmation toast always says which form was copied.
- **WebView2 runtime absent on target machines** → Detect at startup and show an actionable message
  (app-shell spec); document the dependency in the README.
- **Rendered→raw line mapping is only block-accurate, so a selection inside a paragraph reports the
  whole paragraph's range** → Accepted; the spec asks for nearest-block accuracy, and a wider range
  is harmless for the pasting use case.
- **Large folders make the initial scan slow and block the UI** → Scan on a worker thread, push the
  finished `TreeNode` through the same event queue as watcher events.
- **pyinstaller silently ships a build with missing assets** → Packaging step's acceptance requires
  running the built `.exe` and exercising every feature, not just launching it.
- **No regression suite** → Each step's acceptance list is the regression check; later steps re-verify
  earlier acceptance items that they could plausibly break.

## Open Questions

- Pygments (server-side) versus highlight.js (client-side) for code blocks. Both satisfy the spec;
  the choice is local to `rendering.py` or `assets/`, changes no other step, and will be settled in
  step 3 by whichever keeps the bundle simpler under pyinstaller.
