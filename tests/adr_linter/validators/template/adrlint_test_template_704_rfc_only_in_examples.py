# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/validators/template/adrlint_test_templt_704_rfc_only_in_examples.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-TEMPLATE-704 (W): RFC-2119 keyword outside code fences/inline code
                    in template.
Linting Tests: ADRLINT-033/036/037/038/039
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report

from ...conftest import (
    _write_text,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
)


def test_adrlint033_templt704_only_code_and_inline_allowed(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-033
    Rule being tested: ADR-TEMPLATE-704 — RFC terms in code/inline/comments
                       only → no 704
    """
    md = (
        _good_meta_front_matter(
            **{"class": "template", "template_of": "owner"}
        )
        + """
 <!-- key: decision_one_liner -->
 <short-title>
 
 <!-- key: context_and_drivers -->
 This template shows how to use RFC terms in code:
 
 ```
 The implementation MUST validate input.
 ```
 
 Inline: `SHALL return 200`.
 
 <!-- comment with MUST also ignored -->
"""
    )
    p = _write_text(
        _route_and_reset_workspace, "docs/adr-new/ADR-5576-template-rfc.md", md
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, "ADR-TEMPLATE-704")


def test_adrlint036_templt704_rfc_in_prose_triggers(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-036
    Rule being tested: ADR-TEMPLT-704 — RFC terms in prose → 704
    """
    md = (
        _good_meta_front_matter(
            **{"class": "template", "template_of": "owner"}
        )
        + """
 <!-- key: decision_one_liner -->
 <short-title>
 
 <!-- key: context_and_drivers -->
 The system MUST handle this properly.
 
 ```
 But inside code MUST is fine.
 ```
"""
    )
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5581-template-rfc-prose.md",
        md,
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-TEMPLATE-704")


def test_adrlint037_templt704_only_code_blocks_and_inline_ok(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-037
    Rule being tested: ADR-TEMPLATE-704 — only code/inline → no 704
    """
    md = (
        _good_meta_front_matter(
            **{"class": "template", "template_of": "owner"}
        )
        + """
 <!-- key: decision_one_liner -->
 <short-title>
 
 <!-- key: context_and_drivers -->
 This demonstrates proper RFC usage in templates.
 
 ```
 The system MUST validate all inputs.
 ```
 
 Inline code: `SHOULD return JSON`.
"""
    )
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5582-template-clean.md",
        md,
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, "ADR-TEMPLATE-704")


def test_adrlint038_templt704_html_comments_ignored(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-038
    Rule being tested: ADR-TEMPLATE-704 — RFC terms in HTML comments are
    ignored
    """
    md = (
        _good_meta_front_matter(
            **{"class": "template", "template_of": "owner"}
        )
        + """
 <!-- key: decision_one_liner -->
 <short-title>
 
 <!-- This comment contains MUST but should be ignored -->
 
 <!-- key: context_and_drivers -->
 Template content without RFC terms in prose.
 
 ```
 Code block with MUST is fine.
 ```
 """
    )
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5583-template-comment-rfc.md",
        md,
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, "ADR-TEMPLATE-704")


def test_adrlint039_templt704_nested_code_blocks_ok(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-039
    Rule being tested: ADR-TEMPLATE-704 — nested code structures handled
                       correctly
    """
    md = (
        _good_meta_front_matter(
            **{"class": "template", "template_of": "owner"}
        )
        + """
 <!-- key: decision_one_liner -->
 <short-title>
 
 <!-- key: context_and_drivers -->
 Example with nested code:
 
 ```markdown
 Here's how to write ADR content:
 
 The system `MUST validate` inputs properly.
 
 ```yaml
 requirements:
   - system SHALL handle errors
 ```
 ```
 """
    )
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5584-template-nested.md",
        md,
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, "ADR-TEMPLATE-704")
