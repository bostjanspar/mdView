## MODIFIED Requirements

### Requirement: File selection
Activating a `.md` node in the tree SHALL load that file into the content area as the open file,
using the current view mode, and SHALL replace any previously open file. Tree row labels SHALL be
rendered at a font size no larger than the toolbar's control labels, and each row's toggle
indicator and name SHALL remain flush with the pane's left edge at every nesting depth, with only
indentation distinguishing depth.

#### Scenario: Opening a file
- **WHEN** the user clicks `notes.md` in the tree
- **THEN** `notes.md` becomes the open file, its content is displayed in the current view mode, and
  its node is marked as selected

#### Scenario: Clicking a directory
- **WHEN** the user clicks a directory node
- **THEN** that directory toggles between expanded and collapsed and the open file does not change

#### Scenario: Row text size and alignment
- **WHEN** the tree pane is showing a nested folder with files at multiple depths
- **THEN** every row's label text renders at the same reduced size (matching or smaller than the
  toolbar view-mode labels) and every row's toggle/name group starts at the same left position for
  its depth, without centering or being pushed off the visible edge

## ADDED Requirements

### Requirement: Pane visibility toggle
The entire file-tree pane SHALL be hideable and re-showable for the rest of the session via a
toolbar control, independent of any individual directory's expand/collapse state. Hiding the pane
SHALL free its width for the content area; showing it again SHALL restore the pane at its previous
width and expand/collapse state.

#### Scenario: Hiding the pane
- **WHEN** the user activates the tree-pane visibility toggle while the pane is shown
- **THEN** the tree pane is hidden and the content area expands to occupy the freed width

#### Scenario: Showing the pane again
- **WHEN** the user activates the tree-pane visibility toggle while the pane is hidden
- **THEN** the tree pane reappears with the same directory expand/collapse state and open-file
  selection it had before it was hidden

#### Scenario: Hiding does not affect the open file
- **WHEN** the tree pane is hidden while a file is open
- **THEN** the open file remains displayed in the content area, unaffected by the pane's visibility
