# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_003_keys_order.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-003 (E): Canonical section keys missing or out of order.
Validates canonical section structure including both section key markers
and corresponding markdown headers.

Rule: Validates missing sections entirely, wrong section order, present
sections with missing markdown headers, present sections with mismatched
headers, duplicate sections. Uses expected_keys_for(class, template_of)
for canonical section order. Integrates with HEADING_ALIASES for
header-to-key validation.

Enhanced validation sequence:
1. Duplicate section detection
2. Missing section detection
3. Markdown header validation (NEW)
4. Section order validation
5. No key markers detection
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.schema.schema_003_keys_order import (
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


def test_adrlint_schema003_owner_correct_structure_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-003 — owner ADR with correct section
    structure and headers → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Because X, we choose Y so that Z.",
        "",
        "<!-- key: context_and_drivers -->",
        "## Context and Drivers",
        "Context content.",
        "",
        "<!-- key: options_considered -->",
        "## Options Considered",
        "Options content.",
        "",
        "<!-- key: decision_details -->",
        "## Decision Details",
        "Details content.",
        "",
        "<!-- key: consequences_and_risks -->",
        "## Consequences and Risks",
        "Consequences content.",
        "",
        "<!-- key: implementation_notes -->",
        "## Implementation Notes",
        "Implementation content.",
        "",
        "<!-- key: rollout_backout -->",
        "## Rollout & Backout",
        "Rollout content.",
        "",
        "<!-- key: evidence_and_links -->",
        "## Evidence and Links",
        "Evidence content.",
        "",
        "<!-- key: glossary -->",
        "## Glossary",
        "Glossary content.",
        "",
        "<!-- key: related_adrs -->",
        "## Related ADRs",
        "Related content.",
        "",
        "<!-- key: license -->",
        "## License",
        "License content.",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-0003-owner-correct-structure.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)

    rpt = Report()
    run_all(ctx, rpt)

    if _has_code(rpt, _ADR_ERROR_CODE):
        # print(f"- [D PYTEST: SCHEMA-003] Report contents: {rpt}")
        # or
        print(f"- [D PYTEST: SCHEMA-003] Report items: {list(rpt.items)}")

    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema003_governance_correct_structure_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-003 — governance ADR with correct section
    structure and headers → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Because X, we choose Y so that Z.",
        "",
        "<!-- key: context_and_drivers -->",
        "## Context and Drivers",
        "Context content.",
        "",
        "<!-- key: options_considered -->",
        "## Options Considered",
        "Options content.",
        "",
        "<!-- key: decision_details -->",
        "## Decision Details",
        "Details content.",
        "",
        "<!-- key: authority_scope -->",
        "## Authority Scope",
        "Authority content.",
        "",
        "<!-- key: constraint_rules -->",
        "## Constraint Rules",
        "Constraints content.",
        "",
        "<!-- key: precedence_mappings -->",
        "## Precedence Mappings",
        "Precedence content.",
        "",
        "<!-- key: adoption_and_enforcement -->",
        "## Adoption and Enforcement",
        "Adoption content.",
        "",
        "<!-- key: evidence_and_links -->",
        "## Evidence and Links",
        "Evidence content.",
        "",
        "<!-- key: glossary -->",
        "## Glossary",
        "Glossary content.",
        "",
        "<!-- key: related_adrs -->",
        "## Related ADRs",
        "Related content.",
        "",
        "<!-- key: license -->",
        "## License",
        "License content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-correct-structure.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema003_duplicate_sections_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-003 — owner ADR with
    duplicate sections → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "First decision content.",
        "",
        "<!-- key: context_and_drivers -->",
        "## Context and Drivers",
        "Context content.",
        "",
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Duplicate decision content.",
        "",
        "<!-- key: decision_details -->",
        "## Decision Details",
        "Details content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-duplicate-sections.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema003_missing_sections_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-003 — owner ADR
    missing required sections → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
        "",
        "<!-- key: context_and_drivers -->",
        "## Context and Drivers",
        "Context content.",
        "",
        # Missing: options_considered, decision_details,
        #          consequences_and_risks,
        #          implementation_notes, rollout_backout, evidence_and_links,
        #          glossary, related_adrs, license
        "<!-- key: license -->",
        "## License",
        "License content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-missing-sections.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema003_wrong_section_order_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-003 — strategy ADR with wrong
    section order → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: principles -->",
        "## Principles",
        "Principles first (wrong order).",
        "",
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision second (should be first).",
        "",
        "<!-- key: context_and_drivers -->",
        "## Context and Drivers",
        "Context third.",
        "",
        "<!-- key: decision_details -->",
        "## Decision Details",
        "Details fourth.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "strategy-wrong-order.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema003_missing_markdown_headers_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-003 — delta ADR with
    missing markdown headers → error
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
        "Decision content without header.",
        "",
        "<!-- key: context_and_drivers -->",
        "## Context and Drivers",
        "Context with header.",
        "",
        "<!-- key: options_considered -->",
        "Options content without header.",
        "",
        "<!-- key: decision_details -->",
        "## Decision Details",
        "Details with header.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-missing-headers.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema003_mismatched_headers_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-003 — governance ADR with
    mismatched headers → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "engine",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Correct header.",
        "",
        "<!-- key: context_and_drivers -->",
        "## Context and Drivers",
        "Correct header.",
        "",
        "<!-- key: authority_scope -->",
        "## Wrong Header Name",
        "Mismatched header for authority_scope.",
        "",
        "<!-- key: constraint_rules -->",
        "## Implementation Notes",
        "Wrong header for constraint_rules.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-mismatched-headers.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema003_template_wrong_order_triggers_with_template_message(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-003 — template ADR with wrong order → error
    with template-specific messaging
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
        "## Decision Details",
        "<details> (wrong order - should be 4th)",
        "",
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "<decision> (wrong order - should be 1st)",
        "",
        "<!-- key: context_and_drivers -->",
        "## Context and Drivers",
        "<context> (wrong order - should be 2nd)",
        "",
        "<!-- key: options_considered -->",
        "## Options Considered",
        "<options> (correct position - 3rd when reordered)",
        "",
        "<!-- key: consequences_and_risks -->",
        "## Consequences and Risks",
        "<consequences>",
        "",
        "<!-- key: implementation_notes -->",
        "## Implementation Notes",
        "<implementation>",
        "",
        "<!-- key: rollout_backout -->",
        "## Rollout & Backout",
        "<rollout>",
        "",
        "<!-- key: evidence_and_links -->",
        "## Evidence and Links",
        "<evidence>",
        "",
        "<!-- key: glossary -->",
        "## Glossary",
        "<glossary>",
        "",
        "<!-- key: related_adrs -->",
        "## Related ADRs",
        "<related>",
        "",
        "<!-- key: license -->",
        "## License",
        "<license>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-wrong-order.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)

    # Verify template-specific messaging
    error_messages = [
        item[3] for item in rpt.items if item[1] == _ADR_ERROR_CODE
    ]

    # print(
    #    "- [D PYTEST: SCHEMA-003 - template_wrong_order] "
    #    f"Actual error messages: {error_messages}"
    # )

    assert any("sections out of order" in m for m in error_messages)


