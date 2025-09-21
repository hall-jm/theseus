# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/link/adrlint_test_link_201_extends_missing_pin.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-LINK-201 (E): `extends` missing base or version pin.
Linting Tests: ADRLINT-002/019a
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


def test_adrlint002_link201_extends_without_pin_emits(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-002
    Rule being tested: ADR-LINK-201 — delta extends without pin → 201
    """
    md = (
        _good_meta_front_matter(**{"class": "delta", "extends": "ADR-0001"})
        + "Body"
    )
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-9997-extends-nopin.md",
        md,
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-LINK-201")


def test_adrlint019a_link201_missing_pin_edge_case(_route_and_reset_workspace):
    """
    Pre-refactored pytest: ADRLINT-019
    Rule being tested: ADR-LINK-201 — extends present but unpinned
    """
    md = (
        _good_meta_front_matter(**{"class": "delta", "extends": "ADR-0001"})
        + "Body"
    )
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-9997-extends-unpinned.md",
        md,
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-LINK-201")
