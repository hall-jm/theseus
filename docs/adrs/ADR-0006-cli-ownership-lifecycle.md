---
id: ADR-xxxx
title: CLI Ownership & Lifecycle
status: Proposed
class: owner
owners: ["Project Maintainer"]
extends: null
supersedes: null
superseded_by: null
date: 2025-09-21
review_by: 2026-03-21
tags: [theseus, ariadne, cli, ownership, governance]
applies_to: []
change_history: []
---

# ADR-xxxx - CLI Ownership & Lifecycle

## Document Controls

### Status

| Field                  | Value                                   |
| ---------------------- | --------------------------------------- |
| **Version**:           | 0.1.0                                   |
| **Status**:            | Proposed                                |
| **Date**:              | 2025-09-21                              |
| **Applies to Schema**: | 0.1.0                                   |
| **Related**:           | ADR-0001 (Style Guide)                  |

### Changelog

| Version | Date         | Notes                                        |
| ------- | ------------ | -------------------------------------------- |
| 0.1.0   | 2025 Sept 21 | Initial draft of ADR-0006                    |


## Decision (one-liner)
<!-- key: decision_one_liner -->

Because the CLI is the user-facing contract and error boundary, we assign it explicit ownership of argument parsing, message rendering, and exit codes so that failures are predictable, testable, and decoupled from engine/services internals.

## Context & Drivers
<!-- key: context_and_drivers -->

- **Goals**
  - Make user-facing behavior deterministic (help text, flags, errors, exit codes).
  - Keep engine/services swappable behind a stable CLI boundary.
  - Reduce “spaghetti” fixes by separating concerns (parse/format vs. orchestrate vs. IO).
- **Non-goals**
  - Redesigning engine orchestration or validator semantics (handled separately).
  - Introducing new flags beyond current surface unless justified by this ADR.
- **Constraints**
  - Preserve current CLI flags where practical (`--path`, `--fail-on`, `-k`, `--format`, `--emit-metrics`).
  - Respect canonical section/ownership rules from ADR-0001.
- **Assumptions**
  - Call flow is CLI → Engine → Services/Validators as of 21 September 2025.
  - CLI remains the primary entry point for humans and CI.

## Options Considered
<!-- key: options_considered -->
| Option | Fit to Drivers | Complexity | Risk | Reversibility | Notes |
| ------ | -------------- | ---------- | ---- | ------------- | ----- |
| A) Ad-hoc: let CLI, engine, services share responsibilities loosely | Low | Low | High | Medium | Continues ambiguity; brittle errors/exit codes |
| B) “Thin” CLI: push most behavior into engine | Medium | Medium | Medium | High | Engine becomes monolith; user errors feel internal |
| **C) Explicit CLI contract (Chosen)** | **High** | Medium | **Low** | High | Clear parsing/rendering/exit-code boundary |

- **Rejected because…**
  - **A:** Fails determinism; perpetuates drift.
  - **B:** Blurs user vs. internal concerns; harder to test UX separately.

## Decision Details
<!-- key: decision_details -->

**Scope (authoritative for the CLI):**
1) **Parsing & validation (shape only):**
   - The CLI **MUST** parse flags/args and validate their *shape/range* (e.g., required vs. optional, enum sets).
   - The CLI **MUST NOT** inspect ADR contents or file structure; deeper validation belongs to engine/services.

2) **Normalization → Engine:**
   - The CLI **MUST** normalize inputs into an execution request and call a single engine entry point (e.g., `engine.run(...)`).
   - The CLI **MUST NOT** reach into services or validators directly.

3) **User-facing rendering:**
   - The CLI **MUST** own help/usage output, human/CI formatting selection (`--format=md|jsonl`), and top-level error messages.
   - The CLI **SHOULD** render errors without leaking internal stack traces by default; a debug flag **MAY** expose detail.

4) **Exit codes (canonical):**
   - `0` = success (no findings at or above `--fail-on` threshold).
   - `1` = findings at/above threshold (e.g., **E** when `--fail-on=E`).
   - `2` = usage error (invalid args/flags).
   - `3` = operational failure signaled by engine/services (e.g., discovery failure, unreadable files).
   - The CLI **MUST** compute the exit code based on this mapping and engine’s structured result.

5) **Config & environment:**
   - The CLI **MAY** load optional environment/config that affects *only* presentation or routing (e.g., default `--path`).
   - The CLI **MUST NOT** silently alter validator policies; policy toggles are explicit flags or engine configuration.

6) **Stability & tests:**
   - Help text, flag set, and exit-code semantics **MUST** be covered by CLI tests (incl. `-h`, bad flags, missing path, empty set).
   - CLI behavior **SHOULD** be backward compatible or gated by major/minor versioning.

## Consequences & Risks
<!-- key: consequences_and_risks -->
- **Positive:** Deterministic UX; easier CI adoption; clearer fault isolation; safer LLM contributions at the edges.
- **Trade-offs:** Slight duplication (arg shape validation in CLI, deeper checks in engine); stricter boundaries could require minor refactors.
- **Risks:** Teams could attempt to “just add this check” to the CLI—this ADR forbids content-level validation in the CLI.

## Rollout & Backout
<!-- key: rollout_backout -->
- **Phases**
  1. Add CLI tests for `-h`, bad flag, unknown flag, `--path` missing, and empty discovery → exit codes (2/3).
  2. Refactor CLI to emit structured requests to engine only.
  3. Wire up exit-code mapping to engine outcomes.
  4. Document flags and exit-code contract in README.
- **Backout**
  - Revert to prior CLI shim; engine API remains intact. No data migration required.

## Implementation Notes
<!-- key: implementation_notes -->
- CLI lives in `src/adr_linter/cli.py`; engine entry point in `src/adr_linter/engine.py`.
- The CLI prints/exports results; engine produces structured results and severities.
- Discovery/IO errors are raised from services → engine → returned to CLI as operational failures (mapped to exit code `3`).

## Evidence & Links
<!-- key: evidence_and_links -->
- ADR-0001 (Style Guide; canonical keys; class ownership)
- Internal test history demonstrating ambiguity around discovery and exit codes before boundary enforcement (ref: repo tests).

## Glossary
<!-- key: glossary -->
- **CLI:** User-facing command that parses flags/args, renders messages, and returns exit codes.
- **Engine:** Orchestrates validation pipeline and aggregates findings; no direct UX rendering.
- **Services:** IO/discovery/indexing utilities invoked by the engine.

## Related ADRs
<!-- key: related_adrs -->
- ADR-0001 (Style Guide)
- Engine Ownership & Orchestration (owner ADR — planned, unnumbered)
- Services & Discovery Ownership (owner ADR — planned, unnumbered)

<!-- llm_tail:begin -->
```json
{
  "id": "ADR-xxxx",
  "class": "owner",
  "status": "Proposed",
  "extends": null,
  "owners": ["Project Maintainer"]
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
