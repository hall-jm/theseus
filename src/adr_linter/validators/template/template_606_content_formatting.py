# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/template/template_606_content_formatting.py

from __future__ import annotations
import re

from ...constants.validation import (
    DECISION_ONE_LINER_PATTERN_RX,
    DECISION_ONE_LINER_KEY_PATTERN_RX,
    has_placeholder_content,
    is_single_statement,
)

_ERROR_CODE = "ADR-TEMPLATE-606"


def validate_template_606_content_formatting(ctx, rpt) -> None:
    """
    ADR-TEMPLATE-606 — Content formatting matches documented format.

    Validates decision_one_liner section follows:
    "Because X, we choose Y so that Z" pattern.

    Ref: ADR-0001 §4 · ADR-TEMPLATE-606
    """
    meta = ctx.meta
    if meta.get("class") != "template":
        return

    # Find decision_one_liner section - work around parser position issues
    match = DECISION_ONE_LINER_KEY_PATTERN_RX.search(ctx.body)
    if not match:
        return  # Let other validators handle missing sections

    decision_section = match.group(1).strip()

    # Remove HTML comments and markdown syntax for content analysis
    clean_content = re.sub(
        r"<!--.*?-->", "", decision_section, flags=re.DOTALL
    )
    clean_content = re.sub(r"^#+\s*", "", clean_content, flags=re.MULTILINE)
    clean_content = clean_content.strip()

    if not clean_content:
        return  # Empty section, let other validators handle

    # Validate format requirements
    has_correct_structure = DECISION_ONE_LINER_PATTERN_RX.match(clean_content)
    has_placeholders = has_placeholder_content(clean_content)
    is_single = is_single_statement(clean_content)

    if not (has_correct_structure and has_placeholders and is_single):
        rpt.add(
            _ERROR_CODE,
            ctx.path,
            "Template section content formatting does not match documented "
            "format: decision_one_liner",
        )
