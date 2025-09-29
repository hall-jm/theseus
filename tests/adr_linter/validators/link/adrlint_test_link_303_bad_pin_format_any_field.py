# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/link/adrlint_test_link_303_bad_pin_format_any_field.py

"""
ADR-0001 · §8 (regex), §10.2/§10.1 (where pins appear)
ADR-LINK-303 (E): Invalid pin format for any relationship field (
                      e.g.,
                      extends,
                      supersedes,
                      governed_by,
                      informs
                  )
Linting Tests: ADRLINT-019b
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


_ERROR_CODE = "ADR-LINK-303"


def test_adrlint_link303_bad_pin_formats(_route_and_reset_workspace):
    """
    Pre-refactored pytest: ADRLINT-019
    Rule being tested: ADR-LINK-303 — malformed or impossible pins → 203
    """
    cases = [
        "ADR-0001@2025-13-01",
        "ADR-0001@DEADBEEF",
        "ADR-0001@abcde",
        "ADR-0001@",  # empty pin
    ]
    for i, extends_val in enumerate(cases):
        md = (
            _good_meta_front_matter(
                **{"class": "delta", "extends": extends_val}
            )
            + "Body"
        )
        p = _write_text(
            _route_and_reset_workspace,
            f"docs/adr-new/ADR-557{i}-extends-bad.md",
            md,
        )
        ctx = _ctx_from_path(p)
        rpt = Report()
        run_all(ctx, rpt)
        assert _has_code(rpt, _ERROR_CODE), f"Expected 203 for {extends_val}"
