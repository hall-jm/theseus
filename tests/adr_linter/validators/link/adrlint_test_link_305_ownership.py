# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/link/adrlint_test_link_305_ownership.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-LINK-305 (E)**: Missing references to governing ADRs. Escalates to
                    (E) when clear dependency exists.
"""

from __future__ import annotations

from adr_linter.report import Report
from adr_linter.validators.registry import run_all

# from adr_linter.validators.link.link_205_governance import (
#     validate_link_205_governance,
# )

from ...conftest import (  # type: ignore
    _write_and_ctx,
    _good_meta_front_matter,
    _has_code,
)

_ERROR_CODE = "ADR-LINK-305"


def test_adrlint_link305_strategy_missing_owners_ptr(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-LINK-305 — Strategy ADR missing owners_ptr
    """
    md = _good_meta_front_matter(**{"class": "strategy"}) + "Body"
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "strategy-no-governance.md", md
    )
    ctx.all_idx = {}
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ERROR_CODE)


def test_adrlint_link305_delta_missing_extends(_route_and_reset_workspace):
    """
    Rule being tested: ADR-LINK-305 — Delta ADR missing extends
    """
    md = _good_meta_front_matter(**{"class": "delta"}) + "Body"
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-no-extends.md", md
    )
    ctx.all_idx = {}
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ERROR_CODE)


def test_adrlint_link305_nonexistent_reference(_route_and_reset_workspace):
    """
    Rule being tested: ADR-LINK-305 — owners_ptr points to non-existent ADR
    """
    md = (
        _good_meta_front_matter(
            **{"class": "strategy", "owners_ptr": "ADR-9999"}
        )
        + "Body"
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "strategy-bad-ref.md", md
    )
    ctx.all_idx = {}
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ERROR_CODE)


def test_adrlint_link305_owner_exempt(_route_and_reset_workspace):
    """
    Rule being tested: ADR-LINK-305 — Owner ADRs do not require
                       governance refs
    """
    md = _good_meta_front_matter(**{"class": "owner"}) + "Owner ADR body"
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-no-governance.md", md
    )
    ctx.all_idx = {}
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ERROR_CODE)


def test_adrlint_link305_strategy_without_governance_sample(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-LINK-305 — Strategy class without owners_ptr
                       (sample body)
    """
    body = (
        _good_meta_front_matter(**{"class": "strategy"})
        + "# Strategy ADR Missing owners_ptr\nThis should trigger "
        + "ADR-LINK-205."
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "ADR-9995-strategy-without-governance.md",
        body,
    )
    ctx.all_idx = {}
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ERROR_CODE)


def test_adrlint_link305_delta_without_extends_sample(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-LINK-305 — Delta class without extends
                       (sample body)
    """
    body = (
        _good_meta_front_matter(**{"class": "delta"})
        + "# Delta ADR Missing extends\nThis should trigger ADR-LINK-205."
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "ADR-9994-delta-without-extends.md", body
    )
    ctx.all_idx = {}
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ERROR_CODE)
