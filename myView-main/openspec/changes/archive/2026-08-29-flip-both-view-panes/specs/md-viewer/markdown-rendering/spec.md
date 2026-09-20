## MODIFIED Requirements

### Requirement: View modes
The application SHALL offer exactly three view modes — Raw, Rendered, and Both — switchable from a
visible toggle in the content area, where Both shows the raw pane and the rendered pane
side-by-side over the same file. Rendered prose (headings, paragraphs, lists, blockquotes, tables)
SHALL continue to use a normal sans/serif font, never the bundled monospace stack. While Both mode
is active, the application SHALL show a flip control that swaps which side (left/right) displays
the raw pane and which displays the rendered pane; activating it again SHALL restore the previous
side. The flipped/unflipped state SHALL persist while switching between files and while leaving
and returning to Both mode within the same run, and SHALL NOT be persisted across application
restarts.

#### Scenario: Switching to Both
- **WHEN** the user activates the Both mode toggle
- **THEN** the content area splits, showing raw source on one side and rendered output on the other,
  both reflecting the currently open file

#### Scenario: Toggle reflects current mode
- **WHEN** any view mode is active
- **THEN** the toggle visually indicates which of the three modes is current

#### Scenario: Prose stays on a non-monospace font
- **WHEN** a file is displayed in Rendered or Both mode
- **THEN** headings, paragraphs, lists, and other prose elements render in a sans/serif font, and
  only code blocks within the rendered output use the bundled monospace stack

#### Scenario: Flip control only shown in Both mode
- **WHEN** the view mode is Raw or Rendered
- **THEN** the flip control is not shown

#### Scenario: Flipping pane order
- **WHEN** the user activates the flip control while in Both mode with raw on the left and
  rendered on the right
- **THEN** the layout swaps so rendered is on the left and raw is on the right, and both panes keep
  displaying the currently open file

#### Scenario: Flipping back
- **WHEN** the user activates the flip control again after it has already been flipped
- **THEN** the layout returns to raw on the left and rendered on the right

#### Scenario: Flip state survives a file switch
- **WHEN** the panes are flipped and the user opens a different file from the tree while still in
  Both mode
- **THEN** the new file's raw and rendered content appear in the same flipped order

#### Scenario: Flip state survives leaving and returning to Both mode
- **WHEN** the panes are flipped, the user switches to Raw or Rendered mode, and then switches back
  to Both mode
- **THEN** the panes are still shown in the flipped order

#### Scenario: Flip state resets on restart
- **WHEN** the panes are flipped and the user closes and restarts the application
- **THEN** the next Both mode session starts with raw on the left and rendered on the right
