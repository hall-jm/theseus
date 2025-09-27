# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_007_owner_governed_by.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-007 (E): Owner ADR missing required `governed_by` field.
Validates that owner class ADRs have required `governed_by` field for
authority chain.

Rule: IF class == "owner" AND governed_by is missing/empty → ERROR
Authority chain validation: Owner ADRs must declare governance binding
Other classes: governed_by is optional (not validated by this rule)
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.schema.schema_007_owner_governed_by import (
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


def test_adrlint_schema007_owner_missing_governed_by_entirely_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-007 — owner ADR missing governed_by field
    entirely → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                # governed_by field completely missing
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision without governance binding.",
        "<!-- key: context_and_drivers -->",
        "Context content.",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5002-owner-no-governed-by.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema007_owner_null_governed_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-007 — owner ADR with null
    governed_by → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": None,
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision with null governance binding.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-null-governed-by.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema007_owner_empty_string_governed_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-007 — owner ADR with empty string
    governed_by → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision with empty governance binding.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-empty-governed-by.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema007_owner_whitespace_governed_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-007 — owner ADR with whitespace-only
    governed_by → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "   ",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision with whitespace governance binding.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-whitespace-governed-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema007_owner_string_null_governed_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-007 — owner ADR with string "null"
    governed_by → error
    Edge case: string "null" should be treated as missing/invalid
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "null",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision with string null governance binding.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-string-null-governed-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema007_owner_string_null_case_variations_trigger(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-007 — owner ADR with case variations of
    "null" → error
    Edge case: "Null", "NULL", "nULl" should all be treated as invalid
    """
    test_cases = ["Null", "NULL", "nULl", "NULL"]

    for null_variant in test_cases:
        md = [
            _good_meta_front_matter(
                **{
                    "class": "owner",
                    "governed_by": null_variant,
                }
            ),
            "<!-- key: decision_one_liner -->",
            f"Owner decision with {null_variant} governance binding.",
        ]
        p, ctx = _write_and_ctx(
            _route_and_reset_workspace,
            f"owner-{null_variant.lower()}-governed-by.md",
            "\n".join(md),
        )
        rpt = Report()
        run_all(ctx, rpt)
        assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema007_owner_valid_governed_by_date_pin_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-007 — owner ADR with valid date pin
    governed_by → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision with valid date pin governance binding.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-valid-date-governed-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema007_owner_valid_governed_by_hash_pin_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-007 — owner ADR with valid hash pin
    governed_by → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@deadbeef123",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision with valid hash pin governance binding.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-valid-hash-governed-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema007_owner_valid_governed_by_no_pin_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-007 — owner ADR with valid governed_by
    (no pin) → passes
    Note: Pin format validation is handled by different validators (LINK-xxx)
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision with governance binding (no pin).",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-no-pin-governed-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema007_governance_class_ignores_missing_governed_by(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-007 — governance class without
    governed_by → ignored by this validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
                # governed_by field missing - should be ignored for
                # non-owner classes
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance decision without governed_by.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-no-governed-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema007_delta_class_ignores_governed_by(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-007 — delta class without
    governed_by → ignored by this validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",
                # governed_by missing - inherited from base, not validated by
                # this rule
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Delta decision inheriting governance.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-no-governed-by.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema007_strategy_class_ignores_governed_by(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-007 — strategy class without
    governed_by → ignored by this validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                # governed_by missing - optional for strategy class
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategy decision without governance binding.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "strategy-no-governed-by.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema007_strategy_class_with_governed_by_ignores(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-007 — strategy class with
    governed_by → ignored by this validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                # present but not validated by this rule
                "governed_by": "ADR-0001@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategy decision with optional governance binding.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-with-governed-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema007_template_class_ignores_governed_by(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-007 — template class ignores
    governed_by field
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",
                "owners_ptr": "ADR-0001",
                # governed_by field missing - should be ignored for
                # template classes
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<owner-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-owner.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema007_style_guide_class_ignores_governed_by(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-007 — style-guide class without
    governed_by → ignored by this validator
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "style-guide",
                # governed_by field missing - should be ignored for
                # style-guide classes
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Style guide decision without governance binding.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "style-guide-no-governed-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)
