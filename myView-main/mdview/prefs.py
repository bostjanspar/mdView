"""Persisted user preferences (survive app restarts), stored as JSON under %APPDATA%."""

import enum
import json
import os
from pathlib import Path


class FontChoice(enum.StrEnum):
    """The monospace font options exposed by the code-font toggle."""

    JETBRAINS_MONO = "jetbrains-mono"
    CASCADIA_MONO = "cascadia-mono"
    SYSTEM_MONO = "system-mono"


_DEFAULT_FONT_CHOICE = FontChoice.JETBRAINS_MONO


def _prefs_path() -> Path:
    base = os.environ.get("APPDATA") or str(Path.home())
    return Path(base) / "mdview" / "prefs.json"


def load_font_choice() -> FontChoice:
    """Read the persisted font choice, falling back to the default on any error."""
    try:
        data = json.loads(_prefs_path().read_text(encoding="utf-8"))
        return FontChoice(data["font"])
    except (OSError, ValueError, KeyError, json.JSONDecodeError):
        return _DEFAULT_FONT_CHOICE


def save_font_choice(choice: FontChoice) -> None:
    """Persist `choice` so it survives the next app restart."""
    path = _prefs_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"font": choice.value}), encoding="utf-8")
