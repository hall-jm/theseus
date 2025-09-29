# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_005_date_format.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-005 (E): Invalid date format (must be `YYYY-MM-DD`) for `date`
                    or `review_by`.
Linting Tests: ADRLINT-004/017
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

from adr_linter.validators.schema.schema_005_date_format import (
    _ERROR_CODE as _ADR_ERROR_CODE,
)


def test_adrlint_schema005_date_format_enforced(_route_and_reset_workspace):
    """
    Pre-refactored pytest: ADRLINT-004
    Rule being tested: ADR-SCHEMA-005 — invalid date formats emit error.
    """
    md = (
        _good_meta_front_matter(
            **{"date": "2025/09/05", "review_by": "2026-13-01"}
        )
        + "Body"
    )
    p = _write_text(
        _route_and_reset_workspace, "docs/adr-new/ADR-9998-bad-dates.md", md
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema005_invalid_date_formats_comprehensive(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-017
    Rule being tested: ADR-SCHEMA-005 — comprehensive invalid date formats.
    """
    invalid_dates = [
        "2025/09/05",
        "05-09-2025",
        "2025-13-01",
        "2025-02-30",
        "25-09-05",
        "2025-9-5",
        "not-a-date",
    ]
    for i, bad in enumerate(invalid_dates):
        md = _good_meta_front_matter(**{"date": bad}) + "Body"
        p = _write_text(
            _route_and_reset_workspace,
            f"docs/adr-new/ADR-556{i}-bad-date.md",
            md,
        )
        ctx = _ctx_from_path(p)
        rpt = Report()
        run_all(ctx, rpt)
        assert _has_code(
            rpt, _ADR_ERROR_CODE
        ), f"Failed to catch invalid date: {bad}"
