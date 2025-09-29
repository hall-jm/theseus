# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_001_required_meta.py

"""
ADR-SCHEMA-001 — Required metadata & ID format
Ref: ADR-0001 §3 (Required metadata), §14 (SCHEMA-001)
"""

from __future__ import annotations

from ...constants import REQUIRED_META, ID_RX

_ERROR_CODE = "ADR-SCHEMA-001"


def validate_schema_001_required_meta(ctx, rpt) -> None:
    meta = ctx.meta
    path = ctx.path

    # Missing required keys
    missing = [k for k in REQUIRED_META if not meta.get(k)]
    if missing:
        rpt.add(_ERROR_CODE, path, f"missing: {', '.join(missing)}")

    # ID must match ADR-XXXX
    if not ID_RX.match(str(meta.get("id", ""))):
        rpt.add(_ERROR_CODE, path, "id must be ADR-XXXX")
