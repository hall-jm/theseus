# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/link/link_220_closure_info.py

"""
ADR-LINK-220 — Supersede closure: multiple descendants (informational).
Ref: ADR-0001 §10.4
"""
from __future__ import annotations


def validate_link_220_closure_info(
    reverse_graph: dict[str, list[str]], idx: dict, rpt
) -> None:
    """Emit ADR-LINK-220 when a base has >1 descendants."""
    for base, children in reverse_graph.items():
        if len(children) > 1:
            rpt.add(
                "ADR-LINK-220",
                idx[base]["path"],
                f"multiple descendants: {', '.join(children)}",
            )
