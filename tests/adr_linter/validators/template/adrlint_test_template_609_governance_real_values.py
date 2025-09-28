# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/template/adrlint_test_template_609_governance_real_values.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-TEMPLATE-609 (W): Governance template contains real values instead
of placeholders.
Validates that governance template ADRs use placeholders instead of real
governance values in constraint_rules sections.

Rule: IF class == "template" AND template_of == "governance" AND
constraint_rules contains real values → WARNING
Real values include: actual scope names (cli, engine, services, other),
real topic patterns (cli.user_messages)
Placeholders include: <scope>, {topic}, [shared-concern] bracket patterns
Only applies to governance templates with constraint_rules YAML blocks
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.template.template_609_governance_real_values import (  # noqa: E501
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


def test_adrlint_template609_real_scope_values_in_required_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — governance template with real
    scope values in REQUIRED → warning
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
        "```yaml",
        "constraint_rules:",
        "  REQUIRED:",
        "    - 'cli.argument_parsing'",  # Real scope value
        "    - 'engine.orchestration'",  # Real scope value
        "  FORBIDDEN: []",
        "```",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-6009-governance-template-real-scopes.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template609_real_scope_values_in_forbidden_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — governance template with real
    scope values in FORBIDDEN → warning
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
        "```yaml",
        "constraint_rules:",
        "  REQUIRED: []",
        "  FORBIDDEN:",
        "    - 'services.file_io'",  # Real scope value
        "    - 'other.background_tasks'",  # Real scope value
        "```",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-real-forbidden.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template609_real_scope_values_in_owned_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — governance template with real
    scope values in OWNED_BY → warning
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
        "```yaml",
        "constraint_rules:",
        "  REQUIRED: []",
        "  FORBIDDEN: []",
        "  OWNED_BY:",
        "    - topic: 'shared.exit_code_mapping'",  # Real topic pattern
        "      owner: 'engine'",  # Real scope value
        "    - topic: 'cli.user_messages'",  # Real topic pattern
        "      owner: 'cli'",  # Real scope value
        "```",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-real-owned-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template609_mixed_real_placeholder_values_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — governance template with mixed
    real and placeholder values → warning
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
        "```yaml",
        "constraint_rules:",
        "  REQUIRED:",
        "    - '<scope>.example_process'",  # Good placeholder
        # Real scope value - triggers warning
        "    - 'cli.real_process'",
        "  FORBIDDEN:",
        "    - '{other-scope}.boundary'",  # Good placeholder
        "```",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-mixed-values.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template609_angle_bracket_placeholders_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — governance template with angle
    bracket placeholders → passes
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
        "```yaml",
        "constraint_rules:",
        "  REQUIRED:",
        "    - '<scope>.primary_responsibility'",
        "    - '<scope>.secondary_responsibility'",
        "  FORBIDDEN:",
        "    - '<other-scope>.boundary_violation'",
        "  OWNED_BY:",
        "    - topic: '<shared-topic>'",
        "      owner: '<scope>'",
        "```",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-angle-placeholders.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template609_curly_bracket_placeholders_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — governance template with curly
    bracket placeholders → passes
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
        "```yaml",
        "constraint_rules:",
        "  REQUIRED:",
        "    - '{scope}.main_process'",
        "    - '{scope}.sub_process'",
        "  FORBIDDEN:",
        "    - '{other-scope}.forbidden_area'",
        "  OWNED_BY:",
        "    - topic: '{shared-concern}'",
        "      owner: '{scope}'",
        "```",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-curly-placeholders.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template609_square_bracket_placeholders_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — governance template with square
    bracket placeholders → passes
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
        "```yaml",
        "constraint_rules:",
        "  REQUIRED:",
        "    - '[scope].key_function'",
        "  FORBIDDEN:",
        "    - '[external-scope].restricted_function'",
        "  OWNED_BY:",
        "    - topic: '[shared-resource]'",
        "      owner: '[scope]'",
        "```",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-square-placeholders.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template609_mixed_placeholder_types_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — governance template with mixed
    placeholder bracket types → passes
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
        "```yaml",
        "constraint_rules:",
        "  REQUIRED:",
        "    - '<scope>.main_responsibility'",
        "    - '{scope}.secondary_role'",
        "  FORBIDDEN:",
        "    - '[other-scope].boundary'",
        "  OWNED_BY:",
        "    - topic: '<shared-resource>'",
        "      owner: '{scope}'",
        "```",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-mixed-placeholder-types.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template609_owner_template_ignores_constraint_rules(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — owner template with constraint_rules
    → ignored by validator
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
        "<!-- key: constraint_rules -->",
        "```yaml",
        "constraint_rules:",
        "  REQUIRED:",
        # Real values OK in non-governance template
        "    - 'cli.real_process'",
        "    - 'engine.real_function'",
        "```",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-template-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template609_strategy_template_ignores_constraint_rules(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — strategy template
    with constraint_rules → ignored by validator
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
        "<!-- key: constraint_rules -->",
        "```yaml",
        "constraint_rules:",
        "  REQUIRED:",
        # Real values OK in non-governance template
        "    - 'services.file_processing'",
        "```",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-template-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template609_governance_class_ignores_real_values(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — governance class (not template)
    with real values → ignored by validator
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
        "<!-- key: constraint_rules -->",
        "```yaml",
        "constraint_rules:",
        # Real values OK in actual governance ADR
        "  REQUIRED:",
        "    - 'cli.argument_parsing'",
        "    - 'cli.user_messages'",
        "  FORBIDDEN:",
        "    - 'engine.orchestration'",
        "```",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-class-real-values.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template609_owner_class_ignores_constraint_rules(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — owner class with constraint_rules
    → ignored by validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision with constraint rules.",
        "<!-- key: constraint_rules -->",
        "```yaml",
        "constraint_rules:",
        "  REQUIRED:",
        "    - 'cli.specific_function'",  # Real values OK in non-template
        "```",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-class-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template609_governance_template_missing_constraint_rules_ignored(  # noqa: E501
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — governance template missing
    constraint_rules section → ignored by validator
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
        # No constraint_rules section
        "<!-- key: precedence_mappings -->",
        "<precedence>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-no-constraint-rules.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template609_governance_template_malformed_yaml_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — governance template with malformed
    YAML in constraint_rules → ignored by validator
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
        "```yaml",
        "constraint_rules:",
        "  REQUIRED:",
        "    - invalid: yaml: syntax",  # Malformed YAML
        "  FORBIDDEN: [",  # Incomplete structure
        "```",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-malformed-yaml.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template609_governance_template_non_yaml_content_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — governance template with non-YAML
    content in constraint_rules → ignored by validator
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
        "This section should contain YAML constraint rules.",
        "Replace with actual constraint_rules YAML block.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-non-yaml.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template609_all_constraint_sections_real_values_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — governance template with real values
    in all constraint sections → warning
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
        "```yaml",
        "constraint_rules:",
        "  REQUIRED:",
        "    - 'cli.argument_parsing'",
        "    - 'cli.user_interface'",
        "  FORBIDDEN:",
        "    - 'engine.direct_user_access'",
        "    - 'services.ui_rendering'",
        "  OWNED_BY:",
        "    - topic: 'shared.error_codes'",
        "      owner: 'engine'",
        "    - topic: 'shared.logging'",
        "      owner: 'services'",
        "```",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-all-real-values.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template609_complex_placeholder_patterns_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-609 — governance template with complex
    placeholder patterns → passes
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
        "```yaml",
        "constraint_rules:",
        "  REQUIRED:",
        "    - '<scope>.primary_responsibility'",
        "    - '<scope>.secondary_function'",
        "    - '{scope}.additional_duty'",
        "  FORBIDDEN:",
        "    - '<other-scope-1>.boundary_violation'",
        "    - '[other-scope-2].restricted_area'",
        "    - '{external-system}.direct_access'",
        "  OWNED_BY:",
        "    - topic: '<shared-resource-1>'",
        "      owner: '<scope>'",
        "    - topic: '{shared-resource-2}'",
        "      owner: '{scope}'",
        "    - topic: '[cross-cutting-concern]'",
        "      owner: '[scope]'",
        "```",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-complex-placeholders.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)
