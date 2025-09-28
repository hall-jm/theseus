# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/constants/validation.py

"""
Validation patterns, valid values, and metadata definitions.
"""

import re

# --- ADR Structure Constants -------------------------------------------------

VALID_ADR_OWNERSHIP_GROUPS = {"Project Maintainer"}

REQUIRED_META = ["id", "title", "status", "class", "date", "review_by"]

NORMATIVE_KEYS = {"decision_details", "rollout_backout"}

DATE_KEY_NAMES = ("date", "review_by")

# All relationship fields in the system
ALL_RELATIONSHIP_FIELDS = {
    "extends",
    "supersedes",
    "superseded_by",
    "governed_by",
    "informs",
    "informed_by",
    "owners_ptr",
}

# Class validation constraints
VALID_ADR_CLASSES = {
    "delta",
    "governance",
    "owner",
    "strategy",
    "style-guide",
    "template",
}

VALID_SCOPE_VALUES = {"cli", "engine", "services", "other"}
VALID_GOVERNED_CLASSES = {"owner", "delta", "strategy"}
VALID_TEMPLATED_CLASSES = VALID_ADR_CLASSES - {"template"}

# Class-specific allowed relationship fields
CLASS_ALLOWED_RELATIONSHIPS = {
    "owner": {"supersedes", "superseded_by", "governed_by", "informed_by"},
    "governance": {"supersedes", "superseded_by", "informed_by"},
    "strategy": {
        "supersedes",
        "superseded_by",
        "owners_ptr",
        "governed_by",
        "informs",
    },
    "delta": {"extends", "supersedes", "superseded_by", "owners_ptr"},
    "template": {
        "extends",
        "supersedes",
        "superseded_by",
        "governed_by",
        "informs",
        "informed_by",
    },
    # "template": set(),  # No relationship fields allowed
    "style-guide": {"supersedes", "superseded_by"},
}

# Class-specific field restrictions per ADR-0001 §3
# TOREVIEW: also includes `scope` which isn't a relationship: confirm?
# TOREVIEW: If `scope` should not be in this list, then do we need to
#           create "master" lists for all items, all forbidden items, etc.
CLASS_FORBIDDEN_RELATIONSHIPS = {
    "owner": {"extends", "owners_ptr"},
    "governance": {"extends", "owners_ptr", "governed_by", "informs"},
    "strategy": {"owners", "scope"},
    "delta": {"owners", "scope"},
    "template": {
        "extends",
        "supersedes",
        "governed_by",
        "scope",
        "owners",
        "informs",
        "informed_by",
    },
    "style-guide": {"extends", "supersedes", "governed_by", "scope"},
}

# --- LLM Tail ----------------------------------------------------------------

# LLM tail validation field sets
LLM_TAIL_CORE_FIELDS = [
    "id",
    "class",
    "status",
    "extends",
    "governed_by",
    "scope",
    "informs",
    "informed_by",
]

LLM_TAIL_OWNERSHIP_FIELDS = ["owners", "owners_ptr"]

# All fields that should be validated in llm_tail
LLM_TAIL_ALL_FIELDS = LLM_TAIL_CORE_FIELDS + LLM_TAIL_OWNERSHIP_FIELDS


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

# --- Compiled Regex Patterns -------------------------------------------------

CODE_RX = re.compile(r"^ADR-(?P<band>[A-Z]+)-(?P<num>\d{3})$")
PLACEHOLDER_RX = re.compile(r"_placeholder\.py\Z")
DATE_RX = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EXTENDS_RX = re.compile(r"^ADR-\d{4}@(20\d{2}-\d{2}-\d{2}|[0-9a-f]{7,40})$")
ID_RX = re.compile(r"^ADR-\d{4}$")

RFC_2119_RX = re.compile(
    r"\b(" + "|".join(map(re.escape, RFC_2119_TERMS)) + r")\b",
    re.I,  # case-insensitive per ADR-0001
)

