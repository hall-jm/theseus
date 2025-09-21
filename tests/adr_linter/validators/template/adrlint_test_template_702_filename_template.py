# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/validators/template/adrlint_test_templt_702_filename_template.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-TEMPLATE-702 (W): filename does not include `-template-` (discoverability).
Linting Tests: ADRLINT-027
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report

from ...conftest import (
    _write_and_ctx,
    _good_meta_front_matter,
    _has_code,
)


def test_adrlint027_templt702_filename_must_include_template(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-027
    Rule being tested: ADR-TEMPLATE-702 — filename should include -template-
    """
    md = (
        _good_meta_front_matter(
            **{"class": "template", "template_of": "owner"}
        )
        + "Body"
    )
    # bad filename on purpose:
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "docs/adr-new/ADR-5573-bad-name.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-TEMPLATE-702")
