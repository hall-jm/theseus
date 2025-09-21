---
id: ADR-0005
title: Strategy title
status: Proposed
class: style-guide
# Strategy must not redefine owners; optionally point to an Owner ADR
owners_ptr: ADR-001
extends: null
supersedes: null
superseded_by: null
date: 2025-09-03
review_by: 2026-03-03
tags: [strategy]
change_history: []
---

# ADR-0002 - Template: Strategy

## Document Controls

### Status

| Field                  | Value                                   |
| ---------------------- | --------------------------------------- |
| **Version:**           | 0.1.0                                   |
| **Status:**            | Proposed                                |
| **Date:**              | 2025-09-03                              |
| **Applies to Schema:** | 0.1.0                                   |
| **Related:**           | ADR-0001 (Template: Base/Owner), ADR-0002 (Template: Delta) |

### Changelog

| Version | Date         | Notes                                        |
| ------- | ------------ | -------------------------------------------- |
| 0.1.0   | 03 Sept 2025 | Initial draft of template file               |

# Decision (one-liner)
<!-- key: decision_one_liner -->
Because <long-range driver>, we choose <strategic direction> so that <north star>.

## Context & Drivers
<!-- key: context_and_drivers -->
- Market forces: …
- Constraints: …
- Assumptions: …

## Principles
<!-- key: principles -->
- Prefer …
- Avoid …

## Guardrails
<!-- key: guardrails -->
- Do not take on >X SPOFs without mitigation.
- Keep unit economics within …

## North Star Metrics
<!-- key: north_star_metrics -->
- p95 ≤ …
- Cost per 1k requests ≤ …

## Consequences & Risks
<!-- key: consequences_and_risks -->
- Trade-offs at portfolio level …

## Rollout & Backout (Excluded) 
<!-- non-normative: Strategy ADRs exclude rollout/backout; see Style Guide §7 (ADR-SCHEMA-021). -->
**N/A — Strategy documents do not define rollout/backout.**

## Implementation Notes
<!-- key: implementation_notes -->
- How this informs Owner ADRs and Roadmaps …

## Evidence & Links
<!-- key: evidence_and_links -->
- Market research …
- Postmortems …

## Glossary
<!-- key: glossary -->
- …

## Related ADRs
<!-- key: related_adrs -->
- ADR-0001 (Template: Owner/Base)
- ADR-0002 (Template: Delta)

<!-- llm_tail:begin -->
```json
{
  "id": "ADR-0005",
  "class": "style-guide",
  "status": "Proposed",
  "owners_ptr": "ADR-001"
}
```
<!-- llm_tail:end -->