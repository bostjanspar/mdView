## 1. Markup and styling

- [x] 1.1 Add a "Flip panes" button to `mdview/assets/index.html` inside `#content-area` (or the
      toolbar), and verify it exists in the DOM by opening the app and inspecting the element.
- [x] 1.2 In `mdview/assets/app.css`, add a `flipped` modifier class (e.g. `#content-area.both-mode.flipped`)
      that reorders `.raw-view` and `.rendered-view` visually via `order` without changing their DOM
      order or ids, and verify raw/rendered swap sides visually when the class is toggled in
      devtools.

## 2. Behavior

- [x] 2.1 In `mdview/assets/app.js`, add a `panesFlipped` state variable (default `false`), wire the
      flip button's click handler to toggle it and update `#content-area`'s `flipped` class, and
      verify clicking the button swaps the panes and clicking again restores the original order.
- [x] 2.2 Show the flip button only while `currentMode === "both"` (hide/disable it otherwise), and
      verify it disappears when switching to Raw or Rendered mode.
- [x] 2.3 Ensure `panesFlipped` persists across file switches and across leaving/returning to Both
      mode within the same run (i.e. it is not reset by `showView()` or file-open logic), and verify
      by flipping panes, opening a different file, and switching Raw → Both, confirming the flip
      state is unchanged in both cases.
- [x] 2.4 Verify `panesFlipped` resets to `false` on a fresh app launch (no persistence to disk), by
      restarting the app and confirming Both mode opens unflipped.

## 3. Regression check

- [x] 3.1 Manually verify scroll-sync (`mdview/assets/sync.js`) and line-mapping still work correctly
      in both the flipped and unflipped layouts, since panes are reordered via CSS `order` and not
      DOM position.
