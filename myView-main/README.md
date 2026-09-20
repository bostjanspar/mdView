# Markdown Viewer

A standalone Windows desktop markdown viewer.

## Prerequisites

Requires the [Microsoft Edge WebView2 runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/)
to be installed, since the app shell renders through it.

## Development

```bash
python -m pip install -e .
python -m mdview --version
```

## Running with uv

```bash
uv run python -m mdview
```

`uv run` installs the project and its dependencies into a managed environment on first run, then
launches the app — no separate install step needed.

## Building the executable

```bash
python -m pip install -e ".[dev]"
pyinstaller mdview.spec
```

The build produces a single file, `dist/mdview.exe`. That one file is everything needed to run
the app on a Windows machine that has the WebView2 runtime installed — no Python required.

## Running the executable

Double-click `dist/mdview.exe`, or run it from a shell:

```bash
dist/mdview.exe
```
