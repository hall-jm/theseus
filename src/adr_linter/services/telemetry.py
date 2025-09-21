# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/services/telemetry.py

"""
Run-log writers and metrics file bootstrap (impure).
Behavior and formatting identical to prior implementations.

Ref: ADR-0001 §(Missing) · (If needed, ADR-*-* is missing)
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import List, Optional

from ..report import Report


def _run_log_path(root: Path, fmt: str) -> Path:
    """
    Return a repo-root-relative path for today's run log in the chosen format.
      - md    -> docs/adr-new/.adr/YYYY-MM-DD.md
      - jsonl -> docs/adr-new/.adr/YYYY-MM-DD.jsonl
    """
    date_str = datetime.date.today().isoformat()
    log_dir = root / "docs" / "adr-new" / ".adr"
    log_dir.mkdir(parents=True, exist_ok=True)
    ext = "md" if fmt == "md" else "jsonl"
    return log_dir / f"{date_str}.{ext}"


def _write_run_logs_md(items: List[tuple], daily_md: Path) -> None:
    """
    Append this run's lints to docs/adr-new/.adr/YYYY-MM-DD.md with a
    trailing blank line. Print a summary, then items grouped by file and
    sorted by (file, sev, code, line, msg).
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

        sorted_items = sorted(
            items,
            key=lambda t: (
                _split_loc(t[2])[0],
                sev_rank.get(t[0], 9),
                t[1],
                _split_loc(t[2])[1],
                t[3],
            ),
        )

        for file_path, group in groupby(
            sorted_items, key=lambda t: _split_loc(t[2])[0]
        ):
            lines.append(f"- {file_path}")
            for sev, code, location, msg in group:
                lines.append(f"  - [{sev}] {code}: {msg}")
            lines.append("")

    block = "\n".join(lines)

    if not daily_md.exists():
        daily_md.write_text(f"# ADR Lint — {today}\n\n", encoding="utf-8")
    with daily_md.open("a", encoding="utf-8") as f:
        f.write(block + "\n")


def _write_run_logs_jsonl(items: List[tuple], jsonl_path: Path) -> None:
    """
    Append one JSON object per lint to docs/adr-new/.adr/YYYY-MM-DD.jsonl.
    Schema: {"time","severity","code","location","message"}
    """
    now = datetime.datetime.now().strftime("%H:%M:%S")
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)

    with jsonl_path.open("a", encoding="utf-8") as f:
        if not items:
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


# -----------------------------------------------------------------------------
# Metrics Read/Write
# -----------------------------------------------------------------------------


def ensure_metrics_file(metrics_path: Path) -> None:
    """
    Ensure the metrics JSON file exists with '{}' if requested.
    Mirrors prior behavior in engine.py.
    """
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    if not metrics_path.exists():
        metrics_path.write_text("{}", encoding="utf-8")


# TOREVIEW: Figure out a graceful way forward to ensure file I/O is running
#           through io.py and also handling error codes like ADR-PROC-241


def enhanced_metrics_tracking(
    meta,
    body,
    path,
    rpt: Report,
    metrics_path: Optional[Path] = None,
    metrics_scope: str = "style",
):
    """
    Enhanced metrics with configurable scope
    """
    if not metrics_path:
        return

    # Current implementation focuses on style, but framework for expansion
    issues_to_track = []

    # Style issues
    title = meta.get("title", "")
    if title and (not title[0].isupper() or title.endswith(".")):
        issues_to_track.append(("ADR-PROC-241", "title style"))

    # Future: track other issues based on metrics_scope
    if metrics_scope in ("warn", "all"):
        # Could track warning-level issues for trend analysis
        pass

    if metrics_scope == "all":
        # Could track all issues for comprehensive governance metrics
        pass

    # Process tracked issues
    if not issues_to_track:
        return

    # Load existing metrics
    data = {}
    if metrics_path.exists():
        try:
            data = json.loads(metrics_path.read_text("utf-8"))
        except Exception:
            data = {}

    stamp = datetime.date.today().isoformat()

    for code, issue_type in issues_to_track:
        # Record the issue
        file_key = path.as_posix()
        if code not in data:
            data[code] = {}
        if file_key not in data[code]:
            data[code][file_key] = []

        data[code][file_key].append({"date": stamp, "type": issue_type})
        data[code][file_key] = data[code][file_key][-20:]  # Keep last 20

        # Check for escalation (3+ in 30 days)
        recent = [
            entry
            for entry in data[code][file_key]
            if (
                datetime.date.fromisoformat(stamp)
                - datetime.date.fromisoformat(entry["date"])
            ).days
            <= 30
        ]

        if len(recent) >= 3:
            rpt.add(
                "ADR-PROC-242",
                path,
                f"repeated {issue_type} deviation (≥3 in 30d)",
            )
        else:
            rpt.add(code, path, f"{issue_type} deviation")

    # Write updated metrics
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
