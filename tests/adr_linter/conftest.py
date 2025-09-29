# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/conftest.py

"""
ADR-only test utilities & fixtures extracted from the monolith.
Scope-limited to ADR linter tests; no production behavior changes.
"""

from __future__ import annotations
import json
import re

# import datetime as dt
from datetime import (
    date as dt_date,
    timedelta as dt_timedelta,
)
from pathlib import Path
import textwrap
import pytest

from adr_linter.parser.front_matter import parse_front_matter
from adr_linter.parser.structure import (
    parse_document_structure,
    expected_keys_for,
)
from adr_linter.models import ValidationData
from adr_linter.report import Report  # noqa: F401
from adr_linter.constants import CODES as K_CODES  # for assert helpers


# --- marker registration (avoid warnings when placeholders run) --------------


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "adrlint_placeholder: placeholder test for an ADR rule whose real "
        "tests are pending refactor",
    )


# -----------------------------
# Autouse workspace fixture
# -----------------------------
@pytest.fixture(autouse=False)
def _route_and_reset_workspace(tmp_path: Path, request):
    """
    1) Anchor at project root
    2) Date bucket (YYYY-MM-DD) + per-test subdirectory
    3) Filesystem-safe name derived from nodeid
    """
    project_root = (
        Path(__file__).resolve().parents[2]
    )  # project_root -> projects/mirror_cli/
    day = dt_date.today().isoformat()
    base_dir = project_root / "logs" / ".pytest" / "adr_linter" / day
    nodeid = request.node.nodeid
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", nodeid)
    safe = re.sub(r"^.*?\.py_", "", safe)
    test_dir = base_dir / safe
    test_dir.mkdir(parents=True, exist_ok=True)
    return test_dir


# -----------------------------
# Helpers (file + context)
# -----------------------------
def _write_text(base: Path, rel: str, text: str) -> Path:
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def _ctx_from_path(p: Path) -> ValidationData:
    raw = p.read_text(encoding="utf-8")
    meta, end = parse_front_matter(raw)
    body = raw[end:]
    sec = parse_document_structure(body)
    return ValidationData(
        meta=meta, body=body, path=p, section_data=sec, all_idx={}
    )


def _write_and_ctx(root_dir: Path, filename: str, content: str):
    p = _write_text(root_dir, filename, content)
    ctx = _ctx_from_path(p)
    return p, ctx


def _dynamic_meta_dates():
    """
    Generate test-appropriate dates that don't break over time.
    """
    today = dt_date.today()
    return {
        "date": today.strftime("%Y-%m-%d"),
        "review_by": (today + dt_timedelta(days=30)).strftime("%Y-%m-%d"),
    }


def _good_meta_front_matter(**overrides) -> str:
    fm = {
        "id": "ADR-1234",
        "title": "Short Title",
        "status": "Proposed",
        "class": "owner",
        **_dynamic_meta_dates(),  # Always current dates
        # "date": "2025-09-03",
        # "review_by": "2026-03-03",
    }
    fm.update(overrides)
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            lines.append(f"{k}: {json.dumps(v)}")
        elif v is None:
            lines.append(f"{k}:")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def _good_body_structure(adr_class: str, template_of: str = None) -> str:
    """
    Generate valid body structure with all required canonical sections.
    """

    expected_keys = expected_keys_for(adr_class, template_of)
    if not expected_keys:
        return ""  # Style-guide or invalid class

    sections = []
    for key in expected_keys:
        # Add section key marker
        sections.append(f"<!-- key: {key} -->")

        # Add corresponding markdown header
        header_text = _get_header_text_for_key(key)
        sections.append(f"## {header_text}")

        # Special content for decision_one_liner to satisfy SCHEMA-016
        if key == "decision_one_liner":
            decision_one_liner = "Because testing requires valid format, we choose compliant structure so that validation passes."  # noqa:E501
            sections.append(decision_one_liner)
        else:
            sections.append(f"{key.replace('_', ' ').title()} content.")
        sections.append("")  # Empty line

    return "\n".join(sections)


