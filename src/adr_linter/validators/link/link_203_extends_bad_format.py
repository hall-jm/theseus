# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/link/link_203_extends_bad_format.py

"""ADR-LINK-203 — Invalid `extends` pin format.

Ref: ADR-0001 §10.2 (Pinned `extends`)
Behavior mirrors the prior logic in legacy.validate_meta (messages unchanged).
"""

from __future__ import annotations

import datetime
import re


def validate_link_203_extends_bad_format(ctx, rpt) -> None:
    """
    Emit ADR-LINK-203 for malformed `extends` pins (format/date/hex-casing).
    """
    meta = ctx.meta
    path = ctx.path

    ext = meta.get("extends")
    if ext in (None, "", "null", "Null"):
        return

    ext_str = str(ext)
    # NOTE: LINK-201 (missing '@') is handled elsewhere (legacy.validate_meta).
    if "@" not in ext_str:
        return

    try:
        adr_part, pin_part = ext_str.split("@", 1)

        # ADR id format
        if not re.match(r"^ADR-\d{4}$", adr_part):
            rpt.add(
                "ADR-LINK-203",
                path,
                f"bad ADR format in extends: {ext_str}",
            )
            return

        # Pin part: date or lowercase hex
        if re.match(r"^20\d{2}-\d{2}-\d{2}$", pin_part):
            try:
                datetime.date.fromisoformat(pin_part)
            except ValueError:
                rpt.add(
                    "ADR-LINK-203",
                    path,
                    f"invalid date in extends pin: {ext_str}",
                )
            return

        if re.match(r"^[0-9a-f]{7,40}$", pin_part):
            return  # valid lowercase hex

        if re.match(r"^[0-9A-F]{7,40}$", pin_part):
            rpt.add(
                "ADR-LINK-203",
                path,
                f"uppercase hex in extends pin: {ext_str} (must be lowercase)",
            )
            return

        # Anything else: bad pin shape
        rpt.add(
            "ADR-LINK-203",
            path,
            f"bad pin format in extends: {ext_str} (must be YYYY-MM-DD "
            f"or lowercase hex)",
        )
    except ValueError:
        rpt.add("ADR-LINK-203", path, f"malformed extends format: {ext_str}")
