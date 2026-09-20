## Purpose

Presents the opened folder as a navigable, markdown-only tree in the right-hand pane so the user can
find and open any `.md` file in the folder without leaving the application.

## ADDED Requirements

### Requirement: Markdown-only tree
The tree SHALL show the session root folder and, beneath it, only directories and `.md` files.
Directories that contain no `.md` file at any depth SHALL be excluded from the tree.

#### Scenario: Non-markdown files hidden
- **WHEN** a folder contains `a.md`, `b.txt`, and `image.png`
- **THEN** the tree shows only `a.md`

#### Scenario: Empty branch excluded
- **WHEN** a subdirectory `assets/` contains only images, at any depth
- **THEN** `assets/` does not appear in the tree

#### Scenario: Deeply nested markdown keeps its ancestors
- **WHEN** the only markdown file is `docs/api/v2/notes.md`
- **THEN** `docs`, `api`, and `v2` all appear in the tree as the path to that file

### Requirement: Deterministic ordering
The tree SHALL list directories before files at each level, each group sorted case-insensitively by
name, so the same folder always produces the same tree layout.

#### Scenario: Mixed entries at one level
- **WHEN** a level contains `Zebra/`, `alpha/`, `b.md`, and `A.md`
- **THEN** the order shown is `alpha/`, `Zebra/`, `A.md`, `b.md`

### Requirement: Collapse and expand
Each directory node SHALL be independently collapsible and expandable, SHALL start collapsed except
for the directories on the path to the currently open file, and SHALL retain its expand state for
the rest of the session including across tree refreshes.

#### Scenario: Default collapsed
- **WHEN** a folder is opened with no file yet open
- **THEN** every directory node is collapsed

#### Scenario: Path to open file is revealed
- **WHEN** a file at `docs/api/notes.md` is the open file
- **THEN** `docs` and `api` are expanded and that file's node is visibly marked as the open file

#### Scenario: Expand state survives a refresh
- **WHEN** the user expands `docs/` and the tree is then refreshed because a file was added elsewhere
- **THEN** `docs/` is still expanded

### Requirement: File selection
Activating a `.md` node in the tree SHALL load that file into the content area as the open file,
using the current view mode, and SHALL replace any previously open file.

#### Scenario: Opening a file
- **WHEN** the user clicks `notes.md` in the tree
- **THEN** `notes.md` becomes the open file, its content is displayed in the current view mode, and
  its node is marked as selected

#### Scenario: Clicking a directory
- **WHEN** the user clicks a directory node
- **THEN** that directory toggles between expanded and collapsed and the open file does not change

### Requirement: Scan is bounded and non-blocking
The recursive scan SHALL skip symbolic-link cycles and SHALL keep the window responsive while
scanning a large folder.

#### Scenario: Symlink loop
- **WHEN** the folder contains a symlink that points to one of its own ancestors
- **THEN** the scan completes without infinite recursion

#### Scenario: Large folder
- **WHEN** a folder containing several thousand files is opened
- **THEN** the window remains responsive and the tree appears once the scan finishes
