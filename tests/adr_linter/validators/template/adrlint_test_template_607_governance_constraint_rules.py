# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/template/adrlint_test_template_607_governance_constraint_rules.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-TEMPLATE-607 (E): Governance template missing `constraint_rules`
block placeholder.
Validates that governance template ADRs include required
`constraint_rules` section.

Rule: IF class == "template" AND template_of == "governance" AND
constraint_rules section missing → ERROR
Only applies to governance templates (template_of: governance)
Other template types ignore this constraint (different sections required)
Non-template classes ignore this validator
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.template.template_607_governance_constraint_rules import (  # noqa: E501
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


def test_adrlint_template607_governance_missing_constraint_rules_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — governance template missing
    constraint_rules section → error
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
        "<context>",
        "<!-- key: options_considered -->",
        "<options>",
        "<!-- key: decision_details -->",
        "<details>",
        "<!-- key: authority_scope -->",
        "<authority>",
        # constraint_rules section missing - should trigger error
        "<!-- key: precedence_mappings -->",
        "<precedence>",
        "<!-- key: adoption_and_enforcement -->",
        "<adoption>",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-6007-governance-template-missing-constraint.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template607_governance_with_constraint_rules_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — governance template with
    constraint_rules section → passes
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
        "<context>",
        "<!-- key: authority_scope -->",
        "<authority>",
        "<!-- key: constraint_rules -->",
        "Machine-readable constraints:",
        "",
        "```yaml",
        "constraint_rules:",
        "  REQUIRED:",
        "    - '<scope>.example_process'",
        "  FORBIDDEN:",
        "    - '<other_scope>.example_boundary'",
        "  OWNED_BY:",
        "    - topic: '<shared_topic>'",
        "      owner: '<scope>'",
        "```",
        "",
        "<!-- key: precedence_mappings -->",
        "<precedence>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-with-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template607_governance_empty_constraint_rules_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — governance template with
    empty constraint_rules section → passes
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
        "<!-- key: constraint_rules -->",
        "<!-- Placeholder for constraint rules -->",
        "<!-- key: precedence_mappings -->",
        "<precedence>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-empty-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template607_owner_template_ignores_constraint_rules(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — owner template without
    constraint_rules → ignored by validator
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
        "<!-- key: decision_details -->",
        "<details>",
        # No constraint_rules section - valid for owner template
        "<!-- key: consequences_and_risks -->",
        "<consequences>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-template-no-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template607_delta_template_ignores_constraint_rules(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — delta template without
    constraint_rules → ignored by validator
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
        "<context>",
        # No constraint_rules section - valid for delta template
        "<!-- key: decision_details -->",
        "<details>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "delta-template-no-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template607_strategy_template_ignores_constraint_rules(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — strategy template without
    constraint_rules → ignored by validator
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
        "<context>",
        "<!-- key: principles -->",
        "<principles>",
        # No constraint_rules section - valid for strategy template
        "<!-- key: guardrails -->",
        "<guardrails>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-template-no-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template607_style_guide_template_ignores_constraint_rules(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — style-guide template without
    constraint_rules → ignored by validator
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
        "<context>",
        # No constraint_rules section - valid for style-guide template
        "<!-- key: decision_details -->",
        "<details>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "style-guide-template-no-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template607_owner_class_ignores_constraint_rules(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — owner class without
    constraint_rules → ignored by validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision without constraint_rules.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
        # No constraint_rules section - valid for owner class
        "<!-- key: decision_details -->",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-no-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template607_delta_class_ignores_constraint_rules(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — delta class without
    constraint_rules → ignored by validator
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
        "Delta decision without constraint_rules.",
        # No constraint_rules section - valid for delta class
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "delta-no-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template607_governance_class_ignores_constraint_rules(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — governance class without
    constraint_rules → ignored by validator
    Note: Actual governance ADRs are validated by different validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance decision.",
        "<!-- key: authority_scope -->",
        "Authority content.",
        # Missing constraint_rules - handled by different validator
        "<!-- key: precedence_mappings -->",
        "Precedence content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-no-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template607_strategy_class_ignores_constraint_rules(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — strategy class without
    constraint_rules → ignored by validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategy decision without constraint_rules.",
        "<!-- key: principles -->",
        "Principle content.",
        # No constraint_rules section - valid for strategy class
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


def test_adrlint_template607_invalid_template_of_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — template with invalid
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
        "<!-- key: decision_one_liner -->",
        "<invalid-template-decision>",
        # No constraint_rules section but invalid template_of
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-invalid-template-of.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template607_missing_template_of_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — template with missing
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
        "<!-- key: decision_one_liner -->",
        "<template-decision>",
        # No constraint_rules section but missing template_of
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-missing-template-of.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template607_governance_constraint_rules_wrong_case_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — governance template with
    wrong case constraint rules marker → error
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
        "<!-- key: Constraint_Rules -->",  # Wrong case
        "Wrong case marker",
        "<!-- key: precedence_mappings -->",
        "<precedence>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-wrong-case.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template607_governance_constraint_rules_typo_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — governance template with
    typo in constraint rules marker → error
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
        "<!-- key: constraint_rule -->",  # Missing 's'
        "Typo in marker",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-typo.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template607_governance_minimal_sections_with_constraint_rules_passes(  # noqa: E501
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — governance template with
    minimal sections but constraint_rules present → passes
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
        "<!-- key: constraint_rules -->",
        "Minimal constraint rules placeholder.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-minimal.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template607_governance_template_complex_constraint_rules_passes(  # noqa: E501
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-607 — governance template with
    complex constraint_rules content → passes
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
        "<!-- key: authority_scope -->",
        "<authority>",
        "<!-- key: constraint_rules -->",
        "Complex constraint rules template:",
        "",
        "```yaml",
        "constraint_rules:",
        "  REQUIRED:",
        "    - '<scope>.primary_responsibility'",
        "    - '<scope>.secondary_responsibility'",
        "  FORBIDDEN:",
        "    - '<other_scope_1>.boundary_violation'",
        "    - '<other_scope_2>.another_boundary'",
        "  OWNED_BY:",
        "    - topic: '<shared_topic_1>'",
        "      owner: '<scope>'",
        "    - topic: '<shared_topic_2>'",
        "      owner: '<scope>'",
        "```",
        "",
        "These constraints establish clear authority boundaries.",
        "Replace `<scope>` placeholders with actual scope values.",
        "",
        "<!-- key: precedence_mappings -->",
        "<precedence>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-complex-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)
