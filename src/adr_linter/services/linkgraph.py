# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/services/linkgraph.py

"""
Purpose: pure helper(s) to build supersede graphs used by LINK-220/221.
Behavior mirrors the prior legacy implementation (zero change).

Inputs: idx is the index built by the engine (id -> {meta, path, body, ...})
Outputs:
 - graph[id] -> list of ids it supersedes
 - reverse_graph[id] -> list of ids that supersede it (descendants)

Ref: ADR-0001 §(Missing) · (If needed, ADR-*-* is missing)
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
