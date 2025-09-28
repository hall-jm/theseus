# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/template/adrlint_test_template_608_real_values_not_placeholders.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-TEMPLATE-608 (W): Template contains real values instead of placeholders.
Validates that template ADRs use placeholders instead of real values.

Rule: IF class == "template" AND real value patterns detected → WARNING
Templates should use placeholders like <driver>, {option}, [benefit],
YYYY-MM-DD
Real values include: specific dates, version numbers, emails, URLs,
dollar amounts
Non-template classes ignore this validator
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.template.template_608_real_values_not_placeholders import (  # noqa: E501
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


def test_adrlint_template608_specific_date_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — template with
    specific date → warning
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
        "Context with specific date: We need to implement this by 2025-12-31.",
        "<!-- key: decision_details -->",
        "Details content.",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-6008-template-specific-date.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_version_number_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — template with
    version number → warning
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
        "<strategy-decision>",
        "<!-- key: context_and_drivers -->",
        "We are upgrading from Node.js v18.2.1 to handle new requirements.",
        "<!-- key: principles -->",
        "<principles>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-version-number.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_email_address_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — template with
    email address → warning
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
        "<delta-decision>",
        "<!-- key: context_and_drivers -->",
        "Contact admin@example.com for implementation questions.",
        "<!-- key: decision_details -->",
        "<details>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-email-address.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_url_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — template with URL → warning
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
        "<governance-decision>",
        "<!-- key: context_and_drivers -->",
        "Reference documentation at https://docs.example.com/api/v1.",
        "<!-- key: constraint_rules -->",
        "<constraints>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-url.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_dollar_amount_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — template with
    dollar amount → warning
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
        "<style-guide-decision>",
        "<!-- key: context_and_drivers -->",
        "Budget allocation of $50,000 for this initiative.",
        "<!-- key: decision_details -->",
        "<details>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-dollar-amount.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_specific_year_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — template with
    specific year → warning
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
        "Migration scheduled for completion by Q4 2025.",
        "<!-- key: decision_details -->",
        "<details>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-specific-year.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_multiple_real_values_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — template with
    multiple real values → warning
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
        "<strategy-decision>",
        "<!-- key: context_and_drivers -->",
        "Project starts 2025-01-15 with budget $75,000.",
        "Contact team-lead@company.com for details.",
        "<!-- key: principles -->",
        "<principles>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-multiple-real-values.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_angle_bracket_placeholders_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — template with
    angle bracket placeholders → passes
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
        "Context: <context-description>",
        "Drivers: <primary-driver>, <secondary-driver>",
        "<!-- key: decision_details -->",
        "Implementation: <implementation-approach>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-angle-placeholders.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_curly_bracket_placeholders_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — template with
    curly bracket placeholders → passes
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
        "{strategy-description}",
        "<!-- key: context_and_drivers -->",
        "Budget allocation: {budget-amount}",
        "Timeline: {start-date} to {end-date}",
        "<!-- key: principles -->",
        "{strategic-principles}",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-curly-placeholders.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_square_bracket_placeholders_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — template with
    square bracket placeholders → passes
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
        "[delta-summary]",
        "<!-- key: context_and_drivers -->",
        "Contact: [team-email]",
        "Version: [version-number]",
        "<!-- key: decision_details -->",
        "[implementation-details]",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-square-placeholders.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_yyyy_mm_dd_placeholder_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — template with
    YYYY-MM-DD placeholder → passes
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
        "<governance-decision>",
        "<!-- key: context_and_drivers -->",
        "Implementation deadline: YYYY-MM-DD",
        "Review scheduled for: YYYY-MM-DD",
        "<!-- key: constraint_rules -->",
        "<constraints>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-yyyy-mm-dd.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_real_values_in_placeholders_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — template with
    real values inside placeholders → passes
    Context matters: real values within placeholder brackets are acceptable
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
        "<decision based on 2025 planning>",
        "<!-- key: context_and_drivers -->",
        "Budget: <amount like $50,000>",
        "Contact: <email like admin@company.com>",
        "<!-- key: decision_details -->",
        "Reference: <URL like https://docs.example.com>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-real-in-placeholders.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_mixed_content_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — template with
    mixed real/placeholder content → warning
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
        "Project deadline: 2025-06-30",  # Real date
        "Budget: <budget-amount>",  # Placeholder
        "Contact: <team-lead>",  # Placeholder
        "<!-- key: decision_details -->",
        "<implementation-details>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-mixed-content.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_owner_class_ignores_real_values(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — owner class with
    real values → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "We will implement API v2.1.0 by 2025-12-31.",
        "<!-- key: context_and_drivers -->",
        "Budget: $100,000. Contact: admin@company.com",
        "Reference: https://api.company.com/v2",
        "<!-- key: decision_details -->",
        "Implementation details with real values.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-real-values.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_delta_class_ignores_real_values(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — delta class with
    real values → ignored
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
        "Delta modification scheduled for 2025-11-15.",
        "<!-- key: context_and_drivers -->",
        "Version: v3.2.1. Budget impact: $25,000.",
        "<!-- key: decision_details -->",
        "Delta details with real values.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-real-values.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_governance_class_ignores_real_values(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — governance class with
    real values → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "CLI governance effective 2025-10-01.",
        "<!-- key: context_and_drivers -->",
        "Contact: governance@company.com",
        "<!-- key: constraint_rules -->",
        "Constraints with specific dates and contacts.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-real-values.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_strategy_class_ignores_real_values(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — strategy class with
    real values → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategy implementation by Q2 2025.",
        "<!-- key: context_and_drivers -->",
        "Budget: $200,000. Timeline: 2025-01-01 to 2025-06-30.",
        "<!-- key: principles -->",
        "Strategic principles with real values.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "strategy-real-values.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_style_guide_class_ignores_real_values(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — style-guide class with
    real values → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "style-guide",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Style guide updated on 2025-09-15.",
        "<!-- key: context_and_drivers -->",
        "Contact style-team@company.com for questions.",
        "Reference: https://style.company.com/guide",
        "<!-- key: decision_details -->",
        "Style guide with real values.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "style-guide-real-values.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_borderline_patterns_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — template with
    borderline real value patterns → warning
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
        "API endpoint: /api/v1.2/users",  # Version-like pattern
        "Port: 8080",  # Specific port number
        "File: config.json",  # Specific filename
        "<!-- key: decision_details -->",
        "<details>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-borderline-patterns.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template608_generic_placeholders_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-608 — template with
    generic placeholders → passes
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
        "Because <long-range driver>, we choose <strategic direction> "
        "so that <north star>.",
        "<!-- key: context_and_drivers -->",
        "Context: <situation-description>",
        "Drivers: <primary-motivation>, <secondary-factors>",
        "Goals: <what-we-want-to-achieve>",
        "Non-goals: <what-we-explicitly-do-not-want>",
        "<!-- key: constraint_rules -->",
        "```yaml",
        "constraint_rules:",
        "  REQUIRED: ['<scope>.<process>']",
        "  FORBIDDEN: ['<other-scope>.<boundary>']",
        "```",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-generic-placeholders.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)
