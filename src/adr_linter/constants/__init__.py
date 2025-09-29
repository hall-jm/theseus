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
    ALL_RELATIONSHIP_FIELDS,
    VALID_ADR_OWNERSHIP_GROUPS,
    REQUIRED_META,
    NORMATIVE_KEYS,
    DATE_KEY_NAMES,
    VALID_ADR_CLASSES,
    VALID_GOVERNED_CLASSES,
    VALID_TEMPLATED_CLASSES,
    VALID_SCOPE_VALUES,
    VALID_SCOPE_TOPIC_VALUES,
    VALID_SCOPE_YAML_KEYS,
    CLASS_ALLOWED_RELATIONSHIPS,
    CLASS_FORBIDDEN_RELATIONSHIPS,
    RFC_2119_TERMS,
    VALID_STATUS_TRANSITIONS,
    LLM_TAIL_CORE_FIELDS,
    LLM_TAIL_OWNERSHIP_FIELDS,
    LLM_TAIL_ALL_FIELDS,
    # RegEx
    # - Patterns: Compiled
    CODE_RX,
    PLACEHOLDER_RX,
    DATE_RX,
    EXTENDS_RX,
    ID_RX,
    RFC_2119_RX,
    VAGUE_TERMS_RX,
    DECISION_ONE_LINER_PATTERN_RX,
    DECISION_ONE_LINER_KEY_PATTERN_RX,
    CONSTRAINT_RULES_KEY_PATTERN_RX,
    # - Patterns: Lists of RegEx
    PLACEHOLDER_PATTERNS,
    REAL_VALUE_INDICATORS,
    # - Patterns: Lists of Compiled RegEx
    PLACEHOLDER_BRACKET_PATTERNS_RXL,
    # VALID_SCOPE_TOPIC_PATTERNS_RXL,
    # defs
    has_placeholder_content,
    is_single_statement,
    get_scope_topic_patterns,
    detect_real_governance_values,
)

from .sections import (
    SECTIONS_UNIVERSAL_OPENING,
    SECTIONS_UNIVERSAL_CLOSING,
    CLASS_INSERTIONS,
    HEADING_ALIASES,
    get_canonical_keys,
    get_expected_header_text,
    find_markdown_headers,
    validate_section_headers,
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
    "ALL_RELATIONSHIP_FIELDS",
    "VALID_ADR_OWNERSHIP_GROUPS",
    "VALID_GOVERNED_CLASSES",
    "REQUIRED_META",
    "NORMATIVE_KEYS",
    "DATE_KEY_NAMES",
    "VALID_ADR_CLASSES",
    "VALID_SCOPE_VALUES",
    "VALID_SCOPE_TOPIC_VALUES",
    "VALID_SCOPE_YAML_KEYS",
    "VALID_TEMPLATED_CLASSES",
    "CLASS_ALLOWED_RELATIONSHIPS",
    "CLASS_FORBIDDEN_RELATIONSHIPS",
    "RFC_2119_TERMS",
    # RegEx
    # - Patterns: Compiled
    "CODE_RX",
    "PLACEHOLDER_RX",
    "DATE_RX",
    "EXTENDS_RX",
    "ID_RX",
    "RFC_2119_RX",
    "VAGUE_TERMS_RX",
    "DECISION_ONE_LINER_PATTERN_RX",
    "DECISION_ONE_LINER_KEY_PATTERN_RX",
    "CONSTRAINT_RULES_KEY_PATTERN_RX",
    # - Patterns: Lists of RegEx
    "PLACEHOLDER_PATTERNS",
    "REAL_VALUE_INDICATORS",
    "VALID_STATUS_TRANSITIONS",
    # - Patterns: Lists of Compiled RegEx
    "PLACEHOLDER_BRACKET_PATTERNS_RXL",
    # "VALID_SCOPE_TOPIC_PATTERNS_RXL",
    # - defs
    "has_placeholder_content",
    "is_single_statement",
    "get_scope_topic_patterns",
    "detect_real_governance_values",
    # Sections
    "SECTIONS_UNIVERSAL_OPENING",
    "SECTIONS_UNIVERSAL_CLOSING",
    "CLASS_INSERTIONS",
    "HEADING_ALIASES",
    "get_canonical_keys",
    "get_expected_header_text",
    "find_markdown_headers",
    "validate_section_headers",
    # LLM Tail
    "LLM_TAIL_CORE_FIELDS",
    "LLM_TAIL_OWNERSHIP_FIELDS",
    "LLM_TAIL_ALL_FIELDS",
    # Legacy
    "CANONICAL_KEYS_OWNER",
    "CANONICAL_KEYS_DELTA",
    "CANONICAL_KEYS_STRATEGY",
    # File I/O
    "ADR_LOCATIONS",
]
