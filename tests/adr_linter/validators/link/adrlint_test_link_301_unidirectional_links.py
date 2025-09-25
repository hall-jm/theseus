# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/link/adrlint_test_link_301_unidirectional_links.py

"""
ADR-0001 · §3, §7.2, §7.3, §7.5, §8, §10.2
ADR-LINK-301 (E): Handle all uni-directional keys (
                      e.g.,
                      `extends`,
                      `governed_by`
                  )
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


_ERROR_CODE = "ADR-LINK-301"


def test_adrlint_link301_extends_without_pin_emits(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-LINK-301 — delta extends without pin → 301
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
    assert _has_code(rpt, _ERROR_CODE)


def test_adrlint_link301_missing_pin_edge_case(_route_and_reset_workspace):
    """
    Rule being tested: ADR-LINK-301 — extends present but unpinned
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
    assert _has_code(rpt, _ERROR_CODE)
