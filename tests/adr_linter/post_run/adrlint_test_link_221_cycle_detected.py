# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/post_run/adrlint_test_link_221_cycle_detected.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-LINK-221 (E): Supersede closure: cycle detected.
Linting Tests: ADRLINT-029
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


def test_adrlint029_link221_supersede_cycle_detection(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-029
    Rule being tested: ADR-LINK-221 — Supersede closure: cycle detected.
    """
    # ADR A <-> B cycle
    adr_a = (
        _good_meta_front_matter(
            **{
                "id": "ADR-0001",
                "supersedes": "ADR-0002",
                "superseded_by": "ADR-0002",
            }
        )
        + "Body A"
    )
    adr_b = (
        _good_meta_front_matter(
            **{
                "id": "ADR-0002",
                "supersedes": "ADR-0001",
                "superseded_by": "ADR-0001",
            }
        )
        + "Body B"
    )
    _write_text(
        _route_and_reset_workspace, "docs/adr-new/ADR-0001-cycle-a.md", adr_a
    )
    _write_text(
        _route_and_reset_workspace, "docs/adr-new/ADR-0002-cycle-b.md", adr_b
    )

    idx = build_index_from_files(load_files(_route_and_reset_workspace))
    rpt = Report()
    post_run(idx, rpt)
    assert _has_code(rpt, "ADR-LINK-221")
