# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/delta/delta_300_override_target_missing.py

"""ADR-DELTA-300 — Override targets non-existent key in base.

Ref: ADR-0001 §8 (Precedence) and §14 ADR-DELTA-300
Behavior mirrors the legacy check in validate_links_enhanced().
"""

from __future__ import annotations

from ...constants import EXTENDS_RX
from ...parser.structure import parse_document_structure


def validate_delta_300_override_target_missing(ctx, rpt) -> None:
    """
    Emit ADR-DELTA-300 for overrides of keys not present in the base ADR.
    """
    meta = ctx.meta
    path = ctx.path
    all_idx = ctx.all_idx
    section_data = ctx.section_data

    ext = meta.get("extends")
    base = None

    # print(f"\n- [VAL DELTA-300]: ext = {ext}")
    # print(f"\n- [VAL DELTA-300]: base = {base}")

    if ext and isinstance(ext, str) and EXTENDS_RX.match(ext):
        base_id = ext.split("@")[0]
        base = all_idx.get(base_id)

    if not base:
        # print("\n- [VAL DELTA-300]: if not base -> returning")
        return

    overrides = {}

    # Old way:
    """
    for blk in section_data.yaml_blocks:
        if isinstance(blk.get("overrides"), dict):
            overrides.update(blk["overrides"])
    """

    # New way (what it should be):
    # Governance documentation rewrite and refactoring changed how
    # YAML blocks are structured
    for blk in section_data.yaml_blocks:
        if blk.get("kind") == "overrides" and isinstance(
            blk.get("data"), dict
        ):
            if "overrides" in blk["data"]:
                overrides.update(blk["data"]["overrides"])

    if not overrides:
        # print(f"\n- [VAL DELTA-300]: if not overrides -> returning")
        # print(f"\n- [VAL DELTA-300]: ctx.section_data - {section_data}")
        return

    # print(f"\n- [VAL DELTA-300]: overrides = {overrides}")

    base_si = parse_document_structure(base["body"])
    base_keys = {k for k, _, _ in base_si.key_markers}

    for key in overrides.keys():
        if key not in base_keys:
            rpt.add(
                "ADR-DELTA-300",
                path,
                f"override→{key} not found in base {base['meta']['id']}",
            )
