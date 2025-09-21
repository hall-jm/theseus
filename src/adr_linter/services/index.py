# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/services/index.py

"""
Pure index construction helpers (no file IO).

Index construction helpers.
Pure path:  build_index_from_texts(...)
Impure path: load_files(...), build_index_from_files(...), read_text(...)

Ref: ADR-0001 §(Missing) · (If needed, ADR-*-* is missing)
"""

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Iterable, Tuple

from ..constants import ADR_LOCATIONS
from ..parser.front_matter import parse_front_matter
from ..parser.structure import parse_document_structure


# ------------------------- Impure helpers (IO) -------------------------


def load_files(root: Path) -> List[Path]:
    """
    Discover ADR markdown files using ADR_LOCATIONS, skipping any files
    in hidden directories (e.g., '.adr') relative to 'root'.
    Behavior mirrors the prior io.load_files.
    """
    seen: set[Path] = set()
    files: list[Path] = []

    for pattern in ADR_LOCATIONS:
        for p in root.glob(pattern):
            try:
                rel_path = p.relative_to(root)
                if any(part.startswith(".") for part in rel_path.parts):
                    continue
            except ValueError:
                # If not relative to root, skip (mirrors previous behavior)
                continue
            rp = p.resolve()
            if rp not in seen:
                seen.add(rp)
                files.append(p)
    return sorted(files)


def build_index_from_files(
    files: Iterable[Path],
    *,
    encoding: str = "utf-8",
) -> Dict[str, Dict[str, Any]]:
    """
    Impure wrapper: read each file and delegate to build_index_from_texts.
    Mirrors previous io.build_index behavior.
    """
    pairs: list[Tuple[Path, str]] = []
    for p in files:
        text = p.read_text(encoding=encoding)
        pairs.append((p, text))
    return build_index_from_texts(pairs)


def read_text(path: Path, *, encoding: str = "utf-8") -> str:
    """
    Tiny reader wrapper to keep engine free of direct filesystem calls.
    """
    return path.read_text(encoding=encoding)


# TOREVIEW: Legacy holdover; will not delete until it is determined that
#           this version of build_index_*() is not needed
def build_index_from_texts(
    pairs: Iterable[Tuple[Path, str]],
) -> Dict[str, Dict[str, Any]]:
    """
    Given (path, raw text) pairs, parse front-matter and structure.
    Returns the same index shape used elsewhere:
    {
        adr_id:
        {
            "path": Path,
            "meta": dict,
            "body": str,
            "raw": str,
            "section_info": SectionInfo
        }
    }
    """
    idx: Dict[str, Dict[str, Any]] = {}
    for p, text in pairs:
        meta, end = parse_front_matter(text)
        body = text[end:]
        section_info = parse_document_structure(body)
        if meta.get("id"):
            idx[meta["id"]] = {
                "path": p,
                "meta": meta,
                "body": body,
                "raw": text,
                "section_info": section_info,
            }
    return idx
