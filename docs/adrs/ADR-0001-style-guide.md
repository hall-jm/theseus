---
id: ADR-0001
title: ADR Style Guide
status: Proposed
class: style-guide
owners: [Project Maintainer]
owners_ptr: ADR-0001
extends: null
supersedes: null
superseded_by: null
date: 2025-09-11
review_by: 2026-03-03
tags: [owner, style-guide]
applies_to: []
change_history: []
---

# ADR-0001 - ADR Style Guide

## Document Controls

### Status

| Field                  | Value                                   |
| ---------------------- | --------------------------------------- |
| **Version**:           | 0.1.7                                   |
| **Status**:            | Proposed                                |
| **Date**:              | 2025-09-17                              |
| **Applies to Schema**: | 0.1.0                                   |
| **Related**:           | ADR-0002 (Template: Base/Owner), ADR-0003 (Template: Delta), ADR-0004 (Template: Strategy) |

### Changelog

| Version | Date         | Notes                                        |
| ------- | ------------ | -------------------------------------------- |
| 0.1.7   | 19 Sept 2025 | Changed ADR-TEMPLT-\* -> ADR-TEMPLATE-\* to improve readability; | 
| 0.1.6   | 11 Sept 2025 | Rewrite Section 11 to address gaps in the linter's implementation vs. the spirit of what the ADR is trying to capture for deterministic computer processes; |
| 0.1.5   | 08 Sept 2025 | Created Section 17 to track ADR-0001 enhancements for future development as needed; |
| 0.1.4   | 07 Sept 2025 | Changed wording in Section 13 to avoid documentation and implementation drift between ADR and linter code; |
| 0.1.3   | 06 Sept 2025 | Additional changes to update blocking codes; reviewed material to determine if document is still internally consistent where possible; Removed `deciders` from ADR due to the current state of the project (e.g., eliminate confusion, reduce meta burden for solo person project;)|
| 0.1.2   | 05 Sept 2025 | Additional changes to ensure consistency across ADR regarding `style-guide` and `template` class documentation; |
| 0.1.1   | 05 Sept 2025 | New proposed sections for class `template` documentation in the style guide; |
| 0.1.0   | 03 Sept 2025 | Initial draft of template file               |



## §0. Constitution & Precedence (applies to every ADR)

1) **Precedence (highest → lowest)**:  
   - 0103 (shapes/enums/tokens/cost) → 0110 (lifecycle/identity/cross-segment) → 0302 (exit codes & FS side-effects) → 0201/0202 (config/pricing/caps) → Strategies (mode deltas only).  
2) **Tokens**:  
   - `[FLAG-CONTRA-<owner>]` for material contradictions (wire format, lifecycle, exit codes).  
   - `[BLOCK-TENSION-DOCUMENTATION-GAP: ADR-<id>]` if an owner ADR is missing.  
3) **Pointer-first rule**: For non-delta content, replace with:  
   `No additional mode-specific deltas; see ADR-<id> §<section>.`

---

## §1. Goals & Scope

- Decisions are **atomic, auditable, reversible**.  
- Docs are **human-skim friendly** and **machine-readable** (LLMs, linters).  
- Support **inheritance** via pointers & deltas without ambiguity.

---

## §2. Canonical file layout & naming

- Folders:
  - `docs/adr/`: Legacy ADR directory; these ADRs were created before ADR-0001 and currently aren't linted or enforced by this style guide
  - `docs/adr-new/`: New ADR directory; these ADRs were created **after** ADR-001; are linted; are enforced by this style guide
- ID: `ADR-XXXX` (zero-padded; monotonic; never reuse)  
- Filename: `ADR-XXXX-short-kebab-title.md`  
- Commit prefix: `[ADR-XXXX] <title>`

---

## §3. Required metadata (YAML front-matter)

