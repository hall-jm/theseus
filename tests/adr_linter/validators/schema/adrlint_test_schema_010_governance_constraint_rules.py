# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_010_governance_constraint_rules.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-010 (E): Governance ADR missing required `constraint_rules` section.
Validates that governance class ADRs have required `constraint_rules` section.

Rule: IF class == "governance" AND constraint_rules section missing → ERROR
Section detection via HTML markers (`<!-- key: constraint_rules -->`)
Content validation handled by separate ADR-GOVERN validators
Other classes: constraint_rules section not required
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.schema.schema_010_governance_constraint_rules import (  # noqa: E501
    _ERROR_CODE as _ADR_ERROR_CODE,
)

from ...conftest import (
    _write_text,
    _write_and_ctx,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
    # assert_error_code,
)


def test_adrlint_schema010_governance_missing_constraint_rules_section_triggers(  # noqa: E501
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-010 — governance ADR missing constraint_rules
    section → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "CLI governance decision.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
        "<!-- key: options_considered -->",
        "Options content.",
        "<!-- key: decision_details -->",
        "Decision content.",
        "<!-- key: authority_scope -->",
        "Authority scope content.",
        # constraint_rules section completely missing
        "<!-- key: precedence_mappings -->",
        "Precedence content.",
        "<!-- key: adoption_and_enforcement -->",
        "Adoption content.",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5003-governance-no-constraint-rules.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema010_governance_with_constraint_rules_section_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-010 — governance ADR with constraint_rules
    section → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "engine",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Engine governance decision.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
        "<!-- key: options_considered -->",
        "Options content.",
        "<!-- key: decision_details -->",
        "Decision content.",
        "<!-- key: authority_scope -->",
        "Authority scope content.",
        "<!-- key: constraint_rules -->",
        "```yaml",
        "constraint_rules:",
        "  REQUIRED: ['engine.orchestration']",
        "  FORBIDDEN: ['cli.user_messages']",
        "```",
        "<!-- key: precedence_mappings -->",
        "Precedence content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-with-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema010_governance_empty_constraint_rules_section_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-010 — governance ADR with empty
    constraint_rules section → passes
    Content validation is handled by separate ADR-GOVERN validators
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "services",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Services governance decision.",
        "<!-- key: constraint_rules -->",
        "<!-- Empty constraint rules section - content validation "
        "separate -->",
        "<!-- key: precedence_mappings -->",
        "Precedence content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-empty-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema010_governance_constraint_rules_with_content_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-010 — governance ADR with populated
    constraint_rules → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "other",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Other governance decision.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
        "<!-- key: constraint_rules -->",
        "Machine-readable constraints:",
        "",
        "```yaml",
        "constraint_rules:",
        "  REQUIRED:",
        "    - 'other.misc_processes'",
        "    - 'other.background_tasks'",
        "  FORBIDDEN:",
        "    - 'cli.argument_parsing'",
        "    - 'engine.orchestration'",
        "    - 'services.file_io'",
        "  OWNED_BY:",
        "    - topic: 'shared.logging'",
        "      owner: 'other'",
        "```",
        "",
        "These constraints establish authority boundaries.",
        "<!-- key: precedence_mappings -->",
        "Precedence content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-full-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema010_owner_class_ignores_constraint_rules(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-010 — owner class without
    constraint_rules → ignored by this validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision without constraint_rules section.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
        "<!-- key: decision_details -->",
        "Decision content.",
        # No constraint_rules section - should be ignored for owner class
        "<!-- key: consequences_and_risks -->",
        "Risk content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-no-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema010_delta_class_ignores_constraint_rules(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-010 — delta class without
    constraint_rules → ignored by this validator
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
        "Delta decision without constraint_rules section.",
        # No constraint_rules section - should be ignored for delta class
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "delta-no-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema010_strategy_class_ignores_constraint_rules(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-010 — strategy class without
    constraint_rules → ignored by this validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategy decision without constraint_rules section.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
        "<!-- key: principles -->",
        "Principle content.",
        # No constraint_rules section - should be ignored for strategy class
        "<!-- key: guardrails -->",
        "Guardrail content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-no-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema010_template_class_ignores_constraint_rules(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-010 — template class without
    constraint_rules → ignored by this validator
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
        "<owner-decision>",
        "<!-- key: context_and_drivers -->",
        "<context>",
        # No constraint_rules section - should be ignored for template class
        "<!-- key: decision_details -->",
        "<requirements>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-owner.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema010_style_guide_class_ignores_constraint_rules(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-010 — style-guide class without
    constraint_rules → ignored by this validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "style-guide",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Style guide decision without constraint_rules section.",
        "# Style Guide Content",
        "Various style guide sections...",
        # No constraint_rules section - should be ignored for style-guide class
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "style-guide-no-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema010_governance_constraint_rules_wrong_case_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-010 — governance with wrong case
    HTML marker → error
    Validates exact HTML marker matching
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "CLI governance decision.",
        # Wrong case - should be constraint_rules
        "<!-- key: Constraint_Rules -->",
        "```yaml",
        "constraint_rules:",
        "  REQUIRED: ['cli.user_messages']",
        "```",
        "<!-- key: precedence_mappings -->",
        "Precedence content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-wrong-case-marker.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema010_governance_constraint_rules_typo_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-010 — governance with typo in HTML
    marker → error
    Validates exact HTML marker matching
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "engine",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Engine governance decision.",
        # Missing 's' - should be constraint_rules
        "<!-- key: constraint_rule -->",
        "```yaml",
        "constraint_rules:",
        "  REQUIRED: ['engine.orchestration']",
        "```",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-typo-marker.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema010_governance_minimal_sections_with_constraint_rules_passes(  # noqa: E501
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-010 — governance with minimal sections but
    constraint_rules present → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "services",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Services governance decision.",
        "<!-- key: constraint_rules -->",
        "Minimal constraint rules section present.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-minimal-with-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)
