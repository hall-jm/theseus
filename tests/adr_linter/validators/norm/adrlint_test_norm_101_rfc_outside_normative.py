# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/norm/adrlint_test_norm_101_rfc_outside_normative.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-NORM-101 (E): RFC-2119 keyword outside normative sections
Linting Tests: ADRLINT-001/003/007/018
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report

from ...conftest import (
    _write_text,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
    STYLE_GUIDE,
)


def test_adrlint001_norm101_style_guide_bypass(_route_and_reset_workspace):
    """
    Pre-refactored pytest: ADRLINT-001
    Rule being tested: ADR-NORM-101 — style-guide class bypasses RFC scan
    """
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-9999-style-guide.md",
        STYLE_GUIDE,
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, "ADR-NORM-101")


def test_adrlint003_norm101_uppercase_outside_normative(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-003
    Rule being tested: ADR-NORM-101 — uppercase RFC terms outside normative
                       sections → 101
    """
    md = (
        _good_meta_front_matter(**{"class": "owner"})
        + "Outside normative sections we SHOULD trigger a violation.\n"
    )
    p = _write_text(
        _route_and_reset_workspace, "docs/adr-new/ADR-9996-rfc.md", md
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-NORM-101")


def test_adrlint007_norm101_ignores_code_inline_and_html_comments(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-007
    Rule being tested: ADR-NORM-101 — Missing llm_tail → error
    """
    body = [
        _good_meta_front_matter(**{"class": "owner"}),
        "<!-- key: context_and_drivers -->",
        "Outside normative prose with code fence below:\n",
        "```txt\nthis MUST not trigger\n```",
        "Inline `MUST` is ignored.",
        "<!-- comment with MUST also ignored -->",
        "<!-- key: decision_details -->",
        "Normative text MAY be used here properly.",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-5555-rfc-ignore.md",
        "\n".join(body),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, "ADR-NORM-101")


def test_adrlint018_norm101_terms_in_urls_ignored(_route_and_reset_workspace):
    """
    Pre-refactored pytest: ADRLINT-018
    Rule being tested: ADR-NORM-101 — RFC terms inside URLs are ignored
    """
    md = (
        _good_meta_front_matter(**{"class": "owner"})
        + """
+ <!-- key: context_and_drivers -->
+ See https://example.com/MUST-implement for details.
+ """
    )
    p = _write_text(
        _route_and_reset_workspace, "docs/adr-new/ADR-5564-url-rfc.md", md
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, "ADR-NORM-101")
