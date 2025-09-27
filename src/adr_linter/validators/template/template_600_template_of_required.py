# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/template/template_700_template_of_required.py

from __future__ import annotations


def validate_template_700_template_of_required(ctx, rpt) -> None:
    """
    ADR-TEMPLATE-700 — template_of missing/invalid (ADR-0001 §7.5).
    # Ref: ADR-0001 §7.5/§10.5 · ADR-TEMPLATE-700
    """
    meta = ctx.meta
    if meta.get("class") != "template":
        return
    template_of = meta.get("template_of")

    # Preserve legacy short-circuit semantics:
    #   - falsy values (None, "", []), non-strings, or strings not in the
    #     allowed set are invalid. This avoids TypeError for unhashable types
    #     like list while matching legacy behavior.
    allowed = {"owner", "delta", "strategy", "style-guide"}
    if (
        not template_of
        or not isinstance(template_of, str)
        or template_of not in allowed
    ):
        rpt.add(
            "ADR-TEMPLATE-700",
            ctx.path,
            f"template_of={template_of} invalid",
        )
