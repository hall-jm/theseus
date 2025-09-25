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
| **Version**:           | 0.2.0                                   |
| **Status**:            | Proposed                                |
| **Date**:              | 2025-09-21                              |
| **Applies to Schema**: | 0.1.0                                   |
| **Related**:           | ADR-0002 (Template: Base/Owner), ADR-0003 (Template: Delta), ADR-0004 (Template: Strategy) |

### Changelog

| Version | Date         | Notes                                        |
| ------- | ------------ | -------------------------------------------- |
| 0.2.0   | 21 Sept 2025 | Created new `governance` class of ADRs; added new requirements for ADR-SCHEMA-003 to handle, ADR-TEMPLATE-706 to be a catch-all error code for when explicit ADR formatting for a particular section isn't followed; rewrote Section 4 to handle the new `governance` class and create a universal set of keys vs. class-specific set of keys; rewrote Section 0 to handle this ADR's new bootstrap constitution and precedence authority; rewrote sections 0 to 13 in this version; |
| 0.1.7   | 19 Sept 2025 | Changed ADR-TEMPLT-\* -> ADR-TEMPLATE-\* to improve readability; | 
| 0.1.6   | 11 Sept 2025 | Rewrite Section 11 to address gaps in the linter's implementation vs. the spirit of what the ADR is trying to capture for deterministic computer processes; |
| 0.1.5   | 08 Sept 2025 | Created Section 17 to track ADR-0001 enhancements for future development as needed; |
| 0.1.4   | 07 Sept 2025 | Changed wording in Section 13 to avoid documentation and implementation drift between ADR and linter code; |
| 0.1.3   | 06 Sept 2025 | Additional changes to update blocking codes; reviewed material to determine if document is still internally consistent where possible; Removed `deciders` from ADR due to the current state of the project (e.g., eliminate confusion, reduce meta burden for solo person project;)|
| 0.1.2   | 05 Sept 2025 | Additional changes to ensure consistency across ADR regarding `style-guide` and `template` class documentation; |
| 0.1.1   | 05 Sept 2025 | New proposed sections for class `template` documentation in the style guide; |
| 0.1.0   | 03 Sept 2025 | Initial draft of template file               |

## **§0. Constitution & Precedence**

This section explicitly applies to every ADR.

### Authority Model

- **Framework Authority**: Modification of ADR-0001 itself (classes, canonical sections, linter bands); known bootstrap violation as accepted tradeoff to unblock work;  
- **Governance Authority**: Cross-component boundary definition and conflict resolution within declared scope
- **Component Authority**: Decision-making within scope boundaries established by governance
- **Final Authority**: Project Maintainer(s); definition is outside of scope for this ADR
  - LLMs must accept this ambiguity and tension; no remediation was intentionally created for this section's rewriting

### Scope Taxonomy & Precedence

**Domain Scopes** (precedence order for cross-scope conflicts):

1. `cli` - User-facing processes such as user interface, argument parsing, user-facing messages
2. `engine` - Internal pure processes such as orchestration semantics, validator execution, structured response generation, exit code mapping
3. `services` - Impure edge processes such as filesystem operations, network operations, IO failure classification
4. `other` - All other processes not captured in the previous three groups

**Governance Structure**:
- Governance ADRs are defined by:
  - class: `governance`
  - scope: `cli|engine|services|other` (single)
  - supersedes: chain must be linear
  - subscope: future granularity to avoid having a giant `cli` governance ADR forever
- Each domain scope **MUST** have exactly one active governance ADR via linear supersession chain
- Cross-scope conflicts resolved by Domain Scope mapping above
- **Transitional**: ADR-0001 §0 acts as default governance **only until** the first scope-specific Governance ADR for that domain is **Accepted**. Upon acceptance, §0 ceases to govern that scope. *(review_by: 2026-03-01)*

### Constraint Binding Semantics
- `extends`: Content inheritance with delta semantics
- `governed_by`: Authority constraint binding (single)
  - Mandatory for Owner ADRs
  - Delta ADRs inherit governed_by from base unless they narrow scope (then must declare)
  - Strategy ADRs: warn if missing; error if they assert boundaries
- `supersedes`: Decision replacement with reciprocal tracking

### Conflict Resolution Protocol

