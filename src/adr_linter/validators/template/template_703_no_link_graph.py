# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/template/template_703_no_link_graph.py

from __future__ import annotations


def validate_template_703_no_link_graph(ctx, rpt) -> None:
    """
    ADR-TEMPLATE-703 — templates must not participate in link graph.

    Ref: ADR-0001 §7.5/§10.5 · ADR-TEMPLT-703
    """
    meta = ctx.meta
    if meta.get("class") != "template":
        return
    if meta.get("extends") not in (None, "", "null"):
        rpt.add("ADR-TEMPLATE-703", ctx.path, "template has extends")
    if meta.get("supersedes") not in (None, "", "null", []):
        rpt.add("ADR-TEMPLATE-703", ctx.path, "template has supersedes")
