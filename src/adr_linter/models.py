# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/models.py

"""
Core data models used across the ADR linter (shared, importable).
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class SectionData:
    """
    Consolidated section information extracted from one parse pass.
    """

    # (key, start_pos, line_num)
    key_markers: List[Tuple[str, int, int]]
    # (text, level, start_pos, line_num)
    headings: List[Tuple[str, int, int, int]]
    yaml_blocks: List[Dict]
    llm_tail: Optional[Dict]
    # byte offsets in body where RFC scan should be skipped
    exclusion_ranges: List[Tuple[int, int]]
    # key -> raw content of that section (post-marker)
    sections_by_key: Dict[str, str]
    # Enhanced fields for governance validation
    alias_hits: Dict[str, str]  # alias_heading -> canonical_key
    class_hint: Optional[str]  # ADR class from front-matter


@dataclass
class ValidationData:
    """
    Context handed to validators (single unit of review).
    """

    meta: Dict
    body: str
    path: Path
    section_data: SectionData
    # Index for cross-file validation
    all_idx: Dict
