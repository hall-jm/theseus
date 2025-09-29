# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_021_strategy_no_rollout.py

"""
ADR-SCHEMA-021 — Strategy ADR contains `rollout_backout`.

Enforce that strategy ADRs (and strategy templates) must not include
`rollout_backout` either by key marker or via a heading mapped to that key.
Behavior mirrors the legacy checks in `validate_canonical_keys`.

Ref: ADR-0001 §7.3/§14 · ADR-SCHEMA-021
"""

from __future__ import annotations

from ...parser.structure import map_heading_to_key


# REVIEW: This validation depends on HEADINGS_TO_KEYS being complete
# TODO: Verify all expected keys have corresponding heading patterns
# REVIEW:  See also ADR-SCHEMA-003 for similar REVIEW & TODO
def validate_schema_021_strategy_no_rollout(ctx, rpt) -> None:
    meta = ctx.meta
    path = ctx.path
    si = ctx.section_info

    cls = meta.get("class")
    template_of = meta.get("template_of")
    is_strategy = (cls == "strategy") or (
        cls == "template" and template_of == "strategy"
    )
    if not is_strategy:
        return

    # Key marker present?
    found_keys = [k for k, _, _ in si.key_markers]
    if "rollout_backout" in found_keys:
        line_num = next(
            (ln for k, _, ln in si.key_markers if k == "rollout_backout"),
            None,
        )
        if cls == "template":
            rpt.add(
                "ADR-SCHEMA-021",
                path,
                "strategy template contains rollout_backout key marker",
                line_num,
            )
        else:
            rpt.add(
                "ADR-SCHEMA-021",
                path,
                "strategy contains rollout_backout key marker",
                line_num,
            )
        return  # one finding is sufficient

    # Heading maps to rollout_backout?
    for heading_text, _level, _start, line_num in si.headings:
        if map_heading_to_key(heading_text) == "rollout_backout":
            if cls == "template":
                rpt.add(
                    "ADR-SCHEMA-021",
                    path,
                    f"strategy template contains '{heading_text}' heading",
                    line_num,
                )
            else:
                rpt.add(
                    "ADR-SCHEMA-021",
                    path,
                    f"strategy contains '{heading_text}' heading",
                    line_num,
                )
            break
