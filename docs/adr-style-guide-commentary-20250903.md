# ADR Style Guide (v1.0)

## 1) Goals & Scope

* Make decisions **atomic, auditable, and reversible**.
* Keep docs **human-skim friendly** and **machine-readable** (LLMs, linters).
* Support **inheritance** via pointers & deltas without ambiguity.

## 2) Canonical file layout & naming

* Folder: `docs/adr/`
* ID format: `ADR-XXXX` (zero-padded; monotonic; never reuse)
* Filename: `ADR-XXXX-short-kebab-title.md`
* Commit message prefix: `[ADR-XXXX] <title>`

## 3) Required metadata (YAML front-matter)

```yaml
id: ADR-0123
title: Short imperative title
status: Proposed | Accepted | Deprecated | Superseded
deciders: [roles or names]
owners: [primary maintainer(s)]
date: 2025-09-03
review_by: 2026-03-03
extends: null # or ADR-0001@2025-03-14
supersedes: null
superseded_by: null
applies_to:
  env: [prod, staging]        # narrow for deltas
  services: [*]               # or list
tags: [topic, platform]
```

## 4) Canonical section keys & order

Use these **exact keys** (stable for tooling). Headings may be pretty, but keys must map 1:1.

1. `decision_one_liner` (Because → We choose → So that …)
2. `context_and_drivers`
3. `options_considered` (table + explicit rejections)
4. `decision_details` (normative MUST/SHOULD/MAY)
5. `consequences_and_risks` (incl. reversibility score 1–5)
6. `rollout_backout`
7. `implementation_notes`
8. `evidence_and_links`
9. `glossary`
10. `related_adrs`

> Tip: If your renderer doesn’t support hidden keys, put a short HTML comment above each section: `<!-- key: rollout_backout -->`.

## 5) Writing standards

* Use **RFC-2119** keywords for normative text.
* Prefer **numbers & units** over adjectives. (“p95 ≤ 150 ms”, not “fast”.)
* **Active voice**, short sentences (≤20 words), consistent terms.
* Define acronyms once; keep a **mini-glossary**.
* Avoid pronouns with unclear referents; repeat the noun.

## 6) Options rubric (table)

Score 1–5 (higher is better) and explain trade-offs.

| Option | Fit to Drivers | Complexity | Risk | Reversibility | Notes |
| ------ | -------------- | ---------- | ---- | ------------- | ----- |

Include **“Rejected because …”** bullets for each non-chosen option.

## 7) Pointers & deltas (inheritance rules)

* Pin the base ADR and version: `extends: ADR-0001@<date-or-commit>`.
* **Precedence** (highest → lowest):

  1. `overrides.<key>` (child replaces section)
  2. `not_applicable.<key>` (child disables base section with reason)
  3. `adds.<key>` (child adds new, child-only section)
  4. `ptr → ADR-0001#<key>` (inherits base as-is)
* Each child ADR must include a **Diff summary** listing changed keys.
* Scope deltas tightly (`applies_to.env/services/window`) and time-box them.

### Delta ADR block (inside the document body)

```yaml
diff_summary:
  - rollout_backout: override (dry-run thresholds differ)
  - audit_logging: override (reduced sampling)
ptr:
  context_and_drivers: ADR-0001#context_and_drivers
  decision_one_liner: ADR-0001#decision_one_liner
overrides:
  rollout_backout:
    replaces: ADR-0001#rollout_backout
    decision: >
      Canary at 1% in staging for 24h; backout if p95 > 180 ms for 30 min
      or error rate > 0.5%.
not_applicable:
  data_retention:
    reason: Synthetic identities; ephemeral store only.
```

**When to write a delta vs a new ADR**

* **Delta**: temporary, scoped application change (how we apply).
* **New ADR**: lasting policy change (what we believe or require).

## 8) Lifecycle & governance

* Status transitions: `Proposed → Accepted → (Deprecated|Superseded)`.
* Required fields to **Accept**: completed options table, numeric thresholds, owners, rollout/backout, evidence links.
* **Supersedes/Superseded\_by** must be **bi-directional** links.
* **Review\_by** is mandatory; add revisit triggers (e.g., “if p95 > 180 ms for 2 weeks”).
* Record **approvers & date** in the metadata; add a `change_history` list if you revise.

## 9) Evidence & traceability

* Link to PoCs, benchmarks, incidents, issues/PRs; prefer **permalinks**.
* Use stable IDs in text: `BENCH-421`, `PM-2024-09-12`.
* If a claim is data-based, cite the source under **Evidence & Links**.

## 10) LLM-friendliness

* Keep the YAML front-matter compact; use **stable keys** and **numbered lists**.
* Repeat exact phrases (don’t synonym-surf) for concepts you’ll query later.
* Use small, well-labeled **tables** for option scoring and config matrices.
* Add a short **Q\&A**: “Questions this ADR answers”.

## 11) PR & review checklist (copy into PR template)

* [ ] One decision per ADR, clear status & one-liner
* [ ] Options table + explicit rejections
* [ ] Numeric thresholds, units, RFC-2119 language
* [ ] Consequences, risks, **reversibility score**
* [ ] Rollout & **backout** with owners/on-call
* [ ] Evidence links (permalinks)
* [ ] `review_by` and revisit triggers
* [ ] For deltas: `extends@version`, **diff\_summary**, scope window/env/services
* [ ] Cross-links: `supersedes`/`superseded_by` where applicable

## 12) Anti-patterns (avoid)

* Bundling multiple decisions into one ADR
* Vague terms (“robust”, “significant”) without numbers
* Free-text overrides without section keys
* Silent changes to base ADR that break child deltas (always pin `extends`)
* Delta sprawl (consolidate when >2 active deltas on a base)

## 13) Starter templates

### Base ADR (Markdown body; YAML front-matter above)

```markdown
# Decision (one-liner)
Because <driver>, we choose <option> so that <benefit>.

<!-- key: context_and_drivers -->
## Context & Drivers
- …

<!-- key: options_considered -->
## Options Considered
| Option | Fit | Complexity | Risk | Reversibility | Notes |
|---|---|---|---|---|---|
- Rejected because: …

<!-- key: decision_details -->
## Decision Details
- Services MUST …
- Clients SHOULD …

<!-- key: consequences_and_risks -->
## Consequences & Risks
- …

<!-- key: rollout_backout -->
## Rollout & Backout
- Phases …
- Auto-backout thresholds …

## Implementation Notes
…

## Evidence & Links
- …

## Glossary
…

## Related ADRs
- ADR-0001 (base), ADR-0042 (superseded)
```

### Delta ADR (Markdown body; YAML front-matter above)

```markdown
## Diff summary (vs ADR-0001@2025-03-14)
- rollout_backout: override
- audit_logging: override
- others: ptr → ADR-0001

## Overrides
<!-- key: rollout_backout -->
### Rollout & Backout (override)
…

<!-- key: audit_logging -->
### Audit Logging (override)
…

## Inherited sections
- Context & Drivers: ptr → ADR-0001#context_and_drivers
- Decision: ptr → ADR-0001#decision_one_liner
```