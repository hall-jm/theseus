# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/template/template_608_real_values_not_placeholders.py

from __future__ import annotations
import re

from ...constants.validation import (
    PLACEHOLDER_PATTERNS,
    REAL_VALUE_INDICATORS,
)

_ERROR_CODE = "ADR-TEMPLATE-608"


def validate_template_608_real_values_not_placeholders(ctx, rpt) -> None:
    """
    ADR-TEMPLATE-608 — Template contains real values instead of placeholders.

    Ref: ADR-0001 §7.5/§10.5 · ADR-TEMPLATE-608
    """
    meta = ctx.meta
    if meta.get("class") != "template":
        return

    body = ctx.body

    # print(
    #      "- [D VAL TEMPLATE-608] Before for pattern in REAL_VALUE_INDICATORS"
    #  )

    # Check for real value indicators
    for pattern in REAL_VALUE_INDICATORS:
        matches = re.finditer(pattern, body, re.IGNORECASE)

        # print(
        #    f"- [D VAL TEMPLATE-608] In for pattern in "
        #    f"REAL_VALUE_INDICATORS: - pattern: {pattern}"
        # )
        for match in matches:
            # Debug output
            # print(
            #    f"- [D VAL TEMPLATE-608] Found match: '{match.group()}' "
            #    f"with pattern: {pattern}"
            # )

            # Skip if this appears to be inside a placeholder pattern
            text_around = body[max(0, match.start() - 20) : match.end() + 20]
            is_in_placeholder = any(
                re.search(placeholder_pattern, text_around)
                for placeholder_pattern in PLACEHOLDER_PATTERNS
            )

            # print(
            #    f"- [D VAL TEMPLATE-608] Text around: '{text_around}', "
            #    f"is_in_placeholder: {is_in_placeholder}"
            # )

            if not is_in_placeholder:
                rpt.add(
                    _ERROR_CODE,
                    ctx.path,
                    f"template contains real value '{match.group()}' "
                    "instead of placeholder",
                )
                return  # Report first violation only
