# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/link/link_221_cycle_detected.py

"""
ADR-LINK-221 — Supersede closure: cycle detected.
Ref: ADR-0001 §10.4
"""

from __future__ import annotations


def validate_link_221_cycle_detected(
    graph: dict[str, list[str]], idx: dict, rpt
) -> None:
    """
    Run DFS on the supersedes graph; emit ADR-LINK-221 once if any cycle
    exists.
    """
    visited = set()
    rec_stack = set()

    def dfs(node: str) -> bool:
        if node in rec_stack:
            return True
        if node in visited:
            return False
        visited.add(node)
        rec_stack.add(node)
        for nbr in graph.get(node, []):
            if dfs(nbr):
                return True
        rec_stack.remove(node)
        return False

    has_cycle = any(dfs(n) for n in list(graph.keys()) if n not in visited)
    if has_cycle:
        """
        Report on the first node with outgoing edges for stability (parity
        with legacy).
        """
        for node, edges in graph.items():
            if edges:
                rpt.add(
                    "ADR-LINK-221",
                    idx[node]["path"],
                    "supersede cycle detected",
                )
                break