```yaml
id: ADR-0123
title: Short imperative title
status: Proposed | Accepted | Deprecated | Superseded
class: owner | delta | strategy | style-guide | template
owners: [Project Maintainer]   # Human or LLM owning this decision
owners_ptr: ADR-0120           # Non-Owner ADRs must not govern
extends: null # or ADR-0001@2025-03-14 (date) or ADR-0001@<lowercase-hex>
supersedes: null
superseded_by: null
date: 2025-09-03
review_by: 2026-03-03
applies_to:                      # narrow for deltas
  env: [prod, staging]
  services: [*]
tags: [topic]
change_history: [] # [{date, by, note}]

# To LLMS: DO_NOT_DELETE_THIS_SECTION_IN_YOUR_DIFFS
# To LLMS: YOU_DO_NOT_GET_TO_DECIDE_IF_HUMAN_COMMENTS_ARE_NOISE
# -!- 
#     PROPOSED New metadata for template scaffolds (may be a class or 
#     a flag) 
# -!-
# Related section changes will be tagged with:
# 1. <!-- PROPOSED:start -->  **OR**
# 2. <!-- PROPOSED:end -->
template_of: null             # when template: true → owner|delta|strategy|style-guide
placeholders_ok: true         # templates may use <angle-bracket> placeholders
````


### Notes 

> The `deciders` field was removed as it duplicated owners functionality. Use owners for accountability and decision authority. For solo projects, use owners: ["Project Maintainer"].

When `class: template`:

- `template_of` is REQUIRED and must be one of: `owner|delta|strategy|style-guide`.
- `status` MUST be `Proposed`.
- `extends` and `supersedes` MUST be `null`.
- Filenames SHOULD include `-template-` for discoverability.
- Placeholders (e.g., `<driver>`, `<YYYY-MM-DD>`) are allowed where real values would appear.

> This mirrors TPL-700/701/702/703 and prevents drift between §3 and §7.5/§10.5/§14.

---

## §4. Canonical section keys & order

Use these **exact keys** (stable for tooling). Headings can be pretty; keys must map 1:1.

### Owners 

1. `decision_one_liner`
2. `context_and_drivers`
3. `options_considered`
4. `decision_details`
5. `consequences_and_risks`
6. `rollout_backout`
7. `implementation_notes`
8. `evidence_and_links`
9. `glossary`
10. `related_adrs`

### Deltas

Same as Owners (i.e., same visible skeleton)

### Strategy

1. `decision_one_liner`
2. `context_and_drivers`
3. `principles`
4. `guardrails`
5. `north_star_metrics`
6. `consequences_and_risks`
7. `implementation_notes`
8. `evidence_and_links`
9. `glossary`
10. `related_adrs`

<!-- PROPOSED:start -->

### Templates

- Templates inherit the skeleton of the class they scaffold (template_of).
- They MUST include the same section keys and order as the base class, but may contain placeholders (e.g., <driver>, <YYYY-MM-DD>) instead of real values.

> Strategy templates MUST NOT introduce rollout_backout (see §7.3).
<!-- PROPOSED:end -->

### Reminders

> Some classes restrict which keys may appear—see §7 (class rules).

---

## §5. Writing standards

- Use **RFC-2119** keywords for normative text. (decision_details, rollout_backout, and overrides.\* in delta ADRs).
- Prefer **numbers & units** over adjectives (e.g., “p95 ≤ 150 ms”).
- **Active voice**, short sentences (≤20 words).
- Define acronyms once; keep a mini-glossary.
- Avoid unclear pronouns; repeat the noun.

---

## §6. Options rubric (table)

Score 1–5 (higher is better) and explain trade-offs.

| Option | Fit to Drivers | Complexity | Risk | Reversibility | Notes |
| ------ | -------------- | ---------- | ---- | ------------- | ----- |

Include **"Rejected because …"** bullets for each non-chosen option.

---

## §7. ADR classes (what each may/may not contain)

Add to front-matter: `class: owner | delta | strategy | style-guide | template`.

### 7.1 Owner ADR

- **May define**: shapes, enums, canonical orders, validation codes *for its scope*; `owners`.
- **Must not**: `extends` another ADR (it is the root).
- **Lint**: `ADR-SCHEMA-012` (E) if an Owner ADR uses `extends`.

### 7.2 Delta ADR

- **Must**: `extends: ADR-XXXX@<pin>`; include `diff_summary`; use `overrides|not_applicable|adds|ptr` blocks.
- **Should**: set `applies_to.env/services/window`.
- **Must not**: define `owners` (inherits from base).

### 7.3 Strategy ADR

- **May define**: `principles`, `guardrails`, `north_star_metrics`, high-level **options\_considered**.
- **Must not**: include `rollout_backout` or service-specific `decision_details`.
- **Ownership**: **Do not** redefine `owners`; optionally use `owners_ptr: ADR-XXXX`.
- **Lint**: `ADR-SCHEMA-021` (E) if `rollout_backout` is present.

<!-- PROPOSED:start -->
### 7.4 Style-guide ADR

- **Purpose:** Define repository-wide ADR rules.  
- **Exemptions**:
  - Not part of the link graph (**LINK-2xx exempt**).
  - RFC-2119 usage outside normative sections is allowed (**NORM-101 exempt**).
- **Linter**:
  - Exempt from canonical section-order enforcement (**SCHEMA-003 exempt**).
  - Still requires valid front-matter (**SCHEMA-001/002/005** apply).

### 7.5 Template ADRs (scaffolds)

- Identify with front-matter: `class: template` and `template_of` (→ **TPL-700**).
- Filenames SHOULD include `-template-` for discoverability. (→ **TPL-702**).
- Purpose: teaching/scaffolding; not part of the decision link graph (**LINK-2xx exempt**, enforced by **TPL-703**).
- Must:
  - Mirror the section keys & order of `template_of` (see §4 → **SCHEMA-003**; advisory **TPL-705**); `status: Proposed` (→ **TPL-701**).
- May: 
  - Use `<angle-bracket>` placeholders; RFC-2119 tokens are allowed **only** inside code fences/inline code (→ **TPL-704**).
- Must not: 
  - Set `extends` or `supersedes` (keep `null`, → **TPL-703**); must not redefine owners; must not add class-forbidden sections (e.g., `rollout_backout` for strategy → **SCHEMA-021**).
- Optional pointers: owners_ptr for discoverability (do not embed concrete owners in strategy/delta templates).
<!-- PROPOSED:end -->

---

## §8. Pointers & deltas (inheritance rules)

- Pin base ADR + version: `extends: ADR-0001@YYYY-MM-DD` or `@<7–40 lowercase hex>`.
- **Precedence (child over base)**:

  1. `overrides.<key>` (replace)
  2. `not_applicable.<key>` (disable with reason)
  3. `adds.<key>` (new, child-only)
  4. `ptr → ADR-0001#<key>` (inherit as-is)
  
