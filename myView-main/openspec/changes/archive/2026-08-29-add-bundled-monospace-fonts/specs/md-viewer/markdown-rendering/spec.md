## MODIFIED Requirements

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
SHALL continue to use a normal sans/serif font, never the bundled monospace stack.

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
