## Purpose

Keeps the raw and rendered panes showing the same part of the document in Both mode so the user can
read source and output together without manually aligning them.

## ADDED Requirements

### Requirement: Bidirectional scroll sync
In Both mode, scrolling either pane SHALL scroll the other pane to the corresponding location in the
document, in both directions.

#### Scenario: Rendered drives raw
- **WHEN** the user scrolls the rendered pane so that the block starting at source line 120 is at the
  top of its viewport
- **THEN** the raw pane scrolls so that line 120 is at or near the top of its viewport

#### Scenario: Raw drives rendered
- **WHEN** the user scrolls the raw pane so that line 120 is at the top of its viewport
- **THEN** the rendered pane scrolls to the rendered block whose source range contains or most
  closely precedes line 120

### Requirement: Nearest-block accuracy
Alignment SHALL be to the nearest block-level boundary; pixel-exact or line-exact alignment is not
required. The synced pane MUST NOT be off by more than one block from the driving pane's topmost
visible block.

#### Scenario: Line inside a long code block
- **WHEN** the raw pane's top visible line falls in the middle of a 50-line fenced code block
- **THEN** the rendered pane shows that code block, aligned to the block's start

### Requirement: No feedback loop
Sync SHALL NOT cause the panes to oscillate, jitter, or scroll continuously; a programmatic scroll of
one pane MUST NOT be treated as user input that scrolls the other back.

#### Scenario: Single scroll gesture
- **WHEN** the user performs one scroll gesture in the rendered pane
- **THEN** each pane settles at one final position and neither keeps moving afterwards

### Requirement: Sync is scoped to Both mode
Scroll sync SHALL be active only in Both mode and SHALL have no effect in Raw or Rendered mode.

#### Scenario: Raw mode
- **WHEN** the user scrolls in Raw mode
- **THEN** no sync work is performed and behaviour is that of a normal scrollable document

#### Scenario: Re-entering Both mode
- **WHEN** the user switches away from Both mode and back
- **THEN** sync resumes and the panes are aligned to each other again

### Requirement: Sync survives a reload
After a live reload of the open file, scroll sync SHALL continue to work against the newly rendered
content without requiring a mode switch.

#### Scenario: Edit then scroll
- **WHEN** the open file is edited externally in Both mode and the user then scrolls either pane
- **THEN** the other pane follows using the updated source line ranges
