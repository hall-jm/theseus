# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/constants/__init__.py

"""
Constants package for ADR linter.

Provides backward-compatible imports while organizing constants into
logical modules for better maintainability.
"""

# Explicit imports to avoid flake8 F403/F401 warnings
from .codes import (
    CODES,
    CODES_BLOCKING,
    CODES_WARNING,
    CODES_INFO,
    CODES_INFRA,
    SEVERITY,
    SEVERITY_LEVELS,
    SEVERITY_LEVELS_REV,
    generate_codes_table,
)

from .validation import (
    VALID_ADR_OWNERSHIP_GROUPS,
    REQUIRED_META,
    NORMATIVE_KEYS,
    DATE_KEY_NAMES,
    VALID_ADR_CLASSES,
    RFC_2119_TERMS,
    CODE_RX,
    PLACEHOLDER_RX,
    DATE_RX,
    EXTENDS_RX,
    ID_RX,
    RFC_2119_RX,
    VAGUE_TERMS_RX,
    VALID_STATUS_TRANSITIONS,
)

from .sections import (
    SECTIONS_UNIVERSAL_OPENING,
    SECTIONS_UNIVERSAL_CLOSING,
    CLASS_INSERTIONS,
    HEADING_ALIASES,
    get_canonical_keys,
)

from .legacy import (
    CANONICAL_KEYS_OWNER,
    CANONICAL_KEYS_DELTA,
    CANONICAL_KEYS_STRATEGY,
)

# File I/O definitions (keep here as they don't fit other modules)
ADR_LOCATIONS = (
    "docs/adrs/**/*.md",  # New Style Guide Enforced ADR location
    "docs/adrs/*.md",
)

# Re-export all for backward compatibility
__all__ = [
    # Codes
    "CODES",
    "CODES_BLOCKING",
    "CODES_WARNING",
    "CODES_INFO",
    "CODES_INFRA",
    "SEVERITY",
    "SEVERITY_LEVELS",
    "SEVERITY_LEVELS_REV",
    "generate_codes_table",
    # Validation
    "VALID_ADR_OWNERSHIP_GROUPS",
    "REQUIRED_META",
    "NORMATIVE_KEYS",
    "DATE_KEY_NAMES",
    "VALID_ADR_CLASSES",
    "RFC_2119_TERMS",
    "CODE_RX",
    "PLACEHOLDER_RX",
    "DATE_RX",
    "EXTENDS_RX",
    "ID_RX",
    "RFC_2119_RX",
    "VAGUE_TERMS_RX",
    "VALID_STATUS_TRANSITIONS",
    # Sections
    "SECTIONS_UNIVERSAL_OPENING",
    "SECTIONS_UNIVERSAL_CLOSING",
    "CLASS_INSERTIONS",
    "HEADING_ALIASES",
    "get_canonical_keys",
    # Legacy
    "CANONICAL_KEYS_OWNER",
    "CANONICAL_KEYS_DELTA",
    "CANONICAL_KEYS_STRATEGY",
    # File I/O
    "ADR_LOCATIONS",
]
