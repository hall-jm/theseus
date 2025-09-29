# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_014_invalid_relationship_combination.py

"""
ADR-SCHEMA-014 — Invalid relationship field combination for ADR class

RELATIONSHIP FIELD VALIDATION:
Beyond forbidden fields (SCHEMA-009), certain combinations of relationship
fields create architectural inconsistencies or violate governance constraints.
This validator enforces valid relationship patterns per class.

INVALID COMBINATIONS:
- Delta with extends but missing owners_ptr (inheritance without ownership ref)
- Template with template_of but non-null relationship fields
  (scaffolding contamination)
- Strategy with informs but missing owners_ptr
  (strategic direction without ownership)
- Owner with governed_by pointing to non-governance ADR
  (invalid authority binding)

ARCHITECTURAL CONTEXT:
Relationship fields create the governance graph that enforces authority
boundaries. Invalid combinations break the authority chain or create
governance paradoxes that undermine the architectural decision framework.

VALIDATION SCOPE:
This validator checks field combinations and basic reference patterns.
Cross-file validation (target existence, reciprocity) handled by LINK
validators. Governance constraint compliance handled by SCHEMA-015.

Ref: ADR-0001 §3 (Relationship fields), §8 (Inheritance rules),
     §14 (SCHEMA-014)
"""

from __future__ import annotations

from ...constants import (
    CLASS_FORBIDDEN_RELATIONSHIPS,
)

_ERROR_CODE = "ADR-SCHEMA-014"


def validate_schema_014_invalid_relationship_combination(ctx, rpt) -> None:
    """
    Validate relationship field combinations are valid for ADR class.

    VALIDATION LOGIC:
    - Check class-specific relationship field requirements
    - Validate field combination consistency
    - Single-file validation only (no cross-ADR validation)

    COMBINATION RULES:
    Each class has specific relationship field patterns that must be followed
    to maintain governance integrity and authority chain consistency.


    Also:
    Historical Note: ADR-0001 disagreement on whether ADR-SCHEMA-009 vs.
                     ADR-SCHEMA-014 should prevail on if `informed_by`
                     should be allowed.  Decision was to keep template
                     ADRs are scaffolding only for now.
                     You can use the fields for placeholders, but values
                     have to pass `has_value()` checker.
    Rationale: Templates should be pure scaffolding without any governance
               graph participation. Strategic direction should apply to the
               instantiated ADRs, not their templates.
    """
    meta = ctx.meta
    path = ctx.path

    adr_class = meta.get("class")
    if not adr_class:
        return  # No class, skip validation

    # Helper to check if field has non-empty value
    def has_value(field_name):
        value = meta.get(field_name)
        return value and value not in ("", "null", "Null", None)

    # Delta ADR validation
    if adr_class == "delta":
        if has_value("extends") and not has_value("owners_ptr"):
            rpt.add(
                _ERROR_CODE,
                path,
                "delta ADR with 'extends' must have 'owners_ptr'",
            )

    # Template ADR validation
    elif adr_class == "template":
        for field in CLASS_FORBIDDEN_RELATIONSHIPS[adr_class]:
            if has_value(field):
                rpt.add(
                    _ERROR_CODE,
                    path,
                    f"template ADR cannot have relationship field '{field}'",
                )

    # Strategy ADR validation
    elif adr_class == "strategy":
        if has_value("informs") and not has_value("owners_ptr"):
            rpt.add(
                "ADR-SCHEMA-014",
                path,
                "strategy ADR with 'informs' must have 'owners_ptr'",
            )

    # Owner ADR validation
    elif adr_class == "owner":
        if has_value("extends"):
            rpt.add(_ERROR_CODE, path, "owner ADR cannot use 'extends' field")

    # Governance ADR validation
    elif adr_class == "governance":
        # forbidden_relationships = ["extends", "governed_by", "informs"]
        forbidden_relationships = CLASS_FORBIDDEN_RELATIONSHIPS[adr_class]
        for field in forbidden_relationships:
            if has_value(field):
                rpt.add(
                    _ERROR_CODE,
                    path,
                    f"governance ADR cannot use '{field}' field",
                )
