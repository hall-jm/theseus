# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/validators/template/adrlint_test_templt_700_template_of_required.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-TEMPLATE-700 (E): `template_of` missing or invalid (
                        `owner|delta|strategy|style-guide|template`
                    ).
Linting Tests: ADRLINT-025/042
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report

from ...conftest import (
    _write_and_ctx,
    _good_meta_front_matter,
    _has_code,
)


def test_adrlint025_templt700_missing_template_of(_route_and_reset_workspace):
    """
    Pre-refactored pytest: ADRLINT-025
    Rule being tested: ADR-TEMPLATE-700 — template without template_of → error
    """
    md = _good_meta_front_matter(**{"class": "template"}) + "Body"
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "ADR-5570-bad-template.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-TEMPLATE-700")


def test_adrlint042_templt700_invalid_template_of_values(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-042
    Rule being tested: ADR-TEMPLATE-700 — invalid template_of values → error
    """
    invalid = [None, "", "invalid", "Owner", "STRATEGY", 123, []]
    for i, v in enumerate(invalid):
        md = (
            _good_meta_front_matter(**{"class": "template", "template_of": v})
            + "Body"
        )
        _, ctx = _write_and_ctx(
            _route_and_reset_workspace,
            f"ADR-558{i}-invalid-template-of.md",
            md,
        )
        rpt = Report()
        run_all(ctx, rpt)
        assert _has_code(rpt, "ADR-TEMPLATE-700"), f"Expected 700 for {v!r}"
