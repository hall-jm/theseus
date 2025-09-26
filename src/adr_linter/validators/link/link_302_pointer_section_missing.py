# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/link/link_302_pointer_section_missing.py

"""
ADR-LINK-302 — Pointer to section key missing in base (warning).

Behavior matches the legacy implementation: warn when a `ptr` references a
section key that does not exist in the base ADR, *excluding* normative keys
(those are checked by ADR-LINK-304).

Ref: ADR-0001 §10.3 · ADR-LINK-302
"""

from __future__ import annotations

from ...constants import NORMATIVE_KEYS
from ...parser.structure import (
    map_heading_to_key,
    parse_document_structure,
)


_ERROR_CODE = "ADR-LINK-302"


# REVIEW: This validation depends on HEADINGS_TO_KEYS being complete
# TODO: Verify all expected keys have corresponding heading patterns
# REVIEW:  See also ADR-SCHEMA-003, 021 for similar REVIEW & TODO
def validate_link_302_pointer_section_missing(ctx, rpt) -> None:
    meta = ctx.meta
    path = ctx.path
    si = ctx.section_data
    idx = ctx.all_idx

    # Resolve base ADR from extends@pin
    ext = meta.get("extends")
    if not ext or "@" not in str(ext):
        return
    base_id = str(ext).split("@", 1)[0]
    base = idx.get(base_id)
    if not base:
        return

    # Collect ptr map from fenced yaml blocks
    ptr_map = {}
    for blk in si.yaml_blocks:
        if isinstance(blk.get("ptr"), dict):
            ptr_map.update(blk["ptr"])
    if not ptr_map:
        return

    # Build base section key set (markers first, then fallback via headings)
    base_si = parse_document_structure(base["body"])
    base_keys = {k for k, _, _ in base_si.key_markers}
    if not base_keys:
        base_keys = set(
            filter(
                None,
                (
                    map_heading_to_key(h)
                    for (h, _lvl, _pos, _ln) in base_si.headings
                ),
            )
        )

    # Emit 202 for non-normative missing keys only (normative → 204)
    for key in ptr_map.keys():
        if key in NORMATIVE_KEYS:
            continue
        if key not in base_keys:
            rpt.add(
                _ERROR_CODE,
                path,
                f"ptr→{key} missing in base {base_id}",
            )
