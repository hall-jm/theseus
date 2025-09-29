# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/meta/meta_201_tail_mismatch.py

"""
ADR-META-201 — `llm_tail` disagrees with front-matter on required keys.

Ref: ADR-0001 §14 · ADR-META-201
"""

from __future__ import annotations

from ...constants import LLM_TAIL_CORE_FIELDS

_ERROR_CODE = "ADR-META-201"


def validate_meta_201_tail_mismatch(ctx, rpt) -> None:
    tail = ctx.section_data.llm_tail
    if not tail:
        return
    elif tail is not None and not isinstance(tail, dict):
        # META-202's pytest were triggering this validator because it wasn't
        # checking to ensure that the data type was dict
        # TOREVIEW: Does this validator need to record any validation issues
        #           to the report?  Confirm or remove this TOREVIEW if not
        #           needed
        return

    meta = ctx.meta
    mismatches = []

    for field in LLM_TAIL_CORE_FIELDS:
        tail_val = tail.get(field)
        meta_val = meta.get(field)

        # Normalize empty values (treat None, "", "null" as equivalent)
        tail_normalized = (
            None if tail_val in (None, "", "null", "Null") else tail_val
        )
        meta_normalized = (
            None if meta_val in (None, "", "null", "Null") else meta_val
        )

        if tail_normalized != meta_normalized:
            mismatches.append(field)

    # Special handling for ownership fields
    # (either owners OR owners_ptr should match)
    meta_owners = meta.get("owners")
    meta_owners_ptr = meta.get("owners_ptr")
    tail_owners = tail.get("owners")
    tail_owners_ptr = tail.get("owners_ptr")

    # Normalize ownership values
    meta_owners_norm = (
        None if meta_owners in (None, "", "null", "Null") else meta_owners
    )
    meta_owners_ptr_norm = (
        None
        if meta_owners_ptr in (None, "", "null", "Null")
        else meta_owners_ptr
    )
    tail_owners_norm = (
        None if tail_owners in (None, "", "null", "Null") else tail_owners
    )
    tail_owners_ptr_norm = (
        None
        if tail_owners_ptr in (None, "", "null", "Null")
        else tail_owners_ptr
    )

    # Check ownership consistency - simplified logic
    ownership_mismatch = False

    # Compare owners field directly
    if meta_owners_norm != tail_owners_norm:
        ownership_mismatch = True

    # Compare owners_ptr field directly
    if meta_owners_ptr_norm != tail_owners_ptr_norm:
        ownership_mismatch = True

    if ownership_mismatch:
        mismatches.append("ownership")

    # Report all mismatches
    if mismatches:
        rpt.add(
            _ERROR_CODE, ctx.path, f"tail mismatch: {', '.join(mismatches)}"
        )
