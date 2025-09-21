# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_003_keys_order.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-003 (E): Canonical section keys missing or out of order.
Linting Tests: ADRLINT-009/015/046/047/048/049/051
"""


from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report

from ...conftest import (
    _write_text,
    _write_and_ctx,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
    assert_error_code,
)


def test_adrlint009_schema003_canonical_keys_out_of_order_emits(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-009
    Rule being tested: ADR-SCHEMA-003 — canonical keys out of order → error
    """
    md = [
        _good_meta_front_matter(**{"class": "owner"}),
        "<!-- key: decision_details -->",
        "Details first (wrong).",
        "<!-- key: decision_one_liner -->",
        "One-liner after (wrong).",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5557-order.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-SCHEMA-003")


def test_adrlint015_schema003_template_incomplete_triggers_schema(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-015
    Rule being tested: ADR-SCHEMA-003 — template inherits target keys; missing
                       keys → error
    """
    md_incomplete = (
        _good_meta_front_matter(
            **{"class": "template", "template_of": "owner"}
        )
        + "<!-- key: decision_one_liner -->\nContent only has 1 key, needs 10"
    )
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-incomplete.md", md_incomplete
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, "ADR-SCHEMA-003")


def test_adrlint046_schema003_debug_template_validation(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-046
    Rule being tested: ADR-SCHEMA-003 — wrong order in template → error
    """
    md = (
        _good_meta_front_matter(
            **{"class": "template", "template_of": "owner"}
        )
        + """
<!-- key: decision_details -->
Wrong order

<!-- key: decision_one_liner -->
Should be first
"""
    )
    p, ctx = _write_and_ctx(_route_and_reset_workspace, "debug.md", md)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-SCHEMA-003")


def test_adrlint047_schema003_template_missing_keys_triggers(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-047
    Rule being tested: ADR-SCHEMA-003 — template with missing canonical
                       keys → error
    """
    md = (
        _good_meta_front_matter(
            **{"class": "template", "template_of": "owner"}
        )
        + """
<!-- key: decision_details -->
Only has 2 keys when owner template should have 10

<!-- key: decision_one_liner -->
Missing 8 other required owner keys
"""
    )

    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-missing-keys.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-SCHEMA-003")


def test_adrlint048_schema003_template_wrong_section_order_fails(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-048
    Rule being tested: ADR-SCHEMA-003 — wrong section order → error
    """
    md = (
        _good_meta_front_matter(
            **{"class": "template", "template_of": "owner"}
        )
        + """
<!-- key: decision_details -->
Details first (wrong order for owner template)

<!-- key: decision_one_liner -->
One-liner second (should be first)

<!-- key: context_and_drivers -->
Context third (should be second)
"""
    )
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-wrong-order.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, "ADR-SCHEMA-003")


def test_adrlint049_schema003_template_correct_order_passes(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-049
    Rule being tested: ADR-SCHEMA-003 — correct order passes
    """
    md = (
        _good_meta_front_matter(
            **{"class": "template", "template_of": "owner"}
        )
        + """
<!-- key: decision_one_liner -->
<short-title>

<!-- key: context_and_drivers -->
<description>

<!-- key: options_considered -->
<options>

<!-- key: decision_details -->
<requirements>

<!-- key: consequences_and_risks -->
<risks>

<!-- key: rollout_backout -->
<deployment>

<!-- key: implementation_notes -->
<notes>

<!-- key: evidence_and_links -->
<links>

<!-- key: glossary -->
<terms>

<!-- key: related_adrs -->
<related>
"""
    )
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-correct-order.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, "ADR-SCHEMA-003")


def test_adrlint051_schema003_strategy_template_inherits_strategy_keys(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-051
    Rule being tested: ADR-SCHEMA-003 — strategy template:
                       wrong key → error + message mentions strategy
    """
    md = (
        _good_meta_front_matter(
            **{"class": "template", "template_of": "strategy"}
        )
        + """
<!-- key: decision_details -->
Wrong key for strategy template (should use principles)

<!-- key: decision_one_liner -->
One-liner
"""
    )
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "strategy-template-wrong.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, "ADR-SCHEMA-003")
    # Verify error mentions strategy template context
    error_messages = [
        item[3] for item in rpt.items if item[1] == "ADR-SCHEMA-003"
    ]
    assert any(
        "template canonical keys issue for strategy" in m
        for m in error_messages
    )