1. **Same-scope**: Latest superseded governance ADR in linear chain controls
2. **Governance mapping**:  If the governance names a specific topic (e.g., “exit codes → CLI”), that mapping overrides the generic order. Then fall back to **Cross-scope** 
3. **Cross-scope**: Apply domain precedence (cli > engine > services)  
4. **Interface classification**: User-facing → cli; orchestration → engine; IO → services
  - Interface classification edge cases can be handled as exceptions after the core framework works; we need working governance now
5. **Unmapped conflicts**: **ERROR** - work blocks until governance adjudication
  - Create/land a governance ADR in the relevant scope that adjudicates the topic
  - Reference the two conflicting ADRs in `change_history`;

**Machine Constraints**: Governance ADRs use fenced `yaml` blocks as the **sole binding authority**. Prose provides context and rationale but is explicitly non-binding.

**Constraint Enforcement**: Linters and automated tools MUST treat constraint blocks as the authoritative source. Governance prose MUST NOT use RFC-2119 keywords.
 
### Default Behavior

When in doubt for any governance scenario not covered here, HARD FAIL for maximum smoke detection.
When in conflict with later sections regarding process behavior, HARD FAIL for maximum smoke detection.

## §1. Goals & Scope

- **Decisions** are atomic (one decision per ADR), auditable (front-matter + `change_history`), and rollback / backout plan (Owner/Delta ADRs).
- **Authority relationships** are explicit and machine-checkable via required keys:
  - `governed_by` (Owner: REQUIRED; Delta: inherited; Strategy: OPTIONAL).
- **Governance constraints** are enforced to prevent drift; missing or invalid bindings are blocking errors.
- Documents are **human-skim friendly** and **machine-readable** through markdown and HTML comment section markers, fenced YAML for constraints, and RFC-2119 limited to normative sections.
- The system supports unambiguous **relationship types**:
  - `extends` (inheritance, uni-di), `supersedes` / `superseded_by` (replacement, bi-di, manual, linter enforced reciprocity), `governed_by` (authority binding, uni-di), `owners_ptr` (ownership reference), and `informs` / `informed_by` (strategy ownership, bi-di, manual, linter enforced reciprocity).

---

## §2. Canonical file layout & naming

- Folders:
  - `docs/adrs/`: home directory for Theseus ADRs
- ID: `ADR-XXXX` (zero-padded; monotonic; never reuse)  
- Filename: `ADR-XXXX-short-kebab-title.md`  
- Commit prefix: `[ADR-XXXX] <title>`

### Future Enhancements
- Consider ID range allocation for systematic class organization
- Evaluate folder structure for governance vs component ADR separation
- Review filename conventions for improved discoverability

---

## §3. Required metadata (YAML front-matter)

The format for these values MUST only be defined in section 8

```yaml
id: ADR-0123
title: Short imperative title
status: Proposed | Accepted | Deprecated | Superseded
class: owner | delta | strategy | style-guide | template | governance
owners: [Project Maintainer]
owners_ptr: ADR-0120           # Non-Owner ADRs must reference ownership
extends: null                  # or ADR-<id>@<pin> (see §8)
supersedes: null               # or ADR-<id>@<pin> (see §8)
superseded_by: null            # or ADR-<id>@<pin> (see §8)
governed_by: null              # or ADR-<id>@<pin> (see §8)
informs: null                  # or ADR-<id>@<pin> (see §8)(strategy → owner)
informed_by: null              # or ADR-<id>@<pin> (see §8)
scope: null                    # cli|engine|services|other (required for governance)
date: 2025-09-03
review_by: 2026-03-03
applies_to: []                 # narrow for deltas
tags: [topic]
change_history: []
template_of: null              # owner|delta|strategy|style-guide|governance (templates)
```

### **Class-Specific Field Requirements**

**Owner ADRs**:
- **REQUIRED**: `governed_by` (1-to-1; authority constraint binding)
- **FORBIDDEN**: `extends`, `owners_ptr`
- **OPTIONAL**: `informed_by` (list; if referenced by strategies)

**Governance ADRs**:
- **REQUIRED**: `scope` (cli|engine|services|other)
- **FORBIDDEN**: `extends`, `owners_ptr`, `governed_by`, `informs`

**Strategy ADRs**:
- **REQUIRED**: `owners_ptr` (1-to-1)
- **FORBIDDEN**: `owners`, `scope`
- **OPTIONAL**: `governed_by` (1-to-1), `informs` (list; strategy → owner relationship)