- Each delta must include a **diff summary**.
- **Strict pin format**: see §10.2.

---

## §9. ADR-PROC vs ADR-SCHEMA (STRICT-PROCEED-LOG-ONCE)

**Purpose.** Separate minor, presentation-only tensions (PROC) from structural/governance violations (SCHEMA) so work can proceed without bikeshedding or LLM paralysis.

**Principle.** If a check fails but does **not** change meaning or safety, tools/reviewers **SHOULD proceed**, emit one structured log line, and **MUST NOT** block.

**ADR Log Location + File Pattern. ("ADR-LOG")** `docs/adr-new/.adr/` + `<YYYY-MM-DD>.jsonl`

### What belongs where

| Category | Examples | Codes (default severity) |
|---|---|---|
| **PROC (style/presentation; proceed + log)** | Title style (missing initial capital, trailing period); template filename missing `-template-`; non-normative prose drift; optional metadata using `null` vs `""` where both are allowed | `ADR-PROC-241` (**I**) |
| **PROC escalation (pattern neglect)** | ≥3 PROC-241 events for the same file/code in 30 days (tracked in ADR-LOG) | `ADR-PROC-242` (**E**) |
| **PROC shape pattern matching** | New shape/enum/event names that exact-match or prefix-match entries in owner ADR | `ADR-PROC-242` (**I**) |
| **PROC telemetry health** | Missing or stale run logs in ADR-LOG (older than 7 days) | `ADR-PROC-250` (**E**) |
| **SCHEMA (structure/governance; block)** | Canonical key markers missing/out of order; class/status/ID/date format violations; owners redefined where forbidden; invalid/missing `extends@pin`; broken supersede reciprocity | `ADR-SCHEMA-001/002/003/004/005/012/021` (all **E**); `ADR-LINK-200/201/203/204/221` (all **E**) |

