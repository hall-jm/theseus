# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_003_keys_order.py

"""
ADR-SCHEMA-003 — Canonical section keys missing or out of order.

Validates:
- Missing sections entirely
- Wrong section order
- Present sections with missing headers
- Present sections with mismatched headers
- Duplicate sections

Ref: ADR-0001 §4/§7.5 · ADR-SCHEMA-003
"""

from __future__ import annotations

# import re

from ...parser.structure import expected_keys_for
from ...constants import (
    validate_section_headers,
)

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
    """
    ADR-SCHEMA-003 — Canonical section keys missing or out of order.

    Validates canonical section structure including both key markers and
    markdown headers.
    """
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

    # Template-specific error prefix
    def error_prefix() -> str:
        if cls == "template" and template_of:
            return f"template for {template_of}: "
        return ""

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
        rpt.add(
            _ERROR_CODE,
            path,
            f"{error_prefix()}duplicate section '{key}' at "
            f"lines {first_line} and {second_line}",
        )

    # 2. Check for missing sections
    missing = [k for k in expected if k not in found_keys]
    if missing:
        rpt.add(
            _ERROR_CODE,
            path,
            f"{error_prefix()}missing sections: {', '.join(missing)}",
        )

    # 3. Validate markdown headers for present sections
    if (
        found_keys and not duplicates
    ):  # Only check headers if sections exist and no duplicates
        header_violations = validate_section_headers(ctx, found_keys)
        for violation in header_violations:
            rpt.add(
                _ERROR_CODE,
                path,
                f"{error_prefix()}{violation}",
            )

    # 4. Check section order (only if no missing sections, duplicates,
    #    or header issues)
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
            rpt.add(
                _ERROR_CODE,
                path,
                f"{error_prefix()}sections out of order. "
                f"Found: [{', '.join(unique_found_keys)}], "
                f"Expected: [{', '.join(expected)}]",
            )

    # 5. Handle case where no key markers found at all
    elif not si.key_markers:
        rpt.add(
            _ERROR_CODE,
            path,
            f"{error_prefix()}no canonical key markers found",
        )
