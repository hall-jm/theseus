# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/parser/structure.py

from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple, Optional

from .front_matter import parse_front_matter

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

from ..models import SectionInfo
from ..constants import (
    VALID_ADR_CLASSES,
    CANONICAL_KEYS_OWNER,
    CANONICAL_KEYS_DELTA,
    CANONICAL_KEYS_STRATEGY,
)


# TOREVIEW: HEADINGS_TO_KEYS and CANONICAL_KEYS_* must stay in sync
# TODO: Verify any changes to canonical keys include corresponding regex
#       patterns
# TOREVIEW: Ref: ADR-0001 §(Missing) · (If needed, ADR-*-* is missing)
HEADINGS_TO_KEYS = [
    (re.compile(r"^decision\s*\(one-?liner\)$", re.I), "decision_one_liner"),
    (re.compile(r"^context\s*&?\s*drivers?$", re.I), "context_and_drivers"),
    (re.compile(r"^options?\s+considered$", re.I), "options_considered"),
    (re.compile(r"^decision\s+details?$", re.I), "decision_details"),
    (
        re.compile(r"^consequences\s*&\s*risks?$", re.I),
        "consequences_and_risks",
    ),
    (re.compile(r"^rollout\s*(?:&|and)\s*backout$", re.I), "rollout_backout"),
    (re.compile(r"^implementation\s+notes?$", re.I), "implementation_notes"),
    (re.compile(r"^evidence\s*&\s*links?$", re.I), "evidence_and_links"),
    (re.compile(r"^glossary$", re.I), "glossary"),
    (re.compile(r"^related\s+adrs?$", re.I), "related_adrs"),
    (re.compile(r"^principles$", re.I), "principles"),
    (re.compile(r"^guardrails$", re.I), "guardrails"),
    (re.compile(r"^north\s*star\s*metrics?$", re.I), "north_star_metrics"),
]


# CRITICAL: Must add regex patterns to HEADINGS_TO_KEYS when canonical keys
#           change
# TODO: Check sync between HEADINGS_TO_KEYS and CANONICAL_KEYS_* during
#       refactor
#
# Maps markdown headings to canonical section keys.
# TOREVIEW: Ref: ADR-0001 §(Missing) · (If needed, ADR-*-* is missing)
def map_heading_to_key(heading_text: str) -> str | None:
    for rx, key in HEADINGS_TO_KEYS:
        if rx.match(heading_text):
            return key
    return None


def line_from_pos(text: str, pos: int) -> int:
    return _line_from_pos(text, pos)


