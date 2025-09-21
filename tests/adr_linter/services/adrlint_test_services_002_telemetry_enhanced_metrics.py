# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/services/adrlint_test_services_002_telemetry_enhanced_metrics.py

"""
ADR-0001 · §<XXX> Linter Rules Reference
ADR-XXXX-YYYY (E? W? I?): enhanced metrics tracks title style
                          deviation → ADR-PROC-241.
Linting Tests: ADRLINT-011
"""

from __future__ import annotations

from adr_linter.report import Report
from adr_linter.services.telemetry import enhanced_metrics_tracking


def test_adrlint011_metrics_title_style_tracks_proc_241(
    _route_and_reset_workspace,
):
    # FIXME: file locations should be centralized instead of hard-coded
    #        in individual files or pytests
    metrics_path = _route_and_reset_workspace / ".adr" / "lint_metrics.json"
    if metrics_path.exists():
        metrics_path.unlink()

    meta = {
        "id": "ADR-8888",
        "title": "Bad title.",  # ends with dot → style deviation
        "status": "Proposed",
        "class": "owner",
        "date": "2025-09-03",
        "review_by": "2026-03-03",
    }
    rpt = Report()
    enhanced_metrics_tracking(
        meta,
        "Body",
        _route_and_reset_workspace / "docs/adr-new/ADR-8888.md",
        rpt,
        metrics_path,
    )
    assert any(code == "ADR-PROC-241" for _, code, _, _ in rpt.items)
    assert metrics_path.parent.is_dir()
