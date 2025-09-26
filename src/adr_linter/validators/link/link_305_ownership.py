# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/link/link_305_ownership.py

"""
ADR-LINK-305 — Missing references to owning ADRs.
               OWNER ADR, not GOVERNANCE ADR (bad wording).

Behavior is copied verbatim from the legacy implementation.

Ref: ADR-0001 §10.5 · ADR-LINK-305
"""

from __future__ import annotations

from typing import List


_ERROR_CODE = "ADR-LINK-305"


def validate_link_305_ownership(ctx, rpt) -> None:
    """
    ADR-LINK-305: Missing references to governing ADRs

    Check if non-owner ADRs reference their governing documents appropriately.
    (Identical behavior to legacy implementation.)
    """

    # FIXME: Wrong word choice in light of new `governance` ADR class
    #        Needs to be rewritten to clarify this is for ownership of an
    #        ADR, not the cross-ADR governance chain (as of 2025-09-25)
    #        e.g., hypothetical:
    #              ADR-0001 owns ADR-0006 CLI Ownership, but for pieces
    #              that could touch the same item such as CLI error codes
    #              governance is for handling cli <-> engine <-> services
    #              error code handling or scope of ownership and how to
    #              navigate boundary ambiguities

    # FIXME: This validator partially validates LINK-305 (presence of a
    #        reference for strategies; existence of referenced IDs) but does
    #        not implement the core requirement that all non-Owners
    #        (notably Deltas) must have owners_ptr pointing to an Owner ADR.
    #        Sources: §3, §7.2, §7.3.

    meta = ctx.meta
    path = ctx.path
    all_idx = ctx.all_idx

    adr_class = meta.get("class")
    owners_ptr = meta.get("owners_ptr")
    extends = meta.get("extends")

    # Skip owner and style-guide ADRs (they don't need ownership references)
    if adr_class in ("owner", "style-guide", "governance"):
        return

    # Skip templates (they're scaffolds, not real decisions)
    if adr_class == "template":
        return

    # Check for governance references
    missing_ownership: List[str] = []

    # For delta ADRs: extends should provide ownership
    if adr_class == "delta":
        if not extends or extends in ("null", "", None):
            missing_ownership.append("extends (required for delta)")

    # For strategy ADRs: should have owners_ptr
    elif adr_class == "strategy":
        if not owners_ptr:
            missing_ownership.append("owners_ptr (required for strategy)")

    # Collect referenced ownership ADR ids
    ownership_refs: List[str] = []
    if extends:
        base_id = (
            extends.split("@")[0] if "@" in str(extends) else str(extends)
        )
        if base_id.startswith("ADR-"):
            ownership_refs.append(base_id)
    if owners_ptr:
        ownership_refs.append(str(owners_ptr))

    # Verify referenced ADRs exist
    missing_refs: List[str] = []
    for ref in ownership_refs:
        if ref not in all_idx:
            missing_refs.append(ref)

    # Report issues
    if missing_ownership:
        rpt.add(
            _ERROR_CODE,
            path,
            f"Missing ownership references: {', '.join(missing_ownership)}",
        )

    if missing_refs:
        rpt.add(
            _ERROR_CODE,
            path,
            f"References to non-existent ADRs: {', '.join(missing_refs)}",
        )
