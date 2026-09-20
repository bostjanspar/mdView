# copy-reference Specification

## Purpose

Turns a text selection in the viewer into a clipboard-ready `path:start-end` reference — optionally
with the selected source lines attached — so it can be pasted straight into an AI coding agent.

## Requirements

### Requirement: Reference format
A copied reference SHALL be a single line of the form `<path>:<start>-<end>` where `<path>` is the
absolute path of the open file with all separators written as forward slashes, and `<start>` and
`<end>` are 1-based raw source line numbers.

#### Scenario: Windows path
- **WHEN** the open file is at `C:\projects\docs\notes.md` and lines 12 through 18 are selected
- **THEN** the clipboard contains `C:/projects/docs/notes.md:12-18`

#### Scenario: Single line uses range form
- **WHEN** the selection lies entirely within source line 12
- **THEN** the clipboard contains `C:/projects/docs/notes.md:12-12`, never `...notes.md:12`

### Requirement: Reference with content
The application SHALL offer a second copy form that appends the selected raw source lines to the
reference, delimited by a `---` line before and after the content.

#### Scenario: Copy with content
- **WHEN** the user invokes copy-with-content for lines 12–13
- **THEN** the clipboard contains the reference line, then `---`, then the exact raw text of lines 12
  and 13, then `---`

#### Scenario: Content is raw, not rendered
- **WHEN** the selection was made in the rendered pane over a heading written as `## Title`
- **THEN** the copied content is `## Title`, not `Title`

### Requirement: Line numbers always come from raw source
Reported line numbers SHALL always be raw source line numbers of the open file, regardless of which
pane the selection was made in.

#### Scenario: Selection in the rendered pane
- **WHEN** the user selects rendered text that originates from source lines 30–34
- **THEN** the copied reference reports `30-34`

#### Scenario: Selection spanning several rendered blocks
- **WHEN** the selection starts in a block mapped to lines 10–12 and ends in a block mapped to lines
  20–22
- **THEN** the copied reference reports `10-22`

### Requirement: Keyboard shortcuts
The application SHALL bind `Ctrl+1`, `Ctrl+2`, and `Ctrl+3` to the Raw, Rendered, and Both view
modes, `Ctrl+C` to copy reference without content, and `Ctrl+Shift+C` to copy reference with content.

#### Scenario: View mode shortcuts
- **WHEN** the user presses `Ctrl+3`
- **THEN** the view switches to Both mode, identically to using the toggle

#### Scenario: Copy shortcuts
- **WHEN** text is selected in the document view and the user presses `Ctrl+C`
- **THEN** the reference-only string is placed on the clipboard instead of the selected text

### Requirement: Plain-copy fallback
`Ctrl+C` SHALL perform the ordinary copy-selected-text action whenever the focus is not in the
document view, or when there is no selection in the document view.

#### Scenario: Focus in a plain text field
- **WHEN** the focus is in a text input such as a filter box and the user presses `Ctrl+C`
- **THEN** the selected text of that field is copied and no reference is produced

#### Scenario: No selection
- **WHEN** the document view has focus but nothing is selected and the user presses `Ctrl+C`
- **THEN** nothing is written to the clipboard and no reference is produced

### Requirement: Copy is discoverable and confirmed
Both copy actions SHALL be reachable without the keyboard, and the application SHALL confirm to the
user that something was copied.

#### Scenario: Context action
- **WHEN** the user opens the context action for a selection in the document view
- **THEN** entries for "Copy Reference" and "Copy Reference with Content" are offered

#### Scenario: Confirmation
- **WHEN** a copy action succeeds
- **THEN** a brief visible confirmation of what was copied is shown

#### Scenario: No file open
- **WHEN** a copy action is invoked with no file open
- **THEN** nothing is copied and the action is reported as unavailable
