# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/meta/meta_200_tail_missing.py

"""
ADR-META-200 — `llm_tail` missing (optional).

 Ref: ADR-0001 §14 · ADR-META-200
"""

from __future__ import annotations

_ERROR_CODE = "ADR-META-200"


def validate_meta_200_tail_missing(ctx, rpt) -> None:
    if ctx.section_data.llm_tail is None:
        rpt.add(_ERROR_CODE, ctx.path, "llm_tail missing (optional)")
