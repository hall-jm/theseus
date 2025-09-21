# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/link/link_201_extends_missing_pin.py

"""ADR-LINK-201 — `extends` missing base or version pin.

Ref: ADR-0001 §10.2 (Pinned `extends`)
Behavior mirrors the previous inline check in legacy.validate_meta.
"""
from __future__ import annotations


def validate_link_201_extends_missing_pin(ctx, rpt) -> None:
    meta = ctx.meta
    path = ctx.path

    ext = meta.get("extends")
    if ext in (None, "", "null", "Null"):
        return

    ext_str = str(ext)
    if "@" not in ext_str:
        rpt.add("ADR-LINK-201", path, "extends missing version/hash pin")
