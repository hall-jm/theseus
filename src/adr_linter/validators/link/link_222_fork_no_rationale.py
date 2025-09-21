# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/link/link_222_fork_no_rationale.py

"""
ADR-LINK-222 — Supersede fork without rationale in `change_history`.

Ref: ADR-0001 §10.4 (Supersede closure map)
Behavior mirrors the previous `validate_fork_rationale` in legacy.py
"""

from __future__ import annotations

from typing import Dict
from pathlib import Path


def validate_link_222_fork_no_rationale_for_meta(
    meta: Dict, path: Path, rpt
) -> None:
    """
    Emit ADR-LINK-222 when an ADR supersedes 2+ ADRs without fork rationale.
    """
    supersedes = meta.get("supersedes")
    if isinstance(supersedes, str):
        supersedes = [supersedes]
    elif not supersedes:
        supersedes = []

    if len(supersedes) <= 1:
        return

    change_history = meta.get("change_history", [])
    has_rationale = False
    if isinstance(change_history, list):
        for entry in change_history:
            if isinstance(entry, dict):
                note = str(entry.get("note", "")).lower()
                for kw in (
                    "fork",
                    "branch",
                    "split",
                    "diverge",
                    "merge",
                    "consolidate",
                ):
                    if kw in note:
                        has_rationale = True
                        break
            if has_rationale:
                break

    if not has_rationale:
        rpt.add(
            "ADR-LINK-222",
            path,
            f"Fork of {len(supersedes)} ADRs without rationale "
            f"in change_history: {supersedes}",
        )
