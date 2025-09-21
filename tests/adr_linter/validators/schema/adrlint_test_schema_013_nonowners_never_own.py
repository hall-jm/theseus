# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_013_nonowners_never_own.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-013 (E): Non-Owner ADRs must identify ADR ownership
Linting Tests: ADRLINT-020/023b
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


def test_adrlint020_schema013_delta_defines_owners_triggers(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-020
    Rule being tested: ADR-SCHEMA-013 — delta ADR with owners triggers
                       identify-ownership rule.
    """
    md = (
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-01-01",
                "owners": ["Team A"],
            }
        )
        + "Body"
    )
    p = _write_text(
        _route_and_reset_workspace, "docs/adr-new/ADR-5565-delta-owners.md", md
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-SCHEMA-013")


def test_adrlint023b_schema013_strategy_requires_owners_ptr(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-023b
    Rule being tested: ADR-SCHEMA-013 — strategy ADR must include owner
                       pointer.
    """
    md = (
        _good_meta_front_matter(
            **{"class": "strategy", "owners": ["Some Team"]}
        )
        + "Body"
    )
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5568-strategy-owners-b.md",
        md,
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-SCHEMA-013")
