Each numbered group is one step package under `steps/`. **Read the step file before starting the
group** — it holds the scope, the verification command, and the Acceptance checklist. A group is done
only when every box in that step file's Acceptance list is checked. Do not start a group before the
previous group is done.

This file has been expanded to a finer grain than the step files' original `N.M` items so that each
checkbox is a single, independently-checkable unit of work. Each step file's "Task breakdown" section
carries the same items in the same order — the two are kept in sync deliberately (design D7: one
ordering, not two orderings of different content).

Ordered index: [steps/overview.md](steps/overview.md)

## 1. Project scaffold — [steps/01-project-scaffold.md](steps/01-project-scaffold.md)

- [ ] 1.1 Write `pyproject.toml` project metadata and `requires-python`
- [ ] 1.2 Add runtime dependencies (pywebview, watchdog, markdown-it-py, mdit-py-plugins, linkify-it-py, Pygments) to `pyproject.toml`; verify `python -m pip install -e .` succeeds
- [ ] 1.3 Add dev dependencies (pyinstaller, pyright) and preserve the existing `integration` pytest marker
- [ ] 1.4 Create `mdview/__init__.py` with `__version__`
- [ ] 1.5 Create `mdview/assets/` with a placeholder `index.html`
- [ ] 1.6 Create `mdview/__main__.py` with `main() -> int` and argparse for `--version` and `--folder`
- [ ] 1.7 Implement `--version`: print `mdview.__version__`, exit 0
- [ ] 1.8 Implement `--folder`: resolve to absolute path, print with forward slashes, exit 0; print an error naming the missing folder and exit non-zero when it does not exist
- [ ] 1.9 Implement `mdview/paths.py`: `to_forward_slashes(path: Path) -> str`
- [ ] 1.10 Implement `mdview/paths.py`: `is_markdown(path: Path) -> bool` (accepts `.md`/`.MD`, rejects others)
- [ ] 1.11 Verify `to_forward_slashes` and `is_markdown` with a throwaway script covering the acceptance cases, then delete the script
- [ ] 1.12 Write `README.md` stub naming the WebView2 runtime prerequisite
- [ ] 1.13 Verify step 01 acceptance list in full: `pyright mdview` clean, `--folder ./does-not-exist` exits non-zero, no test files remain, no nested function/method definitions

## 2. App shell, open folder, raw view — [steps/02-app-shell-raw-view.md](steps/02-app-shell-raw-view.md)

- [ ] 2.1 Implement `session.py`: `ViewMode` `StrEnum` (`RAW`, `RENDERED`, `BOTH`)
- [ ] 2.2 Implement `session.py`: `SessionState` dataclass (`root`, `open_file`, `view_mode`, `expanded`) with typed mutators
- [ ] 2.3 Implement `files.py`: `FileContent` dataclass (`path`, `text`, `lines`, `had_decode_errors`)
- [ ] 2.4 Implement `files.py`: `read_text_lossy(path) -> FileContent` using UTF-8 `errors="replace"`; verify a lossy read of invalid UTF-8 returns replacement chars instead of raising
- [ ] 2.5 Implement `app.py`: `App` class skeleton exposed as `js_api`, with a `to_payload()` per dataclass
- [ ] 2.6 Implement `App.open_folder()`: native folder picker, updates `SessionState.root`, returns payload
- [ ] 2.7 Implement `App.list_markdown()`: flat listing of markdown files directly under root (temporary dropdown data source)
- [ ] 2.8 Implement `App.load_file(path)`: reads file via `read_text_lossy`, updates `SessionState.open_file`, returns payload
- [ ] 2.9 Implement `App.set_view_mode(mode)`: updates `SessionState.view_mode`, returns payload
- [ ] 2.10 Verify each `App` method's return value from the JS console
- [ ] 2.11 Build `assets/index.html`: two-pane layout (content left, empty tree pane right) and Raw/Rendered/Both toggle markup
- [ ] 2.12 Build `assets/app.css`: layout styling for the two panes and toggle
- [ ] 2.13 Build `assets/app.js`: temporary flat dropdown wired to `list_markdown`/`load_file`; Open Folder button wired to `open_folder`
- [ ] 2.14 Build `assets/app.js`: raw renderer with 1-based line-number gutter in monospace font; verify a 40-line file shows gutter 1–40 matching the file
- [ ] 2.15 Add WebView2-missing detection with an actionable in-window message
- [ ] 2.16 Wire `__main__.py`: `webview.create_window(...)` with `App` as `js_api`, `webview.start()`; verify the window opens and closes cleanly with exit 0
- [ ] 2.17 Verify step 02 acceptance list in full: picker-cancel, empty-folder state, read-only raw pane, invalid UTF-8 handling, file switch replaces content, clean exit, no state persisted across restarts, pyright clean, dataclasses-only boundaries, step 01 still passes

