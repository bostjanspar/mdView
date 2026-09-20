"""Path formatting and classification helpers shared across mdview."""

from pathlib import Path

_MARKDOWN_SUFFIX = ".md"


def to_forward_slashes(path: Path) -> str:
    """Return the absolute, forward-slash form of `path`.

    This is the single place display-path formatting happens; other modules must not
    build their own display path.
    """
    return path.resolve().as_posix()


def is_markdown(path: Path) -> bool:
    """Return whether `path` has a `.md` suffix, case-insensitively."""
    return path.suffix.lower() == _MARKDOWN_SUFFIX