def _line_from_pos(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def parse_document_structure(body: str) -> SectionInfo:
    """Single-pass extraction of document structure (behavior preserved)."""
    # Key markers
    key_markers: List[Tuple[str, int, int]] = []
    for m in re.finditer(r"<!--\s*key:\s*([a-z0-9_]+)\s*-->", body):
        key = m.group(1)
        start = m.start()
        key_markers.append((key, start, _line_from_pos(body, start)))

    # Headings
    headings: List[Tuple[str, int, int, int]] = []
    for m in re.finditer(r"^(#{1,6})\s+([^\n#]+?)\s*$", body, flags=re.M):
        level = len(m.group(1))
        text = m.group(2).strip()
        start = m.start()
        headings.append((text, level, start, _line_from_pos(body, start)))

    # YAML blocks
    yaml_blocks: List[Dict] = []
    for m in re.finditer(r"```yaml\n(.*?)\n```", body, flags=re.S | re.I):
        y = m.group(1)
        if yaml:
            try:
                d = yaml.safe_load(y)
                if isinstance(d, dict):
                    yaml_blocks.append(d)
            except Exception:
                pass

    # LLM tail (prefer last)
    llm_tail: Optional[Dict] = None
    llm_tail_re = re.compile(
        r"<!--\s*llm_tail:begin\s*-->"
        r".*?```json\r?\n"
        r"(?P<json>.*?)\r?\n"
        r"```"
        r".*?<!--\s*llm_tail:end\s*-->",
        re.DOTALL,
    )
    matches = list(llm_tail_re.finditer(body))
    if matches:
        m = matches[-1]
        try:
            llm_tail = json.loads(m.group("json"))
        except Exception:
            llm_tail = None

    # Exclusions for RFC-2119 scanning
    exclusion_ranges: List[Tuple[int, int]] = []
    # Fenced code
    for m in re.finditer(r"```.*?```", body, flags=re.S):
        exclusion_ranges.append((m.start(), m.end()))
    # Inline code
    for m in re.finditer(r"`[^`]*`", body):
        exclusion_ranges.append((m.start(), m.end()))
    # URLs
    for m in re.finditer(r"https?://[^\s\])<>\"']+", body):
        exclusion_ranges.append((m.start(), m.end()))
    # HTML comments
    for m in re.finditer(r"<!--.*?-->", body, flags=re.S):
        exclusion_ranges.append((m.start(), m.end()))
    # Blockquotes (ADR-0001 §11 exemption)
    for m in re.finditer(r"^[ \t]*>.*$", body, flags=re.M):
        exclusion_ranges.append((m.start(), m.end()))

    # Sections by key
    sections_by_key: Dict[str, str] = {}
    parts = re.split(r"<!--\s*key:\s*([a-z0-9_]+)\s*-->", body)
    for i in range(1, len(parts), 2):
        key = parts[i]
        content = parts[i + 1] if i + 1 < len(parts) else ""
        sections_by_key[key] = content

    return SectionInfo(
        key_markers=key_markers,
        headings=headings,
        yaml_blocks=yaml_blocks,
        llm_tail=llm_tail,
        exclusion_ranges=exclusion_ranges,
        sections_by_key=sections_by_key,
    )


# -----------------------------------------------------------------------------
# Canonical section order helper (structure semantics)
# -----------------------------------------------------------------------------


# FIXME: Template validation was broken - previously returned [] for all
#        templates
# BUG: Fixed 2025-09-08 - templates now correctly inherit keys from
#      template_of class
# CRITICAL: This implements ADR-0001 §7.5 requirement that templates mirror
#           canonical section order
# REVIEW: Verify template tests validate section order enforcement correctly
# BLOCKER: Changes here must include HEADINGS_TO_KEYS updates
# TODO: Test that heading mapping works for any new keys added
def expected_keys_for(
    cls: str, template_of: Optional[str] = None
) -> List[str]:
    """
    Return canonical section keys for a given ADR class.
    For templates, return the keys of the class they template (`template_of`).
    Mirrors legacy behavior; used by SCHEMA-003 and TEMPLT-705.

    Ref: ADR-0001 §(Missing) · (If needed, ADR-*-* is missing)
    """
    if cls == "template":
        if template_of and template_of in VALID_ADR_CLASSES:
            return expected_keys_for(template_of)
        # Invalid/missing template_of → empty list to trigger validator error
        return []
    if cls == "owner":
        return CANONICAL_KEYS_OWNER
    if cls == "delta":
        return CANONICAL_KEYS_DELTA
    if cls == "strategy":
        return CANONICAL_KEYS_STRATEGY
    if cls == "style-guide":
        # Style-guides do not require canonical ADR keys
        return []
    return []


# -----------------------------------------------------------------------------
# Index building
# -----------------------------------------------------------------------------


def build_index_from_texts(
    pairs: Iterable[Tuple[Path, str]],
) -> Dict[str, Dict[str, Any]]:
    """
    Pure index builder: given (path, raw text) pairs, parse front-matter and
    structure and return the same index shape legacy/io.build_index produces.
    ZERO behavior change: field names and values are identical.

    Ref: ADR-0001 §(Missing) · (If needed, ADR-*-* is missing)
    """
    idx: Dict[str, Dict[str, Any]] = {}
    for p, text in pairs:
        meta, end = parse_front_matter(text)
        body = text[end:]
        section_info = parse_document_structure(body)

        if meta.get("id"):
            idx[meta["id"]] = {
                "path": p,
                "meta": meta,
                "body": body,
                "raw": text,
                "section_info": section_info,
            }
    return idx


def find_balanced_code_fences(text):
    exclusions = []
    fence_stack = []
    lines = text.split("\n")
    current_pos = 0

    for i, line in enumerate(lines):
        line_start = current_pos
        stripped = line.strip()

        if stripped.startswith("```"):
            if not fence_stack:
                # Start new fence
                fence_stack.append(line_start)
            elif stripped == "```":
                # End fence only with plain ```
                if fence_stack:
                    start = fence_stack.pop()
                    end = current_pos + len(line)
                    exclusions.append((start, end))
            # Any ```language inside a fence is ignored (treated as content)

        current_pos += len(line) + 1

    # Close any unclosed fences
    while fence_stack:
        start = fence_stack.pop()
        exclusions.append((start, len(text)))

    return exclusions
