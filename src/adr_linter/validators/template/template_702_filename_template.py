# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/template/template_702_filename_template.py

from __future__ import annotations


def validate_template_702_filename_template(ctx, rpt) -> None:
    """
    ADR-TEMPLATE-702 — filename SHOULD include -template- (discoverability).

    Ref: ADR-0001 §7.5/§10.5 · ADR-TEMPLATE-702
    """
    meta = ctx.meta
    if meta.get("class") != "template":
        return
    if "-template-" not in ctx.path.name.lower():
        rpt.add("ADR-TEMPLATE-702", ctx.path, "filename missing -template-")
