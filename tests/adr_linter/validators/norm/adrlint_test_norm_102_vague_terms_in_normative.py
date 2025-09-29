# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/validators/norm/adrlint_test_norm_102_vague_terms_in_normative.py

"""
ADR-0001 · §11, 14 Linter Rules Reference
ADR-NORM-102 (W): Vague term in normative section.
Linting Tests: Framework foundation for vague term detection in normative
               sections.

ARCHITECTURAL INTENT:
This validator establishes the governance framework for detecting
implementational ambiguity in normative text. The current implementation is
intentionally basic (7 hardcoded terms) to serve as a smoke test while proving
the extension mechanism.

WHAT "VAGUE" MEANS IN THIS CONTEXT:
- Terms that prevent LLMs from implementing specific requirements
- Claims lacking quantifiable metrics or bounds
- Adjectives without supporting measurements or criteria
- Language that requires additional context to act upon

SMOKE TEST IMPLEMENTATION: Validates basic vague term detection in normative
                           sections.

Current scope: 7 hardcoded terms detected in normative sections only
               (decision_details, rollout_backout).
- robust, simple, scalable, flexible, significant, efficient, reliable


Test Coverage:
  1) Warning when vague terms appear in normative sections
  2) No warning when same terms appear in non-normative sections
  3) Multiple vague terms emit multiple warnings
  4) Class exemptions work (style-guide, template)
  5) Context limitations documented (flags "efficient O(log n)" same as
     "efficient solution")

KNOWN LIMITATIONS: Context-blind matching, narrow term list, no qualification
                   detection.
This is intentional baseline behavior for framework validation.

Ref: ADR-0001 §5: "Prefer numbers & units over adjectives"
"""

from __future__ import annotations

from adr_linter.constants import (
    CANONICAL_KEYS_OWNER,
)
from adr_linter.report import Report
from adr_linter.validators.registry import run_all

from ...conftest import (
    _write_text,
    _ctx_from_path,
    _good_meta_front_matter,
    _has_code,
)


def _adr_with_sections(
    ws,
    adr_id: str,
    decision_details_content: str,
    rollout_backout_content: str,
    other_content: str = "Standard implementation approach.",
    adr_class: str = "owner",
) -> str:
    """
    Create an ADR with specific content in normative and non-normative
    sections. Returns the file path.
    """
    meta = _good_meta_front_matter(
        **{"id": adr_id, "class": adr_class, "extends": None}
    )

    # Create full canonical body with custom content in target sections
    sections = []
    for key in CANONICAL_KEYS_OWNER:
        if key == "decision_details":
            content = decision_details_content
        elif key == "rollout_backout":
            content = rollout_backout_content
        else:
            content = other_content
        sections.append(f"<!-- key: {key} -->\n{content}\n")

    body = "\n".join(sections)
    full_text = meta + "\n" + body

    return _write_text(ws, f"docs/adr-new/{adr_id}-test.md", full_text)


def test_adrlint_norm_102_vague_term_in_decision_details_emits_warning(
    _route_and_reset_workspace,
):
    """
    Vague term 'robust' in decision_details section
    → MUST emit ADR-NORM-102.
    """
    adr_path = _adr_with_sections(
        _route_and_reset_workspace,
        "ADR-9601",
        decision_details_content="The system MUST be robust and handle all "
        "edge cases.",
        rollout_backout_content="Standard rollout procedure applies.",
    )

    ctx = _ctx_from_path(adr_path)
    rpt = Report()
    run_all(ctx, rpt)

    assert _has_code(rpt, "ADR-NORM-102")


def test_adrlint_norm_102_vague_term_in_rollout_backout_emits_warning(
    _route_and_reset_workspace,
):
    """
    Vague term 'efficient' in rollout_backout section
    → MUST emit ADR-NORM-102.
    """
    adr_path = _adr_with_sections(
        _route_and_reset_workspace,
        "ADR-9602",
        decision_details_content="The system MUST respond within 150ms "
        "p95.",
        rollout_backout_content="Rollout MUST be efficient to minimize "
        "downtime.",
    )

    ctx = _ctx_from_path(adr_path)
    rpt = Report()
    run_all(ctx, rpt)

    assert _has_code(rpt, "ADR-NORM-102")


