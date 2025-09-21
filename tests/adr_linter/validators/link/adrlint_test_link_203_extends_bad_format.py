# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/link/adrlint_test_link_203_extends_bad_format.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-LINK-203 (E): Invalid `extends` pin format (must be `@YYYY-MM-DD`
                  or lowercase hex `@[0-9a-f]{7,40}`).
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


def test_adrlint019b_link203_bad_pin_formats(_route_and_reset_workspace):
    """
    Pre-refactored pytest: ADRLINT-019
    Rule being tested: ADR-LINK-203 — malformed or impossible pins → 203
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
        assert _has_code(
            rpt, "ADR-LINK-203"
        ), f"Expected 203 for {extends_val}"
