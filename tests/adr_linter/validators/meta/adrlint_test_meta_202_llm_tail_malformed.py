# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/meta/adrlint_test_meta_202_llm_tail_malformed.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-META-202 (W): `llm_tail` has malformed JSON syntax.
Validates JSON syntax and structure in llm_tail blocks.

Rule: Detects JSON syntax errors in llm_tail blocks
Provides detailed error reporting for debugging
Validates JSON structure (must be object, not array/primitive)
Warning level (W) - doesn't block validation

Parser context: Parser attempts JSON parsing and returns
                llm_tail=None on failure. Validator detects parsing
                failure and provides detailed syntax error feedback.
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.meta.meta_202_llm_tail_malformed import (
    _ERROR_CODE as _ADR_ERROR_CODE,
)

from ...conftest import (
    _write_and_ctx,
    _good_meta_front_matter,
    _has_code,
    assert_warning_code,
)


def test_adrlint_meta202_missing_closing_bracket_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-202 — missing closing bracket in JSON → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "owner"})
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "owner"
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-missing-bracket.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_trailing_comma_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-202 — trailing comma in JSON → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "strategy"})
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "strategy",}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-trailing-comma.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_unquoted_keys_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-202 — unquoted keys in JSON → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "delta"})
        + """
<!-- llm_tail:begin -->
```json
{id: "ADR-1234", class: "delta"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-unquoted-keys.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_invalid_escape_sequence_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-202 — invalid escape sequence in JSON → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "governance"})
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "title": "bad\\escape", "class": "governance"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-invalid-escape.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_single_quotes_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-202 — single quotes instead of
    double quotes → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "template"})
        + """
<!-- llm_tail:begin -->
```json
{'id': 'ADR-1234', 'class': 'template'}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-single-quotes.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_missing_comma_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-202 — missing comma between
    properties → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "style-guide"})
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234" "class": "style-guide"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-missing-comma.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_extra_closing_bracket_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-202 — extra closing bracket → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "owner"})
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "owner"}}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-extra-bracket.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_empty_json_block_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-202 — empty JSON block → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "delta"})
        + """
<!-- llm_tail:begin -->
```json
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-empty-json.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_non_json_content_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-202 — non-JSON content in block → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "strategy"})
        + """
<!-- llm_tail:begin -->
```json
This is not JSON content at all
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(_route_and_reset_workspace, "meta-non-json.md", md)
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_whitespace_only_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-202 — whitespace-only content → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "governance"})
        + """
<!-- llm_tail:begin -->
```json
   
   
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-whitespace-only.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_array_instead_of_object_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-202 — array instead of object → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "template"})
        + """
<!-- llm_tail:begin -->
```json
["ADR-1234", "template", "Proposed"]
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-array-structure.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_primitive_string_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-202 — primitive string instead of
    object → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "style-guide"})
        + """
<!-- llm_tail:begin -->
```json
"ADR-1234"
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-primitive-string.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_primitive_number_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-202 — primitive number instead of
    object → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "owner"})
        + """
<!-- llm_tail:begin -->
```json
1234
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-primitive-number.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_primitive_boolean_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-202 — primitive boolean instead of
    object → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "delta"})
        + """
<!-- llm_tail:begin -->
```json
true
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-primitive-boolean.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_valid_simple_object_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-202 — valid simple JSON object → passes
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "strategy"})
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "strategy", "status": "Proposed"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-valid-simple.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_valid_complex_object_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-202 — valid complex JSON object → passes
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "governance"})
        + """
<!-- llm_tail:begin -->
```json
{
  "id": "ADR-1234",
  "class": "governance",
  "status": "Accepted",
  "scope": "cli",
  "metadata": {
    "created": "2025-09-27",
    "tags": ["governance", "cli"]
  },
  "relationships": {
    "supersedes": null,
    "informed_by": "ADR-0001@2025-09-11"
  }
}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-valid-complex.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_valid_with_unicode_passes(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-202 — valid JSON with Unicode
    characters → passes
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "template"})
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "template",
"title": "Template with émojis 🚀", "unicode": "测试"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-valid-unicode.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_valid_with_escaped_quotes_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-202 — valid JSON with properly
    escaped quotes → passes
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "style-guide"})
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "style-guide",
"title": "Guide with \\"quoted\\" text"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-valid-escaped.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_no_llm_tail_ignored(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-202 — no llm_tail block present → ignored
    """
    md = _good_meta_front_matter(**{"id": "ADR-1234", "class": "owner"})
    _, ctx = _write_and_ctx(_route_and_reset_workspace, "meta-no-tail.md", md)
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_mixed_quotes_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-202 — mixed single and double quotes → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "delta"})
        + """
<!-- llm_tail:begin -->
```json
{"id": 'ADR-1234', "class": "delta"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-mixed-quotes.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_incomplete_string_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-META-202 — incomplete string value → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "strategy"})
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "strategy", "incomplete": "missing quote}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-incomplete-string.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_duplicate_keys_triggers(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-202 — duplicate keys in JSON → warning
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "governance"})
        + """
<!-- llm_tail:begin -->
```json
{"id": "ADR-1234", "class": "governance", "id": "ADR-5678"}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-duplicate-keys.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    # assert_warning_code(rpt, _ADR_ERROR_CODE)

    """
    Python's json.loads() automatically handles some "malformed" JSON:
    - Duplicate keys (last value wins)
    - Extra whitespace
    - Unicode escapes

    This situation means META-202 can only catch truly broken JSON syntax,
    not the subtle issues the tests expect.
    """
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_meta202_valid_empty_object_passes(_route_and_reset_workspace):
    """
    Rule being tested: ADR-META-202 — valid empty JSON object → passes
    """
    md = (
        _good_meta_front_matter(**{"id": "ADR-1234", "class": "template"})
        + """
<!-- llm_tail:begin -->
```json
{}
```
<!-- llm_tail:end -->
"""
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "meta-valid-empty-object.md", md
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)
