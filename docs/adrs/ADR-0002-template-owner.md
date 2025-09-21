## docs/adr/ADR-0001-template-owner.md (Base/Owner ADR)

---
id: ADR-0002
title: Template for `class:owner`
status: Proposed
class: template
owners: []
owners_ptr: ADR-0001
extends: null
superseded_by: null
date: 2025-09-06
review_by: 2026-03-06
applies_to:
  env: [dev]
  services: []
tags: [owner, template, topic, platform]
change_history: [{2025-09-06}]
template_of: owner            # when template: true → owner|delta|strategy|style-guide
placeholders_ok: true         # templates may use <angle-bracket> placeholders
---

# ADR-<ID Number> - <ADR Title>

## Document Controls

### Status

| Field                  | Value                                   |
| ---------------------- | --------------------------------------- |
| **Version**:           | 0.1.0                                   |
| **Status**:            | Proposed                                |
| **Date**:              | <Today's Date>                          |
| **Applies to Schema**: | 0.1.0                                   |
| **Related**:           | ADR-0001 (Style Guide)                  |

### Changelog

| Version | Date           | Notes                                        |
| ------- | -------------- | -------------------------------------------- |
| 0.1.0   | <Today's Date> | Initial draft of ADR                         |


# Decision (one-liner)
<!-- key: decision_one_liner -->
Because <driver>, we choose <option> so that <benefit>.

## Context & Drivers
<!-- key: context_and_drivers -->
- Goals: …
- Non-goals: …
- Constraints: …
- Assumptions: …

## Options Considered
<!-- key: options_considered -->
| Option | Fit to Drivers | Complexity | Risk | Reversibility | Notes |
|---|---|---|---|---|---|
| Option A |  |  |  |  |  |
| Option B |  |  |  |  |  |

- Rejected because: …

## Decision Details
<!-- key: decision_details -->
- Systems MUST …
- Clients SHOULD …
- Data MAY …

## Consequences & Risks
<!-- key: consequences_and_risks -->
- Reversibility score: 1–5 (lower = harder to undo)
- What becomes easier/harder: …

## Rollout & Backout
<!-- key: rollout_backout -->
- Phases: …
- Auto-backout thresholds: …

## Implementation Notes
<!-- key: implementation_notes -->
- …

## Evidence & Links
<!-- key: evidence_and_links -->
- BENCH-###
- PM-YYYY-MM-DD

## Glossary
<!-- key: glossary -->
- …

## Related ADRs
<!-- key: related_adrs -->
- ADR-0001 (style guide)

<!-- llm_tail:begin -->
```json
{
  "id": "ADR-0002",
  "class": "template",
  "status": "Proposed",
  "extends": null,
  "owners_ptr": "ADR-0001"
}
````
<!-- llm_tail:end -->
