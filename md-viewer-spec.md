# Markdown Viewer — Spec

## 1. Goal

A standalone Windows desktop app (Python + pywebview) that behaves like Kate's/VS Code's markdown preview, but adds a folder tree, dual raw/rendered view, live-reload, and a "smart select → copy reference" feature aimed at pasting file:line references into Claude Code.

## 2. Tech Stack

| Concern | Choice |
|---|---|
| App shell / window | `pywebview` (uses WebView2 on Windows) |
| File watching | `watchdog` |
| Markdown rendering | `markdown-it-py` + `mdit-py-plugins` (tasklists, footnotes) + `linkify-it-py` |
| Syntax highlighting | Pygments (server-side) or highlight.js (client-side) |
| Frontend | Plain HTML/CSS/JS injected into the webview (no framework needed) |
| Packaging | `pyinstaller` → single .exe |

## 3. Layout

```
┌─────────────────────────────┬───────────────┐
│                              │  📁 project    │
│   RAW  |  RENDERED  | BOTH   │   ▸ docs       │
│  ┌────────────┬───────────┐ │   ▾ notes      │
│  │            │           │ │     - a.md     │
│  │  raw text  │  rendered │ │     - b.md     │
│  │            │           │ │   ▸ archive    │
│  │            │           │ │                │
│  └────────────┴───────────┘ │  (tree filtered│
│                              │   to *.md,     │
│                              │   collapsible) │
└─────────────────────────────┴───────────────┘
```

- Left/main pane: content area, with a view-mode toggle (Raw / Rendered / Both side-by-side).
- Right pane: folder + file tree, scoped to the opened folder, filtered to `.md` files (directories with no md files anywhere below them are hidden or dimmed). Each directory node is collapsible/expandable, state remembered per session.

## 4. Feature Specs

### 4.1 Open folder
- Menu action / button: "Open Folder…" → native folder picker.
- Recursively scan for `.md` files, build tree, render in right pane.
- Non-md files and empty branches are excluded from the tree.
- Directories collapsed by default except the path to the currently open file (if any).

### 4.2 File selection & view modes
- Clicking a `.md` file in the tree loads it into the main pane.
- Three view modes, switchable via toolbar/tabs:
  - **Raw** — plain text, line numbers, monospace.
  - **Rendered** — HTML output of the markdown.
  - **Both** — split pane, raw left / rendered right (or top/bottom), synced scroll optional/stretch goal.
- Last-used view mode persists across file switches (session-level setting).

### 4.3 Live reload
- `watchdog` observer watches the currently open file (and optionally the whole tree, for detecting new/deleted files).
- On modification of the open file: re-read, re-render, update the webview in place without losing scroll position or selection where possible.
- On files added/removed anywhere in the tree: refresh the tree structure.
- Debounce rapid saves (e.g. 150–300ms) to avoid double-refresh from editors that write in two steps.

### 4.4 Smart select → copy reference
Applies in Raw view (and, where feasible, Rendered view mapped back to source lines via line-tracking during render).

- User selects a range of text/lines.
- A context action ("Copy Reference") produces one of two outputs:
  1. **Reference only** (no content):
     `C:\absolute\path\to\file.md:12-18`
  2. **Reference + content** (for direct paste into chat):
     ```
     C:\absolute\path\to\file.md:12-18
     ---
     <raw text of lines 12-18>
     ---
     ```
- Both options copy to clipboard.
- Line numbers always refer to **raw source line numbers**, even if the selection was made in Rendered view.
- Paths always use forward slashes regardless of OS (e.g. `C:/path/to/file.md`) — the consuming AI agent normalizes as needed.
- Single-line selection still uses range form: `path:12-12` (not `path:12`), for consistent parsing downstream.

### 4.5 Keyboard shortcuts
| Shortcut | Action |
|---|---|
| `Ctrl+1` | Switch to Raw view |
| `Ctrl+2` | Switch to Rendered view |
| `Ctrl+3` | Switch to Both (split) view |
| `Ctrl+C` | Copy reference — no content (`path:start-end`) |
| `Ctrl+Shift+C` | Copy reference — with content |

Note: `Ctrl+C` is overloaded — when there's an active selection in Raw/Rendered view, it produces the reference-only string instead of the plain OS copy-selected-text behavior. Needs a fallback: if focus is in a plain text field (not the document view), `Ctrl+C` should behave as normal copy.

### 4.6 Scroll sync (Both mode)
- In "Both" view, scrolling either pane (raw or rendered) scrolls the other to the corresponding position.
- Implementation approach: during render, tag block-level rendered elements with `data-line="start-end"` sourced from markdown-it's `token.map`. On scroll, find the topmost visible rendered element, read its `data-line`, and scroll the raw pane's line-number gutter to match (and vice versa via nearest preceding `data-line` block when scrolling from raw → rendered).
- Sync only needs to be "close enough" (nearest block), not pixel-perfect.

## 5. Non-Goals (for this version)
- Editing markdown (view-only).
- Syncing scroll position with an external editor like Kate (would require Kate to expose cursor position, which it doesn't).
- Multi-window / multi-folder tabs (single folder + single open file at a time).

## 6. Decisions (confirmed)
1. Path format: forward slashes always, regardless of OS.
2. Both-mode scroll sync: yes, required for v1 (see 4.6).
3. File tree live updates: files appearing/disappearing on disk should reflect live in the tree (create/delete watched recursively); full directory-structure changes beyond that are not required for v1.
4. Keyboard shortcuts: see 4.5 above.
5. Single-line reference format: always `path:12-12` (range form, even for one line).

## 7. Suggested Build Order
1. pywebview shell + open single file + raw/rendered toggle.
2. Add live-reload via watchdog (open file content).
3. Add folder tree (right pane) + file selection + live create/delete watching.
4. Add "Both" split view.
5. Add scroll sync for Both view.
6. Add smart-select copy-reference (no content, `Ctrl+C`) → then the with-content variant (`Ctrl+Shift+C`).
7. Wire up `Ctrl+1/2/3` view-mode shortcuts.
8. Package with pyinstaller.
