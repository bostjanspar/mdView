# live-reload Specification

## Purpose

Keeps the displayed content and the file tree in step with the filesystem so the user never has to
manually refresh after editing markdown in another program.

## Requirements

### Requirement: Open file reloads on change
When the open file is modified on disk, the application SHALL re-read and re-display it
automatically, with no user action required.

#### Scenario: External edit
- **WHEN** the open file is saved from an external editor
- **THEN** the content area shows the new content within 1 second

#### Scenario: Rendered view updates too
- **WHEN** the open file changes while Rendered or Both mode is active
- **THEN** the rendered output is regenerated from the new source, including its source line ranges

### Requirement: Reload preserves reading position
A reload triggered by a file change SHALL preserve the user's scroll position in each visible pane
where the corresponding source location still exists.

#### Scenario: Edit below the viewport
- **WHEN** the user is scrolled to the middle of a long file and a line is appended at the end
- **THEN** the viewport still shows the same region after the reload

#### Scenario: File becomes shorter than the scroll position
- **WHEN** the file is truncated so the previously visible region no longer exists
- **THEN** the view scrolls to the closest still-existing position rather than erroring

### Requirement: Rapid saves are debounced
The application SHALL coalesce filesystem change events that arrive within a short window into a
single reload, so editors that write a file in multiple steps do not cause repeated or flickering
refreshes.

#### Scenario: Two-step editor save
- **WHEN** an editor writes the open file twice within 100 ms
- **THEN** exactly one reload occurs

#### Scenario: Distinct saves
- **WHEN** two saves occur one second apart
- **THEN** two reloads occur, one per save

### Requirement: Tree reflects created and deleted files
The application SHALL update the tree automatically when `.md` files are created or deleted anywhere
under the session root, including in newly created subdirectories.

#### Scenario: File created
- **WHEN** a new `.md` file is created in a watched subdirectory
- **THEN** it appears in the tree without the user reopening the folder

#### Scenario: File deleted
- **WHEN** a `.md` file is deleted
- **THEN** its node disappears from the tree, and any directory that thereby contains no markdown at
  any depth also disappears

#### Scenario: Non-markdown file created
- **WHEN** a `.txt` file is created under the session root
- **THEN** the tree does not change

### Requirement: Watching stops with its scope
The application SHALL stop watching a folder when a different folder is opened or the window is
closed, leaving no watcher threads running.

#### Scenario: Switching folders
- **WHEN** the user opens a second folder
- **THEN** changes in the first folder no longer trigger any update

#### Scenario: Shutdown
- **WHEN** the window is closed
- **THEN** all watcher threads terminate and the process exits
