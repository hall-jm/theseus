# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_002_class_value.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-002 (E): Invalid class (
                        `owner|delta|strategy|style-guide|template`
                    )
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report

from ...conftest import (
    _write_text,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
)


def test_adrlint022_schema002_invalid_class_values(_route_and_reset_workspace):
    """
    Pre-refactored pytest: ADRLINT-022
    Rule being tested: ADR-SCHEMA-002 — invalid class → error
    """
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
        assert _has_code(rpt, "ADR-SCHEMA-002"), f"Failed: {invalid_class!r}"
