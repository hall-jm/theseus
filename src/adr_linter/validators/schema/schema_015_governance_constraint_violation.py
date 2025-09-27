# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_015_governance_constraint_violation.py

"""
ADR-SCHEMA-015 — ADR metadata violates its declared governance constraints

GOVERNANCE CONSTRAINT COMPLIANCE:
ADRs that declare governance binding via `governed_by` must comply with
the constraints defined by their governing ADR. This validator checks
basic metadata compliance against governance scope and authority rules.

VALIDATION SCOPE:
Single-file validation only - checks ADR metadata against its declared
governance binding without cross-file constraint interpretation.
Full governance constraint validation requires cross-ADR analysis.

BASIC CONSTRAINT CHECKS:
- Scope compliance: ADR scope must align with its governance authority
- Authority chain integrity: governed_by must reference valid governance ADR
- Field consistency: ADR fields must be consistent with governance requirements

ARCHITECTURAL CONTEXT:
The governed_by field creates authority binding that must be respected.
ADRs that violate their declared governance constraints undermine the
architectural governance framework and enable boundary drift.

LIMITATION:
This implementation provides basic validation. Full constraint interpretation
requires parsing governance ADR constraint_rules blocks and applying
complex governance logic - deferred to future enhancement.

Ref: ADR-0001 §0.3 (Constraint Binding), §3 (governed_by field),
              §14 (SCHEMA-015)
"""

from __future__ import annotations

from ...constants import (
    VALID_GOVERNED_CLASSES,
)

_ERROR_CODE = "ADR-SCHEMA-015"


def validate_schema_015_governance_constraint_violation(ctx, rpt) -> None:
    """
    Validate ADR metadata complies with declared governance constraints.

    VALIDATION LOGIC:
    - Basic compliance checks for ADRs with governed_by field
    - Single-file validation only (no cross-ADR constraint interpretation)
    - Future enhancement: full governance constraint parsing and validation

    CURRENT IMPLEMENTATION:
    Basic structural validation to establish the validation framework.
    Full governance constraint interpretation requires significant
    architecture for parsing and applying governance rules.

    GOVERNANCE BINDING:
    ADRs with governed_by field declare constraint binding that should
    be validated, but complex constraint interpretation is deferred.
    """
    meta = ctx.meta
    path = ctx.path

    # Only validate ADRs that declare governance binding
    governed_by = meta.get("governed_by")
    if not governed_by or governed_by in ("", "null", "Null", None):
        return  # No governance binding declared

    # Basic validation: governed_by should be properly formatted
    # (Pin format validation handled by LINK validators)

    # TODO: Future enhancement - parse governance constraints and validate
    #       compliance
    # This requires:
    # 1. Cross-file governance ADR lookup
    # 2. YAML constraint block parsing
    # 3. Constraint rule interpretation and application
    # 4. Scope and authority boundary validation

    # Placeholder for basic structural validation
    adr_class = meta.get("class")

    # Basic check: only classes that should have governance binding
    if adr_class not in VALID_GOVERNED_CLASSES:  # per ADR-0001 §3
        rpt.add(
            _ERROR_CODE,
            path,
            f"{adr_class} ADR should not declare 'governed_by' field",
        )

    # Additional basic validation can be added here without requiring
    # full cross-file governance constraint interpretation
