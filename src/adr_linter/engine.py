# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/engine.py

"""
TOREVIEW: [!?] - Need to confirm why this exists if not used in the actual
                 linter
          [??] - Need to confirm if this entry is still needed in this
                 file
"""

from __future__ import annotations


from pathlib import Path
from typing import Optional

from .constants import (
    SEVERITY_LEVELS,
)

from .filters import compile_k

from .models import ValidationContext

from .parser.front_matter import parse_front_matter

from .parser.structure import (
    parse_document_structure,
)

from .report import Report

from .services.index import (
    build_index_from_files,
    load_files,
    read_text as service_read_text,
)

from .services.telemetry import (
    _run_log_path,
    _write_run_logs_md,
    _write_run_logs_jsonl,
    ensure_metrics_file,
    enhanced_metrics_tracking,
)

from .validators.registry import (
    run_all as _run_all_validators,
    post_run as _post_run_validators,
)


def run(
    path: str = ".",
    fail_on: str = "E",
    k_expr: Optional[str] = None,
    emit_metrics: bool = False,
    fmt: str = "md",
) -> int:
    root = Path(path)
    all_files = load_files(root)

    files = all_files
    if k_expr:
        pred = compile_k(k_expr)
        files = [p for p in all_files if pred(p)]

    rpt = Report()
    """
    Build full index from all discovered files (impure call in services.index)
    """
    idx = build_index_from_files(all_files)

    run_log_path = _run_log_path(root, fmt)

    # TODO: Centralized hard-coded variables and values like metrics_path
    # TOREVIEW: Have this logic moved to telemetry.py if values need
    #           to be created or set during runtime
    metrics_path = (
        (root / "logs" / ".adr" / "lint_metrics.json")
        if emit_metrics
        else None
    )
    if metrics_path:
        ensure_metrics_file(metrics_path)

    for p in files:
        """
        Keep the existing double-read behavior; route through services to
        keep engine pure.  i.e., service wrapper

        The current approach reads files twice - once for indexing and once
        for validation. While this seems wasteful, it provides isolation
        between the index-building phase and the validation phase.
        """

        text = service_read_text(p, encoding="utf-8")
        meta, end = parse_front_matter(text)
        body = text[end:]
        section_info = parse_document_structure(body)

        ctx = ValidationContext(
            meta=meta,
            body=body,
            path=p,
            section_info=section_info,
            all_idx=idx,
        )

        _run_all_validators(ctx, rpt)

        enhanced_metrics_tracking(meta, body, p, rpt, metrics_path)

    _post_run_validators(idx, rpt)

    if emit_metrics:
        # Append run logs in chosen format
        if fmt == "md":
            _write_run_logs_md(rpt.items, run_log_path)
        else:
            _write_run_logs_jsonl(rpt.items, run_log_path)

    # print and compute exit code exactly like today
    rpt.print()
    threshold = SEVERITY_LEVELS[fail_on]
    for sev, _, _, _ in rpt.items:
        if SEVERITY_LEVELS.get(sev, 0) >= threshold:
            return 1
    return 0
