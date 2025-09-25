# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/services/linkgraph.py

"""
Build supersede graphs for post-run validators.

Used by:
  - ADR-LINK-320 (I): multiple descendants
  - ADR-LINK-321 (E): cycle detected

Inputs: idx is the index built by the engine (id -> {meta, path, body, ...})
Outputs:
 - graph[id] -> list of ids it supersedes
 - reverse_graph[id] -> list of ids that supersede it (descendants)

NOTE: This introduces cross-file analysis while the main pipeline is
      single-file oriented. Kept intentionally (per product direction),
      with this note documenting the tension for future review.

Ref: ADR-0001 §10.4
"""


from __future__ import annotations

from typing import Dict, List, Tuple


def build_supersede_graph(
    idx: Dict[str, dict],
) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """
    Construct forward and reverse supersede graphs from the ADR index.

    This is a straight lift of the legacy behavior:
      - treat a string `supersedes` as a one-item list
      - ignore targets that aren't present in the index

    Ref: ADR-0001 §(Missing) · (If needed, ADR-*-* is missing)
    """
    graph: Dict[str, List[str]] = {k: [] for k in idx.keys()}
    reverse_graph: Dict[str, List[str]] = {k: [] for k in idx.keys()}

    for sid, info in idx.items():
        supersedes = info["meta"].get("supersedes")
        if isinstance(supersedes, str):
            supersedes = [supersedes]
        if supersedes:
            for target in supersedes:
                if target in graph:
                    graph[sid].append(target)
                    reverse_graph[target].append(sid)

    return graph, reverse_graph
