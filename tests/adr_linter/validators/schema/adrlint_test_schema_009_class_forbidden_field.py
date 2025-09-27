# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_009_class_forbidden_field.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-009 (E): Class-forbidden field present.
Validates that ADR classes don't contain fields forbidden by their
architectural constraints.

Rule: Each ADR class has specific forbidden fields that violate
architectural constraints
Validates field presence (non-empty values trigger errors)
Empty/null values are allowed (treated as "not present")

Forbidden field mappings:
- owner: {extends, owners_ptr}
- governance: {extends, owners_ptr, governed_by, informs}
- strategy: {owners, scope}
- delta: {owners, scope}
- template: {extends, supersedes, governed_by, scope, owners}
- style-guide: {extends, supersedes, governed_by, scope}
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.schema.schema_009_class_forbidden_field import (
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


def test_adrlint_schema009_owner_forbidden_extends_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — owner class with forbidden
    "extends" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                # Forbidden for owner class
                "extends": "ADR-0002@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision with forbidden extends.",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5005-owner-forbidden-extends.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_owner_forbidden_owners_ptr_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — owner class with forbidden
    "owners_ptr" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",  # Forbidden for owner class
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision with forbidden owners_ptr.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-forbidden-owners-ptr.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_governance_forbidden_extends_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — governance class with forbidden
    "extends" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
                # Forbidden for governance class
                "extends": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance decision with forbidden extends.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-forbidden-extends.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_governance_forbidden_owners_ptr_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — governance class with forbidden
    "owners_ptr" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "engine",
                "owners_ptr": "ADR-0001",  # Forbidden for governance class
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance decision with forbidden owners_ptr.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-forbidden-owners-ptr.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_governance_forbidden_governed_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — governance class with forbidden
    "governed_by" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "services",
                # Forbidden for governance class
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance decision with forbidden governed_by.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-forbidden-governed-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_governance_forbidden_informs_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — governance class with forbidden
    "informs" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "other",
                # Forbidden for governance class
                "informs": "ADR-0002@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance decision with forbidden informs.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-forbidden-informs.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_strategy_forbidden_owners_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — strategy class with forbidden
    "owners" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                "owners": [
                    "Project Maintainer"
                ],  # Forbidden for strategy class
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategy decision with forbidden owners.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-forbidden-owners.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_strategy_forbidden_scope_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — strategy class with forbidden
    "scope" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                "scope": "cli",  # Forbidden for strategy class
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategy decision with forbidden scope.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-forbidden-scope.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_delta_forbidden_owners_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — delta class with forbidden
    "owners" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",
                "owners": ["Project Maintainer"],  # Forbidden for delta class
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Delta decision with forbidden owners.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-forbidden-owners.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_delta_forbidden_scope_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — delta class with forbidden
    "scope" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",
                "scope": "engine",  # Forbidden for delta class
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Delta decision with forbidden scope.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-forbidden-scope.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_template_forbidden_extends_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — template class with forbidden
    "extends" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",
                "owners_ptr": "ADR-0001",
                # Forbidden for template class
                "extends": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<owner-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-forbidden-extends.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_template_forbidden_supersedes_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — template class with forbidden
    "supersedes" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "strategy",
                "owners_ptr": "ADR-0001",
                # Forbidden for template class
                "supersedes": "ADR-0002@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<strategy-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-forbidden-supersedes.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_template_forbidden_governed_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — template class with forbidden
    "governed_by" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "governance",
                "owners_ptr": "ADR-0001",
                # Forbidden for template class
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<governance-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-forbidden-governed-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_template_forbidden_scope_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — template class with forbidden
    "scope" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "delta",
                "owners_ptr": "ADR-0001",
                "scope": "services",  # Forbidden for template class
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<delta-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-forbidden-scope.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_template_forbidden_owners_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — template class with forbidden
    "owners" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "style-guide",
                "owners_ptr": "ADR-0001",
                "owners": [
                    "Project Maintainer"
                ],  # Forbidden for template class
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<style-guide-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-forbidden-owners.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_style_guide_forbidden_extends_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — style-guide class with forbidden
    "extends" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "style-guide",
                # Forbidden for style-guide class
                "extends": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Style guide with forbidden extends.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "style-guide-forbidden-extends.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_style_guide_forbidden_supersedes_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — style-guide class with forbidden
    "supersedes" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "style-guide",
                # Forbidden for style-guide class
                "supersedes": "ADR-0002@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Style guide with forbidden supersedes.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "style-guide-forbidden-supersedes.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_style_guide_forbidden_governed_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — style-guide class with forbidden
    "governed_by" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "style-guide",
                # Forbidden for style-guide class
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Style guide with forbidden governed_by.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "style-guide-forbidden-governed-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_style_guide_forbidden_scope_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — style-guide class with forbidden
    "scope" field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "style-guide",
                "scope": "other",  # Forbidden for style-guide class
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Style guide with forbidden scope.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "style-guide-forbidden-scope.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_multiple_forbidden_fields_triggers_multiple_errors(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — ADR with multiple forbidden
    fields → multiple errors
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "extends": "ADR-0002@2025-09-11",  # Forbidden for owner
                "owners_ptr": "ADR-0001",  # Also forbidden for owner
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner with multiple forbidden fields.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-multiple-forbidden.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)

    # Should have multiple SCHEMA-009 errors
    errors = [item for item in rpt.items if item[1] == _ADR_ERROR_CODE]
    assert len(errors) >= 2  # At least 2 forbidden field errors


