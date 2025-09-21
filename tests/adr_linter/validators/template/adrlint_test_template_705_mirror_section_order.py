# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/validators/template/adrlint_test_templt_705_mirror_section_order.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-TEMPLT-705 (W): template does not mirror canonical section order of
                    `template_of` (same keys, same order).
Linting Tests: ADRLINT-034
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report

from ...conftest import (
    _write_and_ctx,
    _good_meta_front_matter,
    _has_code,
)


def test_adrlint034_templt705_section_order_mismatch(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-034
    Rule being tested: ADR-TEMPLATE-705 — section order mismatch → error
    """
    md = (
        _good_meta_front_matter(
            **{"class": "template", "template_of": "owner"}
        )
        + """
<!-- key: decision_details -->
Details first (wrong order for owner template)

<!-- key: decision_one_liner -->
One-liner second (should be first)
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "ADR-5577-template-order.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-TEMPLATE-705")