**Delta ADRs**:
- **REQUIRED**: `extends` (1-to-1), `owners_ptr` (1-to-1)
- **FORBIDDEN**: `owners`, `scope`
- **INHERITED**: `governed_by` (1-to-1; from base ADR unless narrowed)

**Template ADRs**:
- **REQUIRED**: `template_of` (1-to-many)
- **FORBIDDEN**: `extends`, `supersedes`, `governed_by`, `scope`

### **Relationship Field Validation**

**Pin Format**: All relationship fields using `@pin` must follow format:
- `ADR-####@YYYY-MM-DD` or `ADR-####@<7-40 lowercase hex>`

**Reciprocal Relationships**:
- `supersedes` ↔ `superseded_by` (bi-directional, manually maintained, linter enforced reciprocity)
- `informs` ↔ `informed_by` (bi-directional, manually maintained, linter enforced reciprocity)

**Unidirectional Bindings**:
- `governed_by` (authority constraint, no reciprocal)
- `extends` (content inheritance, no reciprocal)

### **Validation Rules**

TODO: Once the Linter Rules are reviewed, updated, and consolidated, delete this "Validation Rules" section to avoid redundant sections

This metadata schema supports governance implementation while maintaining class-specific constraints and relationship validation.

- **ADR-SCHEMA-006 (E)**: Governance ADR missing required `scope` field
- **ADR-SCHEMA-007 (E)**: Owner ADR missing required `governed_by` field  
- **ADR-SCHEMA-008 (E)**: Invalid `scope` value (must be cli|engine|services|other)
- **ADR-SCHEMA-009 (E)**: Class-forbidden field present (e.g., governance with `extends`)
- **ADR-SCHEMA-010 (E)**: Duplicate governance scope among active ADRs

### Notes 

When `class: template`:

- `template_of` is REQUIRED and must be one of: `owner|delta|governance|strategy|style-guide`.
- `status` MUST be `Proposed`.
- `extends` and `supersedes` MUST be `null`.
- Filenames SHOULD include `-template-` for discoverability.
- Placeholders (e.g., `<driver>`, `<YYYY-MM-DD>`) are allowed where real values would appear.

TOREVIEW: the following `>` line for consistencies with later sections covering the `template` class.

> This mirrors TPL-700/701/702/703 and prevents drift between §3 and §7.5/§10.5/§14.

---

## §4. Canonical section keys & order

Use these **exact keys** (stable for tooling). Headings can be pretty; keys must map 1:1.

### Universal Sections (all classes)

All ADR classes **MUST** include these sections in this order:

#### Opening Sections (in order)

- `decision_one_liner`
- `context_and_drivers`  
- `options_considered`
- `decision_details`

#### Class-Specific Sections

- **[Class-specific sections inserted here]**

#### Closing Sections (in order)

- `evidence_and_links`
- `glossary`
- `related_adrs`
- `license`

### Class-Specific Section Insertions

**After `decision_details`, insert the following sections based on class:**

#### Owner

- `consequences_and_risks`
- `implementation_notes`
- `rollout_backout`

#### Governance

- `authority_scope`
- `constraint_rules`
- `precedence_mappings`
- `adoption_and_enforcement`

#### Strategy  

- `principles`
- `guardrails`
- `consequences_and_risks`
- `implementation_notes`
- `north_star_metrics`

#### Delta

Uses base ADR sections (inherited via `extends`)

#### Template

- Templates inherit the skeleton of the class they scaffold (template_of).
- They MUST contain placeholders (e.g., <driver>, <YYYY-MM-DD>) instead of real values.

> Strategy templates MUST NOT introduce rollout_backout (see §7.3).

#### Style-Guide

Based on its nature as a bootstrapping class, style guides are exempt from canonical section keys and ordering.

### Complete Section Orders by Class

**Owner**: `decision_one_liner`, `context_and_drivers`, `options_considered`, `decision_details`, `consequences_and_risks`, `implementation_notes`, `rollout_backout`, `evidence_and_links`, `glossary`, `related_adrs`, `license`

**Governance**: `decision_one_liner`, `context_and_drivers`, `options_considered`, `decision_details`, `authority_scope`, `constraint_rules`, `precedence_mappings`, `adoption_and_enforcement`, `evidence_and_links`, `glossary`, `related_adrs`, `license`

