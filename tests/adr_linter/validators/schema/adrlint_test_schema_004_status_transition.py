# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_004_status_transition.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-004 (E): Invalid status transition or illegal class change.
Linting Tests: ADRLINT-024/032a
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


def test_adrlint024_schema004_superseded_requires_superseded_by(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-024
    Rule being tested: ADR-SCHEMA-004 — Superseded status requires
                       superseded_by.
    """
    md = _good_meta_front_matter(**{"status": "Superseded"}) + "Body"
    p = _write_text(
        _route_and_reset_workspace, "docs/adr-new/ADR-5569-superseded.md", md
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-SCHEMA-004")


def test_adrlint032a_schema004_deprecated_requires_justification(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-032a
    Rule being tested: ADR-SCHEMA-004 — Deprecated without justification
                       is invalid.
    """
    # TOREVIEW: The use of 032a vs. new id value like 033
    md = _good_meta_front_matter(**{"status": "Deprecated"}) + "Body"
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5575-deprecated-invalid.md",
        md,
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-SCHEMA-004")
