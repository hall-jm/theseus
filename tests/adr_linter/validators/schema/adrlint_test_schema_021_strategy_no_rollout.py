# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_021_strategy_no_rollout.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-021 (E): Strategy ADR contains `rollout_backout` (by marker **or**
                    heading `Rollout & Backout`).
Linting Tests: ADRLINT-008/014/041
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


def ignore_test_adrlint008_schema021_strategy_forbids_rollout_backout(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-008
    Rule being tested: ADR-SCHEMA-021 — Strategy ADR forbids
                       'Rollout & Backout' heading.
    """
    md = (
        _good_meta_front_matter(**{"class": "strategy"})
        + "# Heading\n## Rollout & Backout\nContent\n"
    )
    p = _write_text(
        _route_and_reset_workspace, "docs/adr-new/ADR-5556-strategy.md", md
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-SCHEMA-021")


def ignore_test_adrlint014_schema021_strategy_heading_variations(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-014
    Rule being tested: ADR-SCHEMA-021 — Variations of the forbidden heading
                       all trigger.
    """
    cases = [
        "## Rollout and Backout",
        "### Rollout & Backout",
        "## Rollout&Backout",
        "# ROLLOUT & BACKOUT",
    ]
    for i, heading in enumerate(cases):
        md = (
            _good_meta_front_matter(**{"class": "strategy"})
            + f"\n{heading}\nContent"
        )
        p = _write_text(
            _route_and_reset_workspace,
            f"docs/adr-new/ADR-556{i}-strategy-rollout.md",
            md,
        )
        ctx = _ctx_from_path(p)
        rpt = Report()
        run_all(ctx, rpt)
        assert _has_code(
            rpt, "ADR-SCHEMA-021"
        ), f"Failed for heading: {heading}"


def ignore_test_adrlint041_schema021_template_extra_section_rollout_backout(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-041
    Rule being tested: ADR-SCHEMA-021 — Template for strategy including
                       rollout_backout key triggers 021.
                       (Matches monolith behavior.)
    """
    md = (
        _good_meta_front_matter(
            **{"class": "template", "template_of": "strategy"}
        )
        + """
<!-- key: decision_one_liner -->
<short-title>

<!-- key: context_and_drivers -->
<description>

<!-- key: rollout_backout -->
This should trigger SCHEMA-021 for strategy template

<!-- key: principles -->
<principles>
"""
    )
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5586-template-extra.md",
        md,
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-SCHEMA-021")
