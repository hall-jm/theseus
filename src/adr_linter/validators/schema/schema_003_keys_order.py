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

    # Early exit if no validation needed
    if not expected:
        return

    # 1. Check for duplicate sections (highest priority)
    seen_keys = {}
    duplicates = []
    for key, pos, line in si.key_markers:
        if key in seen_keys:
            duplicates.append((key, seen_keys[key], line))
        else:
            seen_keys[key] = line

    # Report duplicates
    for key, first_line, second_line in duplicates:
        if cls == "template" and template_of:
            rpt.add(
                _ERROR_CODE,
                path,
                f"template for {template_of}: duplicate section '{key}' "
                f"at lines {first_line} and {second_line}",
            )
        else:
            rpt.add(
                _ERROR_CODE,
                path,
                f"duplicate section '{key}' at lines {first_line} and "
                f"{second_line}",
            )

    # 2. Check for missing sections
    missing = [k for k in expected if k not in found_keys]
    if missing:
        if cls == "template" and template_of:
            rpt.add(
                _ERROR_CODE,
                path,
                f"template for {template_of}: missing sections: "
                f"{', '.join(missing)}",
            )
        else:
            rpt.add(
                _ERROR_CODE, path, f"missing sections: {', '.join(missing)}"
            )

    # 3. Check order (only if no missing sections and no duplicates)
    if not missing and not duplicates and si.key_markers:
        # Remove duplicates for order checking while preserving sequence
        unique_found_keys = []
        seen_for_order = set()
        for key in found_keys:
            if key not in seen_for_order:
                unique_found_keys.append(key)
                seen_for_order.add(key)

        # Check if order matches expected
        order_correct = unique_found_keys == expected

        if not order_correct:
            if cls == "template" and template_of:
                rpt.add(
                    _ERROR_CODE,
                    path,
                    f"template for {template_of}: sections out of order. "
                    f"Found: [{', '.join(unique_found_keys)}], "
                    f"Expected: [{', '.join(expected)}]",
                )
            else:
                rpt.add(
                    _ERROR_CODE,
                    path,
                    f"sections out of order. "
                    f"Found: [{', '.join(unique_found_keys)}], "
                    f"Expected: [{', '.join(expected)}]",
                )

    # 4. Handle case where no key markers found at all
    elif not si.key_markers:
        if cls == "template" and template_of:
            rpt.add(
                _ERROR_CODE,
                path,
                f"template for {template_of}: no canonical key markers found",
            )
        else:
            rpt.add(_ERROR_CODE, path, "no canonical key markers found")
