"""Markdown-to-HTML rendering with source line mapping."""

from dataclasses import dataclass, field

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import ClassNotFound, get_lexer_by_name

from mdview.files import FileContent

# Code-block highlighting: Pygments (server-side), chosen over highlight.js, because Pygments is
# already a runtime dependency and adds no extra JS asset to bundle under pyinstaller.
_HIGHLIGHT_FORMATTER = HtmlFormatter(nowrap=True)


@dataclass
class LineRange:
    """A 1-based, inclusive line range. The project's only range type."""

    start: int
    end: int


@dataclass
class BlockMapping:
    """A rendered block's tag and the raw source lines it originated from."""

    tag: str
    lines: LineRange


@dataclass
class RenderedDocument:
    """The HTML for a rendered file, plus the source line mapping for each block."""

    html: str
    blocks: list[BlockMapping] = field(default_factory=list)


def _highlight_code(code: str, lang_name: str, _lang_attrs: str) -> str | None:
    """Return Pygments-highlighted spans, or None to fall back to plain preformatted text."""
    if not lang_name:
        return None
    try:
        lexer = get_lexer_by_name(lang_name)
    except ClassNotFound:
        return None
    return highlight(code, lexer, _HIGHLIGHT_FORMATTER)


def _tag_data_line(state: object) -> None:
    """Core-ruler pass: stamp every block-level token with `data-line="start-end"`."""
    for token in state.tokens:  # type: ignore[attr-defined]
        _set_data_line_attr(token)


def _set_data_line_attr(token: Token) -> None:
    if token.map is None or token.nesting == -1:
        return
    start, end = token.map
    token.attrSet("data-line", f"{start + 1}-{end}")


def _build_markdown_it() -> MarkdownIt:
    md = (
        MarkdownIt("commonmark", {"highlight": _highlight_code, "linkify": True})
        .enable(["table", "linkify"])
        .use(tasklists_plugin)
        .use(footnote_plugin)
    )
    md.core.ruler.push("data_line_attrs", _tag_data_line)
    return md


_MARKDOWN_IT = _build_markdown_it()


def _extract_blocks(tokens: list[Token]) -> list[BlockMapping]:
    blocks: list[BlockMapping] = []
    for token in tokens:
        if token.map is None or token.nesting == -1:
            continue
        start, end = token.map
        blocks.append(BlockMapping(tag=token.tag or token.type, lines=LineRange(start + 1, end)))
    return blocks


def render_markdown(content: FileContent) -> RenderedDocument:
    """Render `content.text` to HTML, with every block carrying its source line range."""
    tokens = _MARKDOWN_IT.parse(content.text)
    html = _MARKDOWN_IT.renderer.render(tokens, _MARKDOWN_IT.options, {})
    return RenderedDocument(html=html, blocks=_extract_blocks(tokens))
