# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_003_keys_order.py

"""
ADR-SCHEMA-003 — Canonical section keys missing or out of order.

Behavior mirrors the legacy implementation, including template-specific
messages when `class: template` with a valid `template_of`.

Ref: ADR-0001 §4/§7.5 · ADR-SCHEMA-003
"""

from __future__ import annotations

from ...parser.structure import expected_keys_for


_ERROR_CODE = "ADR-SCHEMA-003"

# REVIEW: This validation depends on HEADINGS_TO_KEYS being complete
# TODO: Verify all expected keys have corresponding heading patterns

# BLOCKER: Tests missing governance class validation entirely
# FIXME: No test coverage for governance template validation
# TODO: Verify expected_keys_for() supports all 6 classes from
#       VALID_ADR_CLASSES
# REVIEW: Test hardcodes owner keys count - should derive from canonical
#         structure


def validate_schema_003_keys_order(ctx, rpt) -> None:
    meta = ctx.meta
    path = ctx.path
    si = ctx.section_data

    cls = meta.get("class", "")
    template_of = meta.get("template_of")
    found_keys = [k for k, _, _ in si.key_markers]
    expected = expected_keys_for(cls, template_of)

    if expected and si.key_markers:
        # Order check (single pass through found markers)
        expected_idx = 0
        for key, _pos, _ln in si.key_markers:
            if expected_idx < len(expected) and key == expected[expected_idx]:
                expected_idx += 1
        correct_order = expected_idx == len(expected)
        missing = [k for k in expected if k not in found_keys]

        if missing or not correct_order:
            issue = ", ".join(missing) if missing else "order mismatch"
            if cls == "template" and template_of:
                rpt.add(
                    _ERROR_CODE,
                    path,
                    "template canonical keys issue for "
                    f"{template_of}: {issue}",
                    # f"{template_of}: {issue} - expected vs. found_keys: "
                    # f"{expected}\n  vs. \n{found_keys}",
                )
            else:
                rpt.add(
                    _ERROR_CODE,
                    path,
                    f"canonical keys issue: {issue}",
                )
    elif expected:
        if cls == "template" and template_of:
            rpt.add(
                "ADR-SCHEMA-003",
                path,
                f"template for {template_of}: no canonical "
                "key markers found",
            )
        else:
            rpt.add(_ERROR_CODE, path, "no canonical key markers found")
