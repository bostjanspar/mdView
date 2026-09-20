"""File reading."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileContent:
    """The decoded contents of a file read from disk."""

    path: Path
    text: str
    lines: list[str]
    had_decode_errors: bool


def read_text_lossy(path: Path) -> FileContent:
    """Read `path` as UTF-8, replacing undecodable bytes rather than raising."""
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    had_decode_errors = "�" in text
    return FileContent(
        path=path,
        text=text,
        lines=text.splitlines(),
        had_decode_errors=had_decode_errors,
    )
