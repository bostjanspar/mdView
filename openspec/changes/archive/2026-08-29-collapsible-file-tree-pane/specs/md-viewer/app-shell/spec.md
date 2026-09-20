## MODIFIED Requirements

### Requirement: Session state
The application SHALL hold, for the lifetime of one run, the session root folder, the currently open
file, the current view mode, the expand/collapse state of each tree directory, and whether the
file-tree pane is currently shown or hidden, and SHALL apply that state consistently as the user
switches files or toggles the pane.

#### Scenario: View mode survives a file switch
- **WHEN** the user selects Rendered mode and then opens a different file from the tree
- **THEN** the new file also opens in Rendered mode

#### Scenario: State is not persisted across runs
- **WHEN** the user closes the application and starts it again
- **THEN** no previous folder or file is reopened, the view mode returns to its default, and the
  file-tree pane starts shown

#### Scenario: Toolbar exposes the pane toggle
- **WHEN** the application window is open
- **THEN** the toolbar shows a control that toggles the file-tree pane's visibility, alongside the
  "Open Folder…" action and the view-mode toggle
