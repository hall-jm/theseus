# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_006_governance_scope.py

"""
ADR-SCHEMA-006 — Governance ADR missing required `scope` field

GOVERNANCE AUTHORITY VALIDATION:
Governance ADRs must declare their authority scope to enable proper
boundary enforcement and conflict resolution per ADR-0001 §0.2.

REQUIRED FIELD VALIDATION:
- class: governance → scope: REQUIRED (cli|engine|services|other)
- All other classes → scope: FORBIDDEN (handled by SCHEMA-009)

ARCHITECTURAL CONTEXT:
The scope field establishes which domain the governance ADR controls,
enabling the precedence resolution system (cli > engine > services > other)
and preventing overlapping authority claims.

Ref: ADR-0001 §0.2 (Scope Taxonomy), §3 (Governance required fields),
     §7.6 (Governance class), §14 (SCHEMA-006)
"""

from __future__ import annotations

# from ...constants import VALID_ADR_CLASSES


_ERROR_CODE = "ADR-SCHEMA-006"


def validate_schema_006_governance_scope(ctx, rpt) -> None:
    """
    Validate governance ADRs have required scope field.

    VALIDATION LOGIC:
    - IF class == "governance" AND scope is missing/empty → ERROR
    - All other classes: no validation (scope forbidden by SCHEMA-009)

    SCOPE VALUES:
    Valid values defined in constants but validated by SCHEMA-008.
    This validator only checks presence, not value validity.
    """
    meta = ctx.meta
    path = ctx.path

    # Only validate governance class for scope requirement
    if meta.get("class") == "governance":
        scope = meta.get("scope")
        if not scope or scope in (None, "", "null", "Null"):
            rpt.add(
                _ERROR_CODE,
                path,
                "governance ADR missing required 'scope' field",
            )