**Strategy**: `decision_one_liner`, `context_and_drivers`, `options_considered`, `decision_details`, `principles`, `guardrails`, `consequences_and_risks`, `implementation_notes`, `north_star_metrics`,  `evidence_and_links`, `glossary`, `related_adrs`, `license`

This structure maintains universal LLM navigation while allowing semantic differentiation where classes need distinct content types. The governance class gets its constraint-specific sections without forcing inappropriate sections like `rollout_backout`.

### Reminders

> Some classes restrict which keys may appear—see §7 (class rules).

---

## §5 Writing Standards

### Universal Writing Principles

- **Active voice**, short sentences (≤20 words).
- Define acronyms once; keep a mini-glossary.
- Avoid unclear pronouns; repeat the noun.
- Prefer **numbers & units** over adjectives (e.g., "p95 ≤ 150 ms").

### Class-Specific Content Standards

#### Owner & Delta ADRs

- Use **RFC-2119** keywords for binding requirements in Owner sections, `decision_details` and `rollout_backout` (and by Delta ADR if inheriting from an ADR with those sections).
- Include specific thresholds, SLOs, and measurable criteria.
- Provide concrete implementation guidance with rollback procedures.

#### Governance ADRs

**RFC-2119 FORBIDDEN** in prose sections - emit ADR-NORM-101 (E) if detected  
**Machine-readable constraint blocks** provide sole binding authority in `constraint_rules`
Prose provides context, rationale, and examples but establishes no binding requirements
Authority boundaries defined exclusively through constraint block mappings

**Governance Constraint Schema**:

- `REQUIRED: [list]` - Topics that MUST be handled by this scope
- `FORBIDDEN: [list]` - Topics that MUST NOT be handled by this scope  
- `OWNED_BY: [{topic, owner}]` - Explicit topic ownership assignments

**Schema Validation Rules**:

- Topics use dot notation hierarchy (e.g., "engine.exit_code_mapping")
- Owner values must match valid scope domains: cli|engine|services|other
- REQUIRED/FORBIDDEN lists cannot contain overlapping topics
- OWNED_BY topic must not appear in scope's REQUIRED/FORBIDDEN lists

**Example**:

```yaml
constraint_rules:
  REQUIRED: [ "cli.argument_parsing", "cli.user_messages" ]
  FORBIDDEN: [ "engine.orchestration", "services.file_io" ]
  OWNED_BY:
    - topic: "shared.exit_code_mapping"  
      owner: "engine"
```

#### Strategy ADRs

- Use **RFC-2119** keywords in `principles` and `guardrails` sections for binding strategic constraints.
- Focus on direction without implementation specifics.
- Metrics in `north_star_metrics` MUST be measurable.

#### Template ADRs

- **RFC-2119 keywords allowed only in fenced code examples**.
- Use `<angle-bracket>` placeholders for variable content.

### Default Behavior

Anything not clearly identified in this section that requires deterministic binary outputs MUST use RFC-2119 keywords in written documentation.
The RFC-2119 keywords provide unambiguous authority signals that enable clear LLM decision-making across all classes.

---

## §6. Options rubric

### Universal Evaluation Criteria

Score 1–5 (higher is better) and explain trade-offs for all ADR classes:

| Option | Fit to Drivers | Complexity | Risk | Reversibility | Notes |
| ------ | -------------- | ---------- | ---- | ------------- | ----- |

Include **"Rejected because …"** bullets for each non-chosen option.

### Class-Specific Evaluation Criteria

#### Owner & Delta ADRs

Additional columns for implementation decisions:

| Option | Performance Impact | Operational Burden | Integration Cost | Rollback Complexity | Notes |
| ------ | ------------------ | ------------------ | ---------------- | ------------------- | ----- |

**Focus**: Technical feasibility, operational impact, measurable outcomes.

#### Governance ADRs 
 
Authority allocation evaluation:

| Option | Authority Clarity | Enforcement Feasibility | Cross-Component Impact | Precedence Consistency | Conflict Resolution | Notes |
| ------ | ----------------- | ----------------------- | ---------------------- | ---------------------- | ------------------- | ----- |

