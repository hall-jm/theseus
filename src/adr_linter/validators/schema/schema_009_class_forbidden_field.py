# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_009_class_forbidden_field.py

"""
ADR-SCHEMA-009 — Class-forbidden field present

CLASS-SPECIFIC FIELD RESTRICTIONS:
Each ADR class has forbidden fields that would violate architectural
constraints or create governance boundary conflicts. This validator
enforces these restrictions per ADR-0001 §3 class-specific field
requirements.

FORBIDDEN FIELD MAPPINGS:
- Owner: extends, owners_ptr (can't inherit, defines ownership)
- Governance: extends, owners_ptr, governed_by, informs (authority source)
- Strategy: owners, scope (references ownership, no governance authority)
- Delta: owners, scope (inherits ownership, no governance authority)
- Template: extends, supersedes, governed_by, scope, owners (scaffolding only)
- Style-guide: extends, supersedes, governed_by, scope (bootstrap exempt)

ARCHITECTURAL RATIONALE:
Forbidden fields prevent architectural violations like:
- Owner ADRs claiming inheritance (breaks authority chain)
- Strategy ADRs defining ownership (breaks reference pattern)
- Templates participating in governance (breaks scaffolding role)

Ref: ADR-0001 §3 (Class-specific requirements), §7 (ADR classes),
     §14 (SCHEMA-009)
"""

from __future__ import annotations

from ...constants import CLASS_FORBIDDEN_RELATIONSHIPS

_ERROR_CODE = "ADR-SCHEMA-009"


def validate_schema_009_class_forbidden_field(ctx, rpt) -> None:
    """
    Validate ADR classes don't contain forbidden fields.

    VALIDATION LOGIC:
    - Check if any forbidden fields are present for the ADR's class
    - Only validate non-empty field values (empty/null allowed)
    - Report each forbidden field violation separately

    FIELD PRESENCE CHECK:
    Considers field "present" if it exists and has non-empty value.
    Empty strings, null, None are treated as "not present".

    ARCHITECTURAL ENFORCEMENT:
    Prevents governance boundary violations and maintains clean
    class separation per the ADR framework design.
    """
    meta = ctx.meta
    path = ctx.path

    adr_class = meta.get("class")
    if not adr_class or adr_class not in CLASS_FORBIDDEN_RELATIONSHIPS:
        return  # Unknown class, skip validation

    forbidden_fields = CLASS_FORBIDDEN_RELATIONSHIPS[adr_class]

    for field in forbidden_fields:
        field_value = meta.get(field)

        # Check if field is present and non-empty
        if field_value and field_value not in ("", "null", "Null"):
            rpt.add(
                _ERROR_CODE,
                path,
                f"{adr_class} ADR cannot use '{field}' field",
            )
