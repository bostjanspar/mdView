"""CLI entry point for mdview."""

import argparse
import sys
from pathlib import Path

import webview

from mdview import __version__
from mdview.app import App
from mdview.paths import to_forward_slashes

_WEBVIEW2_MISSING_MESSAGE = (
    "Markdown Viewer requires the Microsoft Edge WebView2 runtime, which was not found on "
    "this machine. Install it from "
    "https://developer.microsoft.com/en-us/microsoft-edge/webview2/ and try again."
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mdview")
    parser.add_argument(
        "--version", action="store_true", help="Print the version and exit."
    )
    parser.add_argument(
        "--folder", type=str, default=None, help="Folder to open."
    )
    return parser


def _handle_folder(folder: str) -> int:
    path = Path(folder)
    if not path.is_dir():
        print(f"Error: folder not found: {folder}", file=sys.stderr)
        return 1
    print(f"Would open folder: {to_forward_slashes(path)}")
    return 0


def _report_webview2_missing() -> None:
    print(_WEBVIEW2_MISSING_MESSAGE, file=sys.stderr)
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.user32.MessageBoxW(
            0, _WEBVIEW2_MISSING_MESSAGE, "Markdown Viewer", 0x10
        )


def _assets_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "mdview" / "assets"  # type: ignore[attr-defined]
    return Path(__file__).parent / "assets"


def _run_app() -> int:
    app = App()
    index_html = _assets_dir() / "index.html"
    window = webview.create_window(
        "Markdown Viewer", str(index_html), js_api=app, text_select=True
    )
    if window is None:
        _report_webview2_missing()
        return 1
    app.bind_window(window)
    try:
        webview.start(app.start_watch_loop, icon=str(_assets_dir() / "app.ico"))
    except webview.WebViewException:
        _report_webview2_missing()
        return 1
    finally:
        app.shutdown()
    return 0


def main() -> int:
    """Parse CLI arguments and run the requested action."""
    parser = _build_parser()
    args = parser.parse_args()

    if args.version:
        print(__version__)
        return 0

    if args.folder is not None:
        return _handle_folder(args.folder)

    return _run_app()


if __name__ == "__main__":
    sys.exit(main())
