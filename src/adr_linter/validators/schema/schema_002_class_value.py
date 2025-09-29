# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/

"""
ADR-SCHEMA-002 — Class value must be valid

Ref: ADR-0001 §7 (ADR classes), §14 (SCHEMA-002)
"""

from __future__ import annotations

from ...constants import VALID_ADR_CLASSES


_ERROR_CODE = "ADR-SCHEMA-002"


def validate_schema_002_class_value(ctx, rpt) -> None:
    meta = ctx.meta
    path = ctx.path
    if meta.get("class") not in VALID_ADR_CLASSES:
        rpt.add(_ERROR_CODE, path, f"class={meta.get('class')}")
