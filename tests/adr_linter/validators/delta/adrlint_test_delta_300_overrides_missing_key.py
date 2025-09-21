# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/validators/delta/adrlint_test_delta_300_overrides_missing_key.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-DELTA-300 (E): Override targets non-existent key in base.
Linting Tests: (New tests since DELTA-300 did not have pytests)

Covers:
  1) Error when a delta overrides a key that does not exist in the base ADR.
  2) Control: OK when overriding a key that *does* exist in the base ADR.

Notes:
- Override syntax follows ADR-0001 §8/§11: fenced YAML block with `overrides:`.
- Base ADR is kept fully valid (all canonical section keys in order) to avoid
  SCHEMA-003 masking DELTA-300.
"""

from __future__ import annotations

from adr_linter.constants import (
    CANONICAL_KEYS_DELTA,
)
from adr_linter.report import Report
from adr_linter.validators.registry import run_all

from ...conftest import (  # type: ignore
    _write_text,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
)


def _canonical_body(keys: list[str], sentinel: str = "ok") -> str:
    parts = []
    for k in keys:  # Use the provided keys parameter
        parts.append(f"<!-- key: {k} -->\n{sentinel}:{k}\n")
    return "\n".join(parts)


def _write_base_and_delta(
    ws,
    *,
    base_id: str,
    delta_id: str,
    base_keys: list[str],
    delta_body: str,
):
    """
    Create a base Owner ADR with the provided canonical keys and a Delta ADR
    that extends it (pinned). Returns the delta file path.
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
            "extends": f"{base_id}@2025-09-03",  # valid pin format
        }
    )
    # Give the delta a full, valid skeleton (so only the override condition
    # is tested)
    delta_text = (
        delta_meta
        + "\n"
        + _canonical_body(CANONICAL_KEYS_DELTA)
        + "\n"
        + delta_body
    )
    delta_path = _write_text(
        ws, f"docs/adr-new/{delta_id}-delta.md", delta_text
    )
    return delta_path


def test_adrlint300_override_nonexistent_key_emits_error(
    _route_and_reset_workspace,
):
    """
    Base omits 'glossary'; delta overrides 'glossary'
    → MUST emit ADR-DELTA-300.
    """
    base_keys = [k for k in CANONICAL_KEYS_DELTA if k != "glossary"]

    override_block = """```yaml
overrides:
  glossary: "MUST define 'tenant' precisely to avoid ambiguity"
```"""

    delta_path = _write_base_and_delta(
        _route_and_reset_workspace,
        base_id="ADR-9398",
        delta_id="ADR-9399",
        base_keys=base_keys,
        delta_body=override_block,
    )

    ctx = _ctx_from_path(delta_path)

    # Add base document to all_idx manually
    base_path = _route_and_reset_workspace / "docs/adr-new/ADR-9398-base.md"
    base_ctx = _ctx_from_path(base_path)
    ctx.all_idx["ADR-9398"] = {
        "meta": base_ctx.meta,
        "body": base_ctx.body,
        "path": str(base_path),
    }

    rpt = Report()
    run_all(ctx, rpt)

    assert _has_code(rpt, "ADR-DELTA-300")


def test_adrlint300_override_existing_key_is_ok(_route_and_reset_workspace):
    """
    Base includes 'glossary'; delta overrides 'glossary'
    → should NOT emit ADR-DELTA-300.
    """
    base_keys = list(CANONICAL_KEYS_DELTA)  # include everything

    override_block = """```yaml
overrides:
  glossary: "MUST define 'tenant' precisely to avoid ambiguity"
```"""
    delta_path = _write_base_and_delta(
        _route_and_reset_workspace,
        base_id="ADR-9400",
        delta_id="ADR-9401",
        base_keys=base_keys,
        delta_body=override_block,
    )

    ctx = _ctx_from_path(delta_path)
    rpt = Report()
    run_all(ctx, rpt)

    assert not _has_code(rpt, "ADR-DELTA-300")
