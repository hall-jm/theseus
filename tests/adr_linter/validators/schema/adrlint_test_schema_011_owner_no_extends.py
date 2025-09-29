# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_011_owner_no_extends.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-011 (E): Owner ADR must not use `extends`.
Linting Tests: ADRLINT-012/013
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report

from adr_linter.validators.schema.schema_011_owner_no_extends import (
    _ERROR_CODE as _ADR_ERROR_CODE,
)

from ...conftest import (
    _write_text,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
)


def test_adrlint_schema011_owner_adr_extends_any_value_triggers(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-012
    Rule being tested: ADR-SCHEMA-011 — owner ADR must not set extends
                       (any value).
    """
    md = (
        _good_meta_front_matter(
            **{"class": "owner", "extends": "ADR-0001@2025-01-01"}
        )
        + "Body"
    )
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5559-owner-extends.md",
        md,
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema011_owner_adr_extends_empty_string_allowed(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-013
    Rule being tested: ADR-SCHEMA-011 — empty-string extends treated as null
                       (no 012 error per monolith).
    """
    md = _good_meta_front_matter(**{"class": "owner", "extends": ""}) + "Body"
    p = _write_text(
        _route_and_reset_workspace, "docs/adr-new/ADR-5560-owner-empty.md", md
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    # Preserve original assertion from monolith exactly:
    assert not _has_code(rpt, _ADR_ERROR_CODE)
