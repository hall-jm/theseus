# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/meta/meta_151_tail_mismatch.py

"""
ADR-META-151 — `llm_tail` disagrees with front-matter on required keys.

Ref: ADR-0001 §12 · ADR-META-151
"""

from __future__ import annotations


def validate_meta_151_tail_mismatch(ctx, rpt) -> None:
    tail = ctx.section_data.llm_tail
    if not tail:
        return

    meta = ctx.meta
    mismatches = []

    # Core fields
    for k in ("id", "class", "status"):
        if str(tail.get(k)) != str(meta.get(k)):
            mismatches.append(k)

    # extends (normalize None/"")
    if (tail.get("extends") or "") != (meta.get("extends") or ""):
        mismatches.append("extends")

    # Ownership (owners exact OR owners_ptr exact)
    owners = meta.get("owners")
    owners_ptr = meta.get("owners_ptr")
    tail_owners = tail.get("owners")
    tail_owners_ptr = tail.get("owners_ptr")

    ownership_match = False
    if owners and tail_owners == owners:
        ownership_match = True
    elif owners_ptr and tail_owners_ptr == owners_ptr:
        ownership_match = True

    if not ownership_match:
        mismatches.append("ownership")

    if mismatches:
        rpt.add(
            "ADR-META-151", ctx.path, f"tail mismatch: {', '.join(mismatches)}"
        )