> **Note:** Date format errors are **SCHEMA** (`ADR-SCHEMA-005`), not PROC.

### Non-normative prose drift (PROC-241)

Treat a change as **PROC-241** if **all** are true:

1. Diff touches only **non-normative** sections.  
2. No additions/removals of RFC-2119 tokens.  
3. No edits to numbers/units adjacent to RFC terms.  
4. No edits to front-matter schema/link keys (`id,class,status,date,review_by,owners,owners_ptr,extends,supersedes,superseded_by`).  
5. No edits to canonical key marker **order**.

If any fail, evaluate under standard **SCHEMA/LINK/NORM** rules.

### Lint codes

- `ADR-PROC-241` (**I**) — Minor style deviation; proceeded & logged.  
  *Intent*: avoid bikeshedding; permit forward progress.
- `ADR-PROC-242` (**E**) — ≥3 of the same specific violation type in the same file in 30 days 
  *Intent*: curb pattern neglect without blocking one-offs.
- `ADR-PROC-243` (**I**): Possible duplication of existing pattern.
  *Intent*: nudge the author that there may be exact-match or prefix-match existing in an owner ADR without referencing it.
- `ADR-PROC-250` (**E**) — Run logs stale/missing under ADR LOG.


### LLM guidance

- **PROC**: Canonicalize formatting (title case, fence languages, link text) **without changing semantics**. **Do not** introduce RFC-2119 language or adjust numbers/units.  
- **SCHEMA**: Structural/governance issues **MUST** block and **MUST NOT** be auto-resolved by the model.

### Implementation notes (linter)

- Provide a CLI toggle to escalate: `--proc-250-as-error`.  
- Record `{code,file,violation_type,date}` events in ADR-LOG`; compute rolling 30-day counts for PROC-242.  
- Classify date-format violations strictly under `ADR-SCHEMA-005` (never PROC).


---

## §10. Links, pins & inheritance checks

### 10.1 Bi-directional links

- `supersedes: ADR-XXXX@ver` **requires** reciprocal `superseded_by` on the target.
- **Lint**: `ADR-LINK-200` (E) missing reciprocal link.

### 10.2 Pinned `extends` (allowed format)

- Allowed: `ADR-####@YYYY-MM-DD` **or** `ADR-####@<7–40 lowercase hex>`.
- **Regex**: `^ADR-\d{4}@(20\d{2}-\d{2}-\d{2}|[0-9a-f]{7,40})$`
- **Lint**: `ADR-LINK-201` (E) missing pin; `ADR-LINK-203` (E) bad format.

### 10.3 Pointers

- **Warn**: `ADR-LINK-202` (W) pointer to missing section key in base (probable rename).

### 10.4 Supersede closure map

- **Info**: `ADR-LINK-220` closure: multiple descendants; add rationale.
- **Error**: `ADR-LINK-221` cycle detected.
- **Warn**: `ADR-LINK-222` fork without rationale.

<!-- PROPOSED:start -->
### 10.5 Template exemptions

When **class is `template`** or `template: true`:

- Do not enforce pinning for extends or bi-directional supersedes links (keep them null in templates).
- Do not require numeric thresholds/units; placeholders are allowed.
- Do not require delta-only constraints (e.g., diff_summary).
- Still enforce valid front-matter shape and the class ↔ template_of relationship, and forbid class-forbidden sections (e.g., strategy + rollout_backout).
- RFC-2119 tokens are permitted only inside inline code or fenced code examples.
<!-- PROPOSED:end -->

