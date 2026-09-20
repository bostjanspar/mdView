"""Bridge exposed to the webview frontend as `window.pywebview.api`."""

import ctypes
import json
import threading
import time
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

import webview

from mdview.files import FileContent, read_text_lossy
from mdview.paths import to_forward_slashes
from mdview.prefs import FontChoice, load_font_choice, save_font_choice
from mdview.reference import build_reference, build_reference_with_content
from mdview.rendering import LineRange, render_markdown
from mdview.session import SessionState, ViewMode
from mdview.tree import TreeNode, scan_folder
from mdview.watching import (
    ContentChanged,
    Debouncer,
    FileDeleted,
    FolderWatcher,
    MarkdownTreeChanged,
    TreeReady,
)

_WATCH_POLL_INTERVAL_SECONDS = 0.05

_CF_UNICODETEXT = 13
_GMEM_MOVEABLE = 0x0002


def _set_clipboard_text(text: str) -> None:
    """Write `text` to the Windows clipboard as Unicode text, via the Win32 API."""
    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32
    kernel32.GlobalAlloc.restype = ctypes.c_void_p
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    user32.SetClipboardData.argtypes = [ctypes.c_uint, ctypes.c_void_p]

    encoded = text.encode("utf-16-le") + b"\x00\x00"
    handle = kernel32.GlobalAlloc(_GMEM_MOVEABLE, len(encoded))
    pointer = kernel32.GlobalLock(handle)
    ctypes.memmove(pointer, encoded, len(encoded))
    kernel32.GlobalUnlock(handle)
    user32.OpenClipboard(0)
    user32.EmptyClipboard()
    user32.SetClipboardData(_CF_UNICODETEXT, handle)
    user32.CloseClipboard()


@dataclass
class SessionPayload:
    """JS-visible view of `SessionState`."""

    root: str | None
    open_file: str | None
    view_mode: str

    def to_payload(self) -> dict[str, str | None]:
        return {
            "root": self.root,
            "open_file": self.open_file,
            "view_mode": self.view_mode,
        }


@dataclass
class FileContentPayload:
    """JS-visible view of `FileContent`."""

    path: str
    lines: list[str] = field(default_factory=list)
    had_decode_errors: bool = False
    rendered_html: str = ""
    expanded: list[str] = field(default_factory=list)
    error: str | None = None

    def to_payload(self) -> dict[str, object]:
        return {
            "path": self.path,
            "lines": self.lines,
            "had_decode_errors": self.had_decode_errors,
            "rendered_html": self.rendered_html,
            "expanded": self.expanded,
            "error": self.error,
        }


def _selected_path(result: Sequence[str] | str) -> Path:
    if isinstance(result, str):
        return Path(result)
    return Path(result[0])


def _session_payload(state: SessionState) -> dict[str, str | None]:
    payload = SessionPayload(
        root=to_forward_slashes(state.root) if state.root else None,
        open_file=to_forward_slashes(state.open_file) if state.open_file else None,
        view_mode=state.view_mode.value,
    )
    return payload.to_payload()


def _file_content_payload(file_content: FileContent) -> FileContentPayload:
    rendered = render_markdown(file_content)
    return FileContentPayload(
        path=to_forward_slashes(file_content.path),
        lines=file_content.lines,
        had_decode_errors=file_content.had_decode_errors,
        rendered_html=rendered.html,
    )


def _error_payload(path: Path, message: str) -> FileContentPayload:
    return FileContentPayload(path=to_forward_slashes(path), error=message)


def _tree_payload(node: TreeNode) -> dict[str, object]:
    return {
        "name": node.name,
        "path": to_forward_slashes(node.path),
        "is_dir": node.is_dir,
        "children": [_tree_payload(child) for child in node.children],
    }


def _ancestors_within_root(path: Path, root: Path) -> list[Path]:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return []
    ancestors: list[Path] = []
    current = root
    for part in relative.parts[:-1]:
        current = current / part
        ancestors.append(current)
    return ancestors


