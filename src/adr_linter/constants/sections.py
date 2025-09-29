# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/constants/sections.py

"""
Canonical section definitions implementing ADR-0001 §4 architecture.

This module implements the universal + class-specific section structure
defined in ADR-0001 §4, replacing the old hardcoded per-class lists.
"""

import re

from typing import List, Optional
from .validation import VALID_ADR_CLASSES

# --- Universal Sections (ADR-0001 §4) ---------------------------------------

SECTIONS_UNIVERSAL_OPENING = [
    "decision_one_liner",
    "context_and_drivers",
    "options_considered",
    "decision_details",
]

SECTIONS_UNIVERSAL_CLOSING = [
    "evidence_and_links",
    "glossary",
    "related_adrs",
    "license",
]

# --- Class-Specific Section Insertions --------------------------------------

CLASS_INSERTIONS = {
    "owner": [
        "consequences_and_risks",
        "implementation_notes",
        "rollout_backout",
    ],
    "governance": [
        "authority_scope",
        "constraint_rules",
        "precedence_mappings",
        "adoption_and_enforcement",
    ],
    "strategy": [
        "principles",
        "guardrails",
        "consequences_and_risks",
        "implementation_notes",
        "north_star_metrics",
    ],
}

# --- Heading Aliases for Parser ---------------------------------------------

HEADING_ALIASES = {
    # Universal sections
    "Decision (one-liner)": "decision_one_liner",
    "Decision (One-liner)": "decision_one_liner",
    "Context & Drivers": "context_and_drivers",
    "Context and Drivers": "context_and_drivers",
    "Options Considered": "options_considered",
    "Decision Details": "decision_details",
    "Evidence & Links": "evidence_and_links",
    "Evidence and Links": "evidence_and_links",
    "Glossary": "glossary",
    "Related ADRs": "related_adrs",
    "License": "license",
    # Owner/Delta sections
    "Consequences & Risks": "consequences_and_risks",
    "Consequences and Risks": "consequences_and_risks",
    "Implementation Notes": "implementation_notes",
    "Rollout & Backout": "rollout_backout",
    "Rollout and Backout": "rollout_backout",
    # Strategy sections
    "Principles": "principles",
    "Guardrails": "guardrails",
    "North Star Metrics": "north_star_metrics",
    "North-Star Metrics": "north_star_metrics",
    # Governance sections
    "Authority Scope": "authority_scope",
    "Constraint Rules": "constraint_rules",
    "Precedence Mappings": "precedence_mappings",
    "Adoption & Enforcement": "adoption_and_enforcement",
    "Adoption and Enforcement": "adoption_and_enforcement",
}

# --- Canonical Keys API -----------------------------------------------------


def get_canonical_keys(
    class_name: str,
    *,
    template_of: Optional[str] = None,
    base_keys: Optional[List[str]] = None,
    relaxed_delta: bool = False,
) -> List[str]:
    """
    Single source of truth for canonical section keys per ADR-0001 §4.

    Single-file first: enforce universal canonical order everywhere;
    specialize only when explicit front-matter or optional context is provided.

    Args:
        class_name: ADR class (owner, delta, governance, strategy,
                    style-guide, template)
        template_of: For template class, mirror the target class keys
        base_keys: Future hook for cross-file delta validation (unused
                   for now)
        relaxed_delta: For delta class, enforce universal order only (allow
                       base extras)

    Returns:
        Ordered list of canonical section keys for the class

    Limitations:
        This refactor handles simple canonical keys only. Dotted keys
        (e.g., consequences_and_risks.requirements per ADR-0001 §11)
        are not implemented and require parser extensions for RFC-2119
        validation.
    """

    # Style-guide exempt from canonical sections per ADR-0001 §7.4
    if class_name == "style-guide":
        return []

    # Template mirrors template_of class per ADR-0001 §7.5
    if class_name == "template":
        if not isinstance(template_of, str) and class_name == "template":
            # print(
            #    f"-[D constants.section.py] template_of: "
            #    f"{str(template_of)}, {type(template_of)}"
            # )

            # HACK: identifying missing input validation through new pytests
            #       not sure yet how to address this issue as either a new
            #       undocumented error band and what boundary is supposed
            #       to govern this kind of error (e.g., engine? cli?
            #       validation? )

            # e.g.,:
            # raise ValueError(
            #     f"Invalid template_of: expected string, "
            #     f"got {type(template_of).__name__}"
            # )

            return []

        if not template_of or template_of not in VALID_ADR_CLASSES:
            return []  # Let TEMPLATE-700/705 handle the error

        return get_canonical_keys(template_of)

    # Delta relaxed mode: universal sections required in order, base extras
    # allowed
    if class_name == "delta" and relaxed_delta:
        return SECTIONS_UNIVERSAL_OPENING + SECTIONS_UNIVERSAL_CLOSING

    # Standard class: universal + class-specific insertions
    insertions = CLASS_INSERTIONS.get(class_name, [])
    return SECTIONS_UNIVERSAL_OPENING + insertions + SECTIONS_UNIVERSAL_CLOSING


# TOREVIEW: Where should this logic go?  Identifying section headers or
#           section markdown does not need to be located within any
#           individual validator


def find_markdown_headers(body: str) -> dict[str, list[int]]:
    """
    Find all markdown headers and their line numbers.
    """
    headers = {}
    lines = body.split("\n")

    for line_num, line in enumerate(lines, 1):
        # Match markdown headers (## Header Text)
        header_match = re.match(r"^#+\s+(.+)$", line.strip())
        if header_match:
            header_text = header_match.group(1).strip()
            if header_text not in headers:
                headers[header_text] = []
            headers[header_text].append(line_num)

    return headers


def get_expected_header_text(section_key: str) -> str:
    """
    Get all acceptable markdown header texts for a section key.
    """
    acceptable_headers = []

    # Find all heading aliases that map to this section key
    for heading_text, key in HEADING_ALIASES.items():
        if key == section_key:
            acceptable_headers.append(heading_text)

    # If no aliases found, use fallback
    if not acceptable_headers:
        acceptable_headers.append(section_key.replace("_", " ").title())

    return acceptable_headers


# TOREVIEW: Where should this logic go?  Again if this code is validating
#           data but the data is section-related, who owns it?
# TODO:  Need to document and flesh out this boundary to clean it up


def validate_section_headers(ctx, section_keys: list[str]) -> list[str]:
    """
    Validate that section keys have corresponding markdown headers.
    """
    violations = []
    markdown_headers = find_markdown_headers(ctx.body)

    for section_key in section_keys:
        acceptable_headers = get_expected_header_text(section_key)

        # Check if any acceptable header exists
        header_found = any(
            header in markdown_headers for header in acceptable_headers
        )

        if not header_found:
            # Show all acceptable options in error
            header_options = "' or '".join(acceptable_headers)
            violations.append(
                f"section '{section_key}' missing markdown "
                f"header '{header_options}'"
            )

    return violations
