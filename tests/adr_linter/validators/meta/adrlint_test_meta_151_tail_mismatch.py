# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/meta/adrlint_test_meta_151_tail_mismatch.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-META-151 (W): `llm_tail` disagrees with front-matter on required keys.
Linting Tests: ADRLINT-045
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report

from ...conftest import (
    _write_and_ctx,
    _good_meta_front_matter,
    _has_code,
)


def test_adrlint045_meta151_llm_tail_mismatch(_route_and_reset_workspace):
    """
    Pre-refactored pytest: ADRLINT-045
    Rule being tested: ADR-META-151 — llm_tail content disagrees with
                       meta → error
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "owner"})
        + """
<!-- llm_tail:begin -->
```json
{"id":"ADR-9999","class":"delta","status":"Accepted"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "ADR-9991-tail-mismatch.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, "ADR-META-151")
