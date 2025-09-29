# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/report.py

"""
Report model (moved from legacy.py).
Zero-behavior-change extraction: implementation is identical to
legacy.Report.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .constants import CODES, SEVERITY_LEVELS_REV


class Report:
    def __init__(self):
        self.items = []

    def add(
        self,
        code,
        path: Path,
        context: str = None,
        line_num: Optional[int] = None,
    ):
        # Better: fail fast on typos
        if code not in CODES:
            raise ValueError(f"Unknown lint code: {code}")
        sev, base_msg = CODES[code]

        # Use context if provided, otherwise use CODES description
        msg = context if context else base_msg

        location = f"{path.as_posix()}"
        if line_num:
            location += f":{line_num}"
        self.items.append((sev, code, location, msg))

    def has_errors(self):
        return any(sev == "E" for sev, _, _, _ in self.items)

    def has_warnings(self):
        return any(sev == "W" for sev, _, _, _ in self.items)

    def has_info(self):
        return any(sev == "I" for sev, _, _, _ in self.items)

    def print(self):
        """
        Print a summary, then items grouped by file and sorted by
        (file, severity E<W<I, code, line, message).
        """
        from collections import Counter
        from itertools import groupby

        def _split_loc(loc: str) -> tuple[str, str]:
            # Return (path, line-or-empty)
            parts = loc.split(":", 1)
            return (parts[0], parts[1] if len(parts) > 1 else "")

        # Summary
        counts = Counter(sev for sev, _, _, _ in self.items)
        total = len(self.items)
        print(
            f"Summary: total={total}  "
            f"E={counts.get('E', 0)}  W={counts.get('W', 0)}  "
            f"I={counts.get('I', 0)}"
        )
        if total:
            print()

        # Sort by (file, sev, code, line, msg)
        sorted_items = sorted(
            self.items,
            key=lambda t: (
                _split_loc(t[2])[0],  # file
                SEVERITY_LEVELS_REV.get(t[0], 9),  # severity order
                t[1],  # code
                _split_loc(t[2])[1],  # line (string; empty sorts first)
                t[3],  # message
            ),
        )

        # Group by file and print
        for file_path, group in groupby(
            sorted_items, key=lambda t: _split_loc(t[2])[0]
        ):
            print(f"report.py: [file_path] {file_path}")
            for sev, code, location, msg in group:
                print(f"report.py: [{sev}] {code}: {msg}")
            print()  # blank line between files
