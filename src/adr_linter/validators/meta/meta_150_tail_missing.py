# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/meta/meta_150_tail_missing.py

"""
ADR-META-150 — `llm_tail` missing (optional).

 Ref: ADR-0001 §12 · ADR-META-150
"""

from __future__ import annotations


def validate_meta_150_tail_missing(ctx, rpt) -> None:
    if ctx.section_data.llm_tail is None:
        rpt.add("ADR-META-150", ctx.path, "llm_tail missing (optional)")
