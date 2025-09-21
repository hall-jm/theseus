# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_004_status_transition.py

"""
ADR-SCHEMA-004 — Invalid status transition or missing required fields.

Legacy behavior:
 - If status == Superseded: require non-empty `superseded_by`
 - If status == Deprecated: require either non-empty `superseded_by`
   OR a non-empty `change_history` list (rationale)

Ref: ADR-0001 §Status/§14 · ADR-SCHEMA-004
"""

from __future__ import annotations


def validate_schema_004_status_transition(ctx, rpt) -> None:
    meta = ctx.meta
    path = ctx.path

    status = meta.get("status")
    if status == "Superseded":
        sb = meta.get("superseded_by")
        if not sb or sb in (None, "", "null"):
            rpt.add("ADR-SCHEMA-004", path)
        return

    if status == "Deprecated":
        sb = meta.get("superseded_by")
        ch = meta.get("change_history", [])
        has_justification = bool(sb and sb not in (None, "", "null"))
        has_rationale = bool(ch and isinstance(ch, list))
        if not (has_justification or has_rationale):
            rpt.add("ADR-SCHEMA-004", path)
