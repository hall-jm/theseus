# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/registry/adrlint_test_registry_001_manifest_ordering.py

"""
ADR-0001 · §<XXX> Linter Rules Reference
ADR-XXXX-YYYY (E? W? I?): Manifest ordering & phase separation checks.
Linting Tests: ADRLINT-951/952/953/954
"""

from __future__ import annotations


from adr_linter.validators.registry import (
    manifest_codes_per_file,
    ORDERED_RULES_PER_FILE as R_ORDERED_RULES_PER_FILE,
    ORDERED_RULES_POST_RUN_PER_FILE as R_ORDERED_RULES_POST_RUN_PER_FILE,
)


def _index_map():
    return {code: i for i, (code, _) in enumerate(R_ORDERED_RULES_PER_FILE)}


def test_adrlint951_schema_precedes_link_band():
    idx = _index_map()
    s_ix = [i for c, i in idx.items() if c.startswith("ADR-SCHEMA-")]
    l_ix = [i for c, i in idx.items() if c.startswith("ADR-LINK-")]
    if s_ix and l_ix:
        assert max(s_ix) < min(l_ix), "SCHEMA must precede LINK"


def test_adrlint952_norm_precedes_template_band():
    idx = _index_map()
    n_ix = [i for c, i in idx.items() if c.startswith("ADR-NORM-")]
    t_ix = [i for c, i in idx.items() if c.startswith("ADR-TEMPLATE-")]
    if n_ix and t_ix:
        assert max(n_ix) <= min(t_ix), "NORM should not come after TEMPLATE"


def test_adrlint953_post_run_order_is_stable():
    post_codes = [code for code, _ in R_ORDERED_RULES_POST_RUN_PER_FILE]
    assert post_codes == ["ADR-LINK-220", "ADR-LINK-221", "ADR-LINK-222"]


def test_adrlint954_ordering_sanity_smoke():
    per_codes = manifest_codes_per_file()

    def idx(code):
        assert code in per_codes, f"{code} not found in manifest"
        return per_codes.index(code)

    assert idx("ADR-SCHEMA-001") < idx("ADR-SCHEMA-003")
    assert idx("ADR-SCHEMA-002") < idx("ADR-LINK-200")
    assert idx("ADR-SCHEMA-005") < idx("ADR-LINK-200")
    assert idx("ADR-SCHEMA-003") < idx("ADR-LINK-200")
    assert idx("ADR-SCHEMA-021") < idx("ADR-LINK-200")
    assert idx("ADR-LINK-205") < idx("ADR-META-150")
    assert idx("ADR-LINK-205") < idx("ADR-NORM-101")
    assert idx("ADR-NORM-102") < idx("ADR-TEMPLATE-700")
    assert idx("ADR-META-151") < idx("ADR-TEMPLATE-705")
