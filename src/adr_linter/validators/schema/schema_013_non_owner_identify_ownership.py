# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_013_non_owner_identify_ownership.py

"""
ADR-SCHEMA-013 — Non-Owner ADRs must identify ADR ownership.

Ref: ADR-0001 §7 (ADR classes) · §14 (SCHEMA-013)
"""
from __future__ import annotations


def validate_schema_013_non_owner_identify_ownership(ctx, rpt) -> None:
    meta = ctx.meta
    path = ctx.path
    cls = meta.get("class")
    if cls not in ("owner", "style-guide"):
        if not meta.get("owners_ptr"):
            rpt.add("ADR-SCHEMA-013", path)
