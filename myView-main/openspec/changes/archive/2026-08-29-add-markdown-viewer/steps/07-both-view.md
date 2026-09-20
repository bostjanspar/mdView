# Step 07 — Both (split) view

**Previous:** [06](06-tree-live-updates.md) · **Next:** [08 — Scroll sync](08-scroll-sync.md)

**Specs:** `../specs/md-viewer/markdown-rendering/spec.md` (View modes)

## Goal

The third view mode works: raw source and rendered output side-by-side over the same file, each
independently scrollable. No sync yet.

## Scope

- `assets/app.css`, `app.js`: a split layout for `ViewMode.BOTH` — raw pane left, rendered pane right,
  each its own scroll container, with a usable divider. Panes must not collapse to zero width and must
  not force horizontal scrolling of the whole window.
- Mode switching reuses the same raw and rendered renderers from steps 02 and 03; no third rendering
  path.
- The toggle indicates which of the three modes is active.
- Live reload (step 04) updates both panes in Both mode.

Out of scope: scroll sync (step 08), keyboard shortcuts (step 11).

## Task breakdown

- [ ] 7.1 Add split layout CSS for `ViewMode.BOTH`: raw pane left, rendered pane right, each its own scroll container
- [ ] 7.2 Add a usable divider between panes; ensure panes cannot collapse to zero width and the window does not force horizontal scroll
- [ ] 7.3 Wire `app.js` Both mode to reuse the existing raw renderer (no duplication)
- [ ] 7.4 Wire `app.js` Both mode to reuse the existing rendered renderer (no duplication); verify no third rendering path was added
- [ ] 7.5 Make the toggle indicate the active mode across all three modes
- [ ] 7.6 Verify Raw → Rendered → Both → Raw always shows the same file with no blank or duplicated pane
- [ ] 7.7 Verify live reload (step 04) updates both panes in Both mode; `data-line` still present
- [ ] 7.8 Verify narrow window resize collapses neither pane and gutter numbers remain correct
- [ ] 7.9 Verify the Acceptance list below in full

## Notes

- Keep the two panes as separate scroll containers from the start — step 08 attaches listeners to
  exactly these elements.
- Reuse, don't duplicate: if you find yourself writing a second raw renderer for the split layout, stop
  and factor the existing one instead.

## Verification

```bash
python -m mdview        # open a long markdown file and cycle Raw -> Rendered -> Both via the toggle
```

## Acceptance

- [ ] Activating Both splits the content area into a raw pane and a rendered pane, both showing the
      currently open file.
- [ ] Each pane scrolls independently.
- [ ] The toggle visibly indicates the active mode in all three modes.
- [ ] Switching Raw → Rendered → Both → Raw always shows the same file, with no blank pane and no
      duplicated content.
- [ ] Opening a different file from the tree while in Both mode loads it into both panes.
- [ ] Editing the file externally while in Both mode updates both panes (step 04 behaviour still holds).
- [ ] In Both mode, `data-line` attributes are still present on the rendered pane's block elements.
- [ ] The window can be resized narrow without either pane collapsing to zero width and without the
      whole window gaining a horizontal scrollbar.
- [ ] Raw content in Both mode still shows correct 1-based line numbers matching the file.
- [ ] `pyright mdview` reports zero errors.
- [ ] Steps 01–06 acceptance lists still pass.
