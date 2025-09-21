# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/services/adrlint_test_services_001_index_loader_excludes_dot_adr.py

"""
ADR-0001 · §<XXX> Linter Rules Reference
ADR-XXXX-YYYY (E? W? I?): loader must ignore /.adr/ directories.
Linting Tests: ADRLINT-005
"""

from __future__ import annotations

from ..conftest import (
    _write_text,
    _good_meta_front_matter,
)

from adr_linter.services.index import load_files


def test_adrlint005_loader_excludes_dot_adr_dir(_route_and_reset_workspace):
    _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/.adr/2025-01-01.md",
        "# run log\n",
    )
    _write_text(
        _route_and_reset_workspace,
        "docs/adr-new/ADR-0001-demo.md",
        _good_meta_front_matter() + "Body\n",
    )

    found = load_files(_route_and_reset_workspace)
    found_rel = {
        str(p.relative_to(_route_and_reset_workspace)).replace("\\", "/")
        for p in found
    }

    assert "docs/adr-new/ADR-0001-demo.md" in found_rel
    assert not any(
        "/.adr/" in s for s in found_rel
    ), f"Found unexpected telemetry: {found_rel}"
