## Context

See proposal.md - Why/What Changes. The toolbar, content area, tree pane, context menu, and
toast are styled entirely by hardcoded colors in `mdview/assets/app.css` (`#ccc`, `#eee`, `#dde`,
`#f6f6f6`, `#333`, white). The view-mode toggle in `mdview/assets/index.html` is three sibling
`<button>` elements with a shared `view-mode-btn` class; `mdview/assets/app.js` currently tracks
the active mode by toggling an `.active` class on whichever button was clicked and reads the mode
from `data-mode` on click events (exact wiring to confirm in app.js, but the pattern is
click-listener + class toggle, not native form state).

## Goals / Non-Goals

**Goals:**
- One consistent dark navy palette (background, surface, border, text, accent) driven by CSS
  custom properties, applied to every existing surface.
- Convert the view-mode control to real `<input type="radio">` elements (native single-select
  semantics, keyboard-accessible by default) styled as a pill-shaped segmented control.
- Preserve exact current behavior: 3 modes, click-to-switch, Ctrl+1/2/3 shortcuts, per-session
  persistence of last-used mode.

**Non-Goals:**
- No light/dark theme switcher — one theme replaces the other.
- No restructuring of panes, tree, or rendering pipeline.
- No new build tooling (no CSS preprocessor) — plain CSS custom properties are enough for one
  palette.

## Decisions

- **CSS custom properties for the palette**: define `--bg`, `--surface`, `--border`, `--text`,
  `--text-muted`, `--accent` (navy blue, e.g. `#0a1a33` background / `#13294b` surface / `#2f5aa8`
  accent) once at `:root` in app.css and reference them everywhere color is currently hardcoded.
  Alternative considered: leave colors inline per-selector — rejected, it would scatter the same
  six colors across ~15 rules and make future tweaks error-prone.
- **Radio inputs, not ARIA-only buttons, for the view-mode toggle**: replace the three
  `<button data-mode="...">` with `<input type="radio" name="view-mode" value="...">` + `<label>`
  pairs inside the existing `#view-mode-toggle` container (kept as the visual grouping wrapper;
  drop its `role="group"`/`aria-label` in favor of a native `<fieldset>` if that's a clean swap,
  otherwise keep the wrapper attributes for a11y). Visually hide the native radio circle and style
  the `<label>` as the pill segment (`:checked + label` for the active-segment look), so the
  control keeps working with only CSS even if JS fails to attach.
  Alternative considered: keep `<button>` elements and only restyle them to *look* like radio
  buttons — rejected because the user explicitly asked to replace the buttons with radio buttons,
  and native radios give correct semantics/keyboard behavior for free.
- **app.js reads the checked radio instead of an `.active` class**: on `change` of the radio group
  (and still on Ctrl+1/2/3), set `.checked` on the matching input and read `document.querySelector
  ('input[name="view-mode"]:checked').value` wherever the code previously read the `.active`
  button's `data-mode`. This is a one-to-one swap of the existing mode-switching function's
  DOM queries; the persistence/session-state logic that stores the mode string is unchanged.

## Risks / Trade-offs

- [Visually hiding native radio inputs can break keyboard focus rings] → keep the input in the
  layout (not `display:none`) using a visually-hidden technique (0-size + `opacity:0` positioned
  under the label) and add a visible `:focus-visible` outline on the label so keyboard users still
  see focus.
- [Renaming DOM structure could silently break app.js click handlers relying on `button.view-mode-
  btn` selectors] → grep app.js for `view-mode-btn`/`data-mode`/`.active` before editing and update
  every reference in the same change; manually click through all three modes plus Ctrl+1/2/3 after
  the edit.
- [New dark palette could drop contrast below readability for raw/rendered markdown text] →
  pick text/background pairs and spot-check body text, line numbers, code blocks, and table
  borders against the new navy background while implementing.
