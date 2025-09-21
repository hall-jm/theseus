# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/validators/link/adrlint_test_link_202_pointer_section_missing.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-LINK-202 (W): Pointer to section key missing in base.
Linting Tests: Implementation for pointer validation in delta ADRs.

Covers:
  1) Warning when a delta's ptr references a non-existent section in base ADR.
  2) Control: OK when ptr references an existing section in base ADR.
  3) Normative sections excluded (handled by ADR-LINK-204).

Notes:
- Pointer syntax follows ADR-0001 §8: fenced YAML block with `ptr:`.
- Base ADR must have valid canonical sections to avoid SCHEMA-003 interference.
- Requires ctx.all_idx population for cross-document lookups.
"""

from __future__ import annotations

from adr_linter.constants import (
    CANONICAL_KEYS_DELTA,
    NORMATIVE_KEYS,
)
from adr_linter.report import Report
from adr_linter.validators.registry import run_all

from ...conftest import (
    _write_text,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
)


def _canonical_body(keys: list[str], sentinel: str = "ok") -> str:
    """Create canonical section body with proper key markers."""
    parts = []
    for k in keys:
        parts.append(f"<!-- key: {k} -->\n{sentinel}:{k}\n")
    return "\n".join(parts)


def _write_base_and_delta_with_ptr(
    ws,
    *,
    base_id: str,
    delta_id: str,
    base_keys: list[str],
    ptr_block: str,
):
    """
    Create a base Owner ADR with specified keys and a Delta ADR with ptr
    references. Returns the delta file path.
    """
    base_meta = _good_meta_front_matter(
        **{"id": base_id, "class": "owner", "extends": None}
    )
    base_text = base_meta + "\n" + _canonical_body(base_keys)

    _write_text(ws, f"docs/adr-new/{base_id}-base.md", base_text)

    delta_meta = _good_meta_front_matter(
        **{
            "id": delta_id,
            "class": "delta",
            "extends": f"{base_id}@2025-09-03",
        }
    )

    delta_text = (
        delta_meta
        + "\n"
        + _canonical_body(CANONICAL_KEYS_DELTA)
        + "\n"
        + ptr_block
    )

    delta_path = _write_text(
        ws, f"docs/adr-new/{delta_id}-delta.md", delta_text
    )
    return delta_path


def test_adrlint_link_202_ptr_to_missing_section_emits_warning(
    _route_and_reset_workspace,
):
    """
    Base ADR lacks 'glossary' section; delta uses ptr to 'glossary'
    → MUST emit ADR-LINK-202.
    """
    # Base missing 'glossary' section
    base_keys = [k for k in CANONICAL_KEYS_DELTA if k != "glossary"]

    ptr_block = """```yaml
ptr:
  glossary: ADR-9501#glossary
```"""

    delta_path = _write_base_and_delta_with_ptr(
        _route_and_reset_workspace,
        base_id="ADR-9501",
        delta_id="ADR-9502",
        base_keys=base_keys,
        ptr_block=ptr_block,
    )

    ctx = _ctx_from_path(delta_path)

    # Populate all_idx with base document
    base_path = _route_and_reset_workspace / "docs/adr-new/ADR-9501-base.md"
    base_ctx = _ctx_from_path(base_path)
    ctx.all_idx["ADR-9501"] = {
        "meta": base_ctx.meta,
        "body": base_ctx.body,
        "path": str(base_path),
    }

    rpt = Report()
    run_all(ctx, rpt)

    assert _has_code(rpt, "ADR-LINK-202")


def test_adrlint_link_202_ptr_to_existing_section_is_ok(
    _route_and_reset_workspace,
):
    """
    Base ADR includes 'glossary' section; delta uses ptr to 'glossary'
    → should NOT emit ADR-LINK-202.
    """
    # Base includes all sections
    base_keys = list(CANONICAL_KEYS_DELTA)

    ptr_block = """```yaml
ptr:
  glossary: ADR-9503#glossary
```"""

    delta_path = _write_base_and_delta_with_ptr(
        _route_and_reset_workspace,
        base_id="ADR-9503",
        delta_id="ADR-9504",
        base_keys=base_keys,
        ptr_block=ptr_block,
    )

    ctx = _ctx_from_path(delta_path)

    # Populate all_idx with base document
    base_path = _route_and_reset_workspace / "docs/adr-new/ADR-9503-base.md"
    base_ctx = _ctx_from_path(base_path)
    ctx.all_idx["ADR-9503"] = {
        "meta": base_ctx.meta,
        "body": base_ctx.body,
        "path": str(base_path),
    }

    rpt = Report()
    run_all(ctx, rpt)

    assert not _has_code(rpt, "ADR-LINK-202")


def test_adrlint_link_202_ptr_to_normative_section_ignored(
    _route_and_reset_workspace,
):
    """
    Delta uses ptr to missing normative section (decision_details)
    → should NOT emit ADR-LINK-202 (normative keys handled by ADR-LINK-204).
    """
    # Base missing normative section
    base_keys = [k for k in CANONICAL_KEYS_DELTA if k not in NORMATIVE_KEYS]

    ptr_block = """```yaml
ptr:
  decision_details: ADR-9505#decision_details
```"""

    delta_path = _write_base_and_delta_with_ptr(
        _route_and_reset_workspace,
        base_id="ADR-9505",
        delta_id="ADR-9506",
        base_keys=base_keys,
        ptr_block=ptr_block,
    )

    ctx = _ctx_from_path(delta_path)

    # Populate all_idx with base document
    base_path = _route_and_reset_workspace / "docs/adr-new/ADR-9505-base.md"
    base_ctx = _ctx_from_path(base_path)
    ctx.all_idx["ADR-9505"] = {
        "meta": base_ctx.meta,
        "body": base_ctx.body,
        "path": str(base_path),
    }

    rpt = Report()
    run_all(ctx, rpt)

    # Should not emit LINK-202 for normative sections
    assert not _has_code(rpt, "ADR-LINK-202")
