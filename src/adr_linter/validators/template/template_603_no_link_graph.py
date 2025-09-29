# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/template/template_603_no_link_graph.py

from __future__ import annotations

from ...constants.validation import CLASS_FORBIDDEN_RELATIONSHIPS


_ERROR_CODE = "ADR-TEMPLATE-603"


def validate_template_603_no_link_graph(ctx, rpt) -> None:
    """
    ADR-TEMPLATE-603 — templates must not participate in link graph.

    Ref: ADR-0001 §7.5/§10.5 · ADR-TEMPLT-603
    """
    meta = ctx.meta
    if meta.get("class") != "template":
        return

    for field in CLASS_FORBIDDEN_RELATIONSHIPS["template"]:
        value = meta.get(field)

        # print( f"-- [D TEST: TEMPLATE-603] field value: {field}:{value}")

        if value not in (None, "", "null", []):
            rpt.add(
                _ERROR_CODE,
                ctx.path,
                f"template has forbidden relationship: {field} - "
                "see constants.validation.py for forbidden list",
            )
