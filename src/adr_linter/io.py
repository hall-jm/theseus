# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/io.py

"""
Thin I/O facade that re-exports legacy implementations.

Purpose: give callers a stable home for file discovery, indexing,
         telemetry, and run-log writers.
         To confirm, impure boundary (file discovery, read/write,
         run-log writers).
"""

from __future__ import annotations

import datetime
import json

from pathlib import Path
from typing import Iterable, List, Tuple  # , Dict, Any,


from .constants import (
    # --- File I/O Definitions
    ADR_LOCATIONS,
    # --- Lint Code Definitions
    # --- ADR Structure Constants
    # --- RFC-2119 and Validation Patterns
    # --- Status Transition Rules
)

from .services.index import build_index_from_texts


# -----------------------------------------------------------------------------
# File Loading
# -----------------------------------------------------------------------------


def load_files(root: Path):
    """
    Include ADR locations, but exclude generated/telemetry folders like
    **/.adr/**

    "docs/adr-new/**/*.md"
    - New Style Guide Enforced ADR locations
    - Temporary location until existing ADRs can be reviewed and revised to
      conform to new formatting and content standards

    Ref: ADR-0001 §(Missing) · (If needed, ADR-*-* is missing)
    """
    seen, files = set(), []
    for pattern in ADR_LOCATIONS:
        for p in root.glob(pattern):
            """
            Get the relative path from root to check for hidden dirs in ADR
            structure
            """
            try:
                rel_path = p.relative_to(root)
                # Skip any file inside a ".adr" directory or other hidden dirs
                # within the ADR structure (not the full absolute path)
                if any(part.startswith(".") for part in rel_path.parts):
                    continue
            except ValueError:
                # If we can't get relative path, skip
                continue

            rp = p.resolve()
            if rp not in seen:
                seen.add(rp)
                files.append(p)
    return sorted(files)


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------


def _run_log_path(root: Path, fmt: str) -> Path:
    """
    Return a repo-root-relative path for today's run log in the chosen format.
      - md    -> docs/adr-new/.adr/YYYY-MM-DD.md
      - jsonl -> docs/adr-new/.adr/YYYY-MM-DD.jsonl

    Ref: ADR-0001 §(Missing) · (If needed, ADR-*-* is missing)
    """
    date_str = datetime.date.today().isoformat()
    log_dir = root / "docs" / "adr-new" / ".adr"
    log_dir.mkdir(parents=True, exist_ok=True)
    ext = "md" if fmt == "md" else "jsonl"
    return log_dir / f"{date_str}.{ext}"


def _write_run_logs_md(items: List[tuple], daily_md: Path) -> None:
    """
    Append this run's lints to docs/adr-new/.adr/YYYY-MM-DD.md with a
    trailing blank line.

    Print a summary, then items grouped by file and sorted by
        (file, severity E<W<I, code, line, message).

    Ref: ADR-0001 §(Missing) · (If needed, ADR-*-* is missing)
    """
    from collections import Counter
    from itertools import groupby

    def _split_loc(loc: str) -> tuple[str, str]:
        parts = loc.split(":", 1)
        return (parts[0], parts[1] if len(parts) > 1 else "")

    sev_rank = {"E": 0, "W": 1, "I": 2}

    now = datetime.datetime.now().strftime("%H:%M:%S")
    today = datetime.date.today().isoformat()

    counts = Counter(sev for sev, _, _, _ in items)
    total = len(items)
    err = counts.get("E", 0)
    warn = counts.get("W", 0)
    info = counts.get("I", 0)

    # Build the run block
    lines = []
    lines.append(f"## Run {now}")
    lines.append("")
    lines.append("### Summary")
    lines.append("")
    lines.append(f" - Total: {total}")
    lines.append(f"   - Errors: {err}")
    lines.append(f"   - Warnings: {warn}")
    lines.append(f"   - Information: {info}")
    lines.append("")

    if not items:
        lines.append("### Clean Run")
        lines.append("")
        lines.append("No violations found.")
        lines.append("")
    else:
        lines.append("### Details")
        lines.append("")

        # Sort by (file, sev, code, line, msg)
        sorted_items = sorted(
            items,
            key=lambda t: (
                _split_loc(t[2])[0],  # file
                sev_rank.get(t[0], 9),  # severity order
                t[1],  # code
                _split_loc(t[2])[1],  # line (string; empty sorts first)
                t[3],  # message
            ),
        )

        # Group by file and print
        for file_path, group in groupby(
            sorted_items, key=lambda t: _split_loc(t[2])[0]
        ):
            lines.append(f"- {file_path}")
            for sev, code, location, msg in group:
                lines.append(f"  - [{sev}] {code}: {msg}")
            lines.append("")  # blank line between files

    block = "\n".join(lines)

    # Write/append to daily file
    if not daily_md.exists():
        daily_md.write_text(f"# ADR Lint — {today}\n\n", encoding="utf-8")
    with daily_md.open("a", encoding="utf-8") as f:
        f.write(block + "\n")


def _write_run_logs_jsonl(items: List[tuple], jsonl_path: Path) -> None:
    """
    Append one JSON object per lint to docs/adr-new/.adr/YYYY-MM-DD.jsonl.
    Schema: {"time","severity","code","location","message"}

    Ref: ADR-0001 §(Missing) · (If needed, ADR-*-* is missing)
    """
    now = datetime.datetime.now().strftime("%H:%M:%S")
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)

    with jsonl_path.open("a", encoding="utf-8") as f:
        if not items:
            # Log clean run
            rec = {
                "time": now,
                "severity": "I",
                "code": "CLEAN_RUN",
                "location": "",
                "message": "No violations found",
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        else:
            for sev, code, location, msg in items:
                rec = {
                    "time": now,
                    "severity": sev,
                    "code": code,
                    "location": location,
                    "message": msg,
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")


# Public: build index from files on disk (impure)
def build_index(files: Iterable[Path]):
    pairs: list[Tuple[Path, str]] = []
    for p in files:
        text = p.read_text(encoding="utf-8")
        pairs.append((p, text))
    return build_index_from_texts(pairs)
