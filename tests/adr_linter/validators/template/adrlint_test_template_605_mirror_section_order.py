# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/template/adrlint_test_template_605_mirror_section_order.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-TEMPLATE-605 (W): template does not mirror canonical section order
of `template_of` (same keys, same order).
Validates that template class ADRs mirror the canonical section order
of their `template_of` class.

Rule: IF class == "template" AND section order != canonical order
for template_of → WARNING
Uses `expected_keys_for(template_of)` to get canonical section order
from constants. Compares expected vs actual section order for present
sections only. Valid template_of values: owner|delta|governance|
strategy|style-guide
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.template.template_605_mirror_section_order import (
    _ERROR_CODE as _ADR_ERROR_CODE,
)

from ...conftest import (
    _write_text,
    _write_and_ctx,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
    assert_warning_code,
)


def test_adrlint_template605_owner_template_correct_order_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — owner template with correct
    section order → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<decision>",
        "<!-- key: context_and_drivers -->",
        "<context>",
        "<!-- key: options_considered -->",
        "<options>",
        "<!-- key: decision_details -->",
        "<details>",
        "<!-- key: consequences_and_risks -->",
        "<consequences>",
        "<!-- key: implementation_notes -->",
        "<implementation>",
        "<!-- key: rollout_backout -->",
        "<rollout>",
        "<!-- key: evidence_and_links -->",
        "<evidence>",
        "<!-- key: glossary -->",
        "<glossary>",
        "<!-- key: related_adrs -->",
        "<related>",
        "<!-- key: license -->",
        "<license>",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-6005-owner-template-correct.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_owner_template_incorrect_order_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — owner template with incorrect
    section order → warning
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_details -->",
        "<details> (wrong order - should be 4th)",
        "<!-- key: decision_one_liner -->",
        "<decision> (wrong order - should be 1st)",
        "<!-- key: context_and_drivers -->",
        "<context>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-template-wrong-order.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_strategy_template_correct_order_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — strategy template with correct
    section order → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "strategy",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<decision>",
        "<!-- key: context_and_drivers -->",
        "<context>",
        "<!-- key: options_considered -->",
        "<options>",
        "<!-- key: decision_details -->",
        "<details>",
        "<!-- key: principles -->",
        "<principles>",
        "<!-- key: guardrails -->",
        "<guardrails>",
        "<!-- key: consequences_and_risks -->",
        "<consequences>",
        "<!-- key: implementation_notes -->",
        "<implementation>",
        "<!-- key: north_star_metrics -->",
        "<metrics>",
        "<!-- key: evidence_and_links -->",
        "<evidence>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-template-correct.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_strategy_template_incorrect_order_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — strategy template with incorrect
    section order → warning
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "strategy",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: principles -->",
        "<principles> (wrong order - should come after decision_details)",
        "<!-- key: decision_one_liner -->",
        "<decision>",
        "<!-- key: context_and_drivers -->",
        "<context>",
        "<!-- key: decision_details -->",
        "<details>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-template-wrong-order.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_governance_template_correct_order_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — governance template with correct
    section order → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "governance",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<decision>",
        "<!-- key: context_and_drivers -->",
        "<context>",
        "<!-- key: options_considered -->",
        "<options>",
        "<!-- key: decision_details -->",
        "<details>",
        "<!-- key: authority_scope -->",
        "<authority>",
        "<!-- key: constraint_rules -->",
        "<constraints>",
        "<!-- key: precedence_mappings -->",
        "<precedence>",
        "<!-- key: adoption_and_enforcement -->",
        "<adoption>",
        "<!-- key: evidence_and_links -->",
        "<evidence>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-correct.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_governance_template_incorrect_order_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — governance template with
    incorrect section order → warning
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "governance",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: constraint_rules -->",
        "<constraints> (wrong order - should come after authority_scope)",
        "<!-- key: decision_one_liner -->",
        "<decision>",
        "<!-- key: authority_scope -->",
        "<authority>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-wrong-order.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_delta_template_correct_order_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — delta template with correct
    section order → passes
    Delta templates inherit base ADR sections via extends mechanism
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "delta",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<decision>",
        "<!-- key: context_and_drivers -->",
        "<context>",
        "<!-- key: options_considered -->",
        "<options>",
        "<!-- key: decision_details -->",
        "<details>",
        "<!-- key: evidence_and_links -->",
        "<evidence>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-template-correct.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_delta_template_incorrect_order_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — delta template with incorrect
    section order → warning
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "delta",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: evidence_and_links -->",
        "<evidence> (wrong order - should come last)",
        "<!-- key: decision_one_liner -->",
        "<decision>",
        "<!-- key: context_and_drivers -->",
        "<context>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "delta-template-wrong-order.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_style_guide_template_correct_order_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — style-guide template with
    correct section order → passes
    Style-guide class has flexible section ordering per ADR-0001 §4
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "style-guide",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<decision>",
        "<!-- key: context_and_drivers -->",
        "<context>",
        "<!-- key: options_considered -->",
        "<options>",
        "<!-- key: decision_details -->",
        "<details>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "style-guide-template-correct.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_owner_template_subset_correct_order_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — owner template with subset
    of sections in correct order → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<decision>",
        "<!-- key: context_and_drivers -->",
        "<context>",
        "<!-- key: decision_details -->",
        "<details>",
        "<!-- key: license -->",
        "<license>",
        # Missing some sections but present ones are in correct order
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-template-subset-correct.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_strategy_template_subset_incorrect_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — strategy template with subset
    of sections in incorrect order → warning
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "strategy",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: guardrails -->",
        "<guardrails> (wrong order - should come after principles)",
        "<!-- key: decision_one_liner -->",
        "<decision>",
        "<!-- key: principles -->",
        "<principles>",
        # Subset with incorrect order
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-template-subset-wrong.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_missing_template_of_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — template with missing
    template_of → ignored by validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                # template_of missing
            }
        ),
        "<!-- key: decision_details -->",
        "<details>",
        "<!-- key: decision_one_liner -->",
        "<decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-missing-template-of.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_invalid_template_of_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — template with invalid
    template_of → ignored by validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "invalid_type",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_details -->",
        "<details>",
        "<!-- key: decision_one_liner -->",
        "<decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-invalid-template-of.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_owner_class_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — owner class with wrong
    section order → ignored by validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_details -->",
        "Details first (wrong order for owner but not validated here)",
        "<!-- key: decision_one_liner -->",
        "Decision second",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-wrong-order.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_delta_class_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — delta class with wrong
    section order → ignored by validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: evidence_and_links -->",
        "Evidence first (wrong order but not validated here)",
        "<!-- key: decision_one_liner -->",
        "Decision second",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-wrong-order.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_governance_class_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — governance class with wrong
    section order → ignored by validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
            }
        ),
        "<!-- key: constraint_rules -->",
        "Constraints first (wrong order but not validated here)",
        "<!-- key: decision_one_liner -->",
        "Decision second",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-wrong-order.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_strategy_class_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — strategy class with wrong
    section order → ignored by validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: north_star_metrics -->",
        "Metrics first (wrong order but not validated here)",
        "<!-- key: decision_one_liner -->",
        "Decision second",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "strategy-wrong-order.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_style_guide_class_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — style-guide class with wrong
    section order → ignored by validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "style-guide",
            }
        ),
        "<!-- key: glossary -->",
        "Glossary first (wrong order but not validated here)",
        "<!-- key: decision_one_liner -->",
        "Decision second",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "style-guide-wrong-order.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template605_template_no_sections_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-605 — template with no sections
    → passes (no sections to validate order)
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",
                "owners_ptr": "ADR-0001",
            }
        ),
        "# Template Content",
        "This template has no section markers.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-no-sections.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)
