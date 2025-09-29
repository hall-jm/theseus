# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/template/adrlint_test_template_600_template_of_required.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-TEMPLATE-600 (E): `template_of` missing or invalid.
Validates that template class ADRs have valid `template_of` field.

Rule: IF class == "template" AND template_of is missing/invalid → ERROR
Valid template_of values: owner|delta|governance|strategy|style-guide
Other classes ignore template_of (different validator handles forbidden cases)
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.template.template_600_template_of_required import (
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


def test_adrlint_template600_missing_template_of_entirely_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — template ADR missing
    template_of field entirely → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                # template_of field completely missing
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<template-decision>",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-6001-template-no-template-of.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_null_template_of_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — template ADR with null
    template_of → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                "template_of": None,
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<template-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-null-template-of.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_empty_string_template_of_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — template ADR with empty string
    template_of → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                "template_of": "",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<template-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-empty-template-of.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_invalid_string_template_of_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — template ADR with invalid string
    template_of → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                "template_of": "invalid",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<template-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-invalid-template-of.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_case_sensitive_owner_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — template ADR with wrong case
    "Owner" → error Case sensitivity test - must be exact lowercase match
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                # Invalid - case sensitive, should be "owner"
                "template_of": "Owner",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<owner-template-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-case-owner.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_case_sensitive_strategy_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — template ADR with wrong case
    "STRATEGY" → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                # Invalid - should be "strategy"
                "template_of": "STRATEGY",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<strategy-template-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-case-strategy.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_numeric_template_of_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — template ADR with numeric
    template_of → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                "template_of": 123,  # Invalid - numeric value
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<template-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-numeric-template-of.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_array_template_of_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — template ADR with array
    template_of → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                "template_of": ["owner"],  # Invalid - array value
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<template-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-array-template-of.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_valid_owner_template_of_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — template ADR with valid "owner"
    template_of → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                "template_of": "owner",  # Valid value
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<owner-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-valid-owner.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_valid_delta_template_of_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — template ADR with valid "delta"
    template_of → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                "template_of": "delta",  # Valid value
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<delta-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-valid-delta.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_valid_governance_template_of_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — template ADR with valid "governance"
    template_of → passes
    CRITICAL: This test covers the governance template type added in
              ADR-0001 v0.2.0
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                # Valid value (added in v0.2.0)
                "template_of": "governance",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<governance-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-valid-governance.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_valid_strategy_template_of_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — template ADR with valid
    "strategy" template_of → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                "template_of": "strategy",  # Valid value
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<strategy-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-valid-strategy.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_valid_style_guide_template_of_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — template ADR with valid
    "style-guide" template_of → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                "template_of": "style-guide",  # Valid value
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<style-guide-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-valid-style-guide.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_owner_class_ignores_template_of(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — owner class with
    template_of → ignored by this validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                # Invalid for owner, but handled by different validator
                "template_of": "invalid_value",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision with template_of.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-with-template-of.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_delta_class_ignores_template_of(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — delta class with
    template_of → ignored by this validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",
                # Invalid for delta, but handled by different validator
                "template_of": "invalid_value",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Delta decision with template_of.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-with-template-of.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_governance_class_ignores_template_of(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — governance class with
    template_of → ignored by this validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
                # Invalid for governance, but handled by different validator
                "template_of": "invalid_value",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance decision with template_of.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-with-template-of.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_strategy_class_ignores_template_of(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — strategy class with
    template_of → ignored by this validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                # Invalid for strategy, but handled by different validator
                "template_of": "invalid_value",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategy decision with template_of.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-with-template-of.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_style_guide_class_ignores_template_of(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — style-guide class with
    template_of → ignored by this validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "style-guide",
                # Invalid for style-guide, but handled by different validator
                "template_of": "invalid_value",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Style guide decision with template_of.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "style-guide-with-template-of.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_whitespace_template_of_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — template ADR with whitespace
    template_of → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                "template_of": "   ",  # Whitespace only
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<template-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-whitespace-template-of.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_template_class_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — template ADR with "template"
    template_of → error
    Edge case: template_of cannot be "template" (recursive)
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                # Invalid - cannot template templates
                "template_of": "template",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<template-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-recursive-template-of.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template600_hyphenated_governance_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-600 — template ADR with
    "govern-ance" template_of → error
    Edge case: hyphenated variation should be invalid
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "owners_ptr": "ADR-0001",
                # Invalid - wrong format
                "template_of": "govern-ance",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<governance-template-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-hyphenated-governance.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)
