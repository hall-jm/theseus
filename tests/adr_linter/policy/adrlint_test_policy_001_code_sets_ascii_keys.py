# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/policy/adrlint_test_policy_001_code_sets_ascii_keys.py

"""
ADR-0001 · §<XXX> Linter Rules Reference
ADR-XXXX-YYYY (E? W? I?): Code sets & ASCII key checks.
Linting Tests: ADRLINT-801/802/803/804/805/806/807
"""

from __future__ import annotations


from adr_linter.constants import (
    CODES as K_CODES,
    CODES_BLOCKING as K_BLOCKING,
    CODES_WARNING as K_WARNING,
)


def test_adrlint801_policy_validate_blocking_codes():
    """All blocking codes exist and are errors."""
    for code in K_BLOCKING:
        assert code in K_CODES, f"Blocking code {code} not defined"
        assert K_CODES[code][0] == "E", f"Blocking code {code} is not an error"


def test_adrlint802_policy_all_error_codes_are_blocking():
    """All codes with severity 'E' appear in CODES_BLOCKING."""
    error_codes = {c for c, (s, _) in K_CODES.items() if s == "E"}
    missing = error_codes - K_BLOCKING
    assert (
        not missing
    ), f"Error codes missing from CODES_BLOCKING: {sorted(missing)}"


def test_adrlint803_policy_validate_warning_codes():
    """All warning codes exist and are warnings."""
    for code in K_WARNING:
        assert code in K_CODES, f"Warning code {code} not defined"
        assert K_CODES[code][0] == "W", f"Warning code {code} is not a warning"


def test_adrlint804_policy_all_warning_codes_are_warning():
    """All codes with severity 'W' appear in CODES_WARNING."""
    warn_codes = {c for c, (s, _) in K_CODES.items() if s == "W"}
    missing = warn_codes - K_WARNING
    assert (
        not missing
    ), f"Warning codes missing from CODES_WARNING: {sorted(missing)}"


def _assert_ascii_only(seq, label: str):
    for code in seq:
        assert all(
            ord(ch) < 128 for ch in code
        ), f"Non-ASCII character in {label} code: {code}"


def test_adrlint805_policy_codes_ascii_keys_only():
    _assert_ascii_only(K_CODES.keys(), "CODES")


def test_adrlint806_policy_blocking_ascii_keys_only():
    _assert_ascii_only(K_BLOCKING, "CODES_BLOCKING")


def test_adrlint807_policy_warning_ascii_keys_only():
    _assert_ascii_only(K_WARNING, "CODES_WARNING")
