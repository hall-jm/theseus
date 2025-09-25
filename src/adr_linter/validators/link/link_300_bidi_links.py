# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/link/link_300_bidi_links.py

"""
ADR-LINK-300 — Bi-directional link missing reciprocal.

Covers:
  - supersedes ↔ superseded_by
  - informs    ↔ informed_by

Messages:
  - "{src} {field} {target} but target lacks {reciprocal}={src_id}"
  - "unknown reciprocal target: {target}"  (target ADR id not indexed)

Ref: ADR-0001 §10.1
"""
from __future__ import annotations

from typing import Iterable

_ERROR_CODE = "ADR-LINK-300"


def _as_list(v) -> list[str]:
    if v is None:
        return []
    if isinstance(v, str):
        return [v]
    if isinstance(v, Iterable):
        return [str(x) for x in v]
    return [str(v)]


def _id_of(pin: str) -> str:
    return pin.split("@", 1)[0] if "@" in pin else pin


def _check_pair(ctx, rpt, field: str, reciprocal: str) -> None:
    meta = ctx.meta
    path = ctx.path
    all_idx = ctx.all_idx
    src_id = meta.get("id")

    for target in _as_list(meta.get(field)):
        if not target:
            continue
        target_id = _id_of(target)
        tinfo = all_idx.get(target_id)
        if not tinfo:
            rpt.add(_ERROR_CODE, path, f"unknown reciprocal target: {target}")
            continue

        rvals = _as_list(tinfo["meta"].get(reciprocal))
        rids = [_id_of(x) for x in rvals]
        if src_id not in rids:
            rpt.add(
                _ERROR_CODE,
                path,
                f"{src_id} {field} {target} but target lacks "
                f"{reciprocal}={src_id}",
            )


def validate_link_300_bidi_links(ctx, rpt) -> None:
    _check_pair(ctx, rpt, "supersedes", "superseded_by")
    _check_pair(ctx, rpt, "informs", "informed_by")
