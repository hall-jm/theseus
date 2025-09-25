# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/link/link_301_unidi_required_pin.py

"""
ADR-LINK-301 — Required uni-directional binding missing pin (presence is
               binary).

Rules (front-matter only; no prose heuristics):
  - Owner:  governed_by REQUIRED and pinned.
  - Delta:  extends REQUIRED and pinned. governed_by OPTIONAL; if present,
            pinned.
  - Strategy: governed_by OPTIONAL (per §7.3). If present, pinned.
  - Template & Style-guide: skip (not applicable).

Message:
  - "{field} missing version/hash pin"  (key present without '@')
  - "missing {field}"                   (key absent but required)

Ref: ADR-0001 §3, §7.2, §7.3, §7.5, §8, §10.2
"""
from __future__ import annotations


_ERROR_CODE = "ADR-LINK-301"


def _has_at(v) -> bool:
    return isinstance(v, str) and "@" in v


def _present(v) -> bool:
    return v not in (None, "", "null", "Null")


def _require_pinned(rpt, path, field, val):
    if not _present(val):
        rpt.add(_ERROR_CODE, path, f"missing {field}")
    elif not _has_at(val):
        rpt.add(_ERROR_CODE, path, f"{field} missing version/hash pin")


def validate_link_301_unidi_required_pin(ctx, rpt) -> None:
    meta = ctx.meta
    path = ctx.path
    cls = (meta.get("class") or "").lower()

    if cls in ("template", "style-guide"):
        return

    # Owner: governed_by required + pinned
    if cls == "owner":
        _require_pinned(rpt, path, "governed_by", meta.get("governed_by"))
        return

    # Delta: extends required + pinned; governed_by optional, but if present
    #        must be pinned
    if cls == "delta":
        _require_pinned(rpt, path, "extends", meta.get("extends"))
        gb = meta.get("governed_by")
        if _present(gb) and not _has_at(gb):
            rpt.add(_ERROR_CODE, path, "governed_by missing version/hash pin")
        return

    # Strategy: governed_by OPTIONAL; if present, must be pinned
    if cls == "strategy":
        gb = meta.get("governed_by")
        if _present(gb) and not _has_at(gb):
            rpt.add(_ERROR_CODE, path, "governed_by missing version/hash pin")
        return

    # Governance / others: nothing for 301
