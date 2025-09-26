# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/link/adrlint_test_link_304_normative_ptr_missing.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-LINK-204 (E)**: Pointer to normative section key missing in base.
"""

from __future__ import annotations
from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.models import ValidationData
from adr_linter.services.index import load_files, build_index_from_files
from adr_linter.parser.structure import parse_document_structure

from ...conftest import (
    _write_text,
    _good_meta_front_matter,
    _has_code,
)


_ERROR_CODE = "ADR-LINK-304"


def test_adrlint_link304_normative_pointer_validation(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-028
    Rule being tested: ADR-LINK-204 — ptr → missing normative section
                       triggers 204
    """

    # TOREVIEW: This pytest uses more than the usual imports compared to
    #           other pytests. Questions: Is that a gap in conftest.py
    #           or are these services.index explicitly needed only for
    #           ADR-LINK-* error codes?
    # Base ADR without 'decision_details'
    base_md = (
        _good_meta_front_matter(**{"id": "ADR-0001", "class": "owner"})
        + """
<!-- key: decision_one_liner -->
Base decision

<!-- key: context_and_drivers -->
Base context
"""
    )
    _write_text(
        _route_and_reset_workspace, "docs/adrs/ADR-0001-base.md", base_md
    )

    # Delta with ptr to a section the base doesn't have
    delta_body = """```yaml
ptr:
  decision_details: ADR-0001#decision_details
```"""
    delta_md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-0002",
                "class": "delta",
                "extends": "ADR-0001@2025-01-01",
            }
        )
        + "\n"
        + delta_body
    )
    p = _write_text(
        _route_and_reset_workspace, "docs/adrs/ADR-0002-delta.md", delta_md
    )

    all_files = load_files(_route_and_reset_workspace)
    idx = build_index_from_files(all_files)

    ctx = ValidationData(
        meta={
            "id": "ADR-0002",
            "class": "delta",
            "extends": "ADR-0001@2025-01-01",
        },
        body=delta_body,
        path=p,
        section_data=parse_document_structure(delta_body),
        all_idx=idx,
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ERROR_CODE)
