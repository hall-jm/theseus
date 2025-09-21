# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tools/adr_linter/validators/__init__.py

"""
Validator package exports.

Execution order and wiring live in `tools.adr_linter.validators.registry`.
This module intentionally avoids defining a pipeline to prevent duplication.
"""

from __future__ import annotations

# Re-export commonly used rule entrypoints for convenience (optional)
from .link.link_205_governance import validate_link_205_governance
from .link.link_222_fork_no_rationale import (
    validate_link_222_fork_no_rationale_for_meta,
)

__all__ = [
    "validate_link_205_governance",
    "validate_link_222_fork_no_rationale_for_meta",
]
