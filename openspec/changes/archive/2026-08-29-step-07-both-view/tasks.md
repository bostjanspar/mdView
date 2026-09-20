## 1. Split layout

- [x] 1.1 Add split layout CSS for `ViewMode.BOTH`: raw pane left, rendered pane right, each its
      own scroll container
- [x] 1.2 Add a divider between panes; ensure panes cannot collapse to zero width and the window
      does not force horizontal scroll

## 2. Wire Both mode into app.js

- [x] 2.1 Wire `app.js` Both mode to reuse the existing raw renderer (no duplication)
- [x] 2.2 Wire `app.js` Both mode to reuse the existing rendered renderer (no duplication); verify
      no third rendering path was added
- [x] 2.3 Make the toggle indicate the active mode across all three modes

## 3. Verification

- [x] 3.1 Verify Raw -> Rendered -> Both -> Raw always shows the same file with no blank or
      duplicated pane
- [x] 3.2 Verify live reload (step 04) updates both panes in Both mode; `data-line` still present
- [x] 3.3 Verify narrow window resize collapses neither pane and gutter numbers remain correct
- [x] 3.4 Run `pyright mdview` and confirm zero errors
- [x] 3.5 Hand off to the user to run `python -m mdview`, cycle through all three view modes on a
      real file, resize the window narrow, and confirm every item in the step's Acceptance list
      passes, including that steps 01-06's acceptance lists still pass
