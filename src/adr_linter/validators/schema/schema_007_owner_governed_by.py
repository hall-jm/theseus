# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_007_owner_governed_by.py

"""
ADR-SCHEMA-007 — Owner ADR missing required `governed_by` field

AUTHORITY CHAIN VALIDATION:
Owner ADRs must declare their governance authority binding to establish
which governance ADR controls their scope and authority boundaries.

REQUIRED FIELD VALIDATION:
- class: owner → governed_by: REQUIRED (ADR-####@pin format)
- All other classes → governed_by: OPTIONAL (inherited or context-dependent)

ARCHITECTURAL CONTEXT:
The governed_by field creates the authority chain that prevents component
boundary drift. Without it, Owner ADRs operate without governance constraints,
undermining the architectural governance framework.

GOVERNANCE BINDING SEMANTICS:
- governed_by is unidirectional (no reciprocal requirement)
- Pin format validation handled by LINK validators
- Content validation (target exists) handled by LINK validators
- This validator only checks presence for Owner class

Ref: ADR-0001 §0.3 (Constraint Binding), §3 (Owner required fields),
     §7.1 (Owner class), §14 (SCHEMA-007)
"""

from __future__ import annotations

_ERROR_CODE = "ADR-SCHEMA-007"


def validate_schema_007_owner_governed_by(ctx, rpt) -> None:
    """
    Validate Owner ADRs have required governed_by field.

    VALIDATION LOGIC:
    - IF class == "owner" AND governed_by is missing/empty → ERROR
    - All other classes: no validation (governed_by optional for them)

    PIN FORMAT:
    Format validation (ADR-####@pin) handled by LINK validators.
    This validator only checks field presence.

    AUTHORITY CHAIN:
    governed_by establishes which governance ADR controls this owner's scope.
    Missing field breaks authority chain and enables architectural drift.
    """
    meta = ctx.meta
    path = ctx.path

    # Only validate owner class for governed_by requirement
    if meta.get("class") == "owner":
        governed_by = meta.get("governed_by")

        # Check for missing, empty, or null-equivalent values
        is_missing = (
            not governed_by
            or governed_by in (None, "")
            or str(governed_by).lower() == "null"
        )

        if is_missing:
            rpt.add(
                _ERROR_CODE,
                path,
                "owner ADR missing required 'governed_by' field",
            )
