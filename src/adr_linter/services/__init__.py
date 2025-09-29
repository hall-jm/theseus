# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/services/__init__.py

"""
# Change Proposal: Deterministic ADR Discovery & Failure Semantics

## 1) Problem framing (current → pain)

* **Observed behavior:** When `ADR_LOCATIONS` patterns do not match any files
  in the repo (e.g., paths moved), the run continues and prints a “clean”
  summary (0 files scanned).
* **Impact:** False green outcomes, missed violations, and silent drift. Makes
  CI and local runs untrustworthy.
* **Where it happens:** Discovery in `services/index.load_files()` → consumed
  by `engine.run()` → surfaced via CLI.
* **Who it affects:** Anyone expecting a signal when ADRs aren’t found
  (CI gatekeepers, local authors, doc maintainers).

## 2) Goal & non-goals

**Goals**

* Fail fast by default when **no ADR files** are discovered.
* Provide an explicit **warn-only mode** for exploratory runs.
* Make the behavior **visible, documentable, and testable**
  (CLI messages + exit codes + docs).

**Non-goals**

* Redesign of validator logic or bands.
* New config system. (We’ll piggyback on existing CLI args/env for now.)
* Performance optimization. (Out of scope for this change.)

## 3) Behavior contract (proposed)

* **Default mode (CI-safe):**

  * If **zero** ADR files match → **hard error** with a clear message naming
    root + patterns.
  * Exit code is **non-zero** (distinct exit if you want, e.g., 2).
* **Warn-only escape hatch:**

  * If env `THESEUS_ADR_DISCOVERY_WARN_ONLY=1`
    (or CLI `--discovery-warn-only`) → emit a **single-line WARN** and proceed
    with **0 files**.
  * Exit code remains governed by validator results (likely 0 if nothing ran).
* **User-facing messaging:**

  * Include the **resolved root**, **effective patterns**, and
    **how to override** (env/CLI) in the error/warn text.
* **Precedence for discovery inputs:**

  1. CLI `--pattern …` (repeatable)
  2. Env (if you have one; optional)
  3. Defaults in constants/policy
  4. Root: CLI `--root` → env `THESEUS_ADR_ROOT` → `cwd`

## 4) Scope of change (touch points)

* **CLI**: surface/help text (epilog), optional `--discovery-warn-only`.
* **Engine**: treat “no files” as terminal condition unless warn-only is set.
* **Discovery**: single source of truth for patterns/root resolution and the
  count of matches.
* **Report/Exit policy**: keep as-is; just ensure discovery failures don’t
  masquerade as success.

## 5) UX & DX outcomes

* CI/logs show **explicit failure** when no ADRs are found.
* Local authors can set warn-only when testing on partial trees or examples.
* `--help` explicitly documents the behavior and toggles.

## 6) Risks & mitigations

* **Risk:** Breaking repos that currently rely on silent success.

  * **Mitigation:** Document env/flag; short deprecation window if needed.
* **Risk:** Multiple teams with different ADR roots.

  * **Mitigation:** Clear precedence + example invocations in README.

## 7) Acceptance criteria (black-box)

* Running with **no matching files** and **no override** → non-zero exit;
  message includes **root + patterns**.
* Running with **no matching files** and
  **warn-only enabled** → WARN printed once; summary shows **0 files**;
  exit code follows validator policy.
* `--help` shows discovery defaults and toggles.
* CI job fails on missing ADRs without warn-only.
* Tests:
  (a) “no files” default fails
  (b) “no files” warn-only proceeds
  (c) patterns override respected
  (d) root override respected

## 8) Telemetry & observability (optional, later)

* Count and log “no files” events (distinct from “0 errors”).
* Emit a single structured line: `{event: "discovery_empty", root, patterns,
  mode: "error|warn"}`.

## 9) Migration notes

* Add a short **README section** (“Discovery & Failure Semantics”).
* Mention env/flag in the **CLI epilog** and **docs/ARCHITECTURE.md**.
* Consider a minor version bump (behavioral change) and one-line changelog.

## 10) Open questions

* Do we want a **distinct exit code** for discovery failure vs. validator
  errors?
* Should discovery patterns be configurable via a **project file** later?
* Do we want a **deprecation window** (warn-by-default for one release) or
  flip to error immediately?
"""
