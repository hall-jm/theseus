# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/template/template_607_governance_constraint_rules.py

from __future__ import annotations

_ERROR_CODE = "ADR-TEMPLATE-607"


def validate_template_607_governance_constraint_rules(ctx, rpt) -> None:
    """
    ADR-TEMPLATE-607 — Governance template missing `constraint_rules` block
                       placeholder.

    Ref: ADR-0001 §7.5/§10.5 · ADR-TEMPLATE-607
    """
    meta = ctx.meta
    if meta.get("class") != "template":
        return

    template_of = meta.get("template_of")
    if template_of != "governance":
        return

    # Check if constraint_rules section exists
    section_keys = [k for k, _, _ in ctx.section_data.key_markers]
    if "constraint_rules" not in section_keys:
        rpt.add(
            _ERROR_CODE,
            ctx.path,
            "governance template missing constraint_rules section",
        )
