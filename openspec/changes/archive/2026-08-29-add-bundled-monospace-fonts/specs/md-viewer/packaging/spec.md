## MODIFIED Requirements

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
