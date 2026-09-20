"""Markdown-only folder tree scanning."""

from dataclasses import dataclass, field
from pathlib import Path

from mdview.paths import is_markdown


@dataclass
class TreeNode:
    """A directory or markdown file in the scanned tree."""

    name: str
    path: Path
    is_dir: bool
    children: list["TreeNode"] = field(default_factory=list)


def _sort_key(node: TreeNode) -> tuple[bool, str]:
    return (not node.is_dir, node.name.lower())


def _scan_directory(directory: Path, visited: set[Path]) -> list[TreeNode]:
    real_path = directory.resolve()
    if real_path in visited:
        return []
    visited.add(real_path)

    nodes: list[TreeNode] = []
    for entry in directory.iterdir():
        if entry.is_dir():
            children = _scan_directory(entry, visited)
            if children:
                nodes.append(TreeNode(name=entry.name, path=entry, is_dir=True, children=children))
        elif entry.is_file() and is_markdown(entry):
            nodes.append(TreeNode(name=entry.name, path=entry, is_dir=False))

    nodes.sort(key=_sort_key)
    return nodes


def scan_folder(root: Path) -> TreeNode:
    """Recursively scan `root`, keeping only directories that contain `.md` files at any depth."""
    children = _scan_directory(root, visited=set())
    return TreeNode(name=root.name, path=root, is_dir=True, children=children)
