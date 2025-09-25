# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/link/link_303_pin_format_any_field.py

"""
ADR-LINK-303 — Invalid pin format for relationship field (field-agnostic).

Applies to any field among:
  extends, supersedes, superseded_by, governed_by, informs, informed_by

Messages:
  - "bad ADR format in {field}: {value}"
  - "invalid date in {field} pin: {value}"
  - "uppercase hex in {field} pin: {value} (must be lowercase)"
  - "bad pin format in {field}: {value} (must be YYYY-MM-DD or lowercase hex)"
  - "malformed {field} format: {value}"

Ref: ADR-0001 §8 (regex), §10.2/§10.1 (where pins appear)
"""
from __future__ import annotations

import datetime
import re

_ERROR_CODE = "ADR-LINK-303"

# FIXME: These values need to be centralized and not stored in the
#        individual validators

_FIELDS = (
    "extends",
    "supersedes",
    "superseded_by",
    "governed_by",
    "informs",
    "informed_by",
)

_RX_ADR = re.compile(r"^ADR-\d{4}$")
_RX_DATE = re.compile(r"^20\d{2}-\d{2}-\d{2}$")
_RX_HEX_LO = re.compile(r"^[0-9a-f]{7,40}$")
_RX_HEX_UP = re.compile(r"^[0-9A-F]{7,40}$")


def _check_one(rpt, path, field: str, val: str) -> None:
    if "@" not in val:
        return  # missing pin handled by LINK-301 where applicable
    try:
        adr, pin = val.split("@", 1)
    except ValueError:
        rpt.add(_ERROR_CODE, path, f"malformed {field} format: {val}")
        return

    if not _RX_ADR.match(adr):
        rpt.add(_ERROR_CODE, path, f"bad ADR format in {field}: {val}")
        return

    if _RX_DATE.match(pin):
        try:
            datetime.date.fromisoformat(pin)
            return
        except ValueError:
            rpt.add(_ERROR_CODE, path, f"invalid date in {field} pin: {val}")
            return

    if _RX_HEX_LO.match(pin):
        return
    if _RX_HEX_UP.match(pin):
        rpt.add(
            _ERROR_CODE,
            path,
            f"uppercase hex in {field} pin: {val} (must be lowercase)",
        )
        return

    rpt.add(
        _ERROR_CODE,
        path,
        f"bad pin format in {field}: {val} (must be YYYY-MM-DD or "
        "lowercase hex)",
    )


def _iter_vals(v):
    if v is None:
        return []
    if isinstance(v, str):
        return [v]
    try:
        return [str(x) for x in v]
    except TypeError:
        return [str(v)]


def validate_link_303_pin_format_any_field(ctx, rpt) -> None:
    meta = ctx.meta
    path = ctx.path
    for field in _FIELDS:
        for val in _iter_vals(meta.get(field)):
            if val:
                _check_one(rpt, path, field, str(val))