**Scoring Guidelines**:
- **Authority Clarity**: How clearly the option defines ownership boundaries (5 = unambiguous, 1 = overlapping/unclear)
- **Enforcement Feasibility**: How easily constraints can be validated by linters/tools (5 = machine-checkable, 1 = manual judgment)
- **Cross-Component Impact**: Scope of components affected by authority decision (5 = minimal disruption, 1 = widespread changes)
- **Precedence Consistency**: Alignment with existing governance hierarchy (5 = consistent, 1 = creates conflicts)

#### Strategy ADRs

Direction and principle evaluation:

| Option | Strategic Alignment | Measurability | Adoption Feasibility | Long-term Sustainability | Market/Technical Fit | Notes |
| ------ | ------------------- | ------------- | -------------------- | ------------------------ | -------------------- | ----- |

**Focus**: Strategic direction, principle clarity, measurement capability.

### Constraint Validation (Governance Only)

Governance options MUST include constraint enforceability assessment:

- Can the authority boundary be expressed in machine-readable constraints?
- Are there clear escalation paths for violations?
- Does the option create enforceable precedence rules?

---

## **§7. ADR classes (what each may/may not contain)**

Add to front-matter: `class: owner | delta | strategy | style-guide | template | governance`.

TODO: Once the Linter Rules are reviewed, updated, and consolidated, delete any **Lint** or Linter related
      lines in the following sessions

### 7.1 Owner ADR

- **May define**: Component boundaries, implementation decisions, technical specifications within declared scope.
- **Must**: Include `governed_by` (authority constraint binding).
- **Must not**: Use `extends` (it is the root); use `owners_ptr` (it defines ownership).
- **Sections**: See §4 for ADR sections specification
- **Lint**: ADR-SCHEMA-007 (E) if missing `governed_by`; ADR-SCHEMA-011 (E) if uses `extends`.

### 7.2 Delta ADR

- **Must**: Use `extends@pin` (pin per §8) to reference base ADR; include override blocks (`overrides`, `not_applicable`, `adds`, `ptr`).
- **Must**: Use `owners_ptr` (inherits ownership from base).
- **Must not**: Define `owners` or `scope`.
- **Inheritance**: Inherits `governed_by` from base unless scope is narrowed (then must declare).
- **Sections**: Inherits base ADR sections; uses override blocks for modifications.
- **Lint**: ADR-SCHEMA-012 (E) if defines `owners`; ADR-LINK-201 (E) if missing `extends`.

### 7.3 Strategy ADR

- **May define**: High-level principles, strategic direction, success metrics.
- **Must**: Use `owners_ptr` (references ownership).
- **Must not**: Define `owners`, `scope`, or implementation-specific details.
- **Optional**: `governed_by`, `informs` (strategy → owner relationship).
- **Sections**: See §4 for ADR sections specification
- **Lint**: ADR-SCHEMA-012 (E) if defines `owners`.

### 7.4 Style-guide ADR

- **Purpose**: Define repository-wide ADR rules and standards.
- **Exemptions**: 
  - Not part of link graph (LINK-2xx exempt)
  - RFC-2119 usage outside normative sections allowed (NORM-101 exempt)
  - Canonical section-order enforcement exempt (SCHEMA-003 exempt)
- **Must not**: Use `extends`, `supersedes`, `governed_by`, `scope`.
- **Sections**: See §4 for ADR sections specification

### 7.5 Template ADR

- **Must**: Include `template_of` (owner|delta|strategy|style-guide|governance); use `status: Proposed`.
- **Must**: Mirror section keys and order of `template_of` class.
- **Must not**: Use `extends`, `supersedes`, `governed_by`, `scope`; define `owners`.
- **May**: Use `<angle-bracket>` placeholders; RFC-2119 keywords only in fenced code examples.
- **Exemptions**: Link graph participation (LINK-2xx exempt via TPL-703).
- **Lint**: TPL-700 (E) if missing `template_of`; TPL-703 (E) if participates in link graph.

### 7.6 Governance ADR

- **Must**: Include `scope` (cli|engine|services|other); define authority boundaries within declared scope.
- **Must**: Use machine-readable constraint blocks as sole binding authority source (see §5 for syntax specification).
- **Must not**: Use `extends`, `owners_ptr`, `governed_by`, `informs`; use RFC-2119 in prose sections.
- **May**: Use `informed_by` (receives strategic direction).
- **Constraint**: Only one active governance ADR per scope (linear supersession required).
- **Sections**: See §4 for ADR sections specification
- **Lint**: ADR-SCHEMA-006 (E) if missing `scope`; ADR-NORM-101 (E) if RFC-2119 in prose; ADR-SCHEMA-010 (E) if duplicate scope.

