# markdown-rendering Specification

## Purpose

Defines how markdown source is turned into displayable output, how raw source is presented, and how
the user switches between raw, rendered, and split views of the open file.

## Requirements

### Requirement: Rendered markdown output
The application SHALL render CommonMark markdown to HTML, including tables, task lists, footnotes,
and autolinked bare URLs, and SHALL display the result in the content area.

#### Scenario: Standard markdown constructs
- **WHEN** a file containing headings, lists, tables, blockquotes, and inline code is rendered
- **THEN** each construct appears as its corresponding formatted HTML element

#### Scenario: Task list
- **WHEN** a file contains `- [ ] todo` and `- [x] done`
- **THEN** the rendered output shows checkbox items, the second one checked, and neither is editable

#### Scenario: Bare URL
- **WHEN** a file contains a bare URL such as `https://example.com`
- **THEN** the rendered output shows it as a clickable link

### Requirement: Syntax-highlighted code blocks
The application SHALL syntax-highlight fenced code blocks that declare a supported language, and
SHALL render unlabelled or unknown-language blocks as plain preformatted text without failing.
Rendered code blocks (`<pre>`/`<code>`) SHALL use the bundled monospace font stack `'JetBrains
Mono', 'Cascadia Mono', Consolas, monospace` at 14px with a 1.5 line-height, sourced from fonts
bundled with the application rather than relying on a font installed on the OS.

#### Scenario: Labelled fence
- **WHEN** a fenced block is labelled `python`
- **THEN** its keywords, strings, and comments are visually distinguished

#### Scenario: Unknown language label
- **WHEN** a fenced block is labelled with an unrecognised language
- **THEN** the block renders as plain preformatted text and no error is shown

#### Scenario: Bundled font renders without OS fonts installed
- **WHEN** the machine running the application has neither JetBrains Mono nor Cascadia Mono
  installed as OS fonts
- **THEN** rendered code blocks still visually display in the bundled JetBrains Mono font, not a
  system fallback such as Consolas

### Requirement: Source line mapping
Every block-level element in the rendered output SHALL carry the raw source line range it originated
from, expressed as a start and end line number using 1-based raw source lines.

#### Scenario: Paragraph mapping
- **WHEN** a paragraph occupies raw source lines 12 through 14
- **THEN** its rendered element reports the range 12–14

#### Scenario: Mapping after a re-render
- **WHEN** the file changes on disk and is re-rendered
- **THEN** the reported ranges reflect the new source line numbers

### Requirement: Raw view
The application SHALL provide a Raw view showing the file's exact bytes as text in the bundled
monospace font stack `'JetBrains Mono', 'Cascadia Mono', Consolas, monospace` at 14px with a 1.5
line-height, with a 1-based line-number gutter using the same font stack, without reformatting,
wrapping-away, or altering the content.

#### Scenario: Line numbers match the file
- **WHEN** a 40-line file is opened in Raw view
- **THEN** the gutter shows numbers 1 through 40 and line N displays the file's Nth line

#### Scenario: Raw view is read-only
- **WHEN** the user types into the Raw view
- **THEN** the displayed content does not change and the file on disk is untouched

#### Scenario: Bundled font renders without OS fonts installed
- **WHEN** the machine running the application has neither JetBrains Mono nor Cascadia Mono
  installed as OS fonts
- **THEN** the raw pane and its line-number gutter still visually display in the bundled JetBrains
  Mono font, not a system fallback such as Consolas

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

### Requirement: File reading is robust
The application SHALL read markdown files as UTF-8 and SHALL display a readable message in the
content area, without crashing, when a file cannot be read or decoded.

#### Scenario: Non-UTF-8 bytes
- **WHEN** the open file contains bytes that are not valid UTF-8
- **THEN** the undecodable bytes are replaced with a placeholder character and the rest of the file
  still displays

#### Scenario: File deleted while open
- **WHEN** the open file is deleted from disk
- **THEN** the content area shows a "file no longer available" message and the application keeps running