---

## §11. Normative language safety (RFC-2119)

**Detection scope.** RFC-2119 keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, SHALL, SHALL NOT, MAY, RECOMMENDED, NOT RECOMMENDED) establish binding requirements. Detection is **case-insensitive**; authors SHOULD write these in uppercase.

**Allowed locations (exhaustive):**
1) Canonical sections: `<!-- key: decision_details -->`, `<!-- key: rollout_backout -->`.
2) Requirements subsection: `<!-- key: consequences_and_risks.requirements -->` (single, dotted key).
   - **No other dotted key patterns are permitted for normative content.** Examples that are **not** allowed: `decision_details.requirements`, `consequences_and_risks.musts`, etc.
3) **Delta overrides:** RFC-2119 terms in fenced `yaml` **override blocks** (under `overrides:` in Delta ADRs) **establish modified requirements and are permitted.**

**Scanner behavior.**
- Case-insensitive keyword matching.
- **Ignore:** fenced code blocks (``` ```), inline code (`…`), HTML comments (`<!-- … -->`), **blockquotes (`> …`)**, and URLs.  
  *Rationale:* Code/quotes/excerpts/examples must not accidentally create binding requirements.
- Section recognition: primary via HTML markers; fallback heading aliases:
  - “Decision Details” → `decision_details`
  - “Rollout & Backout” / “Rollout and Backout” → `rollout_backout`
  - “Requirements (normative)” under “Consequences & Risks” → `consequences_and_risks.requirements`
- **Report all violations** in a file (no caps).

**Class interactions.**
- `class: style-guide` — exempt from RFC-2119 scanning (examples permitted).
- `class: template` — RFC terms allowed **only** inside fenced code or inline code; otherwise this section applies.

**Lint codes.**
- `ADR-NORM-101` (E): RFC-2119 keyword outside allowed locations.
- `ADR-NORM-102` (W): Vague term in normative text (e.g., “robust”, “simple”) without numbers/units.

### Implementation Notes (non-normative)

Four primary hooks for linter implementation:

1. **Section detection:** Parse HTML markers (`<!-- key: ... -->`) and maintain fallback heading aliases. Dotted keys require exact string matching (`consequences_and_risks.requirements`).

2. **Content filtering:** Skip scanning within fenced blocks, inline code, HTML comments, blockquotes, and URL patterns before applying RFC-2119 regex.

3. **Class-aware routing:** Apply exemptions for `style-guide` (full skip) and `template` (code-fence-only allowance) before normative scanning.

4. **YAML override recognition:** Identify fenced `yaml` blocks containing `overrides:` keys in Delta ADRs; permit RFC-2119 terms within those blocks.

---

## §12. LLM tail (machine context, optional)

Add a final fenced JSON block (delimited by HTML comments) to help tools/LLMs load context.

<!-- llm_tail:begin -->
```json
{
  "id": "ADR-0123",
  "class": "delta",
  "status": "Accepted",
  "extends": "ADR-0120@2025-03-14",
  "owners_ptr": "ADR-0120"
}
```
<!-- llm_tail:end -->

> When present, it must mirror front-matter for: id, class, status, extends, and ownership (owners[] or owners_ptr).

- **Info**: `ADR-META-150` missing (optional).  
- **Warn**: `ADR-META-151` tail disagrees with front-matter for: `id`, `class`, `status`, `extends`, `owners` (or `effective_owner`).

---

## §13. CI Contract

CI blocks on all codes marked (E) in §14 and warns on codes marked (W).

Override via: `--fail-on W` to change threshold.

---

## §14 Linter Rules Reference

**Version**: 0.1.6
**Severity legend**: E=block merge · W=proceed+annotate · I=log only

### Code Bands

