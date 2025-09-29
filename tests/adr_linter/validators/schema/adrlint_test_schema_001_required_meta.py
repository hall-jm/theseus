# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/schema/adrlint_test_schema_001_required_meta.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-SCHEMA-001 (E): Missing required metadata
                    (`id,title,status,class,date,review_by`) or bad `id`.
Linting Tests: ADRLINT-021
"""

from __future__ import annotations
from adr_linter.constants import REQUIRED_META
from adr_linter.report import Report
from adr_linter.validators.registry import run_all
from adr_linter.validators.schema.schema_001_required_meta import (
    _ERROR_CODE as _ADR_ERROR_CODE,
)


from ...conftest import (
    _write_text,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
)


# TODO: Add test coverage for invalid ID formats (bad `id` part of SCHEMA-001)


def test_adrlint_schema001_missing_required_metadata_fields(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-021
    Rule being tested: ADR-SCHEMA-001 — missing required metadata
                       fields → error
    """
    required_fields = REQUIRED_META
    for field in required_fields:
        incomplete_meta = {
            "id": "ADR-1234",
            "title": "Test",
            "status": "Proposed",
            "class": "owner",
            "date": "2025-09-03",
            "review_by": "2026-03-03",
        }
        incomplete_meta[field] = None  # YAML empty
        md = _good_meta_front_matter(**incomplete_meta) + "Body"
        p = _write_text(
            _route_and_reset_workspace,
            f"docs/adr-new/ADR-566{ord(field[0])}-missing-{field}.md",
            md,
        )
        ctx = _ctx_from_path(p)
        rpt = Report()
        run_all(ctx, rpt)
        assert _has_code(
            rpt, _ADR_ERROR_CODE
        ), f"Failed to catch missing {field}"


def test_adrlint_schema001_invalid_id_format(_route_and_reset_workspace):
    """
    Test ADR-SCHEMA-001 catches invalid ID formats (bad `id` requirement)
    """

    # TOREVIEW: Only testing obvious bad IDs - comprehensive testing
    #           deferred until real-world needs
    bad_ids = ["ADR-123", "BAD-1234", "ADR-ABCD"]

    for bad_id in bad_ids:
        meta = {
            "id": bad_id,  # Invalid ID
            "title": "Test",
            "status": "Proposed",
            "class": "owner",
            "date": "2025-09-03",
            "review_by": "2026-03-03",
        }
        md = _good_meta_front_matter(**meta) + "Body"
        p = _write_text(
            _route_and_reset_workspace,
            f"test-{bad_id.replace('-', '')}.md",
            md,
        )
        ctx = _ctx_from_path(p)
        rpt = Report()
        run_all(ctx, rpt)
        assert _has_code(
            rpt, _ADR_ERROR_CODE
        ), f"Failed to catch bad ID: {bad_id}"
