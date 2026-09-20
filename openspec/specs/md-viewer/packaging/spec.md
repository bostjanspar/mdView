# packaging Specification

## Purpose

Delivers the viewer as one self-contained Windows executable so it can be run on a machine that has
no Python installation.

## Requirements

### Requirement: Single-file executable
The project SHALL produce a single `.exe` for Windows that starts the viewer with no external Python
interpreter, virtual environment, or source tree present.

#### Scenario: Run on a clean machine
- **WHEN** the built `.exe` is copied to a Windows machine that has no Python installed but does have
  the WebView2 runtime
- **THEN** double-clicking it opens the viewer window

#### Scenario: Only one artifact needs shipping
- **WHEN** the build completes
- **THEN** a single executable file is the only artifact required to run the application

### Requirement: Bundled assets
The executable SHALL include every frontend asset and data file the viewer needs at runtime,
including the bundled JetBrains Mono and Cascadia Mono woff2 font files under `assets/fonts/`, so
no asset is loaded from a path relative to the source tree.

#### Scenario: Full feature set in the packaged build
- **WHEN** a folder is opened in the packaged executable
- **THEN** the tree, all three view modes, syntax highlighting, live reload, scroll sync, and both
  copy-reference actions all behave as they do when run from source

#### Scenario: Bundled fonts available in the packaged build
- **WHEN** the packaged executable runs on a machine with neither JetBrains Mono nor Cascadia Mono
  installed as OS fonts
- **THEN** the raw pane and rendered code blocks still display in the bundled JetBrains Mono font

### Requirement: Reproducible build command
The build SHALL be invocable as a single documented command from a clean checkout, and SHALL fail
loudly rather than emitting a broken executable.

#### Scenario: Documented build
- **WHEN** a developer runs the documented build command in a fresh environment with dependencies
  installed
- **THEN** the executable is produced and its path is reported

#### Scenario: Build failure
- **WHEN** a required dependency is missing
- **THEN** the build exits with a non-zero status and names what is missing

### Requirement: Windowed launch
The packaged executable SHALL launch without opening a console window.

#### Scenario: Launch from Explorer
- **WHEN** the user double-clicks the executable
- **THEN** only the application window appears; no terminal window is shown