| Band | Range | Purpose |
| ---- | ----- | ------- |
| `ADR-SCHEMA-###` | 001–099 | Front-matter & structure     |
| `ADR-NORM-###`   | 100–149 | Normative language rules     |
| `ADR-META-###`   | 150–169 | LLM tail & meta consistency  |
| `ADR-LINK-###`   | 200–239 | Links, pointers, inheritance |
| `ADR-PROC-###`   | 240–269 | Process & auto-resolve       |
| `ADR-DELTA-###`  | 300–339 | Delta/extends semantics      |

### Blocking Set

**Blocks CI**: 

- `ADR-DELTA-300`
- `ADR-LINK-200/201/203/204/221`
- `ADR-NORM-101`
- `ADR-SCHEMA-001/002/003/004/005/011/012/021`
- `ADR-TEMPLATE-700/703`

**Warns**: 

- `ADR-LINK-202/222`
- `ADR-META-151`  
- `ADR-NORM-102`
- `ADR-PROC-242`
- `ADR-TEMPLATE-701/702/705`

**Info**: 

- `ADR-LINK-220`
- `ADR-META-150`
- `ADR-PROC-241`

### Rules (abbrev.)

#### ADR-DELTA

Description: Inheritance and override semantics for class: `delta` (targets exist, not_applicable/overrides/adds sanity).

- **ADR-DELTA-300 (E)**: Override targets non-existent key in base.

#### ADR-LINK

Description: Cross-ADR graph properties (pins, reciprocity, cycles).

- **ADR-LINK-200 (E)**: `supersedes` without reciprocal `superseded_by`.
- **ADR-LINK-201 (E)**: `extends` missing base or version pin.
- **ADR-LINK-202 (W)**: Pointer to section key missing in base.
- **ADR-LINK-203 (E)**: Invalid `extends` pin format (must be `@YYYY-MM-DD` or lowercase hex `@[0-9a-f]{7,40}`).
- **ADR-LINK-204 (E)**: Pointer to normative section key missing in base.
- **ADR-LINK-205 (E)**: Missing references to governing ADRs. Escalates to (E) when clear dependency exists. 
- **ADR-LINK-220 (I)**: Supersede closure: multiple descendants (informational).
- **ADR-LINK-221 (E)**: Supersede closure: cycle detected.
- **ADR-LINK-222 (W)**: Supersede closure: fork without rationale in `change_history`.

#### ADR-META

- **ADR-META-150 (I)**: `llm_tail` missing (optional).
- **ADR-META-151 (W)**: `llm_tail` disagrees with front-matter on required keys.

#### ADR-NORM

Description: Language-level misuse (RFC-2119 outside normative sections; vague terms in normative text).

- **ADR-NORM-101 (E)**: RFC-2119 keyword outside normative sections.
- **ADR-NORM-102 (W)**: Vague term in normative section.

#### ADR-PROC

Description: Process/telemetry/auto-resolve.

- **ADR-PROC-241 (I)**: Minor style deviation; proceeded and logged.
- **ADR-PROC-242 (E)**: Repeated minor deviation (≥3 in 30d).
- **ADR-PROC-243 (I)**: Possible duplication of existing pattern (exact/prefix name match without reference).
- **ADR-PROC-250 (E)**: Linter run logs stale/missing in ADR linter logs directory.

#### ADR-SCHEMA

Description: Front-matter and class structure constraints that don’t require link graph or prose analysis (e.g., required keys, date formats, class-specific allows/forbids).

- **ADR-SCHEMA-001 (E)**: Missing required metadata (`id,title,status,class,date,review_by`) or bad `id`.
- **ADR-SCHEMA-002 (E)**: Invalid class (`owner|delta|strategy|style-guide|template`).
- **ADR-SCHEMA-003 (E)**: Canonical section keys missing or out of order.
- **ADR-SCHEMA-004 (E)**: Invalid status transition or illegal class change.
- **ADR-SCHEMA-005 (E)**: Invalid date format (must be `YYYY-MM-DD`) for `date` or `review_by`.
- **ADR-SCHEMA-011 (E)**: Owner ADR must not use `extends`.
- **ADR-SCHEMA-012 (E)**: Non-Owner ADRs must never use `owner`.
- **ADR-SCHEMA-013 (E)**: Non-Owner ADRs must identify ADR ownership
- **ADR-SCHEMA-021 (E)**: Strategy ADR contains `rollout_backout` (by marker **or** heading `Rollout & Backout`).