## 3. Markdown rendering and Rendered view — [steps/03-markdown-rendering.md](steps/03-markdown-rendering.md)

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
- [ ] 3.16 Verify step 03 acceptance list in full; delete the scratch fixture

## 4. Live reload of the open file — [steps/04-live-reload-open-file.md](steps/04-live-reload-open-file.md)

- [ ] 4.1 Implement `watching.py`: `Debouncer(delay_ms)` with typed `schedule(...)`, 200 ms default
- [ ] 4.2 Implement `watching.py`: typed event dataclass(es) for queue items (e.g. content-changed, file-deleted)
- [ ] 4.3 Implement `watching.py`: module-level `_MarkdownEventHandler(FileSystemEventHandler)` with methods classifying events and pushing onto a `queue.Queue`
- [ ] 4.4 Implement `watching.py`: `FolderWatcher.start(root)` / `stop()` owning one recursive observer
- [ ] 4.5 Verify events arrive for an external save
- [ ] 4.6 Implement `app.py`: main-thread queue drain loop
- [ ] 4.7 Implement `app.py`: on "open file modified" event, re-read via `read_text_lossy` and re-render if needed
- [ ] 4.8 Implement `app.py`: push new content to the webview via `evaluate_js` from the main thread only
- [ ] 4.9 Verify an external save updates the view within 1 second in both Raw and Rendered mode
- [ ] 4.10 Implement `assets/app.js`: capture the topmost visible `data-line` (Rendered) or gutter line number (Raw) before a content swap
- [ ] 4.11 Implement `assets/app.js`: restore the captured position after the swap, clamping to the last existing line when the file got shorter
- [ ] 4.12 Verify appending a line keeps the viewport; verify truncating scrolls to the nearest existing position
- [ ] 4.13 Handle deletion of the open file: show "file no longer available" message, keep app running
- [ ] 4.14 Create the second debouncer (tree, 200 ms) now even though unused this step, per design D4
- [ ] 4.15 Verify debouncing with a temporary two-writes-in-100ms script and a temporary refresh counter — exactly 1 refresh; two saves a second apart give 2; delete script and counter afterward
- [ ] 4.16 Verify step 04 acceptance list in full: deleted-open-file message, folder switch stops old watchers, window close terminates all threads, `evaluate_js` never called off the main thread

## 5. Folder tree and file selection — [steps/05-folder-tree.md](steps/05-folder-tree.md)

- [ ] 5.1 Implement `tree.py`: `TreeNode(name, path, is_dir, children)` dataclass
- [ ] 5.2 Implement `tree.py`: `scan_folder(root) -> TreeNode` with empty-branch pruning (no `.md` at any depth)
- [ ] 5.3 Implement `tree.py`: dirs-before-files case-insensitive ordering within `scan_folder`
- [ ] 5.4 Implement `tree.py`: symlink-cycle protection via visited real paths
- [ ] 5.5 Build the step-05 scratch folder shape and verify `scan_folder` output against it
- [ ] 5.6 Run the scan on a worker thread, deliver the finished `TreeNode` through the step-04 event queue
- [ ] 5.7 Verify the window stays responsive while scanning a folder with several thousand files
- [ ] 5.8 Implement `assets/tree.js`: render `TreeNode` into the tree pane
- [ ] 5.9 Implement `assets/tree.js`: per-directory expand/collapse toggle
- [ ] 5.10 Implement `assets/tree.js`: open-file highlight
- [ ] 5.11 Implement `assets/tree.js`: directory click toggles expand state without changing the open file
- [ ] 5.12 Verify each `tree.js` interaction individually
- [ ] 5.13 Populate `SessionState.expanded` with the open file's ancestors on load
- [ ] 5.14 Key collapse state by `Path` so it survives a re-scan; verify expansion survives a re-scan
- [ ] 5.15 Remove the step-02 dropdown from `index.html`/`app.js`
- [ ] 5.16 Verify step 05 acceptance list in full; delete the scratch folder

## 6. Live tree updates — [steps/06-tree-live-updates.md](steps/06-tree-live-updates.md)

