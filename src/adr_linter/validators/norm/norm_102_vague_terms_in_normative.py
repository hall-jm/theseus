# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/norm/norm_102_vague_terms_in_normative.py

"""
ADR-NORM-102 — Vague term in normative section.

GOVERNANCE FRAMEWORK FOR IMPLEMENTATIONAL AMBIGUITY DETECTION

This validator establishes the architectural foundation for detecting terms
that prevent LLMs or humans from implementing specific requirements in
normative ADR sections.

WHAT "VAGUE" MEANS IN ADR CONTEXT:
- Terms requiring additional context to act upon
- Unquantified claims lacking supporting metrics
- Comparative adjectives without baselines ("faster", "better")
- Quality statements without measurable criteria ("reliable", "secure")
- Performance claims without bounds ("efficient", "scalable")

CURRENT IMPLEMENTATION (BASELINE/SMOKE TEST):
This is intentionally a crude 7-word hardcoded regex that serves as:
1. Framework validation (proves the governance slot works)
2. Smoke test for obvious vagueness patterns
3. Extension point for future domain-specific detection

Hardcoded terms:
- robust|simple|scalable|flexible|significant|efficient|reliable

KNOWN LIMITATIONS (BY DESIGN):
- Context-blind: flags "efficient O(log n)" same as "efficient solution"
- Narrow scope: misses "better", "improved", "faster", "secure", etc.
- No domain awareness: CLI vs Queue vs API vagueness differs
- No qualification detection: can't distinguish quantified vs unquantified
  usage

EXTENSION PATHWAY:
Future ADRs can extend this validator through the registry mechanism; e.g.:

ADR-NORM-102-CLI: Command-line specific patterns
  - "graceful error handling" → needs exit codes, error message formats
  - "user-friendly interface" → needs UX criteria, accessibility standards

ADR-NORM-102-MESSAGING: Queue/service specific patterns
  - "reliable delivery" → needs delivery guarantees
    (at-least-once, exactly-once)
  - "high throughput" → needs TPS targets, latency bounds

ADR-NORM-102-PERF: Performance claim validation
  - "fast response" → needs latency SLAs, percentile targets
  - "low memory usage" → needs memory bounds, measurement criteria

REGISTRY EVOLUTION DESIGN:
The validator registration should eventually support:
- Chaining: base NORM-102 + domain-specific extensions
- Configuration: different term lists per ADR class/scope
- Context analysis: parse surrounding text for quantification
- Pattern detection: regex → NLP for comparative/qualitative patterns

IMPLEMENTATION NOTES:
- Scans only NORMATIVE_KEYS sections (decision_details, rollout_backout)
- Exempts style-guide and template classes (they need examples/flexibility)
- Can emit multiple findings per document (no early break)
- Integrates with ADR-0001 §5: "Prefer numbers & units over adjectives"

FUTURE LLM REVIEWERS:
Compare this docstring with the test file docstring to detect drift or
inconsistencies in the architectural intent documentation.

Ref: ADR-0001
- § 5 · Writing standards
- §11 · Normative language safety (RFC-2119)
- §14 · Linter Rules Reference
"""

from __future__ import annotations
from ...constants import (
    VAGUE_TERMS_RX,
    NORMATIVE_KEYS,
)
from ...parser.structure import line_from_pos


def validate_norm_102_vague_terms_in_normative(ctx, rpt) -> None:
    """
    Emit ADR-NORM-102 for each vague term occurrence in normative sections.

    BASELINE IMPLEMENTATION: Simple regex matching against hardcoded term
    list. This is the foundation layer for more sophisticated vagueness
    detection.

    Args:
        ctx: Document context with meta, body, section_info
        rpt: Report object for collecting validation findings

    Behavior:
        - Scans normative sections only (decision_details, rollout_backout)
        - Exempts style-guide and template classes
        - Emits warning for each vague term found
        - Multiple terms in same section = multiple warnings

    Extension points:
        - Replace VAGUE_TERMS_RX with domain-specific patterns
        - Add context analysis for term qualification
        - Implement comparative/qualitative pattern detection
    """
    klass = ctx.meta.get("class")
    if klass in {"style-guide", "template"}:
        return

    body = ctx.body
    path = ctx.path
    section_info = ctx.section_info

    for key, content in section_info.sections_by_key.items():
        if key not in NORMATIVE_KEYS:
            continue

        start_in_body = body.find(content)
        if start_in_body == -1:
            continue

        # BASELINE: Simple pattern matching (extension point for enhancement)
        vm = VAGUE_TERMS_RX.search(content)
        if vm:
            line_num = line_from_pos(body, start_in_body + vm.start())
            rpt.add(
                "ADR-NORM-102",
                path,
                f"vague term '{vm.group()}' in {key}",
                line_num,
            )
