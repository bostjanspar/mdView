# Spec Delta

## MODIFIED Requirements

### Requirement: Copy is discoverable and confirmed
Both copy actions SHALL be reachable without the keyboard, and the application SHALL confirm to the user that something was copied.

#### Scenario: Context action
- **WHEN** the user opens the context action for a selection in the document view
- **THEN** entries for "Copy", "Copy Reference", and "Copy Reference with Content" are offered

#### Scenario: Plain copy action
- **WHEN** the user selects "Copy" from the context action
- **THEN** the selected raw text without file name and line number is copied to the clipboard and a confirmation is shown

#### Scenario: Confirmation
- **WHEN** a copy action succeeds
- **THEN** a brief visible confirmation of what was copied is shown

#### Scenario: No file open
- **WHEN** a copy action is invoked with no file open
- **THEN** nothing is copied and the action is reported as unavailable
