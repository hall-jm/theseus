## docs/adr/ADR-0003-template-delta.md (Delta ADR)

```markdown
---
id: ADR-0000
title: Delta title (scoped)
status: Proposed
class: delta
# NOTE: pin to date or commit (lowercase hex)
extends: ADR-0001@2025-03-14
supersedes: null
superseded_by: null
applies_to:
  env: [staging]
  services: [authn, session-gateway]
  window: 2025-09-10..2025-09-24
date: 2025-09-03
review_by: 2025-09-25
tags: [delta]
change_history: []
---

## Diff summary (vs ADR-0001@2025-03-14)
- rollout_backout: override (dry-run thresholds)
- audit_logging: override (reduced sampling)
- others: ptr → ADR-0001

### Overrides (YAML)
```yaml
overrides:
  rollout_backout:
    replaces: ADR-0001#rollout_backout
    decision: >
      Canary at 1% in staging for 24h. Automatic backout if p95 > 180 ms
      for 30 min or error rate > 0.5%.
    steps:
      - Enable feature flag `session_v2` at 1%.
      - Monitor SLO dashboard "AUTH-SLO-DRYRUN".
      - If breach: disable flag; revert routes.
  audit_logging:
    replaces: ADR-0001#audit_logging
    policy: MUST
    sampling: 10% of success; 100% of errors
````

### Inherited sections (YAML)

```yaml
ptr:
  decision_one_liner: ADR-0001#decision_one_liner
  context_and_drivers: ADR-0001#context_and_drivers
  options_considered: ADR-0001#options_considered
  decision_details: ADR-0001#decision_details
  consequences_and_risks: ADR-0001#consequences_and_risks
  implementation_notes: ADR-0001#implementation_notes
  evidence_and_links: ADR-0001#evidence_and_links
  glossary: ADR-0001#glossary
  related_adrs: ADR-0001#related_adrs
```

### Not applicable (YAML)

```yaml
not_applicable:
  data_retention:
    reason: Synthetic identities + ephemeral store only.
```

# Decision (one-liner)

<!-- key: decision_one_liner -->

Inherited via ptr → ADR-0001#decision\_one\_liner.

## Context & Drivers

<!-- key: context_and_drivers -->

Inherited via ptr.

## Options Considered

<!-- key: options_considered -->

Inherited via ptr.

## Decision Details

<!-- key: decision_details -->

Only deltas are normative here; base details inherited via ptr.

## Consequences & Risks

<!-- key: consequences_and_risks -->

Inherited via ptr. Note dry-run specific risks in Overrides.

## Rollout & Backout

<!-- key: rollout_backout -->

Overridden via `overrides.rollout_backout`.

## Implementation Notes

<!-- key: implementation_notes -->

Inherited via ptr.

## Evidence & Links

<!-- key: evidence_and_links -->

Inherited via ptr; add dry-run dashboards/PRs here.

## Glossary

<!-- key: glossary -->

Inherited via ptr.

## Related ADRs

<!-- key: related_adrs -->

* ADR-0001 (base)

<!-- llm_tail:begin -->

```json
{
  "id": "ADR-0000",
  "class": "delta",
  "status": "Proposed",
  "extends": "ADR-0001@2025-03-14",
  "effective_owner": "Architecture Council",
  "changed_keys": ["rollout_backout", "audit_logging"],
  "scope": {"env":"staging","services":["authn","session-gateway"],"window":"2025-09-10..2025-09-24"}
}
```

<!-- llm_tail:end -->

````