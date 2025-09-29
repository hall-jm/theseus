# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_004_status_transition.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-004 (E): MISNAMED TEST - tests field requirements, not transitions

CRITICAL: Test name claims "status_transition" but only tests field
          requirements.

WHAT THESE TESTS ACTUALLY VALIDATE:
- Superseded status must have non-empty superseded_by field
- Deprecated status must have superseded_by OR change_history justification
- Single-file field requirement validation only

WHAT ADR-0001 §14 SPECIFICATION SAYS SCHEMA-004 SHOULD TEST:
- "Invalid status transition or illegal class change"
- Status state machine transitions per VALID_STATUS_TRANSITIONS
- Prevention of illegal class changes

MISSING TEST COVERAGE:
- BLOCKER: No actual transition validation
           (Proposed→Accepted, Accepted→Deprecated, etc.)
- BLOCKER: No class change validation (owner→strategy should fail)
- FIXME: No invalid transition tests (Superseded→Proposed should fail)
- TODO: No tests for valid transitions (Proposed→Accepted should pass)

ARCHITECTURE LIMITATION:
Current single-file test approach cannot validate actual transitions without
cross-file comparison or version history simulation.

FUTURE TEST EXPANSION NEEDED:
1. Rename current tests to reflect actual behavior (field requirements)
2. Add transition validation tests when validator architecture supports it
3. Add class change validation tests
4. Mock or simulate ADR version changes for transition testing

STATUS: Tests work for current limited validator but completely miss
        specification requirements.
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report

from adr_linter.validators.schema.schema_004_status_field_requirements import (
    _ERROR_CODE as _ADR_ERROR_CODE,
)


from ...conftest import (
    _write_text,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
)

# CRITICAL: Test name claims "status_transition" but only tests field
#           requirements.


# MISSING TEST COVERAGE:
# BLOCKER: No actual transition validation
#          (Proposed→Accepted, Accepted→Deprecated, etc.)
# BLOCKER: No class change validation (owner→strategy should fail)
# FIXME: No invalid transition tests (Superseded→Proposed should fail)
# TODO: No tests for valid transitions (Proposed→Accepted should pass)


def test_adrlint_schema004_superseded_requires_superseded_by(
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
    assert _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_deprecated_requires_justification(
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
    assert _has_code(rpt, _ADR_ERROR_CODE)