def _get_header_text_for_key(key: str) -> str:
    """Get appropriate header text for section key."""
    from adr_linter.constants.sections import HEADING_ALIASES

    # Find first alias that maps to this key
    for header_text, mapped_key in HEADING_ALIASES.items():
        if mapped_key == key:
            return header_text

    # Fallback to title case conversion
    return key.replace("_", " ").title()


# -----------------------------
# Assert helpers (report codes)
# -----------------------------


def _has_code(rpt, code: str) -> bool:
    return any(c == code for _, c, _, _ in rpt.items)


def assert_error_code(rpt, code: str):
    assert code in K_CODES, (
        "[conftest.py] Test references code not listed in "
        f"constants.codes: {code}"
    )
    assert (
        K_CODES[code][0] == "E"
    ), f"[conftest.py] Code {code} is not an error"
    assert _has_code(
        rpt, code
    ), f"[conftest.py] Expected error code {code} not found in report"


def assert_warning_code(rpt, code: str):
    assert code in K_CODES, (
        "[conftest.py] Test references code not listed in "
        f"constants.codes: {code}"
    )
    assert (
        K_CODES[code][0] == "W"
    ), f"[conftest.py] Code {code} is not a warning"
    assert _has_code(
        rpt, code
    ), f"[conftest.py] Expected warning code {code} not found in report"


def assert_info_code(rpt, code: str):
    assert code in K_CODES, (
        f"[conftest.py] Test references code not listed in "
        f"constants.codes: {code}"
    )
    assert (
        K_CODES[code][0] == "I"
    ), f"[conftest.py] Code {code} is not informative"
    assert _has_code(
        rpt, code
    ), f"[conftest.py] Expected informative code {code} not found in report"


# -----------------------------
# Sample ADR bodies (string fixtures)
# -----------------------------
STYLE_GUIDE = textwrap.dedent(
    """\
    ---
    id: ADR-9999
    title: SG
    status: Proposed
    class: style-guide
    date: 2025-09-05
    review_by: 2026-01-01
    ---
    # Style Guide
    MUST and SHOULD may appear here; this class is exempt from RFC scanning.
    """
)


BAD_DATES = textwrap.dedent(
    """\
    ---
    id: ADR-9998
    title: Bad Dates
    status: Proposed
    class: owner
    date: 2025/09/05
    review_by: 2026-13-01
    ---
    Body
    """
)


EXTENDS_NO_PIN = textwrap.dedent(
    """\
    ---
    id: ADR-9997
    title: Extends No Pin
    status: Proposed
    class: delta
    extends: ADR-0001
    date: 2025-09-05
    review_by: 2026-01-01
    ---
    Body
    """
)


RFC_OUTSIDE_NORM = textwrap.dedent(
    """\
    ---
    id: ADR-9996
    title: RFC case
    status: Proposed
    class: owner
    date: 2025-09-05
    review_by: 2026-01-01
    ---
    Outside normative sections we SHOULD trigger a violation.
    """
)


NO_GOVERNANCE = textwrap.dedent(
    """\
    ---
    id: ADR-9995
    title: Strategy Without Governance
    status: Proposed
    class: strategy
    date: 2025-09-11
    review_by: 2026-03-11
    ---
    # Strategy ADR Missing owners_ptr
    This should trigger ADR-LINK-205 because it's a strategy class without
    owners_ptr.
    """
)


NO_EXTENDS = textwrap.dedent(
    """\
    ---
    id: ADR-9994
    title: Delta Without Extends
    status: Proposed
    class: delta
    date: 2025-09-11
    review_by: 2026-03-11
    ---
    # Delta ADR Missing extends
    This should trigger ADR-LINK-205 because it's a delta class without
    extends.
    """
)


FORK_WITHOUT_RATIONALE = textwrap.dedent(
    """\
    ---
    id: ADR-9994
    title: Fork Test
    status: Proposed
    class: owner
    supersedes: ["ADR-0001", "ADR-0002"]
    change_history: []
    date: 2025-09-11
    review_by: 2026-03-11
    ---
    # Fork without rationale
    This should trigger ADR-LINK-222 exactly once, not twice.
    """
)
