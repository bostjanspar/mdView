# Implementation Steps — Overview

Twelve step packages, each small enough to finish in one sitting and each ending in a state you can
observe by running a command. **Implement them in the order listed.** Every step file ends in an
**Acceptance** checklist; every box must be checked before the next step is started. Steps are not
mergeable out of order — each one assumes the acceptance list of all previous steps still holds.

Reference material:

- Behaviour contracts: `../specs/md-viewer/**/spec.md`
- Technical approach and decisions (D1–D7): `../design.md`
- Motivation and scope: `../proposal.md`

## Order

Each row also maps to a phase in `md-viewer-spec.md` §7 "Suggested Build Order" (spec phases 1–8),
so the two documents can be cross-checked against each other.

| # | Done | Step | Spec §7 phase | Capabilities advanced | Verified by |
|---|---|---|---|---|---|
| 01 | [x] | [Project scaffold and dependencies](01-project-scaffold.md) | — (prerequisite) | — | `python -m mdview --version`, pyright clean |
| 02 | [x] | [App shell, open folder, raw view](02-app-shell-raw-view.md) | 1. pywebview shell + open file + raw/rendered toggle | app-shell, markdown-rendering (raw) | Launch app, open folder, read a file |
| 03 | [x] | [Markdown rendering and the Rendered view](03-markdown-rendering.md) | 1. pywebview shell + open file + raw/rendered toggle | markdown-rendering | Rendered pane with `data-line` attributes |
| 04 | [x] | [Live reload of the open file](04-live-reload-open-file.md) | 2. Live-reload via watchdog (open file content) | live-reload | Edit file externally, view updates |
| 05 | [x] | [Folder tree and file selection](05-folder-tree.md) | 3. Folder tree + file selection + live create/delete watching | file-tree | Tree pane, click to open |
| 06 | [x] | [Live tree updates on create/delete](06-tree-live-updates.md) | 3. Folder tree + file selection + live create/delete watching | live-reload, file-tree | Create/delete `.md`, tree follows |
| 07 | [x] | [Both (split) view](07-both-view.md) | 4. "Both" split view | markdown-rendering | Side-by-side raw + rendered |
| 08 | [x] | [Scroll sync in Both view](08-scroll-sync.md) | 5. Scroll sync for Both view | scroll-sync | Scroll either pane, other follows |
| 09 | [x] | [Copy reference — reference only](09-copy-reference.md) | 6. Smart-select copy-reference (no content, `Ctrl+C`) | copy-reference | `Ctrl+C` yields `path:12-18` |
| 10 | [x] | [Copy reference — with content](10-copy-reference-content.md) | 6. Smart-select copy-reference (with-content variant) | copy-reference | `Ctrl+Shift+C` yields reference + fenced lines |
| 11 | [x] | [View-mode shortcuts and shell polish](11-shortcuts-and-polish.md) | 7. Wire up `Ctrl+1/2/3` view-mode shortcuts | app-shell, copy-reference | `Ctrl+1/2/3`, toast, error states |
| 12 | [x] | [Package as a single .exe](12-packaging.md) | 8. Package with pyinstaller | packaging | Built `.exe` runs the full feature set |

## Rules that apply to every step

- Follow the Google Python Style Guide.
- No nested function or method definitions — extract to a module-level `_private` function instead.
- No complicated return types — anything with more than one meaningful field is a `@dataclass`.
- Type-annotate public functions and dataclass fields; `pyright` must be clean at the end of each step.
- Write no permanent tests. A throwaway script to verify a step is fine — delete it before the step is
  marked done. Verification is by runnable command with observable output.
- If a step's acceptance list cannot be completed, stop and resolve it rather than moving on.
