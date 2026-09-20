"""Session-scoped application state."""

import enum
from dataclasses import dataclass, field
from pathlib import Path


class ViewMode(enum.StrEnum):
    """The three ways the content area can display the open file."""

    RAW = "raw"
    RENDERED = "rendered"
    BOTH = "both"


@dataclass
class SessionState:
    """In-memory, per-run state. Never persisted across app restarts."""

    root: Path | None = None
    open_file: Path | None = None
    view_mode: ViewMode = ViewMode.RAW
    expanded: set[Path] = field(default_factory=set)

    def set_root(self, root: Path | None) -> None:
        self.root = root

    def set_open_file(self, open_file: Path | None) -> None:
        self.open_file = open_file

    def set_view_mode(self, view_mode: ViewMode) -> None:
        self.view_mode = view_mode

    def toggle_expanded(self, directory: Path) -> None:
        if directory in self.expanded:
            self.expanded.remove(directory)
        else:
            self.expanded.add(directory)