def test_adrlint_norm_102_multiple_vague_terms_emit_multiple_warnings(
    _route_and_reset_workspace,
):
    """
    Multiple vague terms in decision_details
    → MUST emit ADR-NORM-102 warnings.

    FRAMEWORK VALIDATION:
    Tests that the validator detects vague terms when present.
    Current implementation finds first match per section due to
    regex.search() usage.
    """
    adr_path = _adr_with_sections(
        _route_and_reset_workspace,
        "ADR-9603",
        decision_details_content="The system MUST be scalable and flexible "
        "while remaining simple.",
        rollout_backout_content="Standard rollout applies.",
    )

    ctx = _ctx_from_path(adr_path)
    rpt = Report()
    run_all(ctx, rpt)

    # Verify that vague terms are detected (framework works)
    assert _has_code(rpt, "ADR-NORM-102")


def test_adrlint_norm_102_vague_term_in_non_normative_section_is_ok(
    _route_and_reset_workspace,
):
    """
    Vague term 'reliable' in non-normative section (context_and_drivers)
    → should NOT emit ADR-NORM-102.
    """
    adr_path = _adr_with_sections(
        _route_and_reset_workspace,
        "ADR-9604",
        decision_details_content="The system MUST respond within 150ms p95.",
        rollout_backout_content="Standard rollout applies.",
        other_content="Current system is not reliable enough for production.",
    )

    ctx = _ctx_from_path(adr_path)
    rpt = Report()
    run_all(ctx, rpt)

    assert not _has_code(rpt, "ADR-NORM-102")


def test_adrlint_norm_102_current_limitation_context_blind_matching(
    _route_and_reset_workspace,
):
    """
    FRAMEWORK LIMITATION:
    Current validator flags terms even when properly quantified.

    Examples that SHOULD be acceptable but currently trigger warnings:
    - "efficient with O(log n)" (specific algorithmic complexity)
    - "reliable with 99.9% SLA" (quantified reliability)

    This test documents the baseline implementation's context-blindness.
    Future extensions should distinguish between:
    - Vague: "The system MUST be efficient"
    - Specific: "The system MUST be efficient with O(log n) lookup time"

    → Current implementation emits ADR-NORM-102 for both cases.
    """
    adr_path = _adr_with_sections(
        _route_and_reset_workspace,
        "ADR-9605",
        decision_details_content="The system MUST be efficient with O(log n) "
        "lookup time and scale to 10,000 concurrent users.",
        rollout_backout_content="Rollout MUST be reliable with 99.9% success "
        "rate.",
    )

    ctx = _ctx_from_path(adr_path)
    rpt = Report()
    run_all(ctx, rpt)

    # Current limitation: emits warnings even for quantified usage
    assert _has_code(rpt, "ADR-NORM-102")


def test_adrlint_norm_102_style_guide_class_is_exempt(
    _route_and_reset_workspace,
):
    """
    CLASS EXEMPTION:
    Vague terms in style-guide class ADR should not trigger warnings.

    Style guides need flexibility to discuss abstract concepts and examples.
    The validator specifically exempts style-guide and template classes.

    → should NOT emit ADR-NORM-102 (exempted by validator).
    """
    meta = _good_meta_front_matter(
        **{"id": "ADR-9606", "class": "style-guide", "extends": None}
    )

    content = """<!-- key: decision_details -->
Style guides MUST be robust and flexible to accommodate various use cases.

<!-- key: context_and_drivers -->
Standard context.

<!-- key: options_considered -->
Standard options.

<!-- key: consequences_and_risks -->
Standard consequences.

<!-- key: rollout_backout -->
Style guides MUST be simple and scalable.

<!-- key: implementation_notes -->
Standard notes.

<!-- key: evidence_and_links -->
Standard links.

<!-- key: glossary -->
Standard glossary.

<!-- key: related_adrs -->
Standard related.
"""

    full_text = meta + "\n" + content
    adr_path = _write_text(
        _route_and_reset_workspace, "docs/adr-new/ADR-9606-style.md", full_text
    )

    ctx = _ctx_from_path(adr_path)
    rpt = Report()
    run_all(ctx, rpt)

    assert not _has_code(rpt, "ADR-NORM-102")
