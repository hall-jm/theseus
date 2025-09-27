# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_008_invalid_scope_value.py

"""
ADR-SCHEMA-008 — Invalid `scope` value

SCOPE VALUE VALIDATION:
Governance ADRs must use valid scope values from the defined taxonomy
to enable proper precedence resolution and authority boundary enforcement.

VALID SCOPE VALUES:
- "cli" - User-facing processes (UI, argument parsing, user messages)
- "engine" - Internal pure processes (orchestration, validation, responses)
- "services" - Impure edge processes (filesystem, network, IO operations)
- "other" - All other processes not captured above

VALIDATION LOGIC:
- IF class == "governance" AND scope has invalid value → ERROR
- IF class != "governance" AND scope is present → SCHEMA-009 handles
  (forbidden field)
- SCHEMA-006 handles missing scope for governance class

ARCHITECTURAL CONTEXT:
The scope taxonomy enables the precedence resolution system defined in
ADR-0001 §0.2 (cli > engine > services > other). Invalid scope values
break conflict resolution and authority boundary determination.

Ref: ADR-0001 §0.2 (Scope Taxonomy), §3 (Governance scope field),
     §7.6 (Governance class), §14 (SCHEMA-008)
"""

from __future__ import annotations

# Valid scope values per ADR-0001 §0.2 Scope Taxonomy
from ...constants import VALID_SCOPE_VALUES


_ERROR_CODE = "ADR-SCHEMA-008"


def validate_schema_008_invalid_scope_value(ctx, rpt) -> None:
    """
    Validate governance ADRs use valid scope values.

    VALIDATION LOGIC:
    - IF class == "governance" AND scope not in valid set → ERROR
    - Only validates when scope is present (SCHEMA-006 handles missing)
    - Only validates governance class (SCHEMA-009 handles forbidden for
      others)

    SCOPE TAXONOMY:
    Valid values: cli, engine, services, other
    Invalid examples: "frontend", "backend", "database", custom values

    PRECEDENCE SYSTEM:
    Scope values enable automatic conflict resolution via precedence order.
    Invalid values break the governance authority resolution system.
    """
    meta = ctx.meta
    path = ctx.path

    # Only validate governance class scope values
    if meta.get("class") == "governance":
        scope = meta.get("scope")

        # Only validate if scope is present (SCHEMA-006 handles missing)
        if scope:
            print(f"- [D VAL: SCHEMA-008] scope: _{scope}_")
            # Normalize whitespace for validation
            normalized_scope = str(scope).strip()

            if normalized_scope not in VALID_SCOPE_VALUES:
                valid_list = ", ".join(sorted(VALID_SCOPE_VALUES))
                rpt.add(
                    "ADR-SCHEMA-008",
                    path,
                    f"invalid scope '{scope}' - must be one of: {valid_list}",
                )
