## 1. Dark navy palette

- [x] 1.1 Add `:root` CSS custom properties in `mdview/assets/app.css` for the navy palette
      (`--bg`, `--surface`, `--border`, `--text`, `--text-muted`, `--accent`) and verify the file
      still parses as valid CSS (no build errors when the app loads it).
- [x] 1.2 Replace hardcoded colors on `html/body`, `#toolbar`, `#tree-pane`, `.empty-state`,
      `.raw-view`/`.raw-line-number`, `.rendered-view` (incl. `pre`, `table`, `th`/`td`),
      `.tree-row` (default/hover/selected), `.tree-toggle`, `.context-menu` (incl. `li:hover`,
      `li.disabled`), and `.toast` with the new custom properties, and verify by running the app
      (`python -m mdview`), opening a folder with a markdown file, and visually confirming every
      surface (toolbar, tree, raw view, rendered view, right-click context menu, a toast message)
      renders in the dark navy palette with readable text contrast.

## 2. Rounded Open Folder button

- [x] 2.1 Add a rounded style (`border-radius`, navy-themed background/border/hover state) to
      `#open-folder-btn` in `mdview/assets/app.css` and verify visually that the button has
      rounded corners and matches the new palette in default, hover, and focus states.

## 3. View-mode segmented radio control

- [x] 3.1 Grep `mdview/assets/app.js` for `view-mode-btn`, `data-mode`, and `.active` to identify
      every place the current button-based toggle is read or written, and note each site before
      editing (no file change in this task, just verified findings recorded in the task/PR notes).
- [x] 3.2 Replace the three `<button data-mode="...">` elements in `mdview/assets/index.html`
      with `<input type="radio" name="view-mode" value="...">` + `<label>` pairs for Raw,
      Rendered, and Both inside `#view-mode-toggle`, defaulting Raw to `checked`, and verify the
      page still loads without console errors.
- [x] 3.3 Update `mdview/assets/app.js` to set/read the checked radio input instead of toggling
      the `.active` class on a button, keeping the same public behavior (mode persists per
      session, Ctrl+1/2/3 still switch modes), and verify by running the app and confirming: (a)
      clicking each of Raw/Rendered/Both switches the content view, (b) Ctrl+1/2/3 switch modes,
      (c) opening a different file from the tree keeps the previously selected mode.
- [x] 3.4 Style the radio group in `mdview/assets/app.css` as a pill-shaped horizontal segmented
      control (visually hide the native radio circle, style the `<label>` as a segment, highlight
      the `:checked + label` segment with the accent color, add a visible `:focus-visible` outline
      on the label for keyboard navigation) and verify by tabbing through the control with the
      keyboard and confirming focus is visible and the checked segment is clearly highlighted.

## 4. Final verification

- [x] 4.1 Run the app end-to-end (`python -m mdview`), open a folder, switch between all three
      view modes via mouse and keyboard, open the copy-reference context menu, and trigger a toast,
      confirming the whole window (toolbar, content, tree, context menu, toast) reads as one
      consistent dark navy theme with no leftover light-theme colors.
