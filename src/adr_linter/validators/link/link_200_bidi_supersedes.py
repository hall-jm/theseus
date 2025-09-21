# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/link/link_200_bidi_supersedes.py

"""ADR-LINK-200 — `supersedes` without reciprocal `superseded_by`.

Ref: ADR-0001 §10.1 Bi-directional links
Behavior mirrors the prior logic embedded in legacy.validate_links_enhanced.
"""
from __future__ import annotations


def validate_link_200_bidi_supersedes(ctx, rpt) -> None:
    meta = ctx.meta
    path = ctx.path
    all_idx = ctx.all_idx
    sid = meta.get("id")

    supersedes = meta.get("supersedes")

    if isinstance(supersedes, str):
        supersedes = [supersedes]
    if not supersedes:
        return

    superseded_by = None
    reciprocal_found = False

    for target in supersedes:
        # Extract just the ID part before the pin
        # "ADR-8402@2025-09-01" → "ADR-8402"
        target_id = target.split("@")[0]
        target_info = all_idx.get(target_id)

        if not target_info:
            rpt.add("ADR-LINK-200", path, f"supersedes unknown {target}")
            continue

        target_meta = target_info["meta"]
        superseded_by = target_meta.get("superseded_by")

        reciprocal_found = False
        if isinstance(superseded_by, str):
            superseded_by_id = superseded_by.split("@")[0]  # Extract ID part
            reciprocal_found = superseded_by_id == sid
        elif isinstance(superseded_by, list):
            superseded_by_ids = [item.split("@")[0] for item in superseded_by]
            reciprocal_found = sid in superseded_by_ids

        if not reciprocal_found:
            rpt.add(
                "ADR-LINK-200",
                path,
                f"{sid} supersedes {target} but target lacks "
                f"superseded_by={sid}",
            )
