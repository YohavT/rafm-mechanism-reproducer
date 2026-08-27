import json
from pathlib import Path

from pydantic import BaseModel


class HierarchyNode(BaseModel):
    numero: str
    niveau: int
    parent: str | None
    titre: str
    partie: str
    page: int
    # present only in the Low JSON
    contenu: str | None = None
    contenu_len: int | None = None
    a_du_code: bool | None = None


def load_hierarchy(path: Path) -> list[HierarchyNode]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [HierarchyNode.model_validate(n) for n in raw]


def build_index(nodes: list[HierarchyNode]) -> dict[str, HierarchyNode]:
    """numero → node, O(1) lookup for validators."""
    return {n.numero: n for n in nodes}


def to_compact_text(nodes: list[HierarchyNode]) -> str:
    """
    Compact pipe-delimited representation for Stage 2 prompt.
    Format per line: [numero] titre | partie
    Skips Summary and Input Manager sections (not relevant for formula selection).
    """
    lines: list[str] = []
    for n in nodes:
        if n.partie in ("Summary", "Input Manager"):
            continue
        lines.append(f"[{n.numero}] {n.titre} | {n.partie}")
    return "\n".join(lines)
