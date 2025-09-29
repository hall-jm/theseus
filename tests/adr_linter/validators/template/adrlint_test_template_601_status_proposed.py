# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/template/adrlint_test_template_601_status_proposed.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-TEMPLATE-601 (W): `status` not `Proposed` in a template ADR.
Validates that template class ADRs use required `status: Proposed`.

Rule: IF class == "template" AND status != "Proposed" → WARNING
Template ADRs MUST use `status: Proposed` per ADR-0001 §3
Other classes ignore this constraint (different validators handle their
status rules)
"""

from __future__ import annotations

from adr_linter.validators.registry import run_all
from adr_linter.report import Report
from adr_linter.validators.template.template_601_status_proposed import (
    _ERROR_CODE as _ADR_ERROR_CODE,
)

from ...conftest import (
    _write_text,
    _write_and_ctx,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
    assert_warning_code,
)


def test_adrlint_template601_accepted_status_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — template ADR with status
    "Accepted" → warning
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",
                "owners_ptr": "ADR-0001",
                # Invalid for template - should be "Proposed"
                "status": "Accepted",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<owner-decision>",
    ]
    p = _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-6002-template-accepted-status.md",
        "\n".join(md),
    )
    ctx = _ctx_from_path(p)
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_deprecated_status_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — template ADR with status
    "Deprecated" → warning
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "strategy",
                "owners_ptr": "ADR-0001",
                "status": "Deprecated",  # Invalid for template
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<strategy-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-deprecated-status.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_superseded_status_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — template ADR with status
    "Superseded" → warning
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "delta",
                "owners_ptr": "ADR-0001",
                "status": "Superseded",  # Invalid for template
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<delta-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-superseded-status.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_missing_status_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — template ADR with missing
    status → warning

    Note: _good_meta_front_matter() adds a valid "status" by default.
          We need to remove the default "status" value to let this
          test validate the condition.
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "governance",
                "owners_ptr": "ADR-0001",
                # status field missing entirely
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<governance-decision>",
    ]

    # Remove the status line from the YAML front-matter
    md_lines = md[0].split("\n")
    md_lines = [line for line in md_lines if not line.startswith("status:")]
    md_without_status = "\n".join(md_lines)

    md = [
        md_without_status,
        "<!-- key: decision_one_liner -->",
        "<governance-decision>",
    ]

    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-missing-status.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_null_status_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — template ADR with null
    status → warning
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "style-guide",
                "owners_ptr": "ADR-0001",
                "status": None,  # Null status
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<style-guide-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-null-status.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_empty_string_status_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — template ADR with empty string
    status → warning
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",
                "owners_ptr": "ADR-0001",
                "status": "",  # Empty string status
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<owner-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-empty-status.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_case_sensitive_proposed_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — template ADR with wrong case
    "proposed" → warning
    Case sensitivity test - must be exact "Proposed" match
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "strategy",
                "owners_ptr": "ADR-0001",
                # Invalid - case sensitive, should be "Proposed"
                "status": "proposed",
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<strategy-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-case-proposed.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_uppercase_proposed_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — template ADR with
    "PROPOSED" → warning
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "delta",
                "owners_ptr": "ADR-0001",
                "status": "PROPOSED",  # Invalid - should be "Proposed"
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<delta-decision>",
    ]

    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-uppercase-proposed.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


"""
Rule being tested: ADR-TEMPLATE-601 — template ADR with whitespace in
status → warning
    
Note: The code is already stripping out whitespaces from values
      like "status". Spending time breaking the code to let make this
      pytest pass was deemed unnecessary as of 27 September 2025
"""
"""
def test_adrlint_template601_whitespace_status_triggers(
    _route_and_reset_workspace,
):
    ""
    Rule being tested: ADR-TEMPLATE-601 — template ADR with whitespace in
    status → warning
    
    Note: The code is already stripping out whitespaces from values
          like "status". Spending time breaking the code to let make this
          pytest pass was deemed unnecessary as of 27 September 2025
    ""
    md = [
        _good_meta_front_matter(**{
            "class": "template",
            "template_of": "governance",
            "owners_ptr": "ADR-0001",
            "status": " Proposed ",  # Contains whitespace
        }),
        "<!-- key: decision_one_liner -->",
        "<governance-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "template-whitespace-status.md",
        "\n".join(md)
    )
    
    print(f"[D TEST: TEMPLATE-601] md: _{str(md)}_")
    
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)
"""


def test_adrlint_template601_custom_status_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — template ADR with custom
    status → warning
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "style-guide",
                "owners_ptr": "ADR-0001",
                "status": "Draft",  # Custom status value
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<style-guide-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-custom-status.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_proposed_status_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — template ADR with status
    "Proposed" → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "owner",
                "owners_ptr": "ADR-0001",
                "status": "Proposed",  # Valid status for template
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<owner-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-valid-proposed.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_governance_template_proposed_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — governance template with status
    "Proposed" → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "governance",
                "owners_ptr": "ADR-0001",
                "status": "Proposed",  # Valid status for governance template
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<governance-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-template-proposed.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_strategy_template_proposed_passes(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — strategy template with status
    "Proposed" → passes
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "strategy",
                "owners_ptr": "ADR-0001",
                "status": "Proposed",  # Valid status for strategy template
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<strategy-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-template-proposed.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_owner_class_ignores_status(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — owner class with non-Proposed
    status → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "owner",
                "governed_by": "ADR-0001@2025-09-11",
                "status": "Accepted",  # Valid for owner class
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Owner decision with Accepted status.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "owner-accepted-status.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_delta_class_ignores_status(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — delta class with non-Proposed
    status → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "delta",
                "extends": "ADR-0001@2025-09-11",
                "owners_ptr": "ADR-0001",
                "status": "Deprecated",  # Valid for delta class
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Delta decision with Deprecated status.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "delta-deprecated-status.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_governance_class_ignores_status(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — governance class with non-Proposed
    status → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "governance",
                "scope": "cli",
                "status": "Superseded",  # Valid for governance class
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Governance decision with Superseded status.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "governance-superseded-status.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_strategy_class_ignores_status(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — strategy class with non-Proposed
    status → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "strategy",
                "owners_ptr": "ADR-0001",
                "status": "Accepted",  # Valid for strategy class
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Strategy decision with Accepted status.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "strategy-accepted-status.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_style_guide_class_ignores_status(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — style-guide class with non-Proposed
    status → ignored
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "style-guide",
                "status": "Deprecated",  # Valid for style-guide class
            }
        ),
        "<!-- key: decision_one_liner -->",
        "Style guide with Deprecated status.",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace,
        "style-guide-deprecated-status.md",
        "\n".join(md),
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert not _has_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_numeric_status_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — template ADR with numeric
    status → warning
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "delta",
                "owners_ptr": "ADR-0001",
                "status": 1,  # Numeric status value
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<delta-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-numeric-status.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)


def test_adrlint_template601_boolean_status_triggers(
    _route_and_reset_workspace,
):
    """
    Rule being tested: ADR-TEMPLATE-601 — template ADR with boolean
    status → warning
    """
    md = [
        _good_meta_front_matter(
            **{
                "class": "template",
                "template_of": "style-guide",
                "owners_ptr": "ADR-0001",
                "status": True,  # Boolean status value
            }
        ),
        "<!-- key: decision_one_liner -->",
        "<style-guide-decision>",
    ]
    p, ctx = _write_and_ctx(
        _route_and_reset_workspace, "template-boolean-status.md", "\n".join(md)
    )
    rpt = Report()
    run_all(ctx, rpt)
    assert_warning_code(rpt, _ADR_ERROR_CODE)
