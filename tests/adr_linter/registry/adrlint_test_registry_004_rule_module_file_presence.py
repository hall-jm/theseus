# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/registry/adrlint_test_registry_004_rule_module_file_presence.py

"""
ADR-0001 · §<XXX> Linter Rules Reference
ADR-XXXX-YYYY (E? W? I?): Each modularized rule code has a corresponding
                          validator module file.
Linting Tests: ADRLINT-901
"""

from __future__ import annotations


import importlib
import re
from pathlib import Path

from adr_linter.constants import CODES


def _validators_root() -> Path:
    pkg = importlib.import_module("adr_linter.validators")
    return Path(pkg.__file__).resolve().parent


def test_adrlint901_registry_each_rule_has_a_module_file_for_supported_bands():
    # FIXME: This ADR error code bands needs to be centralized along with the
    #        `rx = re.compile()` logic
    band_dir = {
        "DELTA": "delta",
        "LINK": "link",
        "NORM": "norm",
        "META": "meta",
        "SCHEMA": "schema",
        "TEMPLT": "template",
    }
    supported = set(band_dir.keys())
    root = _validators_root()
    rx = re.compile(r"^ADR-(?P<band>[A-Z]+)-(?P<num>\d{3})$")

    missing = []
    for code in CODES.keys():
        m = rx.match(code)
        if not m:
            continue
        band = m.group("band")
        num = m.group("num")
        if band not in supported:
            continue
        sub = root / band_dir[band]
        prefix = f"{band_dir[band]}_{num}_"
        pattern = f"{prefix}*.py"
        exists = any(p.name.startswith(prefix) for p in sub.glob(pattern))
        if not exists:
            missing.append((code, str(sub), pattern))

    assert not missing, "Missing rule module files:\n" + "\n".join(
        f"- {c} → {d}/{pat}" for c, d, pat in missing
    )
