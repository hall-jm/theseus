# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/template/template_705_mirror_section_order.py

from __future__ import annotations

from ...constants import VALID_ADR_CLASSES
from ...parser.structure import expected_keys_for

_ERROR_CODE = "ADR-TEMPLATE-605"


def validate_template_705_mirror_section_order(ctx, rpt) -> None:
    """
    ADR-TEMPLATE-705 — mirror canonical section order of template_of.

    Ref: ADR-0001 §7.5/§10.5 · ADR-TEMPLATE-705
    """

    meta = ctx.meta
    if meta.get("class") != "template":
        return
    template_of = meta.get("template_of")

    if not isinstance(template_of, str):
        return
    elif not template_of or template_of not in VALID_ADR_CLASSES:
        return

    expected = expected_keys_for(template_of)
    found_keys = [k for k, _, _ in ctx.section_data.key_markers]

    if expected and found_keys:
        expected_present = [k for k in expected if k in found_keys]
        actual_order = [k for k in found_keys if k in expected]
        if expected_present != actual_order:
            rpt.add(
                _ERROR_CODE,
                ctx.path,
                f"template section order mismatch for {template_of} "
                f"(expected: {expected_present}, got: {actual_order})",
            )
