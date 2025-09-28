# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/template/adrlint_test_template_606_content_formatting.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-TEMPLATE-606 (W): Content formatting does not match documented format.
Validates that template ADRs follow proper content formatting for the
`decision_one_liner` section.

Rule: IF class == "template" AND decision_one_liner section exists AND
format != "Because X, we choose Y so that Z" → WARNING
Validates explicit format: "Because <driver>, we choose <option> so that
<benefit>."
Accepts placeholder patterns: <angle>, {curly}, [square] brackets
Only validates decision_one_liner section (other sections deferred to future)
Non-template classes ignore this validator
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.template.template_606_content_formatting import (
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


def test_adrlint_template606_correct_angle_bracket_format_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template with correct
    "Because <X>, we choose <Y> so that <Z>" format → passes
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
        "Because <driver>, we choose <option> so that <benefit>.",
        "<!-- key: context_and_drivers -->",
        "<context>",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-6006-template-correct-format.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_correct_curly_bracket_format_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template with correct
    "Because {X}, we choose {Y} so that {Z}" format → passes
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
        "Because {long-range driver}, we choose {strategic direction} so "
        "that {north star}.",
        "<!-- key: context_and_drivers -->",
        "{context}",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-curly-format.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_correct_square_bracket_format_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template with correct
    "Because [X], we choose [Y] so that [Z]" format → passes
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
        "Because [driver], we choose [option] so that [benefit].",
        "<!-- key: context_and_drivers -->",
        "[context]",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-square-format.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_descriptive_placeholders_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template with descriptive
    placeholders in correct format → passes
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
        "Because <performance degradation in user authentication>, we "
        "choose <implement caching layer> so that "
        "<reduce response time by 80%>.",
        "<!-- key: constraint_rules -->",
        "<constraints>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-descriptive-placeholders.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_multiline_format_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template with multiline
    decision_one_liner in correct format → passes
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
        "Because <complex system integration requirements",
        "and performance constraints>, we choose <microservices architecture",
        "with event-driven communication> so that <scalability and "
        "maintainability",
        "are improved>.",
        "<!-- key: context_and_drivers -->",
        "<context>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-multiline-format.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_missing_because_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template
    missing "Because" → warning
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
        "We choose <option> so that <benefit>.",
        "<!-- key: context_and_drivers -->",
        "<context>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-missing-because.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_missing_we_choose_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template
    missing "we choose" → warning
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
        "Because <driver>, <option> so that <benefit>.",
        "<!-- key: context_and_drivers -->",
        "<context>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-missing-we-choose.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_missing_so_that_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template
    missing "so that" → warning
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
        "Because <driver>, we choose <option> <benefit>.",
        "<!-- key: context_and_drivers -->",
        "<context>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-missing-so-that.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_wrong_order_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template
    with wrong word order → warning
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
        "We choose <option> because <driver> so that <benefit>.",
        "<!-- key: constraint_rules -->",
        "<constraints>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-wrong-order.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_multiple_sentences_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template
    with multiple sentences → warning
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
        "This is a decision. Because <driver>, we choose <option> so that "
        "<benefit>. Additional text.",
        "<!-- key: context_and_drivers -->",
        "<context>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-multiple-sentences.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_partial_pattern_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template
    with partial pattern → warning
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
        "Because we need better performance, choose caching.",
        "<!-- key: context_and_drivers -->",
        "<context>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-partial-pattern.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_completely_wrong_format_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template
    with completely wrong format → warning
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
        "This template describes the strategic direction for our project.",
        "<!-- key: context_and_drivers -->",
        "<context>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-wrong-format.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_missing_decision_one_liner_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template
    missing decision_one_liner section → ignored by validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "delta",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: context_and_drivers -->",
        "<context>",
        "<!-- key: decision_details -->",
        "<details>",
        # No decision_one_liner section
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-no-decision-one-liner.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_empty_decision_one_liner_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template
    with empty decision_one_liner section → ignored by validator
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
        "<!-- Empty decision one-liner section -->",
        "<!-- key: constraint_rules -->",
        "<constraints>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-empty-decision-one-liner.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_owner_class_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — owner class
    with wrong format → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "We will implement API v2.0 for better performance.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-wrong-format.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_delta_class_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — delta class
    with wrong format → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Delta modification to improve system reliability.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-wrong-format.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_governance_class_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — governance class
    with wrong format → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "CLI governance defines user interaction boundaries.",
        "<!-- key: constraint_rules -->",
        "Constraint content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-wrong-format.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_strategy_class_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — strategy class
    with wrong format → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategic direction for platform modernization.",
        "<!-- key: principles -->",
        "Principle content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "strategy-wrong-format.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_style_guide_class_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — style-guide class
    with wrong format → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "style-guide",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Style guide for ADR documentation standards.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "style-guide-wrong-format.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_case_insensitive_format_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template with case variations
    in format keywords → passes
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
        "BECAUSE <driver>, WE CHOOSE <option> SO THAT <benefit>.",
        "<!-- key: context_and_drivers -->",
        "<context>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-case-variations.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_mixed_placeholder_types_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template with mixed placeholder
    bracket types → passes
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
        "Because {long-range driver}, we choose <strategic option> "
        "so that [north star benefit].",
        "<!-- key: context_and_drivers -->",
        "<context>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-mixed-placeholders.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template606_no_placeholders_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-606 — template with format but no
    placeholders → warning
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
        "Because performance is poor, we choose caching so that "
        "speed improves.",
        "<!-- key: context_and_drivers -->",
        "<context>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-no-placeholders.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)