### Cross-Class Validation

- **Relationship consistency**: `informs` requires reciprocal `informed_by` manual entry.
- **Authority inheritance**: Delta ADRs inherit `governed_by` from base unless scope narrowed.
- **Scope uniqueness**: Only one active governance ADR per scope domain.

---

## §8. Pointers & Deltas (inheritance rules)

### Pin Format Specification

All relationship fields using `@pin` must follow this format:
- `ADR-####@YYYY-MM-DD` or `ADR-####@<7-40 lowercase hex>`
- **Regex**: `^ADR-\d{4}@(20\d{2}-\d{2}-\d{2}|[0-9a-f]{7,40})$`

**Applies to**: `extends`, `supersedes`, `superseded_by`, `governed_by`, `informs`, `informed_by`

### Delta Inheritance Rules

- **Precedence (child over base)**:
  1. `overrides.<key>` (replace base content)
  2. `not_applicable.<key>` (disable with reason)  
  3. `adds.<key>` (new, child-only content)
  4. `ptr → ADR-####@pin#<key>` (inherit as-is)

### Relationship Inheritance (Delta ADRs)

- **Content inheritance**: `extends` creates content inheritance via delta rules above
- **Authority inheritance**: `governed_by` inherited from base unless delta narrows scope (then must declare)
- **Strategic relationships**: `informs`/`informed_by` not inherited (strategy-specific)
- **Replacement relationships**: `supersedes`/`superseded_by` not inherited (document-specific)

### Requirements

- Each delta must include a **diff summary**
- Delta ADRs can be a base for other deltas, but can only extend or inherit from that Delta's canonical keys (only explicit inheritance chains)

---

## §9. ADR-PROC vs ADR-SCHEMA (STRICT-PROCEED-LOG-ONCE)

**Purpose.** Separate minor, presentation-only tensions (PROC) from structural/governance violations (SCHEMA) so work can proceed without bikeshedding or LLM paralysis.

**Principle.** If a check fails but does **not** change meaning or safety, tools/reviewers **SHOULD proceed**, emit one structured log line, and **MUST NOT** block.

**ADR Log Location + File Pattern. ("ADR-LOG")** `logs/.adr/` + `<YYYY-MM-DD>.jsonl`

### What belongs where

| Category | Examples | Codes (default severity) |
|---|---|---|
| **PROC (style/presentation; proceed + log)** | Title style (missing initial capital, trailing period); template filename missing `-template-`; non-normative prose drift; optional metadata using `null` vs `""` where both are allowed | `ADR-PROC-241` (**I**) |
| **PROC escalation (pattern neglect)** | ≥3 PROC-241 events for the same file/code in 30 days (tracked in ADR-LOG) | `ADR-PROC-242` (**E**) |
| **PROC shape pattern matching** | New shape/enum/event names that exact-match or prefix-match entries in owner ADR | `ADR-PROC-242` (**I**) |
| **PROC telemetry health** | Missing or stale run logs in ADR-LOG (older than 7 days) | `ADR-PROC-250` (**E**) |
| **SCHEMA (structure/governance; block)** | Canonical key markers missing/out of order; class/status/ID/date format violations; owners redefined where forbidden; invalid/missing `extends`; broken supersede reciprocity | `ADR-SCHEMA-001/002/003/004/005/012/021` (all **E**); `ADR-LINK-200/201/203/204/221` (all **E**) |
| (PROPOSED) **GOV (governance validation; block)** | Constraint syntax violations; scope conflicts; authority mapping errors; governance-specific validation | `ADR-GOV-###` codes (all **E**) |

> **Note:** Date format errors are **SCHEMA** (`ADR-SCHEMA-005`), not PROC.

### Non-normative prose drift (PROC-241)

Treat a change as **PROC-241** if **all** are true:

