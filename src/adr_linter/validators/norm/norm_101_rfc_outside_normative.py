# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/norm/norm_101_rfc_outside_normative.py

"""ADR-NORM-101 — RFC-2119 keyword outside normative sections.

Ref: ADR-0001 §11
Behavior mirrors legacy.validate_rfc_terms_optimized (non-template branch)
for 101: same masking, same single-violation emission and message shape.
"""

from __future__ import annotations

from ...constants import RFC_2119_RX, NORMATIVE_KEYS

from ...parser.structure import line_from_pos


def validate_norm_101_rfc_outside_normative(ctx, rpt) -> None:
    """
    Emit ADR-NORM-101 for the first RFC-2119 keyword outside
    normative sections (decision_details, rollout_backout).
    """
    # Style-guide and template are handled elsewhere.
    klass = ctx.meta.get("class")
    if klass in {"style-guide", "template"}:
        return

    body = ctx.body
    section_info = ctx.section_info
    path = ctx.path

    # Start with precomputed exclusions (fences, inline code, URLs, comments).
    normative_exclusions = list(section_info.exclusion_ranges)

    # Exclude normative sections entirely from scanning.
    for key, content in section_info.sections_by_key.items():
        if key in NORMATIVE_KEYS:
            start = body.find(content)
            if start != -1:
                normative_exclusions.append((start, start + len(content)))

    # Build a scan mask where 1 = scan, 0 = skip.
    mask = bytearray(b"\x01") * len(body)
    for start, end in normative_exclusions:
        start = max(0, min(start, len(body)))
        end = max(start, min(end, len(body)))
        if start < end:
            mask[start:end] = b"\x00" * (end - start)

    # Scan for first unmasked RFC-2119 match.
    for m in RFC_2119_RX.finditer(body):
        pos = m.start()
        if pos < len(mask) and mask[pos] == 0:
            continue

        # Try to capture nearest preceding heading text for context.
        containing_section = None
        for heading_text, _, h_pos, _ in reversed(section_info.headings):
            if h_pos < pos:
                containing_section = heading_text
                break

        line_num = line_from_pos(body, pos)
        context = f"term: {m.group()}"
        if containing_section:
            context += f", section: {containing_section}"

        rpt.add(
            "ADR-NORM-101",
            path,
            f"RFC-2119 keyword outside normative sections ({context})",
            line_num,
        )
        break  # match legacy: report only the first
