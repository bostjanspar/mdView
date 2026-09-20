"""Building clipboard-ready file:line references from a selection."""

from dataclasses import dataclass
from pathlib import Path

from mdview.files import FileContent
from mdview.paths import to_forward_slashes
from mdview.rendering import LineRange


@dataclass
class Reference:
    """A clipboard-ready reference, optionally carrying the selected raw source lines."""

    path_text: str
    lines: LineRange
    content: str | None

    def to_clipboard_text(self) -> str:
        reference_line = f"{self.path_text}:{self.lines.start}-{self.lines.end}"
        if self.content is None:
            return reference_line
        return f"{reference_line}\n---\n{self.content}\n---"


def build_reference(path: Path, lines: LineRange) -> Reference:
    """Build a reference-only `Reference` for `lines` of `path` (no attached content)."""
    return Reference(path_text=to_forward_slashes(path), lines=lines, content=None)


def build_reference_with_content(file_content: FileContent, lines: LineRange) -> Reference:
    """Build a `Reference` carrying the exact raw source lines, clamped to the file's last line."""
    end = min(lines.end, len(file_content.lines))
    clamped_lines = LineRange(start=lines.start, end=end)
    content = "\n".join(file_content.lines[lines.start - 1 : end])
    return Reference(
        path_text=to_forward_slashes(file_content.path),
        lines=clamped_lines,
        content=content,
    )
