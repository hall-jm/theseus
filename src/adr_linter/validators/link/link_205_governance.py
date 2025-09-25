# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/link/link_205_governance.py

"""
ADR-LINK-205 — Missing references to governing ADRs.
               OWNER ADR, not GOVERNANCE ADR (bad wording).

Behavior is copied verbatim from the legacy implementation.

Ref: ADR-0001 §10.5 · ADR-LINK-205
"""

from __future__ import annotations

from typing import List


def validate_link_205_governance(ctx, rpt) -> None:
    """
    ADR-LINK-205: Missing references to governing ADRs

    Check if non-owner ADRs reference their governing documents appropriately.
    (Identical behavior to legacy implementation.)
    """

    # FIXME: Wrong word choice in light of new `governance` ADR class
    #        Needs to be rewritten to clarify this is for ownership of an
    #        ADR, not the cross-ADR governance chain (as of 2025-09-25)
    #        e.g., ADR-0001 owns ADR-0006 CLI Ownership, but for pieces
    #              that could touch the same item such as CLI error codes
    #              governance is for handling cli <-> engine <-> services
    #              error code handling or scope of ownership and how to
    #              navigate boundary ambiguities
    meta = ctx.meta
    path = ctx.path
    all_idx = ctx.all_idx

    adr_class = meta.get("class")
    owners_ptr = meta.get("owners_ptr")
    extends = meta.get("extends")

    # Skip owner and style-guide ADRs (they don't need governance references)
    if adr_class in ("owner", "style-guide"):
        return

    # Skip templates (they're scaffolds, not real decisions)
    if adr_class == "template":
        return

    # Check for governance references
    missing_governance: List[str] = []

    # For delta ADRs: extends should provide governance
    if adr_class == "delta":
        if not extends or extends in ("null", "", None):
            missing_governance.append("extends (required for delta)")

    # For strategy ADRs: should have owners_ptr
    elif adr_class == "strategy":
        if not owners_ptr:
            missing_governance.append("owners_ptr (required for strategy)")

    # Collect referenced governance ADR ids
    governance_refs: List[str] = []
    if extends:
        base_id = (
            extends.split("@")[0] if "@" in str(extends) else str(extends)
        )
        if base_id.startswith("ADR-"):
            governance_refs.append(base_id)
    if owners_ptr:
        governance_refs.append(str(owners_ptr))

    # Verify referenced ADRs exist
    missing_refs: List[str] = []
    for ref in governance_refs:
        if ref not in all_idx:
            missing_refs.append(ref)

    # Report issues
    if missing_governance:
        rpt.add(
            "ADR-LINK-205",
            path,
            f"Missing governance references: {', '.join(missing_governance)}",
        )

    if missing_refs:
        rpt.add(
            "ADR-LINK-205",
            path,
            f"References to non-existent ADRs: {', '.join(missing_refs)}",
        )