1. Diff touches only **non-normative** sections.  
2. No additions/removals of RFC-2119 tokens.  
3. No edits to numbers/units adjacent to RFC terms.  
4. No edits to front-matter schema/link keys (`id,class,status,date,review_by,owners,owners_ptr,extends,supersedes,superseded_by,governed_by,informs,informed_by,scope`).
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
- (PROPOSED) **GOV**: Governance constraint and authority issues **MUST** block and **MUST NOT** be auto-resolved by the model.


### Implementation notes (linter)

- Provide a CLI toggle to escalate: `--proc-250-as-error`.  
- Record `{code,file,violation_type,date}` events in ADR-LOG`; compute rolling 30-day counts for PROC-242.  
- Classify date-format violations strictly under `ADR-SCHEMA-005` (never PROC).
- (PROPOSED) Governance constraint syntax errors classified under `ADR-GOV-###` codes (never PROC).

---

## §10. Links, pins & inheritance checks

### 10.1 Bi-directional links

- `supersedes: ADR-<id>@<pin> (see §8)` **requires** reciprocal `superseded_by` on the target.
- `informs: ADR-<id>@<pin> (see §8)` **requires** reciprocal `informed_by` on the target.
- **Lint**: `ADR-LINK-200` (E) missing reciprocal link.

### 10.2 Pinned `extends` (allowed format)

- See Section 8 for allowed pinned formats
- **Lint**: `ADR-LINK-201` (E) missing pin; `ADR-LINK-203` (E) bad format.

### 10.3 Pointers

- **Warn**: `ADR-LINK-202` (W) pointer to missing section key in base (probable rename).

### 10.4 Supersede closure map

- **Info**: `ADR-LINK-220` closure: multiple descendants; add rationale.
- **Error**: `ADR-LINK-221` cycle detected.
- **Warn**: `ADR-LINK-222` fork without rationale.

### 10.5 Template exemptions

When **class is `template`**:

- Do not enforce pinning for extends or bi-directional links (keep them null in templates).
- Do not require numeric thresholds/units; placeholders are allowed.
- Do not require delta-only constraints (e.g., diff_summary).
- Still enforce valid front-matter shape and the class ↔ template_of relationship, and forbid class-forbidden sections per §7 class rules.
- RFC-2119 tokens are permitted only inside inline code or fenced code examples.

---

## §11. Normative language safety (RFC-2119)

**Detection scope.** RFC-2119 keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, SHALL, SHALL NOT, MAY, RECOMMENDED, NOT RECOMMENDED) establish binding requirements. Detection is **case-insensitive**; authors SHOULD write these in uppercase.

**Allowed locations (exhaustive):**
1) Canonical sections: See Section 5 for the authoritative list (e.g., `<!-- key: decision_details -->`, `<!-- key: rollout_backout -->`).
2) Requirements subsection: `<!-- key: consequences_and_risks.requirements -->` (single, dotted key).
   - **No other dotted key patterns are permitted for normative content.** Examples that are **not** allowed: `decision_details.requirements`, `consequences_and_risks.musts`, etc.
3) **Delta overrides:** RFC-2119 terms in fenced `yaml` **override blocks** (under `overrides:` in Delta ADRs) **establish modified requirements and are permitted.**

**Scanner behavior.**
- Case-insensitive keyword matching.
- **Ignore:** fenced code blocks (``` ```), inline code (`…`), HTML comments (`<!-- … -->`), **blockquotes (`> …`)**, and URLs.  
  *Rationale:* Code/quotes/excerpts/examples must not accidentally create binding requirements.
  
- Section recognition: primary via Markdown markers; fallback heading aliases:
  - “Decision Details” → `decision_details`
  - “Rollout & Backout” / “Rollout and Backout” → `rollout_backout`
  - “Requirements (normative)” under “Consequences & Risks” → `consequences_and_risks.requirements`
- **Report all violations** in a file (no caps).

**Class interactions.**
- `class: governance` — exempt from RFC-2119 scanning in prose (constraint blocks provide binding authority).
- `class: style-guide` — exempt from RFC-2119 scanning (examples permitted).
- `class: template` — RFC terms allowed **only** inside fenced code or inline code; otherwise this section applies.

**Lint codes.**
- `ADR-NORM-101` (E): RFC-2119 keyword outside allowed locations.
- `ADR-NORM-102` (W): Vague term in normative text (e.g., “robust”, “simple”) without numbers/units.

### Implementation Notes (non-normative)

Four primary hooks for linter implementation:

