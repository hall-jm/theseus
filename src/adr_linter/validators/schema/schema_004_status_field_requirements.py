# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_004_status_field_requirements.py

"""
ADR-SCHEMA-004 — Status field requirements
                 (MISNAMED - NOT transition validation)

CRITICAL: This validator has a misleading name and incomplete implementation.

WHAT IT ACTUALLY DOES:
- Validates Superseded status requires non-empty `superseded_by` field
- Validates Deprecated status requires either `superseded_by` OR
  `change_history`
- Single-file validation only (no cross-file state comparison)

WHAT ADR-0001 §14 SPECIFICATION CLAIMS IT SHOULD DO:
- "Invalid status transition or illegal class change"
- Should validate status changes against VALID_STATUS_TRANSITIONS state machine
- Should prevent illegal class changes between ADR versions

ARCHITECTURE CONSTRAINT:
Single-file validation context means true "transition" validation
(old state → new state) would require different validator architecture or
cross-file analysis capability.

FUTURE REFACTOR OPTIONS:
1. Rename this to schema_004a_status_field_requirements.py (accurate name)
2. Create schema_004b_status_transitions.py for actual transition validation
3. Keep useful field validation, add proper transition logic when architecture
supports it

Ref: ADR-0001 §Status transitions, §14 SCHEMA-004,
     constants/validation.py VALID_STATUS_TRANSITIONS
"""

from __future__ import annotations


_ERROR_CODE = "ADR-SCHEMA-004"

# TECHNICAL DEBT IDENTIFIED:
# BLOCKER: Missing actual status transition validation logic
# BLOCKER: Missing class change validation entirely
# FIXME: Function name misleads - should be
#        schema_004_status_field_requirements
# TODO: Real transition validation requires cross-file comparison capability
# REVIEW: Current implementation is useful but misscoped


def validate_schema_004_status_transition(ctx, rpt) -> None:
    meta = ctx.meta
    path = ctx.path

    status = meta.get("status")
    if status == "Superseded":
        sb = meta.get("superseded_by")
        if not sb or sb in (None, "", "null"):
            rpt.add(_ERROR_CODE, path)
        return

    if status == "Deprecated":
        sb = meta.get("superseded_by")
        ch = meta.get("change_history", [])
        has_justification = bool(sb and sb not in (None, "", "null"))
        has_rationale = bool(ch and isinstance(ch, list))
        if not (has_justification or has_rationale):
            rpt.add(_ERROR_CODE, path)
