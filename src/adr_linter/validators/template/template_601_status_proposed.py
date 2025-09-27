# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/template/template_601_status_proposed.py

from __future__ import annotations

_ERROR_CODE = "ADR-TEMPLATE-601"


def validate_template_601_status_proposed(ctx, rpt) -> None:
    """
    ADR-TEMPLATE-601 — status MUST USE Proposed (ADR-0001 §3).

    Ref: ADR-0001 §3/§7.5/§10.5 · ADR-TEMPLATE-601
    """
    meta = ctx.meta

    print(f"[D VAL: TEMPLATE-601] status: _{meta.get("status")}_")

    if meta.get("class") != "template":
        return
    if meta.get("status") != "Proposed":
        rpt.add(
            _ERROR_CODE,
            ctx.path,
            f"status={meta.get('status')} in template",
        )