def test_adrlint_schema003_strategy_correct_structure_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-003 — strategy ADR with correct section
    structure and headers → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
        "",
        "<!-- key: context_and_drivers -->",
        "## Context and Drivers",
        "Context content.",
        "",
        "<!-- key: options_considered -->",
        "## Options Considered",
        "Options content.",
        "",
        "<!-- key: decision_details -->",
        "## Decision Details",
        "Details content.",
        "",
        "<!-- key: principles -->",
        "## Principles",
        "Principles content.",
        "",
        "<!-- key: guardrails -->",
        "## Guardrails",
        "Guardrails content.",
        "",
        "<!-- key: consequences_and_risks -->",
        "## Consequences and Risks",
        "Consequences content.",
        "",
        "<!-- key: implementation_notes -->",
        "## Implementation Notes",
        "Implementation content.",
        "",
        "<!-- key: north_star_metrics -->",
        "## North Star Metrics",
        "Metrics content.",
        "",
        "<!-- key: evidence_and_links -->",
        "## Evidence and Links",
        "Evidence content.",
        "",
        "<!-- key: glossary -->",
        "## Glossary",
        "Glossary content.",
        "",
        "<!-- key: related_adrs -->",
        "## Related ADRs",
        "Related content.",
        "",
        "<!-- key: license -->",
        "## License",
        "License content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-correct-structure.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema003_delta_correct_structure_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-003 — delta ADR with correct section
    structure and headers → passes
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
        "## Decision (one-liner)",
        "Decision content.",
        "",
        "<!-- key: context_and_drivers -->",
        "## Context and Drivers",
        "Context content.",
        "",
        "<!-- key: options_considered -->",
        "## Options Considered",
        "Options content.",
        "",
        "<!-- key: decision_details -->",
        "## Decision Details",
        "Details content.",
        "",
        "<!-- key: evidence_and_links -->",
        "## Evidence and Links",
        "Evidence content.",
        "",
        "<!-- key: glossary -->",
        "## Glossary",
        "Glossary content.",
        "",
        "<!-- key: related_adrs -->",
        "## Related ADRs",
        "Related content.",
        "",
        "<!-- key: license -->",
        "## License",
        "License content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-correct-structure.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema003_style_guide_exempt_from_validation(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-003 — style-guide class exempt from
    canonical section enforcement → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "style-guide",
            }
        ),
        "# Style Guide Content",
        "",
        "## Custom Section 1",
        "Custom content.",
        "",
        "## Another Custom Section",
        "More custom content.",
        "",
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content in wrong order but allowed for style-guide.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "style-guide-custom-structure.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema003_no_key_markers_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-003 — owner ADR with no key markers → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "# ADR Content",
        "",
        "## Some Header",
        "Content without any key markers.",
        "",
        "## Another Header",
        "More content without key markers.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-no-key-markers.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema003_template_governance_correct_structure_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-003 — governance template with correct
    section structure → passes
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
        "## Decision (one-liner)",
        "<governance-decision>",
        "",
        "<!-- key: context_and_drivers -->",
        "## Context and Drivers",
        "<context>",
        "",
        "<!-- key: options_considered -->",
        "## Options Considered",
        "<options>",
        "",
        "<!-- key: decision_details -->",
        "## Decision Details",
        "<details>",
        "",
        "<!-- key: authority_scope -->",
        "## Authority Scope",
        "<authority>",
        "",
        "<!-- key: constraint_rules -->",
        "## Constraint Rules",
        "<constraints>",
        "",
        "<!-- key: precedence_mappings -->",
        "## Precedence Mappings",
        "<precedence>",
        "",
        "<!-- key: adoption_and_enforcement -->",
        "## Adoption and Enforcement",
        "<adoption>",
        "",
        "<!-- key: evidence_and_links -->",
        "## Evidence and Links",
        "<evidence>",
        "",
        "<!-- key: glossary -->",
        "## Glossary",
        "<glossary>",
        "",
        "<!-- key: related_adrs -->",
        "## Related ADRs",
        "<related>",
        "",
        "<!-- key: license -->",
        "## License",
        "<license>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-governance-correct.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema003_governance_missing_class_specific_sections_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-003 — governance ADR missing class-specific
    sections → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "services",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
        "",
        "<!-- key: context_and_drivers -->",
        "## Context and Drivers",
        "Context content.",
        "",
        "<!-- key: decision_details -->",
        "## Decision Details",
        "Details content.",
        "",
        # Missing governance-specific sections: authority_scope,
        #                                       constraint_rules,
        #                                       precedence_mappings,
        #                                       adoption_and_enforcement
        "<!-- key: evidence_and_links -->",
        "## Evidence and Links",
        "Evidence content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-missing-class-sections.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema003_strategy_class_specific_order_wrong_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-003 — strategy ADR with class-specific
    sections in wrong order → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
        "",
        "<!-- key: context_and_drivers -->",
        "## Context and Drivers",
        "Context content.",
        "",
        "<!-- key: decision_details -->",
        "## Decision Details",
        "Details content.",
        "",
        "<!-- key: guardrails -->",
        "## Guardrails",
        "Guardrails before principles (wrong order).",
        "",
        "<!-- key: principles -->",
        "## Principles",
        "Principles after guardrails (should be before).",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-class-wrong-order.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)
