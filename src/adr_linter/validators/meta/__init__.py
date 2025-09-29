# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/meta/__init__.py

from .meta_200_tail_missing import validate_meta_200_tail_missing
from .meta_201_tail_mismatch import validate_meta_201_tail_mismatch
from .meta_202_llm_tail_malformed import validate_meta_202_llm_tail_malformed


# single source for registry
META_RULES_PER_FILE = [
    ("ADR-META-200", validate_meta_200_tail_missing),
    ("ADR-META-201", validate_meta_201_tail_mismatch),
    ("ADR-META-202", validate_meta_202_llm_tail_malformed),
]

META_RULES_POST_RUN = []

__all__ = [
    "META_RULES_PER_FILE",
    "META_RULES_POST_RUN",
]
