# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/policy/adrlint_test_policy_002_vs_constants_parity.py

"""
ADR-0001 · §<XXX> Linter Rules Reference
ADR-XXXX-YYYY (E? W? I?): Code sets & ASCII key checks.
Linting Tests: ADRLINT-808/809/910
"""

from __future__ import annotations


from adr_linter.constants import CODES as K_CODES
from adr_linter.policy import CODES as P_CODES


def test_adrlint808_codes_keys_match_policy_vs_constants():
    assert set(P_CODES.keys()) == set(K_CODES.keys())


def test_adrlint809_codes_metadata_match_policy_vs_constants():
    for code, (sev, title) in K_CODES.items():
        assert P_CODES[code]["severity"] == sev
        assert P_CODES[code]["title"] == title


def test_adrlint910_policy_codes_match_constants_keys_and_severity():
    assert set(P_CODES.keys()) == set(K_CODES.keys())
    for code, (sev, _title) in K_CODES.items():
        assert P_CODES[code]["severity"] == sev
