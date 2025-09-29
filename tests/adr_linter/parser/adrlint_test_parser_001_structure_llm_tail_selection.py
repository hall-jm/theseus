# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/parser/adrlint_test_parser_001_structure_llm_tail_selection.py

"""
ADR-0001 · §<XXX> Linter Rules Reference
ADR-XXXX-YYYY (E? W? I?): llm_tail: prefer real JSON block over json-example.
Linting Tests: ADRLINT-010
"""

from __future__ import annotations


from adr_linter.parser.front_matter import parse_front_matter
from adr_linter.parser.structure import parse_document_structure

from ..conftest import (
    _write_text,
)


def test_adrlint010_llm_tail_ignores_json_example_and_uses_real_tail(
    _route_and_reset_workspace,
):
    md = [
        "---",
        "id: ADR-1234",
        "title: Short Title",
        "status: Proposed",
        "class: owner",
        "date: 2025-09-03",
        "review_by: 2026-03-03",
        "---",
        "<!-- llm_tail:begin -->",
        "```json-example",
        '{"id":"X","class":"delta","status":"Accepted"}',
        "```",
        "<!-- llm_tail:end -->",
        "",
        "<!-- llm_tail:begin -->",
        "```json",
        '{"id":"ADR-1234","class":"owner","status":"Proposed","extends":null}',
        "```",
        "<!-- llm_tail:end -->",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5558-llm-tail.md",
        "\n".join(md),
    )
    raw = p.read_text(encoding="utf-8")
    _, end = parse_front_matter(raw)
    sec = parse_document_structure(raw[end:])
    assert sec.llm_tail is not None
    assert sec.llm_tail.get("id") == "ADR-1234"
    assert sec.llm_tail.get("class") == "owner"
