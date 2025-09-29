# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/services/index.py

"""
ADR file discovery and index construction (impure I/O layer).

Pure path:  parser.structure.build_index_from_texts(...)
Impure path: load_files(...), build_index_from_files(...), read_text(...)

Ref: ADR-0001 §(Missing) · (If needed, ADR-*-* is missing)
"""

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Iterable, Tuple

from ..constants import ADR_LOCATIONS
from ..parser.structure import build_index_from_texts


# ------------------------- Impure helpers (IO) -------------------------


def load_files(root: Path) -> List[Path]:
    """
    Discover ADR markdown files using ADR_LOCATIONS, skipping any files
    in hidden directories (e.g., '.adr') relative to 'root'.
    Behavior mirrors the prior io.load_files.
    """
    seen: set[Path] = set()
    files: list[Path] = []

    # TODO: If ADR_LOCATIONS do not exist in current file structure,
    #       fail now and raise exception
    for pattern in ADR_LOCATIONS:
        for p in root.glob(pattern):
            try:
                rel_path = p.relative_to(root)
                if any(part.startswith(".") for part in rel_path.parts):
                    continue
            except ValueError:
                # If not relative to root, skip
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
    Impure wrapper: read each file and delegate to pure build_index_from_texts.
    Maintains clean separation between I/O and parsing logic.
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
