# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/meta/meta_202_llm_tail_malformed.py

"""
ADR-META-202 — `llm_tail` has malformed JSON syntax.

MALFORMED JSON VALIDATION:
Detects and reports JSON syntax errors in llm_tail blocks that prevent
proper parsing and break LLM tooling integration.

VALIDATION SCOPE:
- JSON syntax validation (brackets, quotes, commas)
- Basic structure validation (must be object, not array/primitive)
- Invalid escape sequences, trailing commas, etc.
- Detailed error reporting for debugging

ARCHITECTURAL CONTEXT:
Parser extracts llm_tail block and attempts JSON parsing. When parsing
fails, parser returns llm_tail=None. This validator detects the parsing
failure and provides detailed syntax error feedback.

VALIDATION TIMING:
Should run before META-201 to catch JSON syntax errors that would break
field comparison validation.

Ref: ADR-0001 §12 (LLM tail), §14 (META-202)
"""

from __future__ import annotations
import json
import re

_ERROR_CODE = "ADR-META-202"


def validate_meta_202_llm_tail_malformed(ctx, rpt) -> None:
    """
    Validate llm_tail JSON syntax and structure.

    VALIDATION LOGIC:
    - Check if llm_tail block exists but parsing failed (llm_tail is None)
    - Re-attempt JSON parsing with detailed error reporting
    - Validate JSON structure (must be object for metadata)

    ERROR REPORTING:
    Provides specific syntax error details to help with debugging
    rather than silent parsing failure.
    """

    body = ctx.body if hasattr(ctx, "body") else ""
    llm_tail = ctx.section_data.llm_tail

    # Single pattern that matches all llm_tail blocks
    llm_tail_pattern = re.compile(
        r"<!--\s*llm_tail:begin\s*-->"
        r".*?```json\s*"
        r"(?P<json>.*?)"  # Remove \r?\n requirement
        r"\s*```"
        r".*?<!--\s*llm_tail:end\s*-->",
        re.DOTALL,
    )

    match = llm_tail_pattern.search(body)
    if not match:
        return  # No llm_tail block found - ignore completely

    json_content = match.group("json").strip()

    # Now analyze what we found
    if not json_content:
        # Empty JSON block
        rpt.add(
            _ERROR_CODE,
            ctx.path,
            "llm_tail JSON block is empty or only json markdown codeblock "
            "with no contents",
        )
        return

    # If parser successfully parsed it, no validation needed
    if llm_tail is not None:
        # print("- [D VAL: META-202] if llm_tail is not None")
        # print(f"-- [D VAL: META-202] llm_tail is type: {type(llm_tail)}")
        # Additional validation: ensure it's an object, not array/primitive
        if not isinstance(llm_tail, dict):
            rpt.add(
                _ERROR_CODE,
                ctx.path,
                "llm_tail must be JSON object, found: "
                f"{type(llm_tail).__name__}",
            )
        return

    # Parser failed to parse - attempt detailed error reporting
    if not json_content:
        rpt.add(_ERROR_CODE, ctx.path, "llm_tail JSON block is empty")
        return

    try:
        parsed = json.loads(json_content)
        # If we can parse it but parser couldn't, report the discrepancy
        if not isinstance(parsed, dict):
            rpt.add(
                _ERROR_CODE,
                ctx.path,
                "llm_tail must be JSON object, found: "
                f"{type(parsed).__name__}",
            )
        else:
            rpt.add(
                _ERROR_CODE,
                ctx.path,
                "llm_tail parsing discrepancy - validator parsed successfully "
                "but parser failed",
            )
    except json.JSONDecodeError as e:
        # Provide detailed JSON syntax error
        rpt.add(
            _ERROR_CODE,
            ctx.path,
            f"llm_tail malformed JSON: {e.msg} at line {e.lineno}, "
            f"column {e.colno}",
        )
    except Exception as e:
        # Catch other JSON-related errors
        rpt.add(_ERROR_CODE, ctx.path, f"llm_tail JSON error: {str(e)}")
