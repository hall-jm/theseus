# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_010_governance_constraint_rules.py

"""
ADR-SCHEMA-010 — Governance ADR missing required `constraint_rules` section

GOVERNANCE CONSTRAINT ENFORCEMENT:
Governance ADRs must include a constraint_rules section with machine-readable
YAML blocks that define REQUIRED/FORBIDDEN/OWNED_BY authority mappings.

SECTION VALIDATION:
- class: governance → constraint_rules section: REQUIRED
- Section must contain YAML block with constraint schema
- Content validation (YAML syntax, schema) handled by ADR-GOVERN validators
- This validator only checks section presence

ARCHITECTURAL CONTEXT:
The constraint_rules section provides the sole binding authority for governance
per ADR-0001 §0.4. Without it, governance ADRs have no enforceable constraints
and become documentation-only rather than machine-checkable governance.

CONSTRAINT SCHEMA REFERENCE:
```yaml
constraint_rules:
  REQUIRED: [list]     # Topics this scope must handle
  FORBIDDEN: [list]    # Topics this scope must not handle
  OWNED_BY: [{topic, owner}]  # Explicit ownership assignments
```

Ref: ADR-0001 §0.4 (Machine Constraints), §4 (Governance sections),
     §5.3 (Governance constraint schema), §7.6 (Governance class),
     §14 (SCHEMA-010)
"""

from __future__ import annotations


_ERROR_CODE = "ADR-SCHEMA-010"


def validate_schema_010_governance_constraint_rules(ctx, rpt) -> None:
    """
    Validate governance ADRs have required constraint_rules section.

    VALIDATION LOGIC:
    - IF class == "governance" AND constraint_rules section missing → ERROR
    - Section presence checked via HTML markers or heading aliases
    - Content validation (YAML syntax, schema) deferred to ADR-GOVERN
      validators

    SECTION DETECTION:
    Uses parser section detection (key markers or heading aliases).
    Follows same pattern as other canonical section validation.

    MACHINE CONSTRAINT AUTHORITY:
    constraint_rules section contains the sole binding authority source
    for governance constraints. Missing section = no enforceable governance.
    """
    meta = ctx.meta
    path = ctx.path

    # Only validate governance class for constraint_rules requirement
    if meta.get("class") == "governance":
        # Check if constraint_rules section exists
        sections_by_key = ctx.section_data.sections_by_key

        # Primary detection: HTML key marker
        has_constraint_rules = "constraint_rules" in sections_by_key

        # Fallback: Check for heading alias (future enhancement)
        # Note: heading aliases for constraint_rules defined in
        #       constants/sections.py

        if not has_constraint_rules:
            rpt.add(
                _ERROR_CODE,
                path,
                "governance ADR missing required 'constraint_rules' section",
            )
