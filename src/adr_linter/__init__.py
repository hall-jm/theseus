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
