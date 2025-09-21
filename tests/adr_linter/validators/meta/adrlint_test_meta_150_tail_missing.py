# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/meta/adrlint_test_meta_150_tail_missing.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-META-150 (I): `llm_tail` missing (optional).
Linting Tests: ADRLINT-044
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report

from ...conftest import (
    _write_and_ctx,
    _good_meta_front_matter,
    _has_code,
)


def test_adrlint044_meta150_llm_tail_missing(_route_and_reset_workspace):
    """
    Pre-refactored pytest: ADRLINT-044
    Rule being tested: ADR-META-150 — Missing llm_tail → error
    """
    md = _good_meta_front_matter() + "Body without llm_tail"
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "ADR-9990-no-tail.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-META-150")
