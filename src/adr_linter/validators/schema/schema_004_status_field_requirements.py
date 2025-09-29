# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_004_status_field_requirements.py

"""
ADR-SCHEMA-004 — Status field requirements and lifecycle consistency validation

SCOPE: Single-file internal consistency validation only. This validator focuses
on status-lifecycle consistency within individual ADR files and avoids
duplicating class-field validation handled by other validators (SCHEMA-007,
SCHEMA-012, etc.).

PHASE 1 (Implemented):
- Status field requirements (Superseded requires superseded_by, etc.)
- Valid status values per VALID_STATUS_TRANSITIONS
- Basic field format validation

PHASE 2 (Implemented):
- Status-lifecycle internal consistency
  (e.g., Accepted ADRs can't have superseded_by)
- Prevents nonsensical metadata combinations within single ADR
- Prevents some status dates getting out of order with other statue dates
- Self-referential validation (ADR can't supersede itself)

EXPLICITLY OUT OF SCOPE:
- Cross-file transition validation (old state → new state)
- Validations handled by other bands (e.g., ADR-LINK)
- Class-field validation (handled by other SCHEMA validators)
- External file dependencies or git history analysis

FUTURE ENHANCEMENT OPPORTUNITIES:
- Cross-file actual transition validation (requires architectural changes)
- Integration with version control for true state change detection
- Enhanced field format validation with regex patterns

Ref: ADR-0001 §14 SCHEMA-004, constants/validation.py VALID_STATUS_TRANSITIONS
"""

from __future__ import annotations
from datetime import datetime, date as date_obj

from ...constants.validation import VALID_STATUS_TRANSITIONS

_ERROR_CODE = "ADR-SCHEMA-004"


# FIXME: This kind of code does not need to be in a validator
#        Extract to a centralized location for wider, unversal use


def parse_date(date_str):
    """
    If already date object, return the date object.
    Parse YYYY-MM-DD date string, return None if invalid.
    """

    if isinstance(date_str, date_obj):
        return date_str
    elif not isinstance(date_str, str):
        return None

    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


# TOREVIEW: This function may need to be moved to a centralized location so it
#           can be used reliably across the entire application?


def validate_date_logic_consistency(meta: dict, path) -> list[str]:
    """Validate date-related consistency for status lifecycle."""
    violations = []
    status = meta.get("status")
    review_by = meta.get("review_by")
    edit_date = meta.get("date")

    review_date = parse_date(review_by) if review_by else None
    adr_date = parse_date(edit_date) if edit_date else None
    today = date_obj.today()

    # Status-specific review_by validation
    if status in ["Deprecated", "Superseded"]:
        if review_by and review_by not in (None, "", "null"):
            violations.append(
                f"{status} ADRs cannot have future 'review_by' dates "
                "(no reviews needed)"
            )

    elif status == "Proposed":
        if not review_by or review_by in (None, "", "null"):
            violations.append(
                "Proposed ADRs should have 'review_by' date for "
                "decision timeline"
            )
        elif review_date and review_date < today:
            violations.append(
                "Proposed ADRs cannot have past 'review_by' dates"
            )

    # Cross-date validation
    if adr_date and review_date:
        if review_date <= adr_date:
            violations.append("'review_by' date must be after 'date' field")

    # print (
    #     f"- [D VAL: SCHEMA-004] date checks: review_by vs. "
    #     f"adr_date: {review_by} vs. {adr_date}"
    # )

    return violations


# TOREVIEW: This function may need to be moved to a centralized location so it
#           can be used reliably across the entire application?


def validate_status_lifecycle_consistency(meta: dict, path) -> list[str]:
    """
    Validate internal consistency between status and other metadata fields.
    """
    violations = []
    status = meta.get("status")
    adr_id = meta.get("id")

    superseded_by = meta.get("superseded_by")
    supersedes = meta.get("supersedes")
    # review_by = meta.get("review_by")

    # Status-specific lifecycle consistency rules
    if status == "Proposed":
        if superseded_by and superseded_by not in (None, "", "null"):
            violations.append(
                "Proposed ADRs cannot have 'superseded_by' field "
                "(not yet accepted)"
            )
        if supersedes and supersedes not in (None, "", "null"):
            violations.append(
                "Proposed ADRs cannot have 'supersedes' field "
                "(not yet accepted)"
            )

    elif status == "Accepted":
        if superseded_by and superseded_by not in (None, "", "null"):
            violations.append(
                "Accepted ADRs cannot have 'superseded_by' field "
                "(accepted ADRs are current)"
            )

    elif status == "Deprecated":
        if supersedes and supersedes not in (None, "", "null"):
            violations.append(
                "Deprecated ADRs cannot have 'supersedes' field "
                "(deprecated ADRs don't supersede others)"
            )

    elif status == "Superseded":
        if supersedes and supersedes not in (None, "", "null"):
            violations.append(
                "Superseded ADRs cannot have 'supersedes' field "
                "(superseded ADRs don't supersede others)"
            )

    # Status-specific self-referential validation
    # (different from LINK cycle detection)
    if adr_id:
        if superseded_by and adr_id in str(superseded_by):
            violations.append(
                "ADR cannot be superseded by itself "
                f"(superseded_by references {adr_id})"
            )
        if supersedes and adr_id in str(supersedes):
            violations.append(
                "ADR cannot supersede itself "
                f"(supersedes references {adr_id})"
            )

    return violations


def validate_schema_004_status_field_requirements(ctx, rpt) -> None:
    """
    ADR-SCHEMA-004 — Status field requirements and lifecycle
    consistency validation.

    Validates status-dependent field requirements and internal
    consistency.
    """
    meta = ctx.meta
    path = ctx.path

    status = meta.get("status")

    # Validate status is a valid value
    if status and status not in VALID_STATUS_TRANSITIONS:
        rpt.add(
            _ERROR_CODE,
            path,
            f"invalid status '{status}' - must be one of: "
            f"{', '.join(VALID_STATUS_TRANSITIONS.keys())}",
        )
        return  # Skip further validation if status is invalid

    # Phase 1: Status-specific field requirements
    if status == "Superseded":
        superseded_by = meta.get("superseded_by")
        if not superseded_by or superseded_by in (None, "", "null"):
            rpt.add(
                _ERROR_CODE,
                path,
                "Superseded status requires non-empty 'superseded_by' field",
            )

    elif status == "Deprecated":
        superseded_by = meta.get("superseded_by")
        change_history = meta.get("change_history", [])

        # Check for justification via superseded_by or change_history
        has_superseded_by = superseded_by and superseded_by not in (
            None,
            "",
            "null",
        )
        has_change_history = (
            change_history
            and isinstance(change_history, list)
            and len(change_history) > 0
        )

        if not (has_superseded_by or has_change_history):
            rpt.add(
                _ERROR_CODE,
                path,
                "Deprecated status requires justification via 'superseded_by' "
                "field or 'change_history' entries",
            )

    # Remove pin format validation - handled by LINK-303
    # (Pin format validation removed to avoid duplication with ADR-LINK
    #  validators)

    # Phase 2: Status-lifecycle internal consistency validation
    lifecycle_violations = validate_status_lifecycle_consistency(meta, path)
    for violation in lifecycle_violations:
        rpt.add(_ERROR_CODE, path, violation)

    # Phase 2: Date logic consistency validation
    date_violations = validate_date_logic_consistency(meta, path)
    for violation in date_violations:
        rpt.add(_ERROR_CODE, path, violation)
