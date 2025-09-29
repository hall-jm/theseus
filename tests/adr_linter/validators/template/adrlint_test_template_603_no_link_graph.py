# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/template/adrlint_test_template_603_no_link_graph.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-TEMPLATE-603 (E): template participates in link graph (forbidden
relationship fields non-null). Validates that template class ADRs do not
participate in the link graph.

Rule: IF class == "template" AND any forbidden relationship field is
      non-null → ERROR
Forbidden fields: extends, supersedes, governed_by, informs, informed_by
Other classes ignore this constraint (different validators handle their
relationship rules)
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.template.template_603_no_link_graph import (
    _ERROR_CODE as _ADR_ERROR_CODE,
)

from ...conftest import (
    _write_text,
    _write_and_ctx,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
    assert_error_code,
)


def test_adrlint_template603_extends_field_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — template ADR with extends
    field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",
                "owners_ptr": "ADR-0001",
                # Forbidden for template
                "extends": "ADR-0002@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<owner-decision>",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-6003-template-extends.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_supersedes_field_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — template ADR with supersedes
    field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "strategy",
                "owners_ptr": "ADR-0001",
                # Forbidden for template
                "supersedes": "ADR-0003@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<strategy-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-supersedes.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_governed_by_field_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — template ADR with governed_by
    field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "delta",
                "owners_ptr": "ADR-0001",
                # Forbidden for template
                "governed_by": "ADR-0004@2025-09-11",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<delta-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-governed-by.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_informs_field_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — template ADR with informs
    field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "governance",
                "owners_ptr": "ADR-0001",
                "informs": "ADR-0005@2025-09-11",  # Forbidden for template
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<governance-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-informs.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_informed_by_field_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — template ADR with informed_by
    field → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "style-guide",
                "owners_ptr": "ADR-0001",
                "informed_by": "ADR-0006@2025-09-11",  # Forbidden for template
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<style-guide-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-informed-by.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_multiple_forbidden_fields_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — template ADR with multiple forbidden
    fields → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",
                "owners_ptr": "ADR-0001",
                "extends": "ADR-0002@2025-09-11",  # Forbidden
                "supersedes": "ADR-0003@2025-09-11",  # Also forbidden
                "governed_by": "ADR-0004@2025-09-11",  # Also forbidden
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<owner-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-multiple-forbidden.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_extends_no_pin_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — template ADR with extends
    (no pin) → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "strategy",
                "owners_ptr": "ADR-0001",
                "extends": "ADR-0002",  # Forbidden even without pin
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<strategy-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-extends-no-pin.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_supersedes_hash_pin_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — template ADR with supersedes
    (hash pin) → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "delta",
                "owners_ptr": "ADR-0001",
                # Forbidden with hash pin
                "supersedes": "ADR-0003@deadbeef123",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<delta-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-supersedes-hash.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_informs_list_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — template ADR with informs as
    list → error
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "governance",
                "owners_ptr": "ADR-0001",
                # Forbidden list
                "informs": ["ADR-0004@2025-09-11", "ADR-0005@2025-09-11"],
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<governance-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-informs-list.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_error_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_no_forbidden_fields_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — template ADR with no forbidden
    fields → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",
                "owners_ptr": "ADR-0001",
                # No forbidden relationship fields present
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<owner-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-no-forbidden.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_null_fields_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — template ADR with null forbidden
    fields → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "strategy",
                "owners_ptr": "ADR-0001",
                "extends": None,  # Null values should pass
                "supersedes": None,
                "governed_by": None,
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<strategy-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-null-fields.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_empty_string_fields_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — template ADR with empty string
    forbidden fields → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "delta",
                "owners_ptr": "ADR-0001",
                "extends": "",  # Empty strings should pass
                "supersedes": "",
                "informs": "",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<delta-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-empty-strings.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_string_null_fields_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — template ADR with "null" string
    forbidden fields → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "governance",
                "owners_ptr": "ADR-0001",
                # String "null" should pass per implementation
                "extends": "null",
                "governed_by": "null",
                "informed_by": "null",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<governance-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-string-null.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_empty_array_fields_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — template ADR with empty array
    forbidden fields → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "style-guide",
                "owners_ptr": "ADR-0001",
                "informs": [],  # Empty arrays should pass per implementation
                "informed_by": [],
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<style-guide-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-empty-arrays.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_owner_class_ignores_relationship_fields(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — owner class with relationship
    fields → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "supersedes": "ADR-0002@2025-09-11",  # Valid for owner
                "informed_by": "ADR-0003@2025-09-11",  # Valid for owner
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision with relationship fields.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "owner-with-relationships.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_delta_class_ignores_relationship_fields(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — delta class with relationship
    fields → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",  # Valid for delta
                "owners_ptr": "ADR-0001",
                "governed_by": "ADR-0002@2025-09-11",  # Valid for delta
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Delta decision with relationship fields.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "delta-with-relationships.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_governance_class_ignores_relationship_fields(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — governance class with relationship
    fields → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
                "supersedes": "ADR-0003@2025-09-11",  # Valid for governance
                "informed_by": "ADR-0004@2025-09-11",  # Valid for governance
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance decision with relationship fields.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-with-relationships.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_strategy_class_ignores_relationship_fields(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — strategy class with relationship
    fields → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                "governed_by": "ADR-0002@2025-09-11",  # Valid for strategy
                "informs": "ADR-0003@2025-09-11",  # Valid for strategy
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategy decision with relationship fields.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-with-relationships.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_style_guide_class_ignores_relationship_fields(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — style-guide class with relationship
    fields → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "style-guide",
                "supersedes": "ADR-0004@2025-09-11",  # Valid for style-guide
                "informed_by": "ADR-0005@2025-09-11",  # Valid for style-guide
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Style guide with relationship fields.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "style-guide-with-relationships.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template603_governance_template_no_scope_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-603 — governance template without scope
    field → passes
    Governance templates should not have scope
    (different from governance ADRs)
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "governance",
                "owners_ptr": "ADR-0001",
                # No scope field - correct for governance template
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<governance-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-no-scope.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)
