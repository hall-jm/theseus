# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/post_run/adrlint_test_link_220_closure_info.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-LINK-220 (I): Supersede closure: multiple descendants (informational).
Linting Tests: ADRLINT-059
"""

from __future__ import annotations

from adr_linter.services.index import load_files, build_index_from_files
from adr_linter.validators.registry import post_run
from adr_linter.report import Report

from ..conftest import (
    _write_text,
    _good_meta_front_matter,
    _has_code,
)


def test_adrlint031_link220_multiple_descendants_info(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-031
    Rule being tested: ADR-LINK-220 — Supersede closure: multiple descendants
                                      (informational).
    """
    # Base ADR
    base_md = _good_meta_front_matter(**{"id": "ADR-0001"}) + "Base"
    _write_text(
        _route_and_reset_workspace, "docs/adr-new/ADR-0001-base.md", base_md
    )

    # Two children superseding base
    child1_md = (
        _good_meta_front_matter(**{"id": "ADR-0002", "supersedes": "ADR-0001"})
        + "Child 1"
    )
    child2_md = (
        _good_meta_front_matter(**{"id": "ADR-0003", "supersedes": "ADR-0001"})
        + "Child 2"
    )
    _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-0002-child1.md",
        child1_md,
    )
    _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-0003-child2.md",
        child2_md,
    )

    all_files = load_files(_route_and_reset_workspace)
    idx = build_index_from_files(all_files)
    rpt = Report()
    post_run(idx, rpt)
    assert _has_code(rpt, "ADR-LINK-220")