def test_adrlint_schema009_forbidden_field_null_value_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — forbidden field with null
    value → passes
    Empty/null values are treated as "not present"
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                # null value should pass (not considered present)
                "extends": None,
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner with null forbidden field.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-null-forbidden.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_forbidden_field_empty_string_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — forbidden field with empty
    string → passes
    Empty values are treated as "not present"
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
                # empty string should pass (not considered present)
                "extends": "",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance with empty forbidden field.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-empty-forbidden.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_owner_allowed_fields_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — owner class with only allowed
    fields → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",  # allowed
                "supersedes": "ADR-0002@2025-09-11",  # allowed
                "informed_by": "ADR-0003@2025-09-11",  # allowed
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner with only allowed fields.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-allowed-fields.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_governance_allowed_fields_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — governance class with only allowed
    fields → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",  # allowed
                "supersedes": "ADR-0002@2025-09-11",  # allowed
                "informed_by": "ADR-0003@2025-09-11",  # allowed
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance with only allowed fields.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-allowed-fields.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_strategy_allowed_fields_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — strategy class with only allowed
    fields → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",  # allowed
                "governed_by": "ADR-0001@2025-09-11",  # allowed
                "informs": "ADR-0002@2025-09-11",  # allowed
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategy with only allowed fields.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "strategy-allowed-fields.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_delta_allowed_fields_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — delta class with only allowed
    fields → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",  # allowed
                "owners_ptr": "ADR-0001",  # allowed
                "governed_by": "ADR-0001@2025-09-11",  # allowed
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Delta with only allowed fields.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-allowed-fields.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_template_allowed_fields_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — template class with only allowed
    fields → passes

    Historical Note: ADR-0001 disagreement on whether ADR-SCHEMA-009 vs.
                     ADR-SCHEMA-014 should prevail on if `informed_by`
                     should be allowed.  Decision was to keep template
                     ADRs are scaffolding only for now.
    Rationale: Templates should be pure scaffolding without any governance
               graph participation. Strategic direction should apply to the
               instantiated ADRs, not their templates.
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",  # allowed
                "owners_ptr": "ADR-0001",  # allowed
                # "informed_by": "ADR-0002@2025-09-11",  # allowed
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<owner-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-allowed-fields.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_style_guide_allowed_fields_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — style-guide class with only allowed
    fields → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "style-guide",
                "owners": ["Project Maintainer"],  # allowed
                "informed_by": "ADR-0002@2025-09-11",  # allowed
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Style guide with only allowed fields.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "style-guide-allowed-fields.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema009_unknown_class_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-009 — unknown class with any
    fields → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                # Unknown class should be ignored
                "class": "unknown_class",
                "extends": "ADR-0001@2025-09-11",
                "scope": "invalid",
                "owners": ["Someone"],
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Unknown class decision.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "unknown-class.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)