#### ADR-TEMPLATE

- **ADR-TEMPLATE-700 (E)**: `template_of` missing or invalid (`owner|delta|strategy|style-guide|template`).
- **ADR-TEMPLATE-701 (W)**: `status` not `Proposed` in a template ADR.
- **ADR-TEMPLATE-702 (W)**: filename does not include `-template-` (discoverability).
- **ADR-TEMPLATE-703 (E)**: template participates in link graph (`extends` or `supersedes` non-null).
- **ADR-TEMPLATE-704 (W)**: RFC-2119 keyword outside code fences/inline code in template.
- **ADR-TEMPLATE-705 (W)**: template does not mirror canonical section order of `template_of` (same keys, same order).

Notes:

> TPL-704 gives you a gentle guardrail for examples that accidentally leak MUST/SHOULD outside code fences in templates (consistent with your §7.5 and §10.5 language).
> TPL-705 is a soft wrapper around SCHEMA-003 so reviewers can see “it failed because it’s a template not mirroring the base,” while SCHEMA-003 remains the hard rule that enforces order. You can omit 705 if you prefer only the hard fail.

### STRICT-PROCEED (Auto-resolve) Policy

**Qualifies**:

- typos/casing/punctuation
- non-normative prose drift
- optional `adds.*` omissions
- link text style when URL resolves

**Does NOT qualify (block)**:

- thresholds/units/SLOs
- any RFC-2119 misuse
  - any RFC-2119 misuse (including templates outside fenced/inline code)
- canonical keys order/missing
- lifecycle/status/class flips
- ownership changes in non-owner docs
- `extends` pin issues
- bi-directional link issues
- **normative** missing pointer

### Section Recognition

- Primary: HTML markers `<!-- key: … -->`.
- Secondary (fallback): Markdown headings mapped to keys (aliases)
  - `Rollout & Backout` → `rollout_backout`
  - `Decision (one-liner)` → `decision_one_liner`
  - `Context & Drivers`, `Decision Details`, `Options Considered`, `Consequences & Risks`, `Implementation Notes`, `Evidence & Links`, `Glossary`, `Related ADRs`, plus strategy-only `Principles`, `Guardrails`, `North Star Metrics`.

### Regexes (core)

- **RFC-2119**: 
  - built from list `{"MUST", "MUST NOT", …}`
  - scanned outside normative sections and outside code fences/inline code
- **Extends pin**: 
  - `^ADR-\d{4}@(20\d{2}-\d{2}-\d{2}|[0-9a-f]{7,40})$` *(lowercase hex required)*
- **LLM tail capture**: 
  - HTML delimited block with fenced ```json```; DOTALL; tolerant to CRLF.

### Telemetry

- File: `.adr/lint_metrics.json` (repo root)
- Stores timestamps per `{code, file}` to auto-escalate minor deviations to warnings when ≥3 in 30 days

### Typical Fixes

- **ADR-SCHEMA-003**: Add missing `<!-- key: … -->` markers in canonical order.
- **ADR-SCHEMA-021**: Remove `## Rollout & Backout` from strategy (or convert doc class).
- **ADR-NORM-101**: Move RFC-2119 phrasing into a normative section or de-normativize the wording.
- **ADR-LINK-203**: Pin `extends` as `ADR-0001@2025-03-14` or `ADR-0001@deadbeef`.

## CI Entry (example)

```yaml
- name: Run ADR linter
  run: python tools/adr_linter.py --fail-on E
```

## §15. PR & review checklist

