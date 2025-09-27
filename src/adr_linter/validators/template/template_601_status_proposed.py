# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/template/template_701_status_proposed.py

from __future__ import annotations


def validate_template_701_status_proposed(ctx, rpt) -> None:
    """
    ADR-TEMPLATE-701 — status SHOULD be Proposed (ADR-0001 §7.5).

    Ref: ADR-0001 §7.5/§10.5 · ADR-TEMPLATE-701
    """
    meta = ctx.meta
    if meta.get("class") != "template":
        return
    if meta.get("status") != "Proposed":
        rpt.add(
            "ADR-TEMPLATE-701",
            ctx.path,
            f"status={meta.get('status')} in template",
        )