- [ ] 6.1 Route `.md` create events into the second debouncer, emitting a "tree dirty" event
- [ ] 6.2 Route `.md` delete events into the second debouncer, emitting "tree dirty"
- [ ] 6.3 Route `.md` move events into the second debouncer, emitting "tree dirty"
- [ ] 6.4 Verify a `.txt` creation produces no event
- [ ] 6.5 Confirm newly created subdirectories are covered by the existing recursive observer (do not assume)
- [ ] 6.6 On "tree dirty", re-run `scan_folder` on the worker thread in `app.py`
- [ ] 6.7 Push the new `TreeNode` to the webview, keeping content reload and tree refresh independent (neither suppresses the other)
- [ ] 6.8 Implement `assets/tree.js` re-render from the new `TreeNode` restoring expansion state from `SessionState.expanded`
- [ ] 6.9 Keep the selection highlight on the open file across a tree refresh
- [ ] 6.10 Verify new file appears, brand-new nested directory path appears, deletion removes node and cascades pruning of markdown-free parents
- [ ] 6.11 Verify a simultaneous edit + create produces both a content refresh and a tree refresh
- [ ] 6.12 Verify a burst of ten creations produces one tree refresh (temporary counter, then remove it)
- [ ] 6.13 Verify step 06 acceptance list in full

## 7. Both (split) view — [steps/07-both-view.md](steps/07-both-view.md)

- [ ] 7.1 Add split layout CSS for `ViewMode.BOTH`: raw pane left, rendered pane right, each its own scroll container
- [ ] 7.2 Add a usable divider between panes; ensure panes cannot collapse to zero width and the window does not force horizontal scroll
- [ ] 7.3 Wire `app.js` Both mode to reuse the existing raw renderer (no duplication)
- [ ] 7.4 Wire `app.js` Both mode to reuse the existing rendered renderer (no duplication); verify no third rendering path was added
- [ ] 7.5 Make the toggle indicate the active mode across all three modes
- [ ] 7.6 Verify Raw → Rendered → Both → Raw always shows the same file with no blank or duplicated pane
- [ ] 7.7 Verify live reload (step 04) updates both panes in Both mode; `data-line` still present
- [ ] 7.8 Verify narrow window resize collapses neither pane and gutter numbers remain correct
- [ ] 7.9 Verify step 07 acceptance list in full

## 8. Scroll sync — [steps/08-scroll-sync.md](steps/08-scroll-sync.md)

- [ ] 8.1 Implement `sync.js`: find the topmost visible `data-line` element in the rendered pane
- [ ] 8.2 Implement `sync.js` rendered→raw: scroll the raw pane so that line is at/near the top; verify aligning the block at line 120 puts line 120 near the raw pane's top
- [ ] 8.3 Implement `sync.js`: compute the raw pane's topmost visible line number
- [ ] 8.4 Implement `sync.js` raw→rendered: find the rendered element whose `data-line` range contains it, else the nearest preceding one, scroll it into view; verify a top line inside a 50-line fence shows that block aligned to its start
- [ ] 8.5 Implement the module-level `syncing` guard, set before a programmatic scroll
- [ ] 8.6 Clear the `syncing` guard on the next animation frame so the induced scroll event is ignored
- [ ] 8.7 Verify one gesture settles both panes with no oscillation and fast scrolling never makes panes fight
- [ ] 8.8 Attach sync listeners only on Both-mode entry
- [ ] 8.9 Detach sync listeners on Both-mode exit; verify sync is inert in Raw and Rendered mode
- [ ] 8.10 Re-bind listeners and re-align on Both-mode re-entry
- [ ] 8.11 Re-bind after a live reload so sync works against new `data-line` values; verify after an external edit and a file switch
- [ ] 8.12 Verify step 08 acceptance list in full, including no console errors at either scroll extreme

## 9. Copy reference — reference only — [steps/09-copy-reference.md](steps/09-copy-reference.md)

