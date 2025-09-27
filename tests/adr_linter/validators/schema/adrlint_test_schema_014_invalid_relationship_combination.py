# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_014_invalid_relationship_combination.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-014 (E): Invalid relationship field combination for ADR class.
Validates relationship field combinations are architecturally valid per class.

Rule: Goes beyond forbidden fields (SCHEMA-009) to check combination logic
Single-file validation only (no cross-ADR validation)

Validation Rules:
1. Delta with extends but missing owners_ptr → ERROR
2. Template with any relationship fields → ERROR
   (extends, supersedes, governed_by, etc.)
3. Strategy with informs but missing owners_ptr → ERROR
4. Owner with extends field → ERROR
5. Governance with forbidden relationships → ERROR
   (extends, governed_by, informs)

Relationship fields: extends, supersedes, superseded_by, governed_by, informs,
                     informed_by, owners_ptr
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.schema.schema_014_invalid_relationship_combination import (  # noqa:E501
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


def test_adrlint_schema014_delta_extends_missing_owners_ptr_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — delta with extends but missing
    owners_ptr → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                # owners_ptr missing - required when extends is present
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Delta with extends but no owners_ptr.",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5006-delta-invalid-combo.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_delta_extends_with_owners_ptr_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — delta with extends and
    owners_ptr → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",  # Required with extends
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Delta with valid extends/owners_ptr combo.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-valid-combo.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_template_extends_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — template with extends
    relationship → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",
                "owners_ptr": "ADR-0001",
                "extends": "ADR-0001@2025-09-11",  # Invalid for template
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<owner-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-with-extends.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_template_supersedes_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — template with supersedes
    relationship → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "strategy",
                "owners_ptr": "ADR-0001",
                "supersedes": "ADR-0002@2025-09-11",  # Invalid for template
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<strategy-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-with-supersedes.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_template_governed_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — template with governed_by
    relationship → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "governance",
                "owners_ptr": "ADR-0001",
                "governed_by": "ADR-0001@2025-09-11",  # Invalid for template
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<governance-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-with-governed-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_template_informs_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — template with informs
    relationship → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "delta",
                "owners_ptr": "ADR-0001",
                "informs": "ADR-0002@2025-09-11",  # Invalid for template
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<delta-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-with-informs.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_template_informed_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — template with informed_by
    relationship → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "style-guide",
                "owners_ptr": "ADR-0001",
                "informed_by": "ADR-0002@2025-09-11",  # Invalid for template
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<style-guide-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-with-informed-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_template_no_relationships_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — template with no relationship
    fields → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",
                "owners_ptr": "ADR-0001",
                # No relationship fields - valid for template
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<owner-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-no-relationships.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_strategy_informs_missing_owners_ptr_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — strategy with informs but missing
    owners_ptr → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "informs": "ADR-0002@2025-09-11",
                # owners_ptr missing - required when informs is present
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategy with informs but no owners_ptr.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-informs-no-owners-ptr.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_strategy_informs_with_owners_ptr_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — strategy with informs and
    owners_ptr → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "informs": "ADR-0002@2025-09-11",
                "owners_ptr": "ADR-0001",  # Required with informs
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategy with valid informs/owners_ptr combo.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-valid-informs-combo.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_owner_extends_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — owner with extends field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "extends": "ADR-0002@2025-09-11",  # Invalid for owner
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner with forbidden extends field.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-with-extends.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_owner_valid_relationships_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — owner with valid
    relationships → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "supersedes": "ADR-0002@2025-09-11",
                "informed_by": "ADR-0003@2025-09-11",
                # extends not present - valid for owner
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner with valid relationships.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-valid-relationships.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_governance_extends_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — governance with extends → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
                "extends": "ADR-0001@2025-09-11",  # Invalid for governance
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance with forbidden extends.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-with-extends.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_governance_governed_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — governance with governed_by → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "engine",
                # Invalid for governance
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance with forbidden governed_by.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-with-governed-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_governance_informs_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — governance with informs → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "services",
                "informs": "ADR-0002@2025-09-11",  # Invalid for governance
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance with forbidden informs.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-with-informs.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_governance_valid_relationships_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — governance with valid
    relationships → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "other",
                "supersedes": "ADR-0002@2025-09-11",
                "informed_by": "ADR-0003@2025-09-11",
                # No forbidden relationships (extends, governed_by, informs)
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance with valid relationships.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-valid-relationships.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_multiple_violations_triggers_multiple_errors(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — multiple invalid
    combinations → multiple errors
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",
                "owners_ptr": "ADR-0001",
                # Invalid for template
                "extends": "ADR-0001@2025-09-11",
                # Also invalid for template
                "supersedes": "ADR-0002@2025-09-11",
                # Also invalid for template
                "governed_by": "ADR-0003@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Template with multiple invalid relationships.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-multiple-violations.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)

    # Should have multiple SCHEMA-014 errors
    errors = [item for item in rpt.items if item[1] == _ADR_ERROR_CODE]
    assert len(errors) >= 3  # At least 3 relationship violations


def test_adrlint_schema014_empty_relationship_fields_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — empty relationship fields should
    not trigger errors
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                # Empty string should not trigger validation
                "extends": "",
                # Empty string should not trigger validation
                "owners_ptr": "",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Delta with empty relationship fields.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "delta-empty-relationships.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_null_relationship_fields_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — null relationship fields should not
    trigger errors
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "informs": None,  # null should not trigger validation
                "owners_ptr": None,  # null should not trigger validation
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategy with null relationship fields.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-null-relationships.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_style_guide_with_relationships_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — style-guide with valid
    relationships → passes
    Style-guide class has fewer restrictions on relationships
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "style-guide",
                "superseded_by": "ADR-0002@2025-09-11",
                "informed_by": "ADR-0003@2025-09-11",
                # Style-guide allows most relationships except forbidden
                # ones (SCHEMA-009)
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Style guide with valid relationships.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "style-guide-with-relationships.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_delta_no_extends_with_owners_ptr_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — delta without extends but with
    owners_ptr → passes
    owners_ptr only required when extends is present
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "owners_ptr": "ADR-0001",
                # extends not present - owners_ptr still valid
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Delta with owners_ptr but no extends.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "delta-no-extends-with-owners-ptr.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema014_strategy_no_informs_no_owners_ptr_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-014 — strategy without informs or
    owners_ptr → passes
    owners_ptr only required when informs is present
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "governed_by": "ADR-0001@2025-09-11",
                # No informs, no owners_ptr - valid combination
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategy without informs or owners_ptr.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-no-informs-no-owners-ptr.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)
