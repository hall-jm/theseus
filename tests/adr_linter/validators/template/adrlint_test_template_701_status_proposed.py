# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/validators/template/adrlint_test_templt_701_status_proposed.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-TEMPLATE-701 (W): `status` not `Proposed` in a template ADR.
Linting Tests: ADRLINT-043
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report

from ...conftest import (
    _write_and_ctx,
    _good_meta_front_matter,
    _has_code,
)


def test_adrlint043_templt701_status_must_be_proposed(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-043
    Rule being tested: ADR-TEMPLATE-701 — invalid statuses → error
    """
    for i, status in enumerate(["Accepted", "Deprecated", "Superseded", ""]):
        md = (
            _good_meta_front_matter(
                **{
                    "class": "template",
                    "template_of": "owner",
                    "status": status,
                }
            )
            + "Body"
        )
        _, ctx = _write_and_ctx(
            _route_and_reset_workspace, f"ADR-589{i}-template-status.md", md
        )
        rpt = Report()
        run_all(ctx, rpt)
        assert _has_code(
            rpt, "ADR-TEMPLATE-701"
        ), f"Expected 701 for status={status!r}"
