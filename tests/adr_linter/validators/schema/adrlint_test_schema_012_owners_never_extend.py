# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_012_owners_never_extend.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-012 (E): Non-Owner ADRs must never use `owners`.
                 e.g., Templates forbidden from defining owners
                       (human authority)
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report

from adr_linter.validators.schema.schema_012_non_owner_no_owners import (
    _ERROR_CODE as _ADR_ERROR_CODE,
)

from ...conftest import (
    _write_text,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
)


# BLOCKER: Test docstring says "must never use `owner`" but validator checks
#          "owners" field
# FIXME: Test filename suggests "owners_never_extend" but validates ownership
#        definition
# REVIEW: Test only covers strategy class - missing delta, governance, template
#         classes


def test_adrlint_schema012_strategy_redefining_owners_is_invalid(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-023a
    Rule being tested: ADR-SCHEMA-012 — Non-owner guide ADRs must not redefine
                       owners.
    """
    # FIXME: This test is limited to 'strategy' ADRs only; during refactoring
    #        behavior changes were allowed; hence this issue is documented,
    #        not fixed
    md = (
        _good_meta_front_matter(
            **{"class": "strategy", "owners": ["Some Team"]}
        )
        + "Body"
    )
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5568-strategy-owners.md",
        md,
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ADR_ERROR_CODE)
