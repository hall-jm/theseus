# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_004_status_field_requirements.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-004 (E): Status field requirements or lifecycle consistency
violation. Validates status field requirements and internal lifecycle
consistency within individual ADR files.

Rule:

Phase 1: Status field requirements (Superseded requires superseded_by,
Deprecated needs justification).

Phase 2: Status-lifecycle consistency (Accepted ADRs can't have superseded_by,
etc.).

Enhanced: Date logic consistency(review_by validation, cross-date checks).
          Self-reference validation (ADR can't supersede itself).
          Valid status values against VALID_STATUS_TRANSITIONS.

Three validation functions:
- validate_schema_004_status_field_requirements() # Main validator
- validate_status_lifecycle_consistency() # Phase 2 logic
- validate_date_logic_consistency() # Enhanced date validation
"""

from __future__ import annotations

from datetime import (
    date as dt_date,
    timedelta as dt_timedelta,
)

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.schema.schema_004_status_field_requirements import (
    _ERROR_CODE as _ADR_ERROR_CODE,
)

from ...conftest import (
    _write_text,
    _write_and_ctx,
    _ctx_from_path,
    _good_meta_front_matter,
    _good_body_structure,
    _has_code,
    assert_error_code,
)


def test_adrlint_schema004_invalid_status_value_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — invalid status value → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "status": "Invalid",  # Not in VALID_STATUS_TRANSITIONS
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-0004-invalid-status.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_superseded_without_superseded_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — superseded status without
    superseded_by → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "status": "Superseded",
                # superseded_by field missing - required for Superseded status
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "superseded-no-superseded-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_deprecated_without_justification_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — deprecated status without
    justification → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "status": "Deprecated",
                # Missing justification field or content for Deprecated status
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "deprecated-no-justification.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_accepted_with_superseded_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — accepted status with
    superseded_by → error
    Status-lifecycle conflict: Accepted ADRs can't have superseded_by
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "status": "Accepted",
                # Conflict with Accepted status
                "superseded_by": "ADR-0005@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "accepted-with-superseded-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_proposed_with_superseded_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — proposed status with
    superseded_by → error
    Status-lifecycle conflict: Proposed ADRs can't have superseded_by
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                "status": "Proposed",
                # Conflict with Proposed status
                "superseded_by": "ADR-0006@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "proposed-with-superseded-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_proposed_with_supersedes_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — proposed status with supersedes → error
    Status-lifecycle conflict: Proposed ADRs can't have supersedes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",
                "status": "Proposed",
                # Conflict with Proposed status
                "supersedes": "ADR-0007@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "proposed-with-supersedes.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_deprecated_with_supersedes_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — deprecated status with
    supersedes → error
    Status-lifecycle conflict: Deprecated ADRs can't have supersedes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
                "status": "Deprecated",
                # Conflict with Deprecated status
                "supersedes": "ADR-0008@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "deprecated-with-supersedes.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_superseded_with_supersedes_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — superseded status with
    supersedes → error
    Status-lifecycle conflict: Superseded ADRs can't have supersedes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "status": "Superseded",
                "superseded_by": "ADR-0009@2025-09-11",
                # Conflict with Superseded status
                "supersedes": "ADR-0010@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "superseded-with-supersedes.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_self_reference_superseded_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — ADR superseded by itself → error
    Self-reference violation: ADR can't supersede itself
    """
    md = [
        _good_meta_front_matter(
            **{
                "id": "ADR-0011",
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                "status": "Superseded",
                "superseded_by": "ADR-0011@2025-09-11",  # Self-reference
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "self-reference-superseded-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_self_reference_supersedes_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — ADR supersedes itself → error
    Self-reference violation: ADR can't supersede itself
    """
    md = [
        _good_meta_front_matter(
            **{
                "id": "ADR-0012",
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "status": "Accepted",
                "supersedes": "ADR-0012@2025-09-11",  # Self-reference
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "self-reference-supersedes.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_deprecated_with_review_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — deprecated status with
    review_by → error
    Date logic violation: Deprecated ADRs shouldn't have review_by
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",
                "status": "Deprecated",
                "review_by": "2026-01-01",  # Conflict with Deprecated status
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "deprecated-with-review-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_superseded_with_review_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — superseded status with
    review_by → error
    Date logic violation: Superseded ADRs shouldn't have review_by
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "engine",
                "status": "Superseded",
                "superseded_by": "ADR-0013@2025-09-11",
                "review_by": "2026-02-01",  # Conflict with Superseded status
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "superseded-with-review-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_proposed_without_review_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — proposed status without
    review_by → error
    Date logic violation: Proposed ADRs should have review_by
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                "status": "Proposed",
                # review_by field is set in this function call;
                # setting it to Noneto test validator
                "review_by": None,
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]

    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "proposed-without-review-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)

    # print(
    #    f"- [D PYTEST: SCHEMA-004 - proposed_without_review_by] "
    #    f"All report items: {list(rpt.items)}"
    # )
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_review_by_before_date_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — review_by before date field → error
    Date logic violation: review_by must be after date
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "status": "Proposed",
                "date": "2025-09-15",
                "review_by": "2025-09-10",  # Before date field
            }
        ),
        # Complete strategy ADR structure
        _good_body_structure("owner"),
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "review-by-before-date.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)

    print(
        f"- [D PYTEST: SCHEMA-004 - review_by_before_date_triggers] "
        f"All report items: {list(rpt.items)}"
    )

    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_past_review_by_for_proposed_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — past review_by for proposed → error
    Date logic violation: Proposed ADRs with past review_by dates
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",
                "status": "Proposed",
                "date": "2025-01-01",
                # Past date (assuming current date > 2025-01-15)
                "review_by": "2025-01-15",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "past-review-by-proposed.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_valid_proposed_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — valid proposed status → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "status": "Proposed",
                "date": "2025-09-15",
                "review_by": "2026-03-15",  # Future date, after date field
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "valid-proposed.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_valid_accepted_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — valid accepted status → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                "status": "Accepted",
                "date": "2025-09-15",
                # No review_by (acceptable for Accepted), no superseded_by
                "review_by": None,
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "valid-accepted.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_valid_superseded_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — valid superseded status → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "services",
                "status": "Superseded",
                # Required for Superseded
                "superseded_by": "ADR-0014@2025-09-11",
                "date": "2025-09-15",
                # review_by field is set in this function call;
                # setting it to None to test validator
                "review_by": None,
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "valid-superseded.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_valid_deprecated_with_justification_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — valid deprecated status with
    justification → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",
                "status": "Deprecated",
                "date": "2025-09-15",
                # Deprecated ADRs don't need reviews
                "review_by": None,
                # Justification provided in change_history or other field
                "change_history": [
                    "Deprecated due to security vulnerabilities"
                ],
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "valid-deprecated.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)

    # print(
    #     f"- [D PYTEST: SCHEMA-004 - valid_deprecated_with_justification] "
    #     f"All report items: {list(rpt.items)}"
    # )

    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_accepted_with_supersedes_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — accepted status with
    supersedes → passes
    Valid combination: Accepted ADRs can supersede other ADRs
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "status": "Accepted",
                # Valid for Accepted status
                "supersedes": "ADR-0015@2025-09-11",
                "date": "2025-09-15",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "accepted-with-supersedes.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_deprecated_with_dual_justification_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — deprecated with both superseded_by
    and change_history → passes (either justification is valid)
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "status": "Deprecated",
                "superseded_by": "ADR-0016@2025-09-11",
                # Deprecated ADRs don't need reviews
                "review_by": None,
                "change_history": ["Deprecated due to security issues"],
                "date": "2025-09-15",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "deprecated-dual-justification.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_superseded_change_history_no_superseded_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — superseded with change_history but
    no superseded_by → error (Superseded requires superseded_by)
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                "status": "Superseded",
                "change_history": ["Superseded by newer strategy"],
                "date": "2025-09-15",
                # superseded_by missing - required for Superseded status
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "superseded-change-history-no-superseded-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_review_by_equals_date_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — review_by equals date field → error
    (must be after, not equal)
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "status": "Proposed",
                "date": "2025-09-15",
                "review_by": "2025-09-15",  # Same as date field
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "review-by-equals-date.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_empty_string_superseded_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — superseded with empty string
    superseded_by → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                "status": "Superseded",
                "superseded_by": "",  # Empty string, not valid
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "empty-string-superseded-by.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_null_superseded_by_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — superseded with
    null superseded_by → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",
                "status": "Superseded",
                "superseded_by": None,  # Null value, not valid
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "null-superseded-by.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_empty_array_change_history_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — deprecated with empty array
    change_history → error (no justification)
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
                "status": "Deprecated",
                "change_history": [],  # Empty array, no justification
            }
        ),
        "<!-- key: decision_one_liner -->",
        "## Decision (one-liner)",
        "Decision content.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "empty-array-change-history.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_schema004_review_by_today_proposed_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-SCHEMA-004 — proposed with review_by on yesterday's
    date → error (edge case boundary); today == review_by != error
    """

    yesterday = (dt_date.today() - dt_timedelta(days=1)).strftime("%Y-%m-%d")
    base_date = (dt_date.today() - dt_timedelta(days=7)).strftime("%Y-%m-%d")

    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "status": "Proposed",
                "date": base_date,
                "review_by": yesterday,  # Yesterday is past
            }
        ),
        _good_body_structure("owner"),
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "review-by-today-proposed.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)
