# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/constants.py

"""
TOREVIEW: [!?] - Need to confirm why this exists if not used in the actual
                 linter
          [??] - Need to confirm if this entry is still needed in this
                 file
"""

import re

# -----------------------------
# Constants
# -----------------------------

# --- File I/O Definitions ----------------------------------------------------

ADR_LOCATIONS = (
    "docs/adrs/**/*.md",  # New Style Guide Enforced ADR location
    "docs/adrs/*.md",
)

# --- Lint Code Definitions ---------------------------------------------------

# TOREVIEW: Consolidate & Refactor
SEVERITY = {"E": "block merge", "W": "proceed + annotate", "I": "log only"}
SEVERITY_LEVELS = {"I": 0, "W": 1, "E": 2}
SEVERITY_LEVELS_REV = {"I": 0, "W": 1, "E": 2}


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
        "Invalid class (`owner|delta|strategy|style-guide|template`).",
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
    "ADR-SCHEMA-011": ("E", "Owner ADR must not use `extends`."),
    "ADR-SCHEMA-012": ("E", "Non-Owner ADRs must never use `owner`."),
    "ADR-SCHEMA-013": ("E", "Non-Owner ADRs must identify ADR ownership."),
    "ADR-SCHEMA-021": (
        "E",
        "Strategy ADR contains `rollout_backout` (by marker **or** heading "
        "`Rollout & Backout`).",
    ),
    # T
    "ADR-TEMPLATE-700": (
        "E",
        "`template_of` missing or invalid "
        "(`owner|delta|strategy|style-guide|template`).",
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
    # TOREVIEW: Adding codes for testing downstream tooling:
    #           e.g., tools/adr_check_code_consistency.py
    # "ADR-TEST-999": ("E", "Fake code for testing gap detection"),
}

# Derived sets (computed from CODES, not hardcoded)
CODES_BLOCKING = {
    code for code, (severity, _) in CODES.items() if severity == "E"
}
CODES_WARNING = {
    code for code, (severity, _) in CODES.items() if severity == "W"
}
CODES_INFO = {code for code, (severity, _) in CODES.items() if severity == "I"}


# Optional: validation that derived sets match expectations
def _validate_severity_sets():
    """Ensure severity-based sets are complete and non-overlapping."""
    all_derived = CODES_BLOCKING | CODES_WARNING | CODES_INFO
    assert all_derived == set(
        CODES.keys()
    ), "Severity sets don't cover all codes"
    assert (
        len(CODES_BLOCKING & CODES_WARNING & CODES_INFO) == 0
    ), "Severity sets overlap"


# Call validation in development/test environments
# if __name__ == "__main__" or os.getenv("VALIDATE_CONSTANTS"):
#     _validate_severity_sets()

# Infrastructure test codes (linter quality checks, no validators)
"""
Reasoning: Keeping infrastructure codes separate from business validation
           codes while giving verification scripts a way to categorize
           them as "legitimate but different" rather than "orphaned."

Decision: The verification script can then check: is this code in
          CODES.keys()? Business rule.
          Is it in INFRA_CODES? Infrastructure test.
          Neither? Actually orphaned.
"""
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

# --- ADR Structure Constants -------------------------------------------------

VALID_ADR_OWNERSHIP_GROUPS = {"Project Maintainer"}

REQUIRED_META = ["id", "title", "status", "class", "date", "review_by"]

NORMATIVE_KEYS = {"decision_details", "rollout_backout"}

"""
Implement ADR-LINK-201 (missing pin) and make RFC regex case-insensitive,
add date rule ADR-SCHEMA-005

Enforce YYYY-MM-DD and actual calendar validity
"""
DATE_KEY_NAMES = ("date", "review_by")

# FIXME: This section of code is out of sync with new version of
#        ADR-0001 §4. Canonical section keys & order

# TOREVIEW: This list needs to be consolidated and centralized in a single
#           location
VALID_ADR_CLASSES = {
    "delta",
    "governance",
    "owner",
    "strategy",
    "style-guide",
    "template",
}

# TOREVIEW: Adding new keys requires updating HEADINGS_TO_KEYS patterns
#           currently located in 'adr_linter.py'
CANONICAL_KEYS_OWNER = [
    "decision_one_liner",
    "context_and_drivers",
    "options_considered",
    "decision_details",
    "consequences_and_risks",
    "rollout_backout",
    "implementation_notes",
    "evidence_and_links",
    "glossary",
    "related_adrs",
]

CANONICAL_KEYS_DELTA = CANONICAL_KEYS_OWNER[:]

# TOREVIEW: Adding new keys requires updating HEADINGS_TO_KEYS patterns
#           currently located in 'adr_linter.py'
CANONICAL_KEYS_STRATEGY = [
    "decision_one_liner",
    "context_and_drivers",
    "principles",
    "guardrails",
    "north_star_metrics",
    "consequences_and_risks",
    "implementation_notes",
    "evidence_and_links",
    "glossary",
    "related_adrs",
]

# --- RFC-2119 and Validation Patterns ----------------------------------------

RFC_2119_TERMS = [
    "MUST",
    "MUST NOT",
    "SHOULD",
    "SHOULD NOT",
    "SHALL",
    "SHALL NOT",
    "MAY",
    "RECOMMENDED",
    "NOT RECOMMENDED",
]

CODE_RX = re.compile(r"^ADR-(?P<band>[A-Z]+)-(?P<num>\d{3})$")
PLACEHOLDER_RX = re.compile(r"_placeholder\.py\Z")

DATE_RX = re.compile(r"^\d{4}-\d{2}-\d{2}$")

EXTENDS_RX = re.compile(r"^ADR-\d{4}@(20\d{2}-\d{2}-\d{2}|[0-9a-f]{7,40})$")

ID_RX = re.compile(r"^ADR-\d{4}$")

RFC_2119_RX = re.compile(
    r"\b(" + "|".join(map(re.escape, RFC_2119_TERMS)) + r")\b",
    re.I,  # <-- case-insensitive per ADR-0001
)

VAGUE_TERMS_RX = re.compile(
    r"\b(robust|simple|scalable|flexible|significant|efficient|reliable)\b",
    re.I,
)

# --- Status Transition Rules -------------------------------------------------


VALID_STATUS_TRANSITIONS = {
    "Proposed": {"Accepted", "Deprecated", "Superseded"},
    "Accepted": {"Deprecated", "Superseded"},
    "Deprecated": {"Superseded"},  # Can still be superseded for clarity
    "Superseded": set(),  # Terminal state
}


# TOREVIEW: Creation of utils sub-directory or file for defs like the one
#           shown below;
# FIXME: Yes, this code should not be in the constants.py file, but I wanted
#        to finally remove legacy.py from the repo and this was the last
#        orphaned def(); it never got fully implemented, but having code
#        to generate code output for ADR documentation may be helpful in the
#        future;
def generate_codes_table():
    """Generate markdown table of all lint codes for documentation"""
    lines = [
        "| Code | Severity | Description |",
        "| ---- | -------- | ----------- |",
    ]
    for code, (sev, desc) in sorted(CODES.items()):
        lines.append(f"| {code} | {sev} | {desc} |")
    return "\n".join(lines)