VAGUE_TERMS_RX = re.compile(
    r"\b(robust|simple|scalable|flexible|significant|efficient|reliable)\b",
    re.I,
)

# Pattern for "Because X, we choose Y so that Z" format
DECISION_ONE_LINER_PATTERN_RX = re.compile(
    r"Because\s+.+?,\s+we\s+choose\s+.+?\s+so\s+that\s+.+?\.",
    re.IGNORECASE | re.DOTALL,
)

DECISION_ONE_LINER_KEY_PATTERN_RX = re.compile(
    r"<!-- key: decision_one_liner -->\s*\n(.*?)(?=<!-- key: \w+|$)",
    re.DOTALL,
)

# --- Regex List of RegEx -----------------------------------------------------

# Common placeholder patterns in templates
PLACEHOLDER_PATTERNS = [
    r"<[^>]+>",  # <angle-bracket placeholders>
    r"\{[^}]+\}",  # {curly-bracket placeholders}
    r"\[[^\]]+\]",  # [square-bracket placeholders]
    r"YYYY-MM-DD",  # Date placeholders
    r"TODO:",  # TODO markers
    r"PLACEHOLDER",  # Explicit placeholder text
    r"EXAMPLE",  # Example text
    # Section patterns
    r"Because\s+<[^>]+>,\s+we\s+choose\s+<[^>]+>\s+so\s+that\s+<[^>]+>\.",
    r"Because\s+\{[^}]+\},\s+we\s+choose\s+\{[^}]+\}\s+so\s+that\s+\{[^}]+\}\.",  # noqa: E501
    r"Because\s+\[[^\]]+\],\s+we\s+choose\s+\[[^\]]+\]\s+so\s+that\s+\[[^\]]+\]\.",  # noqa: E501
]

# Real value indicators that suggest non-placeholder content
REAL_VALUE_INDICATORS = [
    r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
    r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b",  # noqa: E501
    r"\b(20\d{2})\b",  # Specific years like 2024, 2025
    r"\b(v\d+\.\d+)\b",  # Version numbers like v1.2
    r"@\w+\.\w+",  # Email patterns
    r"https?://[^\s]+",  # Actual URLs
    r"\$\d+",  # Specific dollar amounts
    r"\b\d{1,3}(,\d{3})*\b",  # Large numbers with commas
]

# --- Regex List of Compiled RegEx --------------------------------------------

PLACEHOLDER_BRACKET_PATTERNS_RXL = [
    re.compile(r"<[^>]+>"),  # Angle brackets
    re.compile(r"\{[^}]+\}"),  # Curly brackets
    re.compile(r"\[[^\]]+\]"),  # Square brackets
]

# --- Status Transition Rules -------------------------------------------------

VALID_STATUS_TRANSITIONS = {
    "Proposed": {"Accepted", "Deprecated", "Superseded"},
    "Accepted": {"Deprecated", "Superseded"},
    "Deprecated": {"Superseded"},  # Can still be superseded for clarity
    "Superseded": set(),  # Terminal state
}


# --- Validation API ----------------------------------------------------------

# TOREVIEW: Because of how TEMPLATE-606 was implemented, it created a need for
#           parsing placeholder content and determinining single statement
#           (e.g., one statement ending with one period '.') and to me, that
#           logic looked like it should be centralized somewhere for wider
#           reuse instead of being stuck in a validation rule file.
# TODO: Where should validation logic go?  parser? here like sections.py
#       provides canonical key API?


def has_placeholder_content(content: str) -> bool:
    """
    Check if content contains any placeholder bracket patterns.
    """
    return any(
        pattern.search(content) for pattern in PLACEHOLDER_BRACKET_PATTERNS_RXL
    )


def is_single_statement(content: str) -> bool:
    """
    Check if content is a single statement (one sentence).
    """
    sentences = re.split(r"[.!?]+\s+", content.strip())
    return len([s for s in sentences if s.strip()]) == 1
