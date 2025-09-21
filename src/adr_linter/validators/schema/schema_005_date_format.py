# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_005_date_format.py

from __future__ import annotations
import datetime

# from typing import Optional

from ...constants import DATE_RX, DATE_KEY_NAMES


def _is_valid_iso_date_like(v) -> bool:
    """Accept:
    - datetime.date/datetime.datetime
    - str exactly 'YYYY-MM-DD' that is a real calendar date
    """
    if isinstance(v, datetime.datetime):
        v = v.date()
    if isinstance(v, datetime.date):
        return True
    s = str(v)
    if not DATE_RX.fullmatch(s):
        return False
    try:
        datetime.date.fromisoformat(s)
        return True
    except Exception:
        return False


def validate_schema_005_date_format(ctx, rpt) -> None:
    """ADR-SCHEMA-005 — Invalid date format for `date` or `review_by`.
    Behavior mirrors the previous checks in legacy.validate_meta.
    """
    meta = ctx.meta
    path = ctx.path

    # First pass (with explicit '(got: ...)' detail)
    for k in DATE_KEY_NAMES:
        v = meta.get(k)
        if v and not _is_valid_iso_date_like(v):
            rpt.add(
                "ADR-SCHEMA-005", path, f"{k} must be YYYY-MM-DD (got: {v})"
            )

    # Second pass (plain message; retained for parity with legacy)
    for k in ("date", "review_by"):
        v = meta.get(k)
        if v:
            try:
                datetime.date.fromisoformat(str(v))
            except Exception:
                rpt.add("ADR-SCHEMA-005", path, f"{k} must be YYYY-MM-DD")
