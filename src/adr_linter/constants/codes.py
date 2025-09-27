# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/constants/codes.py

"""
Lint code definitions, severities, and derived sets.
"""

# --- Severity Definitions ----------------------------------------------------

SEVERITY = {"E": "block merge", "W": "proceed + annotate", "I": "log only"}
SEVERITY_LEVELS = {"I": 0, "W": 1, "E": 2}
SEVERITY_LEVELS_REV = {"I": 0, "W": 1, "E": 2}

# --- Lint Codes --------------------------------------------------------------

CODES = {
    # D
    "ADR-DELTA-300": ("E", "Override targets non-existent key in base."),
    # L
    "ADR-LINK-300": ("E", "Bi-directional link missing reciprocal"),
    "ADR-LINK-301": ("E", "Required uni-directional binding missing pin"),
    "ADR-LINK-302": ("W", "Pointer to section key missing in base"),
    "ADR-LINK-303": (
        "E",
        "Invalid pin format for relationship field - see  "
        "ADR-0001 §8 'Pointers & Deltas (inheritance rules)' for details",
    ),
    "ADR-LINK-304": ("E", "Pointer to normative section key missing in base"),
    "ADR-LINK-305": ("E", "Missing references to owner ADRs"),
    "ADR-LINK-320": ("I", "Supersede closure: multiple descendants"),
    "ADR-LINK-321": ("E", "Supersede closure: cycle detected"),
    "ADR-LINK-322": (
        "W",
        "Supersede closure: fork without rationale in `change_history`",
    ),
    # M
    "ADR-META-150": ("I", "`llm_tail` missing (optional)."),
    "ADR-META-151": (
        "W",
        "`llm_tail` disagrees with front-matter on " "required keys.",
    ),
    # N
    "ADR-NORM-101": ("E", "RFC-2119 keyword outside normative sections."),
    "ADR-NORM-102": (
        "W",
        "Vague term in normative section.",
    ),
    # P
    "ADR-PROC-241": ("I", "Minor style deviation; proceeded and logged."),
    "ADR-PROC-242": ("E", "Repeated minor deviation (≥3 in 30d)."),
    "ADR-PROC-243": (
        "I",
        "Possible duplication of existing pattern (exact/prefix name match "
        "without reference).",
    ),
    "ADR-PROC-250": (
        "E",
        "Linter run logs stale/missing in ADR linter logs directory.",
    ),
    # S
    "ADR-SCHEMA-001": (
        "E",
        "Missing required metadata (`id,title,status,class,date,review_by`) "
        "or bad `id`.",
    ),
    "ADR-SCHEMA-002": (
        "E",
        "Invalid class (`owner|delta|governance|strategy|"
        "style-guide|template`).",
    ),
    "ADR-SCHEMA-003": ("E", "Canonical section keys missing or out of order."),
    "ADR-SCHEMA-004": (
        "E",
        "Invalid status transition or illegal class change.",
    ),
    "ADR-SCHEMA-005": (
        "E",
        "Invalid date format (must be `YYYY-MM-DD`) for `date` or "
        "`review_by`.",
    ),
    "ADR-SCHEMA-006": ("E", "Governance ADR missing required 'scope' field"),
    "ADR-SCHEMA-007": ("E", "Owner ADR missing required 'governed_by' field"),
    "ADR-SCHEMA-008": (
        "E",
        "Invalid scope value - must be cli|engine|services|other",
    ),
    "ADR-SCHEMA-009": ("E", "Class-forbidden field present"),
    "ADR-SCHEMA-010": (
        "E",
        "Governance ADR missing required 'constraint_rules' section",
    ),
    "ADR-SCHEMA-011": ("E", "Owner ADR must not use `extends`."),
    "ADR-SCHEMA-012": ("E", "Non-Owner ADRs must never use `owner`."),
    "ADR-SCHEMA-013": ("E", "Non-Owner ADRs must identify ADR ownership."),
    "ADR-SCHEMA-014": (
        "E",
        "Invalid relationship field combination for ADR class",
    ),
    "ADR-SCHEMA-015": (
        "E",
        "ADR metadata violates its declared governance constraints",
    ),
    # T
    "ADR-TEMPLATE-700": (
        "E",
        "`template_of` missing or invalid "
        "(`owner|delta|governance|strategy|style-guide|template`).",
    ),
    "ADR-TEMPLATE-701": ("W", "`status` not `Proposed` in a template ADR."),
    "ADR-TEMPLATE-702": (
        "W",
        "filename does not include `-template-` (discoverability).",
    ),
    "ADR-TEMPLATE-703": (
        "E",
        "template participates in link graph (`extends` or `supersedes` "
        "non-null).",
    ),
    "ADR-TEMPLATE-704": (
        "W",
        "RFC-2119 keyword outside code fences/inline code in template.",
    ),
    "ADR-TEMPLATE-705": (
        "W",
        "template does not mirror canonical section order of `template_of` "
        "(same keys, same order).",
    ),
}

# --- Derived Sets (computed from CODES) -------------------------------------

CODES_BLOCKING = {
    code for code, (severity, _) in CODES.items() if severity == "E"
}
CODES_WARNING = {
    code for code, (severity, _) in CODES.items() if severity == "W"
}
CODES_INFO = {code for code, (severity, _) in CODES.items() if severity == "I"}

# --- Infrastructure Test Codes ----------------------------------------------

CODES_INFRA = {
    "ADR-REGISTRY-001",
    "ADR-REGISTRY-002",
    "ADR-REGISTRY-003",
    "ADR-REGISTRY-004",
    "ADR-POLICY-001",
    "ADR-POLICY-002",
    "ADR-POLICY-003",
    "ADR-SERVICES-001",
    "ADR-SERVICES-002",
    "ADR-PARSER-001",
    "ADR-PARSER-002",
    "ADR-FILTERS-001",
}

# --- Validation Functions ---------------------------------------------------


def _validate_severity_sets():
    """Ensure severity-based sets are complete and non-overlapping."""
    all_derived = CODES_BLOCKING | CODES_WARNING | CODES_INFO
    assert all_derived == set(
        CODES.keys()
    ), "Severity sets don't cover all codes"
    assert (
        len(CODES_BLOCKING & CODES_WARNING & CODES_INFO) == 0
    ), "Severity sets overlap"


def generate_codes_table():
    """Generate markdown table of all lint codes for documentation."""
    lines = [
        "| Code | Severity | Description |",
        "| ---- | -------- | ----------- |",
    ]
    for code, (sev, desc) in sorted(CODES.items()):
        lines.append(f"| {code} | {sev} | {desc} |")
    return "\n".join(lines)
