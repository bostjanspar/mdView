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

| # | Step | Capabilities advanced | Verified by |
|---|---|---|---|
| 01 | [Project scaffold and dependencies](01-project-scaffold.md) | — | `python -m mdview --version`, pyright clean |
| 02 | [App shell, open folder, raw view](02-app-shell-raw-view.md) | app-shell, markdown-rendering (raw) | Launch app, open folder, read a file |
| 03 | [Markdown rendering and the Rendered view](03-markdown-rendering.md) | markdown-rendering | Rendered pane with `data-line` attributes |
| 04 | [Live reload of the open file](04-live-reload-open-file.md) | live-reload | Edit file externally, view updates |
| 05 | [Folder tree and file selection](05-folder-tree.md) | file-tree | Tree pane, click to open |
| 06 | [Live tree updates on create/delete](06-tree-live-updates.md) | live-reload, file-tree | Create/delete `.md`, tree follows |
| 07 | [Both (split) view](07-both-view.md) | markdown-rendering | Side-by-side raw + rendered |
| 08 | [Scroll sync in Both view](08-scroll-sync.md) | scroll-sync | Scroll either pane, other follows |
| 09 | [Copy reference — reference only](09-copy-reference.md) | copy-reference | `Ctrl+C` yields `path:12-18` |
| 10 | [Copy reference — with content](10-copy-reference-content.md) | copy-reference | `Ctrl+Shift+C` yields reference + fenced lines |
| 11 | [View-mode shortcuts and shell polish](11-shortcuts-and-polish.md) | app-shell, copy-reference | `Ctrl+1/2/3`, toast, error states |
| 12 | [Package as a single .exe](12-packaging.md) | packaging | Built `.exe` runs the full feature set |

## Rules that apply to every step

- Follow the Google Python Style Guide.
- No nested function or method definitions — extract to a module-level `_private` function instead.
- No complicated return types — anything with more than one meaningful field is a `@dataclass`.
- Type-annotate public functions and dataclass fields; `pyright` must be clean at the end of each step.
- Write no permanent tests. A throwaway script to verify a step is fine — delete it before the step is
  marked done. Verification is by runnable command with observable output.
- If a step's acceptance list cannot be completed, stop and resolve it rather than moving on.
