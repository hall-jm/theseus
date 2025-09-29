# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/parser/front_matter.py

from __future__ import annotations
import re
from typing import Tuple, Dict

try:
    import yaml  # type: ignore
except Exception:
    yaml = None


def parse_front_matter(text: str) -> Tuple[Dict, int]:
    """
    Parse YAML front-matter delimited by:
        ---
        <yaml>
        ---
    Tolerant to BOM, LF/CRLF, and leading whitespace.
    Returns (meta_dict, end_index).
    """
    if text.startswith("\ufeff"):
        text = text[1:]
    normalized = text.replace("\r\n", "\n")

    m = re.search(
        r"^\s*---\s*\n"  # opening fence
        r"(.*?)"  # YAML payload
        r"\n---\s*(?:\n|$)",  # closing fence, allow EOF
        normalized,
        flags=re.S | re.M,
    )
    if not m:
        return {}, 0

    fm = m.group(1)

    def _kv_fallback(payload: str) -> dict:
        """Very simple 'key: value' parser (comments/empties ignored)."""
        result = {}
        for raw in payload.splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            k, v = line.split(":", 1)
            result[k.strip()] = v.strip()
        return result

    meta = {}
    if yaml:
        try:
            data = yaml.safe_load(fm)
            meta = data if isinstance(data, dict) else _kv_fallback(fm)
        except Exception:
            meta = _kv_fallback(fm)
    else:
        meta = _kv_fallback(fm)

    # Map the normalized match back to original text to get end index
    block_norm = normalized[m.start() : m.end()]
    block_orig = (
        block_norm if "\r\n" not in text else block_norm.replace("\n", "\r\n")
    )
    start_idx = text.find(block_orig)
    end_idx = (
        start_idx + len(block_orig) if start_idx != -1 else len(block_orig)
    )
    return meta, end_idx
