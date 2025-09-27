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

VALID_ADR_CLASSES = {
    "delta",
    "governance",
    "owner",
    "strategy",
    "style-guide",
    "template",
}

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

# --- Compiled Regex Patterns ------------------------------------------------

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

# --- Status Transition Rules -------------------------------------------------

VALID_STATUS_TRANSITIONS = {
    "Proposed": {"Accepted", "Deprecated", "Superseded"},
    "Accepted": {"Deprecated", "Superseded"},
    "Deprecated": {"Superseded"},  # Can still be superseded for clarity
    "Superseded": set(),  # Terminal state
}
