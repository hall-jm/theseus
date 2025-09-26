# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/__init__.py

"""
Theseus ADR Linter - Governance tools for architectural decision records.

- [X] Reviewed & verified by Claude Sonnet 4 on 21 September 2025
- [ ] Next review should be performed by 21 March 2025

ARCHITECTURE OVERVIEW
====================

Entry Points:
- CLI: `python -m adr_linter.cli` or `theseus` command
- Direct: `from adr_linter.engine import run`

Call Flow:
CLI args → Engine → File Discovery → Validators → Report

COMPONENT RESPONSIBILITIES
=========================

cli.py:
- Argument parsing (--path, --fail-on, -k, --format, --emit-metrics)
- Output formatting (md, jsonl)
- Exit code handling
- Entry: main() → engine.run()

engine.py:
- Orchestration of validation pipeline
- Calls services.index.load_files() for discovery
- Two-phase validation: per-file then post-run
- Metrics tracking and run log generation
- Exit code computation based on severity threshold

services/index.py:
- File discovery using ADR_LOCATIONS patterns
- Document loading and parsing
- Index building for cross-document validation
- Pure/impure separation (IO isolation)

validators/:
- Rule implementations organized by validation band
- Each validator takes (context, report) and adds findings
- Bands: schema, link, norm, meta, template, delta
- Registry coordinates execution order

FILE DISCOVERY PROCESS
=====================

Discovery happens in services.index.load_files():
1. Use glob patterns from constants.ADR_LOCATIONS:
   - "docs/adrs/**/*.md"
   - "docs/adrs/*.md"
2. Skip files in hidden directories (parts starting with ".")
3. Deduplicate by resolved path
4. Apply -k keyword filter if specified
5. Return sorted list of ADR file paths

This discovery runs on every execution - no caching or state.

VALIDATION CODES
===============

30+ validation rules across 6 bands:
- SCHEMA: Front-matter structure, section ordering, class constraints
- LINK: Cross-references, supersede relationships, pointer validation
- NORM: RFC-2119 placement, vague term detection
- META: LLM tail consistency (optional metadata)
- TEMPLATE: Template compliance, section mirroring
- DELTA: Override validation, dependency resolution

Severities: E (Error/blocking), W (Warning), I (Info/logging)

CURRENT ARGUMENTS
================

theseus --path PATH --fail-on E|W|I -k KEYWORD --emit-metrics --format md|jsonl
"""

"""
## Strategic Analysis of the Refactoring Tension

### **Decision One-Liner**

Because the constants/validators/registry form a tightly coupled triad with
governance infrastructure missing, we choose to establish governance
foundations before validator implementation so that we avoid cascading rework
cycles.

### **Context and Drivers**

- **Current state**: Constants define governance class but no governance
                     validation infrastructure exists
- **Coupling problem**: Registry hardcodes validator imports, constants define
                        codes, but no single authority for "what should exist"
- **Bootstrap paradox**: Need governance ADRs to document authority, but can't
                         validate governance ADRs without governance
                         validators
- **Technical debt**: TOREVIEW/TODO/FIXME comments indicate known drift
                      between documentation and implementation

### **Options Considered**

1. **Constants-first**: Fix all constant mismatches, then build validators
                        → Risk of defining wrong interfaces
2. **Validator-first**: Implement missing validators with current constants
                        → Risk of building on broken foundations
3. **Governance-infrastructure-first**: Build governance parsing/validation
                        foundation → Risk of over-engineering before
                        understanding requirements
4. **Documentation-driven**: Document current state completely, then plan
                             consolidation → Risk of analysis paralysis

### **Decision Details**

**MUST** establish governance validation infrastructure before implementing
         governance-dependent validators
**SHOULD** consolidate constants/registry/validator relationships into a
           single source of truth
**MAY** accept temporary duplication during transition to avoid system-wide
        breakage

### **Principles**

- **Fail-fast on governance violations**: Better to block on missing
                                          governance than allow drift
- **Single source of truth**: Each concept (valid classes, canonical keys,
                              code definitions) should have one authoritative
                              definition
- **Incremental safety**: Changes should be reversible and testable in
                          isolation

### **Guardrails**

- **No cross-file constant duplication**: Derived values must be computed, not
                                          copied
- **No validator implementation without corresponding constant definitions**:
        Prevents magic strings
- **No governance-dependent validators without governance parsing
    infrastructure**:
        Prevents incomplete validation

### **Consequences and Risks**

**Trade-offs**: Slower initial progress but prevents rework cycles when
                governance requirements clarify
**Risk**: Over-architecting governance infrastructure before understanding all
          use cases
**Mitigation**: Start with minimal governance parsing (scope validation) and
                extend incrementally

### **Implementation Notes**

**Phase 1**: Create governance constants
             (VALID_SCOPE_VALUES, CANONICAL_KEYS_GOVERNANCE)
**Phase 2**: Extend SectionInfo to parse governance constraint blocks
**Phase 3**: Implement basic governance validators (006-008)
**Phase 4**: Build governance-dependent delta validators (501-503, 508, 510)

The core tension is that governance is foundational to the entire validation
system, but implementing it requires touching every major component. The
conservative approach is to build governance foundations incrementally rather
than attempting a big-bang refactor.
"""
