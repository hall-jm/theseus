# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/link/link_304_normative_ptr_missing.py

"""ADR-LINK-304 — Pointer to normative section key missing in base.

Ref: ADR-0001 §10.3 Pointers
Behavior mirrors the legacy implementation for normative-section pointers.
"""
from __future__ import annotations

from ...constants import NORMATIVE_KEYS, EXTENDS_RX
from ...parser.structure import parse_document_structure


_ERROR_CODE = "ADR-LINK-304"


def validate_link_304_normative_ptr_missing(ctx, rpt) -> None:
    """
    Emit ADR-LINK-304 when ptr→<normative_key> is missing in base ADR.
    """
    meta = ctx.meta
    path = ctx.path
    all_idx = ctx.all_idx
    section_info = ctx.section_data

    # TOREVIEW: Pins vs IDs: This code resolves the base by ID only
    #           (split("@")[0]), ignoring the pin’s version/hash. That
    #           means it checks against the current indexed body of the
    #           base ADR, not the pinned snapshot.
    # This behavior may diverge from strict “at-pin” validation implied by §8
    # if the base evolved.

    ext = meta.get("extends")
    base = None
    if ext and isinstance(ext, str) and EXTENDS_RX.match(ext):
        base_id = ext.split("@")[0]
        base = all_idx.get(base_id)
    if not base:
        return

    # Collect pointers from fenced YAML blocks: ptr: { key: ... }
    ptr_map = {}
    for blk in section_info.yaml_blocks:
        if isinstance(blk.get("ptr"), dict):
            ptr_map.update(blk["ptr"])
    if not ptr_map:
        return

    # Determine which keys exist in the base ADR
    base_section_info = parse_document_structure(base["body"])
    base_keys = {k for k, _, _ in base_section_info.key_markers}
    if not base_keys:
        """
        Fallback via heading mapping already handled inside legacy parser if
        needed
        """
        pass

    # Emit 304 only for normative section pointers missing in base
    for key in ptr_map.keys():
        if key in NORMATIVE_KEYS and key not in base_keys:
            rpt.add(
                _ERROR_CODE,
                path,
                f"ptr→{key} missing normative section in base "
                f"{base['meta']['id']}",
            )