- [ ] 9.1 Implement `reference.py`: `Reference(path_text, lines, content)` dataclass with `to_clipboard_text()`
- [ ] 9.2 Implement `reference.py`: `build_reference(path, lines) -> Reference` using `to_forward_slashes`; verify a single-line selection yields `:12-12`, never `:12`
- [ ] 9.3 Implement `app.py`: `copy_reference(start, end) -> str` bridge method building the `Reference`, writing the clipboard, returning what it wrote
- [ ] 9.4 Verify `copy_reference` by pasting into a text editor
- [ ] 9.5 Implement `copy.js`: raw-pane selection → gutter line numbers mapping
- [ ] 9.6 Implement `copy.js`: rendered-pane selection → nearest `data-line` ancestor walk from anchor and focus
- [ ] 9.7 Implement `copy.js`: union the two endpoint ranges (handles backwards selections); verify a rendered selection from source 30–34 yields `30-34` and a multi-block selection yields the union
- [ ] 9.8 Implement the `Ctrl+C` handler: `preventDefault` + call `copy_reference` only when focus is in the document view and selection is non-empty
- [ ] 9.9 Implement the plain-copy fallback: no `preventDefault` outside the document view or with no selection; verify a text input copies normally and an empty selection leaves the clipboard untouched
- [ ] 9.10 Verify step 09 acceptance list in full, including backwards selections and the no-file-open case

## 10. Copy reference — with content — [steps/10-copy-reference-content.md](steps/10-copy-reference-content.md)

- [ ] 10.1 Implement `reference.py`: `build_reference_with_content(content, lines) -> Reference` slicing raw lines from `FileContent.lines`
- [ ] 10.2 Implement the with-content `to_clipboard_text()` form: reference line, `---`, raw lines, `---`; verify a paste matches the source lines byte-for-byte
- [ ] 10.3 Implement `app.py`: `copy_reference_with_content(start, end) -> str` sharing the clipboard-writing helper with `copy_reference`
- [ ] 10.4 Verify by grep that only one code path writes the clipboard
- [ ] 10.5 Implement `copy.js`: `Ctrl+Shift+C` handler reusing step 09's range-resolution code
- [ ] 10.6 Implement the context menu on the document view offering "Copy Reference" and "Copy Reference with Content"
- [ ] 10.7 Verify each context menu entry matches its shortcut's output
- [ ] 10.8 Implement out-of-range clamping to the last line in reference building
- [ ] 10.9 Verify an over-long range clamps instead of raising
- [ ] 10.10 Verify step 10 acceptance list in full, including `## Title` copying as raw source and blank lines preserved across a multi-block selection

## 11. Shortcuts and shell polish — [steps/11-shortcuts-and-polish.md](steps/11-shortcuts-and-polish.md)

- [ ] 11.1 Implement `app.js`: `Ctrl+1`/`Ctrl+2`/`Ctrl+3` handlers routed through the same code path as the toggle
- [ ] 11.2 Verify each shortcut leaves the UI identical to the equivalent toggle click, including the active indicator
- [ ] 11.3 Suppress shortcuts while focus is in a text input; verify
- [ ] 11.4 Implement the non-blocking copy confirmation (toast) naming which form was copied
- [ ] 11.5 Verify the toast appears for both copy actions and dismisses itself
- [ ] 11.6 Confirm/finish `SessionState`: last-used view mode applies to newly opened files
- [ ] 11.7 Confirm nothing persists across restarts (view mode resets to default)
- [ ] 11.8 Finish the WebView2-missing message (actionable, in-window)
- [ ] 11.9 Finish the unreadable-file message (in-window, no traceback)
- [ ] 11.10 Finish the deleted-open-file message
- [ ] 11.11 Finish the empty-folder message
- [ ] 11.12 Add the first-run empty state in the content area
- [ ] 11.13 Verify step 11 acceptance list in full, including simulating the WebView2-missing path and documenting how it was simulated

## 12. Packaging — [steps/12-packaging.md](steps/12-packaging.md)

- [ ] 12.1 Write the pyinstaller spec file for a single-file windowed build
- [ ] 12.2 Bundle `mdview/assets/` and any highlighting data required by the step-03 choice
- [ ] 12.3 Verify one file in `dist/` runs the app
- [ ] 12.4 Resolve asset paths through `sys._MEIPASS` when frozen, falling back to source-relative paths in dev
- [ ] 12.5 Verify syntax highlighting and all three view modes work in the packaged build
- [ ] 12.6 Write `README.md` build instructions (documented command)
- [ ] 12.7 Write `README.md` run instructions and the WebView2 prerequisite
- [ ] 12.8 Verify the README instructions from a fresh shell exactly as written
- [ ] 12.9 Verify the packaged build end to end: tree, live reload, tree updates, scroll sync
- [ ] 12.10 Verify the packaged build end to end: both copy actions with correct forward-slash paths, `Ctrl+1/2/3`, copy confirmation, no console errors
- [ ] 12.11 Verify the build fails non-zero and names the missing dependency when one is removed
- [ ] 12.12 Confirm no throwaway scripts, fixtures, or test files remain in the working tree
