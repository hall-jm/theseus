# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/template/template_600_template_of_required.py

from __future__ import annotations

from ...constants import VALID_TEMPLATED_CLASSES

_ERROR_CODE = "ADR-TEMPLATE-600"


def validate_template_600_template_of_required(ctx, rpt) -> None:
    """
    ADR-TEMPLATE-600 — template_of missing/invalid (ADR-0001 §7.5).
    # Ref: ADR-0001 §7.5/§10.5 · ADR-TEMPLATE-600
    """
    meta = ctx.meta
    if meta.get("class") != "template":
        return
    template_of = meta.get("template_of")

    # Preserve legacy short-circuit semantics:
    #   - falsy values (None, "", []), non-strings, or strings not in the
    #     allowed set are invalid. This avoids TypeError for unhashable types
    #     like list while matching legacy behavior.

    if (
        not template_of
        or not isinstance(template_of, str)
        or template_of not in VALID_TEMPLATED_CLASSES
    ):
        rpt.add(
            _ERROR_CODE,
            ctx.path,
            f"template_of={template_of} invalid",
        )
