# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_016_decision_format.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-016 (E): Content formatting does not match documented format.
Validates that non-template ADRs follow proper content formatting for the
`decision_one_liner` section.

Rule: IF class != "template" AND class != "style-guide" AND decision_one_liner
format invalid → ERROR
Enforces "Because X, we choose Y so that Z" structure with real content
         (not placeholders)
Requires single statement (no multiple sentences)
Rejects placeholder patterns (<>, {}, []) in real ADRs
Templates handled by TEMPLATE-606, style-guide exempt
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.schema.schema_016_decision_format import (
    _ERROR_CODE as _ADR_ERROR_CODE,
)

from ...conftest import (
    _write_text,
    _write_and_ctx,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
    assert_error_code,
)


def test_adrlint_schema016_owner_correct_format_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — owner ADR with correct
    "Because X, we choose Y so that Z" format → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Because API response times exceed 200ms under load, we choose Redis "
        "caching so that user experience improves to sub-100ms response "
        "times.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-0016-owner-correct-format.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_delta_correct_format_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — delta ADR with correct format → passes
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
        "Because security requirements changed after pen testing, we choose "
        "OAuth 2.0 with PKCE so that authentication meets enterprise security "
        "standards.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-correct-format.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_governance_correct_format_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — governance ADR with
    correct format → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Because CLI and Engine components both handle error messaging "
        "causing inconsistent user experience, we choose CLI-only error "
        "display authority so that users receive uniform error messages.",
        "<!-- key: constraint_rules -->",
        "Constraint content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-correct-format.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_strategy_correct_format_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — strategy ADR with
    correct format → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Because technical debt prevents rapid feature delivery, we choose "
        "systematic refactoring approach so that development velocity "
        "increases by 40%.",
        "<!-- key: principles -->",
        "Principle content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "strategy-correct-format.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_owner_missing_because_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — owner ADR missing "Because" → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "We choose microservices architecture so that scalability improves.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-missing-because.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_delta_missing_we_choose_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — delta ADR missing "we choose" → error
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
        "Because performance is degraded, PostgreSQL so that queries "
        "run faster.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-missing-we-choose.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_governance_missing_so_that_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — governance ADR missing
    "so that" → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "engine",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Because component boundaries are unclear, we choose explicit "
        "ownership rules.",
        "<!-- key: constraint_rules -->",
        "Constraint content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-missing-so-that.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_strategy_wrong_order_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — strategy ADR with wrong word
    order → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "We choose agile methodology because time-to-market is critical so "
        "that delivery speed increases.",
        "<!-- key: principles -->",
        "Principle content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "strategy-wrong-order.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_owner_multiple_sentences_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — owner ADR with
    multiple sentences → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "This is context. Because API latency exceeds SLA requirements, we "
        "choose caching layer so that response times improve. Additional "
        "details follow.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-multiple-sentences.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_delta_placeholder_content_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — delta ADR with
    placeholder content → error
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
        "Because <performance issues>, we choose <caching solution> so that "
        "<response time improves>.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "delta-placeholder-content.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_governance_curly_bracket_placeholders_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — governance ADR
    with curly bracket placeholders → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "services",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Because {boundary conflicts}, we choose {authority model} so that "
        "{clear ownership}.",
        "<!-- key: constraint_rules -->",
        "Constraint content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-curly-placeholders.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_strategy_square_bracket_placeholders_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — strategy ADR
    with square bracket placeholders → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Because [market pressure], we choose [strategic direction] so that "
        "[competitive advantage].",
        "<!-- key: principles -->",
        "Principle content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-square-placeholders.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_owner_completely_wrong_format_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — owner ADR
    with completely wrong format → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "This ADR describes our decision to implement a new caching system.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-wrong-format.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_template_class_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — template class
    with wrong format → ignored
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
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-ignored.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_style_guide_class_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — style-guide class
    with wrong format → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "style-guide",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Style guide for ADR documentation and formatting standards.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "style-guide-ignored.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_missing_decision_one_liner_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — owner ADR missing decision_one_liner
    section → ignored by validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: context_and_drivers -->",
        "Context content.",
        "<!-- key: decision_details -->",
        "Decision details.",
        # No decision_one_liner section
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-no-decision-one-liner.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_empty_decision_one_liner_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — governance ADR
    with empty decision_one_liner section → ignored by validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "other",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<!-- Empty decision one-liner section -->",
        "<!-- key: constraint_rules -->",
        "Constraint content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-empty-decision-one-liner.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_case_insensitive_format_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — delta ADR with case variations
    in format keywords → passes
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
        "BECAUSE database queries are slow, WE CHOOSE query optimization SO "
        "THAT performance improves by 60%.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-case-variations.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_multiline_format_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — strategy ADR with multiline
    decision_one_liner → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Because current infrastructure cannot handle projected 10x user "
        "growth and maintenance costs are escalating exponentially, we choose "
        "cloud-native microservices architecture with container orchestration "
        "so that scalability and operational efficiency improve dramatically.",
        "<!-- key: principles -->",
        "Principle content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-multiline-format.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_partial_placeholder_real_content_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — owner ADR with partial placeholder
    and real content → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Because API response times exceed SLA requirements, we choose "
        "<caching solution> so that performance meets targets.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-partial-placeholder.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_real_content_with_angle_brackets_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — governance ADR with angle brackets
    in content → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Because error handling is inconsistent between <CLI> and <Engine> "
        "components, we choose CLI-only error authority so that user "
        "experience improves.",
        "<!-- key: constraint_rules -->",
        "Constraint content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-angle-brackets.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema016_no_placeholders_correct_structure_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-016 — owner ADR with correct structure
    and no placeholders → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Because database connection pooling is insufficient under peak load "
        "causing timeout errors, we choose HikariCP connection pool with "
        "optimized settings so that connection availability improves and user "
        "sessions remain stable.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-real-content-correct.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)
