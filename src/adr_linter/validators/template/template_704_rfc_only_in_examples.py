# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/template/template_704_rfc_only_in_examples.py

from __future__ import annotations

from ...constants import RFC_2119_RX
from ...parser.structure import find_balanced_code_fences, line_from_pos


def validate_template_704_rfc_only_in_examples(ctx, rpt) -> None:
    """ADR-TEMPLATE-704 — RFC-2119 terms only inside code fences/inline code.

    Extracted from legacy.validate_rfc_terms_optimized (template branch).
    Behavior unchanged.

    Ref: ADR-0001 §7.5/§10.5 · ADR-TEMPLATE-704
    """
    meta = ctx.meta
    if meta.get("class") != "template":
        return

    body = ctx.body
    path = ctx.path

    # Build exclusions
    exclusions = []
    exclusions.extend(find_balanced_code_fences(body))

    # NOTE: placeholder to satisfy flake8; actual inline handled below
    # for m in RFC_2119_RX.finditer(r"`[^`]*`"):
    #     pass

    # Inline code
    for m in __import__("re").finditer(r"`[^`]*`", body):
        exclusions.append((m.start(), m.end()))

    # URLs
    for m in __import__("re").finditer(r"https?://[^\s\])<>\"']+", body):
        exclusions.append((m.start(), m.end()))

    # HTML comments
    for m in __import__("re").finditer(
        r"<!--.*?-->", body, flags=__import__("re").S
    ):
        exclusions.append((m.start(), m.end()))

    # Blockquotes
    for m in __import__("re").finditer(
        r"^[ \t]*>.*$", body, flags=__import__("re").M
    ):
        exclusions.append((m.start(), m.end()))

    # Build mask
    mask = bytearray(b"\x01") * len(body)
    for start, end in exclusions:
        start = max(0, min(start, len(body)))
        end = max(start, min(end, len(body)))
        if start < end:
            mask[start:end] = b"\x00" * (end - start)

    # Scan
    for m in RFC_2119_RX.finditer(body):
        pos = m.start()
        if pos < len(mask) and mask[pos] == 1:
            line_num = line_from_pos(body, pos)
            rpt.add(
                "ADR-TEMPLATE-704",
                path,
                f"RFC-2119 term '{m.group()}' outside code fences in template",
                line_num,
            )
            break  # first only (unchanged)
