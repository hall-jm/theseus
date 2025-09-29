# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/registry/adrlint_test_registry_002_post_run_tests_parity.py

"""
ADRLINT-meta · ADR-registry ↔ tests parity (post-run validators)

Checks that for every code in ORDERED_RULES_POST_RUN_PER_FILE there is a
corresponding test file under:
    tests/adrlinter/post_run/

Expected filename pattern:
    adrlint_test_<band-lower>_<NNN>*.py
Examples:
    tests/adrlinter/post_run/adrlint_test_link_220_closure_info.py
    tests/adrlinter/post_run/adrlint_test_link_221_cycle_detected.py
    tests/adrlinter/post_run/adrlint_test_link_222_fork_no_rationale_graph.py

Behavior:
  - Default (non-strict): if any are missing, XFAIL with a clear summary.
  - Strict: set ADR_TEST_PARITY_STRICT=1 to make missing items FAIL.

Allowlist:
  - Keep short. Use for intentionally-missing rules (e.g., known placeholder).

Notes:
  - Files ending with *_placeholder.py are **ignored** on purpose and do not
    count as coverage.
"""

from __future__ import annotations

import os
import pytest

from pathlib import Path

from adr_linter.constants import (
    CODE_RX as _CODE_RX,
    PLACEHOLDER_RX as _PLACEHOLDER_RX,
)
from adr_linter.validators.registry import (
    ORDERED_RULES_POST_RUN_PER_FILE,
)

# import adr_linter.validators.registry as reg
# print("Registry dir:", dir(reg))

# Known intentional gaps (keep small!).
# TOREVIEW: Before refactoring, ADR-LINK-202 was the only identified (known?)
#           missing pytest, but ADR-NORM-102 was also missing after this
#           refactoring started
ALLOWLIST_MISSING: set[str] = {
    # "ADR-LINK-202",
}

# Map ADR band token to validators tests subdir
# FIXME: This ADR error code bands needs to be centralized along with the
#        `rx = re.compile()` logic
BAND_DIR = {
    "SCHEMA": "schema",
    "LINK": "link",
    "DELTA": "delta",
    "META": "meta",
    "NORM": "norm",
    "TEMPLATE": "template",
}


def _tests_root() -> Path:
    """
    Locate the project tests root by walking upward until a 'tests' directory
    containing 'adrlinter' exists. Fallback: two levels up from this file.
    """
    here = Path(__file__).resolve()
    for d in [here] + list(here.parents):
        if d.name == "tests" and (d / "adr_linter").is_dir():
            return d
    # Our file lives in .../tests/adrlinter/registry/...,
    #   so parents[2] is tests/
    return here.parents[2]


def _is_placeholder(path: Path) -> bool:
    """
    True if a test filename is a placeholder we should ignore.
    Policy: any filename that ends with '_placeholder.py' is ignored.
    """
    return bool(_PLACEHOLDER_RX.search(path.name))


def _post_run_dir() -> Path:
    return _tests_root() / "adr_linter" / "post_run"


def _pattern_for(band: str, num: str) -> str:
    """
    Filename pattern we expect to find: 'adrlint_test_<band>_<NNN>*.py'
    Note: for template band, filenames use 'templt'
          (e.g., adrlint_test_templt_700_*.py)
    but the directory is 'template' (handled via BAND_DIR).
    """
    token = BAND_DIR[band]
    return f"adrlint_test_{token}_{num}*.py"


def test_adrlint1002_registry002_post_run_tests_parity():
    """
    Ensure there's at least one non-placeholder test file per per-file
    ADR code.  Non-strict by default; set ADR_TEST_PARITY_STRICT=1 to
    enforce.
    """
    results: list[tuple[str, str, str]] = []  # (code, hint, status)

    tests_dir = _post_run_dir()

    for code, _fn in ORDERED_RULES_POST_RUN_PER_FILE:
        m = _CODE_RX.match(code)
        if not m:
            continue  # Ignore non-standard codes

        band = m.group("band")
        num = m.group("num")
        pattern = _pattern_for(band, num)

        all_matches = list(tests_dir.glob(pattern))
        real_matches = [p for p in all_matches if not _is_placeholder(p)]
        placeholder_matches = [p for p in all_matches if _is_placeholder(p)]

        if real_matches:
            continue  # all good, nothing to report

        # Build display hint
        display_token = "templt" if band == "TEMPLT" else BAND_DIR[band]
        hint = (
            f"- {code}  →  {tests_dir.as_posix()}/"
            f"adrlint_test_{display_token}_{num}_<short>.py"
        )

        if placeholder_matches and code not in ALLOWLIST_MISSING:
            results.append((code, hint, "PLACEHOLDER"))
        elif not all_matches and code not in ALLOWLIST_MISSING:
            results.append((code, hint, "MISSING"))

    # if not results:
    #    return  # all good

    strict = os.getenv("ADR_TEST_PARITY_STRICT") == "1"

    summary_lines = [
        "Parity check on per-file ADR test files:",
        "  • OK           = has real pytest file(s)",
        "  • PLACEHOLDER  = only placeholder(s) exist",
        "  • MISSING      = no test file at all",
        "",
        *[
            f"  • {code} [{status}] "
            f"(expected like: {hint.split('/mirror_cli', 1)[-1].strip()})"
            for code, hint, status in results
        ],
        "",
        "How to fix quickly:",
        "  - Add a real test file matching the pattern above, OR",
        "  - If intentionally missing for now, add the ADR code to "
        "ALLOWLIST_MISSING in this test.",
        "",
        "Tip: enable strict gate with ADR_TEST_PARITY_STRICT=1 in CI once "
        "placeholders exist.",
    ]
    message = "\n".join(summary_lines)

    if strict and len(results) > 0:
        pytest.fail(message)
    elif not strict and len(results) > 0:
        pytest.xfail(message)
    else:
        assert (
            len(results) == 0
        ), f"Missing test coverage for: {[code for code, _, _ in results]}"
