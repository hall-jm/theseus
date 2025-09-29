# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/meta/adrlint_test_meta_201_tail_mismatch.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-META-201 (W): `llm_tail` disagrees with front-matter on required keys.
Validates consistency between front-matter metadata and llm_tail JSON block.

Rule: Compares front-matter metadata with llm_tail JSON block
Reports mismatches on core fields and governance relationship fields
Handles ownership field validation (owners vs owners_ptr)
Warning level (W) - doesn't block validation

Field validation scope:
- Core fields: id, class, status, extends, governed_by, scope, informs,
               informed_by
- Ownership fields: owners, owners_ptr (special logic - either can match)
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.meta.meta_201_tail_mismatch import (
    _ERROR_CODE as _ADR_ERROR_CODE,
)

from ...conftest import (
    _write_and_ctx,
    _good_meta_front_matter,
    _has_code,
    assert_warning_code,
)


def test_adrlint_meta201_id_mismatch_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-201 — llm_tail ID disagrees with
    front-matter → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "owner"})
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-5678", "class": "owner", "status": "Proposed"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-id-mismatch.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_class_mismatch_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-201 — llm_tail class disagrees with
    front-matter → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "owner"})
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "delta", "status": "Proposed"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-class-mismatch.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_status_mismatch_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-201 — llm_tail status disagrees with
    front-matter → warning
    """
    md = (
        _good_meta_front_matter(
            **{"id": "ADR-1234", "class": "strategy", "status": "Proposed"}
        )
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "strategy", "status": "Accepted"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-status-mismatch.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_extends_mismatch_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-201 — llm_tail extends disagrees with
    front-matter → warning
    """
    md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-1234",
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",
            }
        )
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "delta", "extends": "ADR-0002@2025-09-11",
"owners_ptr": "ADR-0001"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-extends-mismatch.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_governed_by_mismatch_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-201 — llm_tail governed_by disagrees with
    front-matter → warning
    """
    md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-1234",
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
            }
        )
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "owner", "governed_by": "ADR-0002@2025-09-11"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-governed-by-mismatch.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_scope_mismatch_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-201 — llm_tail scope disagrees with
    front-matter → warning
    """
    md = (
        _good_meta_front_matter(
            **{"id": "ADR-1234", "class": "governance", "scope": "cli"}
        )
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "governance", "scope": "engine"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-scope-mismatch.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_informs_mismatch_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-201 — llm_tail informs disagrees with
    front-matter → warning
    """
    md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-1234",
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                "informs": "ADR-0002@2025-09-11",
            }
        )
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "strategy", "owners_ptr": "ADR-0001",
"informs": "ADR-0003@2025-09-11"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-informs-mismatch.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_informed_by_mismatch_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-201 — llm_tail informed_by disagrees with
    front-matter → warning
    """
    md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-1234",
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "informed_by": "ADR-0002@2025-09-11",
            }
        )
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "owner", "governed_by": "ADR-0001@2025-09-11",
"informed_by": "ADR-0003@2025-09-11"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-informed-by-mismatch.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_owners_mismatch_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-201 — llm_tail owners disagrees with
    front-matter → warning
    """
    md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-1234",
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "owners": ["Project Maintainer"],
            }
        )
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "owner", "governed_by": "ADR-0001@2025-09-11",
"owners": ["Different Owner"]}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-owners-mismatch.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_owners_ptr_mismatch_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-201 — llm_tail owners_ptr disagrees with
    front-matter → warning
    """
    md = (
        _good_meta_front_matter(
            **{"id": "ADR-1234", "class": "strategy", "owners_ptr": "ADR-0001"}
        )
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "strategy", "owners_ptr": "ADR-0002"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-owners-ptr-mismatch.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_ownership_type_mismatch_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-201 — front-matter has owners, tail has
    owners_ptr → warning
    """
    md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-1234",
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "owners": ["Project Maintainer"],
            }
        )
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "owner", "governed_by": "ADR-0001@2025-09-11",
"owners_ptr": "ADR-0001"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-ownership-type-mismatch.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_ownership_missing_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-201 — front-matter has ownership, tail has
    none → warning
    """
    md = (
        _good_meta_front_matter(
            **{"id": "ADR-1234", "class": "strategy", "owners_ptr": "ADR-0001"}
        )
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "strategy"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-ownership-missing.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_null_values_equivalent_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-201 — null/empty values treated as
    equivalent → passes
    """
    md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-1234",
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "extends": None,
                "scope": "",
                "status": "",
            }
        )
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "owner", "status": null,
"governed_by": "ADR-0001@2025-09-11", "extends": null, "scope": null}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-null-values.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_missing_fields_equivalent_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-201 — missing fields vs null fields
    equivalent → passes
    """
    md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-1234",
                "class": "governance",
                "scope": "cli",
                "status": None,  # Explicitly override default
            }
        )
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "governance", "scope": "cli", "status": null,
"extends": null, "governed_by": null}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-missing-fields.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_no_llm_tail_ignored(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-201 — no llm_tail present → ignored
    by validator
    """
    md = _good_meta_front_matter(
        **{
            "id": "ADR-1234",
            "class": "owner",
            "governed_by": "ADR-0001@2025-09-11",
        }
    )
    _, ctx = _write_and_ctx(_route_and_reset_workspace, "meta-no-tail.md", md)
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_perfect_match_passes(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-201 — perfect match between front-matter
    and tail → passes
    """
    md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-1234",
                "class": "delta",
                "status": "Accepted",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",
                "governed_by": "ADR-0002@2025-09-11",
            }
        )
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "delta", "status": "Accepted", "extends":
"ADR-0001@2025-09-11", "owners_ptr": "ADR-0001",
"governed_by": "ADR-0002@2025-09-11"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-perfect-match.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_malformed_json_ignored(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-201 — malformed JSON in llm_tail → ignored
    Note: JSON parsing errors should be handled gracefully
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "owner"})
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "owner", "invalid": json}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-malformed-json.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    # Should not crash - malformed JSON should be handled gracefully
    # May or may not trigger META-201 depending on implementation


def test_adrlint_meta201_multiple_mismatches_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-201 — multiple field mismatches → warning
    Should report each mismatch (implementation detail)
    """
    md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-1234",
                "class": "owner",
                "status": "Proposed",
                "governed_by": "ADR-0001@2025-09-11",
            }
        )
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-5678", "class": "delta", "status": "Accepted",
"governed_by": "ADR-0002@2025-09-11"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-multiple-mismatches.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta201_empty_llm_tail_ignored(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-201 — empty llm_tail block → ignored
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "owner"})
        + """
<!-- llm_tail:begin -->
```json
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-empty-tail.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    # Empty JSON block should be handled gracefully


def test_adrlint_meta201_extra_tail_fields_ignored(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-201 — extra fields in tail not
    validated → passes
    Only validates specified field scope
    """
    md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-1234",
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                "status": "Accepted",
            }
        )
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "strategy", "owners_ptr": "ADR-0001",
"status": "Accepted", "extra_field": "ignored", "another_field": 123}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-extra-fields.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)
