# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/constants/legacy.py

"""
Deprecated constants maintained for backward compatibility.

These constants are deprecated and will be removed in a future version.
Use get_canonical_keys() from sections.py instead.
"""

import warnings
from .sections import get_canonical_keys

# Issue deprecation warning once per import
warnings.warn(
    "CANONICAL_KEYS_* constants are deprecated. Use get_canonical_keys() "
    "instead.",
    DeprecationWarning,
    stacklevel=2,
)

# --- Deprecated Canonical Keys (computed from new architecture) -------------

CANONICAL_KEYS_OWNER = get_canonical_keys("owner")
CANONICAL_KEYS_DELTA = get_canonical_keys("delta", relaxed_delta=True)
CANONICAL_KEYS_STRATEGY = get_canonical_keys("strategy")

# Note: CANONICAL_KEYS_GOVERNANCE, CANONICAL_KEYS_TEMPLATE not provided
# as they didn't exist in the original constants.py
