# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/validators/link/adrlint_test_link_300_bidirectional_links.py

"""
ADR-0001 · §10.1 Bi-directional links
           §14 Linter Rules Reference
ADR-LINK-300 (E): Handle all bi-directional keys missing the reciprocal (
                      e.g.,
                      `supersedes` <-> `superseded_by`,
                      `informs` <-> `informed_by`
                  )

Covers:
  1) Missing reciprocal (should FAIL with ADR-LINK-300)
  2) Proper reciprocal present (should PASS)
  3) Multiple supersedes where one base lacks reciprocal (should FAIL)
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report

from ...conftest import (  # type: ignore
    _write_text,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
)

_ERROR_CODE = "ADR-LINK-300"


def _owner_doc(id_: str, *, supersedes=None, superseded_by=None) -> str:
    """
    Compose a minimal, valid Owner ADR with optional supersedes/superseded_by.
    """
    overrides = {
        "id": id_,
        "class": "owner",
    }
    if supersedes is not None:
        overrides["supersedes"] = supersedes
    if superseded_by is not None:
        overrides["superseded_by"] = superseded_by

    fm = _good_meta_front_matter(**overrides)
    body = """
<!-- key: decision_one_liner -->
Short one-liner.

<!-- key: context_and_drivers -->
Context.
"""
    return fm + body


def _write_pair_for_missing_recip(
    root, *, base_id: str, new_id: str, pin: str
) -> str:
    """
    Write two ADRs:
      • base_id: owner ADR, no superseded_by (missing reciprocal)
      • new_id: owner ADR, supersedes base_id@pin
    Return path to the *new* ADR (the one that declares supersedes).
    """
    base_path = f"docs/adrs/{base_id}-base.md"
    new_path = f"docs/adrs/{new_id}-new.md"

    base_txt = _owner_doc(base_id, superseded_by=None)  # explicit null is fine
    new_txt = _owner_doc(new_id, supersedes=f"{base_id}@{pin}")

    _write_text(root, base_path, base_txt)
    p = _write_text(root, new_path, new_txt)
    return p


def _write_triplet_one_missing(
    root, *, a_id: str, b_id: str, c_id: str, pin: str
) -> str:
    """
    B supersedes A and C; A has reciprocal; C is missing reciprocal.
    Should still emit ADR-LINK-200.
    Returns path to B.
    """
    a_path = f"docs/adrs/{a_id}-old.md"
    b_path = f"docs/adrs/{b_id}-new.md"
    c_path = f"docs/adrs/{c_id}-old.md"

    # A has proper reciprocal pointing to B
    a_txt = _owner_doc(a_id, superseded_by=f"{b_id}@{pin}")

    # C is missing reciprocal (None/null)
    c_txt = _owner_doc(c_id, superseded_by=None)

    # B supersedes both A and C
    b_txt = _owner_doc(b_id, supersedes=f"{a_id}@{pin}, {c_id}@{pin}")

    _write_text(root, a_path, a_txt)
    _write_text(root, c_path, c_txt)
    p = _write_text(root, b_path, b_txt)
    return p


def _write_pair_for_ok_recip(
    root, *, base_id: str, new_id: str, pin: str
) -> tuple[str, str]:
    """
    Write two ADRs with proper reciprocity:
      • base_id: superseded_by new_id@pin
      • new_id:  supersedes base_id@pin
    Returns (path_to_base, path_to_new)
    """
    base_path = f"docs/adrs/{base_id}-base.md"
    new_path = f"docs/adrs/{new_id}-new.md"

    base_txt = _owner_doc(base_id, superseded_by=f"{new_id}@{pin}")
    new_txt = _owner_doc(new_id, supersedes=f"{base_id}@{pin}")

    p_base = _write_text(root, base_path, base_txt)
    p_new = _write_text(root, new_path, new_txt)
    return p_base, p_new


def test_adrlint_link300_missing_reciprocal_superseded_by_emits_error(
    _route_and_reset_workspace,
):
    """
    New ADR B: supersedes A@<pin>; A lacks superseded_by → emit ADR-LINK-200.
    """
    p = _write_pair_for_missing_recip(
        _route_and_reset_workspace,
        base_id="ADR-8400",
        new_id="ADR-8401",
        pin="2025-09-01",
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ERROR_CODE)


def test_adrlint_link300_reciprocal_present_passes(_route_and_reset_workspace):
    p_base, p_new = _write_pair_for_ok_recip(
        _route_and_reset_workspace,
        base_id="ADR-8402",
        new_id="ADR-8403",
        pin="2025-09-01",
    )

    # Only test the document that declares supersedes
    ctx = _ctx_from_path(p_new)
    base_ctx = _ctx_from_path(p_base)
    ctx.all_idx["ADR-8402"] = {
        "meta": base_ctx.meta,
        "body": base_ctx.body,
        "path": str(p_base),
    }

    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ERROR_CODE)


def test_adrlint_link300_multiple_supersedes_one_missing_reciprocal_error(
    _route_and_reset_workspace,
):
    """
    B supersedes A and C.
    A has reciprocal;
    C missing reciprocal ⇒ ADR-LINK-200.
    """
    p = _write_triplet_one_missing(
        _route_and_reset_workspace,
        a_id="ADR-8404",
        b_id="ADR-8405",
        c_id="ADR-8406",
        pin="2025-09-01",
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ERROR_CODE)
