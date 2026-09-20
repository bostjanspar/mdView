## Purpose

Provides the desktop application window, the folder-opening entry point, and the session-scoped
state that every other markdown-viewer capability reads and writes.

## ADDED Requirements

### Requirement: Application window
The application SHALL launch as a single standalone desktop window on Windows, with a content area
on the left and a file-tree pane on the right, and SHALL exit cleanly when the window is closed.

#### Scenario: Launching the app
- **WHEN** the user starts the application
- **THEN** a single window opens showing an empty content area, an empty tree pane, and a view-mode
  toggle offering Raw, Rendered, and Both

#### Scenario: Closing the app
- **WHEN** the user closes the window
- **THEN** all background watchers stop and the process exits with status 0 within 2 seconds

### Requirement: Open folder
The application SHALL expose an "Open Folder…" action that presents the native OS folder picker and
scopes the session to the chosen folder.

#### Scenario: Folder chosen
- **WHEN** the user picks a folder in the native picker
- **THEN** the tree pane is populated from that folder and the folder becomes the session root

#### Scenario: Picker cancelled
- **WHEN** the user cancels the native picker
- **THEN** the current session root, tree, and open file are left unchanged

#### Scenario: Folder with no markdown files
- **WHEN** the user picks a folder containing no `.md` files at any depth
- **THEN** the tree pane shows an explicit empty-state message rather than an empty pane or an error

### Requirement: Session state
The application SHALL hold, for the lifetime of one run, the session root folder, the currently open
file, the current view mode, and the expand/collapse state of each tree directory, and SHALL apply
that state consistently as the user switches files.

#### Scenario: View mode survives a file switch
- **WHEN** the user selects Rendered mode and then opens a different file from the tree
- **THEN** the new file also opens in Rendered mode

#### Scenario: State is not persisted across runs
- **WHEN** the user closes the application and starts it again
- **THEN** no previous folder or file is reopened and the view mode returns to its default

### Requirement: Startup errors are surfaced
The application SHALL report an actionable message in the window when a required platform component
is missing, rather than failing silently or crashing without explanation.

#### Scenario: WebView2 runtime missing
- **WHEN** the application starts on a machine without the WebView2 runtime
- **THEN** the user is shown a message naming the missing runtime and how to install it