- [ ] One decision per ADR; clear status & one-liner  
- [ ] Options table with explicit rejections  
- [ ] Numeric thresholds/units where applicable  
- [ ] Consequences/risks & reversibility  
- [ ] Rollout & **backout** (Owner/Delta only)  
- [ ] Evidence links (permalinks)  
- [ ] `review_by` and revisit triggers  
- [ ] Deltas: `extends@pin`, `diff_summary`, scoped `applies_to`  
- [ ] Cross-links: `supersedes`/`superseded_by` bi-directional  
- [ ] Non-normative sections contain **no** RFC-2119 keywords  
- [ ] Minor tensions auto-resolved & logged (PROC-241/242)  
- [ ] (Optional) LLM tail present & consistent (META-151 warns on drift)

## §16. Canonical Skeleton (for linter & discoverability)

(You can keep the canonical skeleton if you like; it won’t hurt, but it’s no longer required for class `style-guide`.)

<!-- key: decision_one_liner -->
Define the structure and linting rules for ADRs across this repo.

<!-- key: context_and_drivers -->
We want ADRs that are human-skim friendly and machine-enforceable; this style guide standardizes both.

<!-- key: options_considered -->
Centralized style guide vs. ad-hoc per ADR; linter-enforced vs. best-effort review.

<!-- key: decision_details -->
All ADRs **MUST** include canonical section markers in the order defined in §4.  
Strategy ADRs **MUST NOT** include `rollout_backout`.  
Delta ADRs **MUST** pin `extends` and **MUST NOT** redefine `owners`.

<!-- key: consequences_and_risks -->
Stricter CI may add review friction; mitigations: auto-resolve minor issues and clear lint messaging.

<!-- key: rollout_backout -->
**Rollout**: adopt the linter in CI; fix violations incrementally.  
**Backout**: temporarily disable specific codes via CI allow-list; no runtime impact.

<!-- key: implementation_notes -->
Tooling lives in `tools/adr_linter.py`; reserved code bands and regexes in §15.

<!-- key: evidence_and_links -->
- RFC 2119 — Key words for use in RFCs to Indicate Requirement Levels

<!-- key: glossary -->
**Normative**: text that sets requirements; **Delta**: ADR that modifies a base ADR by pin.

<!-- key: related_adrs -->
ADR-0002 (Template: Owner), ADR-0003 (Template: Delta), ADR-0004 (Template: Strategy)

## §17. Enhancement Registry

### Implementation Notes

- Use existing `adr_check_code_consistency.py` framework
- Leverage `anchor_snapshot.py` comment detection where possible

### ADR Improvements (in order)

(empty)

### Linter Improvements (in order)

#### High Priority

- **Class Validation Completeness Check** - Parse ADR §7 class rules, verify linter implements each requirement, flag bypassed validation (would have caught template bug)

#### Medium Priority  

- **Comment-Based Technical Debt Scanner** - Auto-detect "TOREVIEW", "passes incorrectly" patterns
- Expand linter validation to match ADR-0001 §9 specification
  - context: ADR-0001 §9 now defines complete PROC/SCHEMA boundary but linter only implements title format checking
  - tasks:
    - Implement prose drift detection (5-point heuristic)
    - Add template filename convention checking
    - Build governance reference validation (LINK-205)
    - Add pattern duplication detection (PROC-245)
    - Expand PROC-241 beyond title checking    

#### Deferred

- **Spec-Implementation Gap Analysis** - Cross-reference all ADR requirements with code

### pytest Improvements (in order)

#### High Priority

(empty)

#### Medium Priority

- Add test cases for new PROC/LINK validation rules
  - dependency "Expand linter validation to match ADR-0001 §9 specification"
  - tasks:
    - Test prose drift heuristic edge cases
    - Test PROC-242 escalation timing
    - Test LINK-205 conditional escalation
    - Test PROC-245 pattern matching

#### Deferred

(empty)

<!-- llm_tail:begin -->
```json
{
  "id": "ADR-0001",
  "class": "style-guide",
  "status": "Proposed",
  "extends": null,
  "owners_ptr": "ADR-0001"
}
```
<!-- llm_tail:end -->