class App:
    """The `js_api` object bound into the webview window."""

    def __init__(self) -> None:
        self._window: webview.Window | None = None
        self._state = SessionState()
        self._watcher = FolderWatcher()
        self._content_debouncer = Debouncer()
        self._tree_debouncer = Debouncer()
        self._stop_event = threading.Event()
        self._font_choice: FontChoice = load_font_choice()

    def bind_window(self, window: webview.Window) -> None:
        self._window = window

    def start_watch_loop(self) -> None:
        """Run on a dedicated thread (see `__main__.py`); drains watch events until `shutdown()`."""
        while not self._stop_event.is_set():
            time.sleep(_WATCH_POLL_INTERVAL_SECONDS)
            self._drain_watch_events()

    def shutdown(self) -> None:
        self._stop_event.set()
        self._content_debouncer.cancel()
        self._tree_debouncer.cancel()
        self._watcher.stop()

    def open_folder(self) -> dict[str, str | None]:
        window = self._window
        if window is None:
            return _session_payload(self._state)
        result = window.create_file_dialog(webview.FileDialog.FOLDER)
        if result:
            root = _selected_path(result).resolve()
            self._state.set_root(root)
            self._state.set_open_file(None)
            self._state.expanded.clear()
            self._watcher.start(root, lambda: self._state.open_file)
            self._start_tree_scan(root)
        return _session_payload(self._state)

    def _start_tree_scan(self, root: Path) -> None:
        thread = threading.Thread(target=self._scan_and_enqueue, args=(root,), daemon=True)
        thread.start()

    def _scan_and_enqueue(self, root: Path) -> None:
        tree = scan_folder(root)
        self._watcher.events.put(TreeReady(root=root, tree=tree))

    def load_file(self, path: str) -> dict[str, object]:
        file_path = Path(path).resolve()
        try:
            file_content = read_text_lossy(file_path)
        except OSError as exc:
            return _error_payload(file_path, f"Cannot read file: {exc.strerror or exc}").to_payload()
        self._state.set_open_file(file_content.path)
        self._content_debouncer.cancel()
        root = self._state.root
        if root is not None:
            self._state.expanded.update(_ancestors_within_root(file_content.path, root))
        payload = _file_content_payload(file_content)
        payload.expanded = [to_forward_slashes(p) for p in self._state.expanded]
        return payload.to_payload()

    def toggle_fullscreen(self) -> None:
        window = self._window
        if window is not None:
            window.toggle_fullscreen()

    def set_view_mode(self, mode: str) -> dict[str, str | None]:
        self._state.set_view_mode(ViewMode(mode))
        return _session_payload(self._state)

    def get_font(self) -> str:
        return self._font_choice.value

    def set_font(self, font: str) -> str:
        self._font_choice = FontChoice(font)
        save_font_choice(self._font_choice)
        return self._font_choice.value

    def toggle_expanded(self, path: str) -> None:
        self._state.toggle_expanded(Path(path).resolve())

    def copy_reference(self, start: int, end: int) -> str:
        open_file = self._state.open_file
        if open_file is None:
            return ""
        lines = LineRange(start=min(start, end), end=max(start, end))
        reference = build_reference(open_file, lines)
        text = reference.to_clipboard_text()
        _set_clipboard_text(text)
        return text

    def copy_reference_with_content(self, start: int, end: int) -> str:
        open_file = self._state.open_file
        if open_file is None:
            return ""
        lines = LineRange(start=min(start, end), end=max(start, end))
        file_content = read_text_lossy(open_file)
        reference = build_reference_with_content(file_content, lines)
        text = reference.to_clipboard_text()
        _set_clipboard_text(text)
        return text

    def _drain_watch_events(self) -> None:
        for event in self._watcher.drain():
            if isinstance(event, ContentChanged):
                self._content_debouncer.schedule(self._reload_open_file)
            elif isinstance(event, FileDeleted):
                self._content_debouncer.cancel()
                self._show_file_deleted()
            elif isinstance(event, MarkdownTreeChanged):
                self._tree_debouncer.schedule(self._refresh_tree)
            elif isinstance(event, TreeReady):
                if event.root == self._state.root:
                    self._push_tree_ready(event.tree)

    def _refresh_tree(self) -> None:
        root = self._state.root
        if root is not None:
            self._start_tree_scan(root)

    def _push_tree_ready(self, tree: TreeNode) -> None:
        window = self._window
        if window is None:
            return
        payload = {
            "tree": _tree_payload(tree),
            "expanded": [to_forward_slashes(p) for p in self._state.expanded],
            "open_file": to_forward_slashes(self._state.open_file) if self._state.open_file else None,
        }
        window.evaluate_js(f"window.mdview.onTreeReady({json.dumps(payload)})")

    def _reload_open_file(self) -> None:
        open_file = self._state.open_file
        window = self._window
        if open_file is None or window is None or not open_file.exists():
            return
        try:
            file_content = read_text_lossy(open_file)
        except OSError as exc:
            error_payload = _error_payload(open_file, f"Cannot read file: {exc.strerror or exc}")
            window.evaluate_js(f"window.mdview.onFileReloaded({json.dumps(error_payload.to_payload())})")
            return
        payload = _file_content_payload(file_content).to_payload()
        window.evaluate_js(f"window.mdview.onFileReloaded({json.dumps(payload)})")

    def _show_file_deleted(self) -> None:
        window = self._window
        self._state.set_open_file(None)
        if window is not None:
            window.evaluate_js("window.mdview.onFileDeleted()")
