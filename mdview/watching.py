"""Filesystem watching: classify events, debounce, and queue them for the drain loop."""

import queue
import threading
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver

from mdview.paths import is_markdown
from mdview.tree import TreeNode

DEFAULT_DEBOUNCE_MS = 200


@dataclass
class ContentChanged:
    """The currently open file was modified on disk."""

    path: Path


@dataclass
class FileDeleted:
    """The currently open file was deleted from disk."""

    path: Path


@dataclass
class MarkdownTreeChanged:
    """A markdown file elsewhere under the root was created or deleted."""

    path: Path


@dataclass
class TreeReady:
    """A background `scan_folder` for `root` finished."""

    root: Path
    tree: TreeNode


WatchEvent = ContentChanged | FileDeleted | MarkdownTreeChanged | TreeReady


class Debouncer:
    """Coalesces rapid `schedule()` calls into a single delayed callback invocation."""

    def __init__(self, delay_ms: int = DEFAULT_DEBOUNCE_MS) -> None:
        self._delay_seconds = delay_ms / 1000
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    def schedule(self, callback: Callable[[], None]) -> None:
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
            timer = threading.Timer(self._delay_seconds, callback)
            timer.daemon = True
            timer.start()
            self._timer = timer

    def cancel(self) -> None:
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None


class _MarkdownEventHandler(FileSystemEventHandler):
    """Classifies filesystem events under a watched root and pushes them onto a queue."""

    def __init__(
        self,
        open_file: Callable[[], Path | None],
        events: "queue.Queue[WatchEvent]",
    ) -> None:
        self._open_file = open_file
        self._events = events

    def on_modified(self, event: FileSystemEvent) -> None:
        self._classify(event)

    def on_created(self, event: FileSystemEvent) -> None:
        self._classify(event)

    def on_deleted(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        path = Path(str(event.src_path))
        if path == self._open_file():
            self._events.put(FileDeleted(path=path))
        elif is_markdown(path):
            self._events.put(MarkdownTreeChanged(path=path))

    def on_moved(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            self._events.put(MarkdownTreeChanged(path=Path(str(event.src_path))))
            return
        src_path = Path(str(event.src_path))
        dest_path = Path(str(event.dest_path))
        if src_path == self._open_file():
            self._events.put(FileDeleted(path=src_path))
        elif is_markdown(src_path):
            self._events.put(MarkdownTreeChanged(path=src_path))
        if is_markdown(dest_path):
            self._events.put(MarkdownTreeChanged(path=dest_path))

    def _classify(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        path = Path(str(event.src_path))
        if path == self._open_file():
            self._events.put(ContentChanged(path=path))
        elif is_markdown(path):
            self._events.put(MarkdownTreeChanged(path=path))


class FolderWatcher:
    """Owns one recursive `watchdog` observer over a session root."""

    def __init__(self) -> None:
        self._observer: BaseObserver | None = None
        self.events: "queue.Queue[WatchEvent]" = queue.Queue()

    def start(self, root: Path, open_file: Callable[[], Path | None]) -> None:
        self.stop()
        handler = _MarkdownEventHandler(open_file=open_file, events=self.events)
        observer = Observer()
        observer.schedule(handler, str(root), recursive=True)
        observer.start()
        self._observer = observer

    def stop(self) -> None:
        observer = self._observer
        if observer is not None:
            observer.stop()
            observer.join()
            self._observer = None

    def drain(self) -> list[WatchEvent]:
        drained: list[WatchEvent] = []
        while True:
            try:
                drained.append(self.events.get_nowait())
            except queue.Empty:
                break
        return drained
