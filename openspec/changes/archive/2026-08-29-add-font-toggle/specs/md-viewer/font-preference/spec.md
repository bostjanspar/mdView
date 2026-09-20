## Purpose

Lets the user choose the monospace font used for code/raw markdown content at runtime, and remembers that choice across app restarts, independent of the app's normal in-memory-only session state.

## ADDED Requirements

### Requirement: Font toggle in the toolbar
The application SHALL show a toolbar control offering JetBrains Mono, Cascadia Mono, and System monospace as the font for code/raw markdown content, alongside the existing view-mode toggle.

#### Scenario: Toggle visible on launch
- **WHEN** the application window is open
- **THEN** the toolbar shows a three-way font control with JetBrains Mono, Cascadia Mono, and System options, one of which is marked selected

### Requirement: Font choice applies to code content only
Selecting a font in the toggle SHALL immediately change the font used for the raw view, raw line numbers, and rendered code blocks, and SHALL NOT change the font used for the toolbar or file-tree pane.

#### Scenario: Switching font updates code content
- **WHEN** the user selects Cascadia Mono in the font toggle
- **THEN** the raw view, raw line numbers, and any rendered code blocks immediately render in Cascadia Mono

#### Scenario: Toolbar chrome is unaffected
- **WHEN** the user selects any font in the font toggle
- **THEN** the toolbar and file-tree pane text remain in the application's normal UI font

### Requirement: Font choice persists across restarts
The application SHALL remember the user's font choice and apply it automatically the next time the application starts, without requiring the user to reselect it or reopen a file.

#### Scenario: Choice survives a restart
- **WHEN** the user selects a font, then fully closes and restarts the application
- **THEN** the font toggle shows that same font selected, and any code content opened afterward renders in that font

#### Scenario: No prior choice
- **WHEN** the application starts for the first time, with no font previously chosen
- **THEN** JetBrains Mono is selected and applied by default

#### Scenario: Corrupt stored preference
- **WHEN** the application starts and the stored font preference is missing, unreadable, or names an unknown font
- **THEN** the application starts normally with JetBrains Mono selected and applied, rather than failing to start
