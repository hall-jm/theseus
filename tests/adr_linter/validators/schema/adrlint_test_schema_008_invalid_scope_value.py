# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_008_invalid_scope_value.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-008 (E): Invalid `scope` value.
Validates that governance class ADRs have valid scope values from defined
taxonomy.

Rule: IF class == "governance" AND scope not in
      {cli, engine, services, other} → ERROR
Only validates governance class with present scope values
SCHEMA-006 handles missing scope, SCHEMA-009 handles forbidden scope for
other classes

Valid scope values: cli, engine, services, other (ADR-0001 §0.2 Scope Taxonomy)
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.schema.schema_008_invalid_scope_value import (
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


def test_adrlint_schema008_governance_invalid_scope_frontend_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with invalid scope
    frontend" → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                # Invalid - not in {cli, engine, services, other}
                "scope": "frontend",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Frontend governance decision.",
        "<!-- key: constraint_rules -->",
        "Frontend constraints.",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5004-governance-invalid-frontend.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_governance_invalid_scope_backend_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with invalid scope
    "backend" → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "backend",  # Invalid scope
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Backend governance decision.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-invalid-backend.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_governance_invalid_scope_database_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with invalid scope
    "database" → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "database",  # Invalid scope
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Database governance decision.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-invalid-database.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_governance_invalid_scope_web_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with invalid scope
    "web" → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "web",  # Invalid scope
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Web governance decision.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-invalid-web.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_governance_invalid_scope_api_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with invalid scope
    "api" → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "api",  # Invalid scope
            }
        ),
        "<!-- key: decision_one_liner -->",
        "API governance decision.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-invalid-api.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_governance_invalid_scope_custom_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with custom invalid
    scope → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "my_custom_scope",  # Invalid scope
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Custom scope governance decision.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-invalid-custom.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_governance_valid_scope_cli_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with valid scope
    "cli" → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",  # Valid scope
            }
        ),
        "<!-- key: decision_one_liner -->",
        "CLI governance decision.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-valid-cli.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_governance_valid_scope_engine_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with valid scope
    "engine" → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "engine",  # Valid scope
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Engine governance decision.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-valid-engine.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_governance_valid_scope_services_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with valid scope
    "services" → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "services",  # Valid scope
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Services governance decision.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-valid-services.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_governance_valid_scope_other_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with valid scope
    "other" → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "other",  # Valid scope
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Other governance decision.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-valid-other.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_governance_missing_scope_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with missing
    scope → ignored
    SCHEMA-006 handles missing scope validation
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                # scope field missing - handled by SCHEMA-006,
                #                       not this validator
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance decision without scope.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-missing-scope.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_governance_null_scope_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with null
    scope → ignored
    SCHEMA-006 handles null scope validation
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": None,  # null scope - handled by SCHEMA-006
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance decision with null scope.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-null-scope.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_governance_case_sensitive_cli_uppercase_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with "CLI"
    (uppercase) → error
    Case sensitivity test - must be exact lowercase match
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "CLI",  # Invalid - case sensitive, should be "cli"
            }
        ),
        "<!-- key: decision_one_liner -->",
        "CLI governance decision with wrong case.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-case-cli-upper.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_governance_mixed_case_engine_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with "Engine"
    (mixed case) → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "Engine",  # Invalid - should be "engine"
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Engine governance decision with mixed case.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-case-engine-mixed.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_governance_whitespace_scope_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with whitespace in
    scope → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": " cli ",  # Invalid - contains whitespace
            }
        ),
        "<!-- key: decision_one_liner -->",
        "CLI governance decision with whitespace in scope.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-whitespace-scope.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)

    # Originally, this pytest was showing white spaces broke the
    # validator, but since it was such a simple fix, the logic was
    # flipped to test to ensure white spaces are removed from `scope`
    # not assert_error_code(rpt, _ADR_ERROR_CODE)  # <-- Original test
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_owner_class_with_scope_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — owner class with scope → ignored
    SCHEMA-009 handles forbidden scope for other classes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                # Invalid for owner, but handled by SCHEMA-009
                "scope": "invalid_scope",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision with scope.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-with-scope.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_delta_class_with_scope_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — delta class with scope → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",
                # Invalid for delta, but handled by SCHEMA-009
                "scope": "invalid_scope",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Delta decision with scope.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-with-scope.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_strategy_class_with_scope_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — strategy class with scope → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                # Invalid for strategy, but handled by SCHEMA-009
                "scope": "invalid_scope",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategy decision with scope.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "strategy-with-scope.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_template_class_with_scope_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — template class with scope → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "governance",
                "owners_ptr": "ADR-0001",
                # Invalid for template, but handled by SCHEMA-009
                "scope": "invalid_scope",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<governance-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-with-scope.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_governance_numeric_scope_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with numeric
    scope → error
    Edge case: numeric values should be invalid
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "123",  # Invalid - numeric scope
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance decision with numeric scope.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-numeric-scope.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema008_governance_empty_string_scope_ignored(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-008 — governance ADR with empty string
    scope → ignored
    Empty string scope handled by SCHEMA-006
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "",  # Empty string - handled by SCHEMA-006
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance decision with empty scope.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-empty-scope.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)
