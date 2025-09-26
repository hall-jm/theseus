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

from ..models import SectionData
from ..constants import (
    HEADING_ALIASES,
    get_canonical_keys,
)


def map_heading_to_key(heading_text: str) -> str | None:
    """
    Map markdown headings to canonical section keys using aliases.

    Primary: HTML markers <!-- key: ... --> (handled in
             parse_document_structure)
    Fallback: Heading aliases for human-friendly headings
    """
    return HEADING_ALIASES.get(heading_text.strip())


def line_from_pos(text: str, pos: int) -> int:
    return _line_from_pos(text, pos)


def _line_from_pos(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def parse_document_structure(
    body: str, *, class_hint: Optional[str] = None
) -> SectionData:
    """
    Single-pass extraction of document structure with enhanced parser contract.

    Args:
        body: ADR document body (after front-matter)
        class_hint: ADR class from front-matter to help with governance parsing

    Returns:
        SectionInfo with enhanced metadata for governance validation
    """
    # Key markers (primary section detection)
    key_markers: List[Tuple[str, int, int]] = []
    for m in re.finditer(
        r"<!--\s*key:\s*([a-z0-9_]+(?:\.[a-z0-9_]+)?)\s*-->", body
    ):
        key = m.group(1)
        start = m.start()
        key_markers.append((key, start, _line_from_pos(body, start)))

    # Headings (fallback section detection)
    headings: List[Tuple[str, int, int, int]] = []
    alias_hits: Dict[str, str] = {}

    for m in re.finditer(r"^(#{1,6})\s+([^\n#]+?)\s*$", body, flags=re.M):
        level = len(m.group(1))
        text = m.group(2).strip()
        start = m.start()
        headings.append((text, level, start, _line_from_pos(body, start)))

        # Check for heading aliases
        canonical_key = map_heading_to_key(text)
        if canonical_key:
            alias_hits[text] = canonical_key

    # Duplicate section detection
    _detect_duplicate_sections(key_markers, alias_hits)

    # Enhanced YAML blocks with metadata
    yaml_blocks: List[Dict] = []
    for m in re.finditer(r"```yaml\n(.*?)\n```", body, flags=re.S | re.I):
        y = m.group(1)
        start, end = m.span()

        if yaml:
            try:
                data = yaml.safe_load(y)
                if isinstance(data, dict):
                    # Determine YAML block kind for governance validation
                    kind = _classify_yaml_block(data, class_hint)
                    yaml_blocks.append(
                        {"kind": kind, "data": data, "span": (start, end)}
                    )
            except Exception:
                # Malformed YAML - include for error reporting
                yaml_blocks.append(
                    {
                        "kind": "malformed",
                        "data": None,
                        "span": (start, end),
                        "raw": y,
                    }
                )

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
    parts = re.split(
        r"<!--\s*key:\s*([a-z0-9_]+(?:\.[a-z0-9_]+)?)\s*-->", body
    )
    for i in range(1, len(parts), 2):
        key = parts[i]
        content = parts[i + 1] if i + 1 < len(parts) else ""
        sections_by_key[key] = content

    return SectionData(
        key_markers=key_markers,
        headings=headings,
        yaml_blocks=yaml_blocks,
        llm_tail=llm_tail,
        exclusion_ranges=exclusion_ranges,
        sections_by_key=sections_by_key,
        # Enhanced fields (need to update SectionInfo model)
        alias_hits=alias_hits,
        class_hint=class_hint,
    )


def _detect_duplicate_sections(
    key_markers: List[Tuple[str, int, int]], alias_hits: Dict[str, str]
) -> None:
    """
    Detect actual duplicates: multiple HTML markers for same key, or
    conflicting aliases. Having HTML marker + matching heading is NOT a
    duplicate - it's the preferred pattern.
    """
    # Check for duplicate HTML markers (same key multiple times)
    marker_keys = [key for key, _, _ in key_markers]
    duplicate_markers = [
        key for key in set(marker_keys) if marker_keys.count(key) > 1
    ]

    if duplicate_markers:
        for dup_key in duplicate_markers:
            raise ValueError(
                f"HTML marker '<!-- key: {dup_key} -->' appears multiple times"
            )

    # Check for conflicting aliases (multiple headings mapping to same key,
    # but only if that key doesn't have an HTML marker)
    canonical_keys = {key for key, _, _ in key_markers}
    alias_key_counts = {}
    for alias, key in alias_hits.items():
        if (
            key not in canonical_keys
        ):  # Only care about conflicts for keys without HTML markers
            alias_key_counts[key] = alias_key_counts.get(key, 0) + 1

    conflicting_aliases = {
        key: count for key, count in alias_key_counts.items() if count > 1
    }
    if conflicting_aliases:
        for key in conflicting_aliases:
            aliases = [alias for alias, k in alias_hits.items() if k == key]
            raise ValueError(f"Multiple headings map to '{key}': {aliases}")


def _classify_yaml_block(data: Dict, class_hint: Optional[str]) -> str:
    """
    Classify YAML blocks for governance validation seam.

    Returns:
        "constraint_rules" - Governance constraint blocks
        "overrides" - Delta override blocks
        "ptr" - Delta pointer blocks
        "unknown" - Other YAML blocks
    """
    if "constraint_rules" in data:
        return "constraint_rules"
    elif "overrides" in data:
        return "overrides"
    elif "ptr" in data:
        return "ptr"
    else:
        return "unknown"


# -----------------------------------------------------------------------------
# Canonical section order helper (updated to use new API)
# -----------------------------------------------------------------------------


def expected_keys_for(
    cls: str, template_of: Optional[str] = None, relaxed_delta: bool = False
) -> List[str]:
    """
    Return canonical section keys for a given ADR class.

    Updated to use get_canonical_keys() API from constants.sections.
    Maintains backward compatibility for existing callers.

    Args:
        cls: ADR class name
        template_of: For template class, the target class to mirror
        relaxed_delta: For delta class, use relaxed validation

    Returns:
        List of canonical section keys in order

    Ref: ADR-0001 §4 Canonical section keys & order
    """
    return get_canonical_keys(
        cls, template_of=template_of, relaxed_delta=relaxed_delta
    )


# -----------------------------------------------------------------------------
# Index building (updated to pass class hint)
# -----------------------------------------------------------------------------


def build_index_from_texts(
    pairs: Iterable[Tuple[Path, str]],
) -> Dict[str, Dict[str, Any]]:
    """
    Pure index builder: given (path, raw text) pairs, parse front-matter and
    structure and return the same index shape legacy/io.build_index produces.

    Updated to pass class hint to parser for enhanced governance support.
    """
    idx: Dict[str, Dict[str, Any]] = {}
    for p, text in pairs:
        meta, end = parse_front_matter(text)
        body = text[end:]
        class_hint = meta.get("class")
        section_data = parse_document_structure(body, class_hint=class_hint)

        if meta.get("id"):
            idx[meta["id"]] = {
                "path": p,
                "meta": meta,
                "body": body,
                "raw": text,
                "section_data": section_data,
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
