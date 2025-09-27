# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_002_class_value.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-002 (E): Invalid class (
                        `delta|governance|owner|strategy|style-guide|template`
                    )
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.schema.schema_002_class_value import (
    _ERROR_CODE as _ADR_ERROR_CODE,
)

from ...conftest import (
    _write_text,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
)


# FIXME: Test docstring was missing 'governance' class - documentation drift
#        from validator implementation
# TODO: Consider positive test cases to verify all valid classes are accepted
# TOREVIEW: Test uses hardcoded invalid cases - could reference
#           VALID_ADR_CLASSES for maintenance


def test_adrlint_schema002_invalid_class_values(_route_and_reset_workspace):
    """
    Pre-refactored pytest: ADRLINT-022
    Rule being tested: ADR-SCHEMA-002 — invalid class → error
    """

    # TODO: Could import VALID_ADR_CLASSES and test against complement set
    invalid_classes = ["invalid", "Owner", "STRATEGY", "", None, 123]
    for i, invalid_class in enumerate(invalid_classes):
        md = _good_meta_front_matter(**{"class": invalid_class}) + "Body"
        p = _write_text(
            _route_and_reset_workspace,
            f"docs/adr-new/ADR-567{i}-invalid-class.md",
            md,
        )
        ctx = _ctx_from_path(p)
        rpt = Report()
        run_all(ctx, rpt)
        assert _has_code(rpt, _ADR_ERROR_CODE), f"Failed: {invalid_class!r}"
