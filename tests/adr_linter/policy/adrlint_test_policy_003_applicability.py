# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/policy/adrlint_test_policy_003_applicability.py

"""
ADR-0001 · §<XXX> Linter Rules Reference
ADR-XXXX-YYYY (E? W? I?): Code sets & ASCII key checks.
Linting Tests: ADRLINT-911/912/913/914
"""

from __future__ import annotations


from adr_linter.constants import (
    CODES_BLOCKING as K_BLOCKING,
    CODES_WARNING as K_WARNING,
    VALID_ADR_CLASSES,
)
from adr_linter.policy import (
    APPLICABILITY as P_APPLICABILITY,
    CODES as P_CODES,
    BLOCKING as P_BLOCKING,
    WARNING as P_WARNING,
    applies_to as policy_applies_to,
)


# TOREVIEW: Since policy.py is importing constants.py values,
#           is this pytest still needed?


def test_adrlint911_policy_blocking_warning_sets_match_constants():
    # assert P_CODES == set(K_CODES)
    assert P_BLOCKING == set(K_BLOCKING)
    assert P_WARNING == set(K_WARNING)


def test_adrlint912_policy_applicability_is_well_formed():
    for code in P_CODES.keys():
        assert code in P_APPLICABILITY
        classes = P_APPLICABILITY[code]
        assert classes, f"{code} must have at least one applicable class"
        assert classes.issubset(set(VALID_ADR_CLASSES))


def test_adrlint913_policy_applicability_template_only_for_templt():
    for code in P_CODES.keys():
        if code.startswith("ADR-TEMPLATE-7"):
            assert P_APPLICABILITY[code] == {"template"}


def test_adrlint914_policy_applies_to_helper_consistent_with_matrix_examples():
    assert not policy_applies_to("style-guide", "ADR-NORM-101")
    assert not policy_applies_to("style-guide", "ADR-SCHEMA-003")
    assert policy_applies_to("template", "ADR-TEMPLATE-700")
    assert not policy_applies_to("owner", "ADR-TEMPLATE-700")
