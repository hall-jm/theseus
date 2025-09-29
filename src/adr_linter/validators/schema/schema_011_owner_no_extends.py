# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_011_owner_no_extends.py

"""
ADR-SCHEMA-011 — Owner ADR must not use `extends`.

Ref: ADR-0001 §7.1 (Owner ADR) · §14 (SCHEMA-011)
"""
from __future__ import annotations


_ERROR_CODE = "ADR-SCHEMA-011"


def validate_schema_011_owner_no_extends(ctx, rpt) -> None:
    meta = ctx.meta
    path = ctx.path
    if meta.get("class") == "owner":
        ext = meta.get("extends")
        if ext not in (None, "", "null", "Null"):
            rpt.add(_ERROR_CODE, path)
