# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/schema_016_decision_format.py

from __future__ import annotations
import re

# Import centralized format validation from TEMPLATE-606
from ..template.template_606_content_formatting import (
    DECISION_ONE_LINER_PATTERN_RX,
    DECISION_ONE_LINER_KEY_PATTERN_RX,
    is_single_statement,
)


_ERROR_CODE = "ADR-SCHEMA-016"


def validate_schema_016_decision_format(ctx, rpt) -> None:
    """
    ADR-SCHEMA-016 — Content formatting matches documented format.

    Validates decision_one_liner section follows
    "Because X, we choose Y so that Z" format for all non-template ADR classes.

    Ref: ADR-0001 §4 · ADR-SCHEMA-016
    """
    meta = ctx.meta
    if meta.get("class") == "template":
        return  # TEMPLATE-606 handles templates

    adr_class = meta.get("class")
    if adr_class == "style-guide":
        return  # Style-guide exempt from canonical sections per ADR-0001 §7.4

    # Find decision_one_liner section - reuse section extraction logic
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

    # Validate format requirements for real ADRs (stricter than templates)
    has_correct_structure = DECISION_ONE_LINER_PATTERN_RX.match(clean_content)
    is_single = is_single_statement(clean_content)

    # Real ADRs should have actual content, not placeholder patterns
    has_placeholder_content = any(
        [
            re.search(r"<[^>]+>", clean_content),  # <angle brackets>
            re.search(r"\{[^}]+\}", clean_content),  # {curly brackets}
            re.search(r"\[[^\]]+\]", clean_content),  # [square brackets]
        ]
    )

    if not has_correct_structure or not is_single or has_placeholder_content:
        error_details = []
        if not has_correct_structure:
            error_details.append("incorrect structure")
        if not is_single:
            error_details.append("multiple sentences")
        if has_placeholder_content:
            error_details.append("contains placeholders")

        rpt.add(
            _ERROR_CODE,
            ctx.path,
            f"decision_one_liner format violation: {', '.join(error_details)}",
        )
