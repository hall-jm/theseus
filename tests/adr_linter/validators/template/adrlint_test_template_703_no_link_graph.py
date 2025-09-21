# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/validators/template/adrlint_test_templt_703_no_link_graph.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-TEMPLATE-703 (E): template participates in link graph (`extends` or
                    `supersedes` non-null).
Linting Tests: ADRLINT-026
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report

from ...conftest import (
    _write_and_ctx,
    _good_meta_front_matter,
    _has_code,
)


def test_adrlint026_templt703_template_must_not_extend(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-026
    Rule being tested: ADR-TEMPLATE-703 — template with extends → error
    """
    md = (
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",
                "extends": "ADR-0001@2025-01-01",
            }
        )
        + "Body"
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "ADR-5572-template-extends.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-TEMPLATE-703")