1. **Section detection:** Parse HTML markers (`<!-- key: ... -->`) and maintain fallback heading aliases. Dotted keys require exact string matching (`consequences_and_risks.requirements`).

2. **Content filtering:** Skip scanning within fenced blocks, inline code, HTML comments, blockquotes, and URL patterns before applying RFC-2119 regex.

3. **Class-aware routing:** Apply exemptions for `style-guide` (full skip), `governance` (full skip), and `template` (code-fence-only allowance) before normative scanning.

4. **YAML override recognition:** Identify fenced `yaml` blocks containing `overrides:` keys in Delta ADRs; permit RFC-2119 terms within those blocks. Governance `constraint_rules:` blocks do not permit RFC-2119 terms.

---

## §12. LLM tail (machine context, optional)

<!-- llm_tail:begin -->
```json
{
  "id": "ADR-0123",
  "class": "delta",
  "status": "Accepted",
  "extends": "ADR-0120@2025-03-14",
  "owners_ptr": "ADR-0120"
  "governed_by": "ADR-0110@2025-03-14",
  "scope": null
}
```
<!-- llm_tail:end -->

> When present, it must mirror front-matter for: id, class, status, extends, ownership (owners[] or owners_ptr), governed_by, and scope.

**Info**: `ADR-META-150` missing (optional).  
**Warn**: `ADR-META-151` tail disagrees with front-matter for: `id`, `class`, `status`, `extends`, ownership (`owners[]` or `owners_ptr`), `governed_by`, `scope`.

---

## §13. CI Contract

CI blocks on all codes marked (E) in §14 and warns on codes marked (W).

(PROPOSED) Governance validation codes (ADR-GOV-###) are all blocking (E) by default.

Override via: `--fail-on W` to change threshold.

---

## §14 Linter Rules Reference

**Version**: 0.1.6
**Severity legend**: E=block merge · W=proceed+annotate · I=log only

### Code Bands

| Band               | Range   | Purpose                      |
| ------------------ | ------- | ---------------------------- |
| `ADR-SCHEMA-###`   | 001–099 | Front-matter & structure     |
| `ADR-NORM-###`     | 100–149 | Normative language rules     |
| `ADR-META-###`     | 150–169 | LLM tail & meta consistency  |
| `ADR-LINK-###`     | 200–239 | Links, pointers, inheritance |
| `ADR-PROC-###`     | 240–269 | Process & auto-resolve       |
| `ADR-DELTA-###`    | 300–339 | Delta/extends semantics      |
| `ADR-TEMPLATE-###` | 340–379 | Template structure & usage   |

#### Discrepencies

Upon reviewing the linting outcome of drafting a new ADR for CLI System Architecture, new gaps were identified:

- Does ADR-TEMPLATE-\* focus on ensuring templates follow proper inheritance issues?
- Does ADR-TEMPLATE-\* focus on ensuring templates used to create new ADRs with the proper template structure?
  - If a new ADR (e.g., 0006) has the right section in the right place (e.g., ## Decision (one-liner)) but the actual section is structured differently (e.g., paragraphs for a decision vs. a 1 line user story) is that a rule violation?

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
  - TOADD: Must have corresponding markdown headers which would cover (2025-09-21)
    - Missing sections entirely
    - Wrong section order
    - Present sections with missing headers
    - Present sections with mismatched headers
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
- TOADD: **ADR-TEMPLATE-706 (W)**: content formatting matches documented format. (2025-09-21)
  - Example: ## Decision is explicitly a one-liner following the format of: "Because <long-range driver>, we choose <strategic direction> so that <north star>."
  - In the validator and/or pytest for this rule, we can capture additional insights as to what this rule will cover **OR** which sections are explicitly ignored for now.
  - Expectation for this rule is: 
    - Make decisions **atomic, auditable, and reversible**.
    - Keep docs **human-skim friendly** and **machine-readable** (LLMs, linters).


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
- [ ] Deltas: `extends`, `diff_summary`, scoped `applies_to`  
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

## License

Architecture Decision Records ("ADRs") are covered by the 
Creative Commons Attribution-NonCommercial 4.0 International License.
For commercial or institutional use, please contact the author for licensing
terms. Canonical URL: https://creativecommons.org/licenses/by-nc/4.0/

© 2025 John Hall
Canonical GitHub Repository URL: https://github.com/hall-jm/theseus/
