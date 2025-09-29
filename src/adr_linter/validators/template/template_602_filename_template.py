# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/template/template_602_filename_template.py

from __future__ import annotations


_ERROR_CODE = "ADR-TEMPLATE-602"


def validate_template_602_filename_template(ctx, rpt) -> None:
    """
    ADR-TEMPLATE-602 — filename SHOULD include -template- (discoverability).

    Ref: ADR-0001 §7.5/§10.5 · ADR-TEMPLATE-602
    """
    meta = ctx.meta
    if meta.get("class") != "template":
        return
    if "-template-" not in ctx.path.name.lower():
        rpt.add(_ERROR_CODE, ctx.path, "filename missing -template-")
