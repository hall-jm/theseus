# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_012_non_owner_no_owners.py

"""
ADR-SCHEMA-012 — Non-Owner ADRs must never use `owners`.

Ref: ADR-0001 §7 (ADR classes) · §14 (SCHEMA-012)
"""
from __future__ import annotations


def validate_schema_012_non_owner_no_owners(ctx, rpt) -> None:
    meta = ctx.meta
    path = ctx.path
    cls = meta.get("class")
    # Style-guide and Owner are allowed; others must not define owners
    if cls not in ("owner", "style-guide"):
        if meta.get("owners"):
            rpt.add("ADR-SCHEMA-012", path)
