# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/filters/adrlint_test_filters_001_compile_k_predicate.py

"""
ADR-0001 · §<XXX> Linter Rules Reference
ADR-XXXX-YYYY (E? W? I?): k-filter parser (and/or/not) selects correct files.
Linting Tests: ADRLINT-006
"""

from __future__ import annotations

from pathlib import Path

from adr_linter.filters import compile_k as _compile_k


def test_adrlint006_k_filter_predicate_and_or_not(_route_and_reset_workspace):
    paths = [
        _route_and_reset_workspace / "docs/adr-new/ADR-0001-owner.md",
        _route_and_reset_workspace / "docs/adr-new/ADR-0003-strategy.md",
        _route_and_reset_workspace / "docs/adr-new/notes.md",
    ]
    pred = _compile_k("(0001 or 0003) and not notes")
    kept = [p.name for p in paths if pred(Path(p))]
    assert set(kept) == {"ADR-0001-owner.md", "ADR-0003-strategy.md"}
