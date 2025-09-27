# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_006_governance_scope.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-006 (E): Governance ADR missing required `scope` field.
Validates that governance class ADRs have required `scope` field with valid
values.

Rule: IF class == "governance" AND scope is missing/empty → ERROR
Valid scope values: cli|engine|services|other
Other classes ignore scope (different validator handles forbidden cases)
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.schema.schema_006_governance_scope import (
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


def test_adrlint_schema006_governance_missing_scope_entirely_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-006 — governance ADR missing scope field
    entirely → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                # scope field completely missing
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance decision without scope.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5001-governance-no-scope.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema006_governance_null_scope_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-006 — governance ADR with null scope → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": None,
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
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema006_governance_empty_string_scope_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-006 — governance ADR with empty string
    scope → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "",
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
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema006_governance_whitespace_scope_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-006 — governance ADR with whitespace-only
    scope → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "   ",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance decision with whitespace scope.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-whitespace-scope.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema006_governance_valid_cli_scope_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-006 — governance ADR with valid 'cli'
    scope → passes
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
        "CLI context.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-cli-scope.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema006_governance_valid_engine_scope_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-006 — governance ADR with valid 'engine'
    scope → passes
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
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-engine-scope.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema006_governance_valid_services_scope_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-006 — governance ADR with valid 'services'
    scope → passes
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
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-services-scope.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema006_governance_valid_other_scope_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-006 — governance ADR with valid 'other'
    scope → passes
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
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-other-scope.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema006_owner_class_ignores_missing_scope(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-006 — owner class without scope → ignored by
    this validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                # scope field missing - should be ignored for non-governance
                # classes
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision without scope.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-no-scope.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema006_delta_class_ignores_scope(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-006 — delta class with scope → ignored by
    this validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",
                "scope": "cli",  # scope present but ignored for delta class
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


def test_adrlint_schema006_strategy_class_ignores_scope(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-006 — strategy class with scope → ignored by
    this validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                # scope present but ignored for strategy class
                "scope": "engine",
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


def test_adrlint_schema006_template_class_ignores_scope(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-006 — template class ignores scope field
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "governance",
                "owners_ptr": "ADR-0001",
                # scope field missing - should be ignored for template classes
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<governance-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-governance.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema006_governance_string_null_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-006 — governance ADR with string "null"
    scope → error
    Edge case: string "null" should be treated as missing/invalid
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "null",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance decision with string null scope.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "governance-string-null.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)
