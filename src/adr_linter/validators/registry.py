# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/registry.py

"""
Registry that orchestrates validator execution.

R1: Introduce declarative manifests (zero behavior change).
 - ORDERED_RULES_PER_FILE is the single source of truth for per-file order.
 - run_all(ctx, rpt) now iterates ORDERED_RULES_PER_FILE.
 - ORDERED_RULES_POST_RUN documents the post-run order; post_run() continues
   to build graphs and call validators in that same order (no behavior change).

NOTE:
 - Applicability gating via policy (R2) is intentionally out-of-scope here.
 - The R1, R2, etc. labeling came from a 14-Sept-2025 ChatGPT working session
   and is not captured in any documentation like WORKPLAN.md

Ref: ADR-0001 §(Missing) · (If needed, ADR-*-* is missing)
"""

from __future__ import annotations

import os

from typing import Callable, List, Set, Tuple  # Optional,

# from ..constants import (
#     EXTENDS_RX,
#     # flake8 imported but not used issue
#     # CODES as _CODES,  # parity helpers / future tests
# )

from ..policy import (
    applies_to as _policy_applies_to,  # R2: policy-driven applicability
)
from ..services.linkgraph import build_supersede_graph

# -------------------- Top-level imports for validators -----------------------

# 1) SCHEMA (meta/front-matter)
from .schema import SCHEMA_RULES_PER_FILE  # , SCHEMA_RULES_POST_RUN

# 3) LINK (per-file)
from .link import LINK_RULES_PER_FILE, LINK_RULES_POST_RUN

# 4) DELTA (per-file)
from .delta.delta_300_override_target_missing import (
    validate_delta_300_override_target_missing,
)

# 5) NORM / META
from .norm.norm_101_rfc_outside_normative import (
    validate_norm_101_rfc_outside_normative,
)
from .norm.norm_102_vague_terms_in_normative import (
    validate_norm_102_vague_terms_in_normative,
)
from .meta import META_RULES_PER_FILE  # , LINK_RULES_POST_RUN

# 6) TEMPLATE
from .template import TEMPLATE_RULES_PER_FILE  # , TEMPLATE_RULES_POST_RUN

# -------------------- R2 diagnostics toggle (optional, no behavior change) ---

_REGISTRY_DIAG = bool(os.environ.get("ADR_REGISTRY_DIAG"))

# --------- R2 helper: driver-level applicability gating (fail-open) ----------

"""
Keep early-returns inside validators; the driver now also checks policy to
avoid calling inapplicable rules for the current document class.

Bootstrapping: these schema rules must run even if 'class' is missing/invalid,
                so we force-run them before relying on policy applicability.
"""

# TOREVIEW: Once ADR-GOVERN-* rules are active, what needs to _ALWAYS_RUN_?
_ALWAYS_RUN_CODES: Set[str] = {
    "ADR-SCHEMA-001",  # required meta
    "ADR-SCHEMA-002",  # class value
    "ADR-SCHEMA-005",  # date format
}


def _should_run(doc_class: str | None, code: str) -> bool:
    if code in _ALWAYS_RUN_CODES:
        return True
    # Defer to policy for all other rules
    try:
        return _policy_applies_to(doc_class, code)
    except Exception:
        # Defensive: if policy lookup ever fails, err on the side of running
        # (matches prior behavior where validators were called and self-gated).
        return True


def _post_should_run(idx, code: str) -> bool:
    # Post-run has no bootstrapping; check policy across classes present.

    classes_present: Set[str | None] = set()
    for _sid, info in idx.items():
        classes_present.add(info["meta"].get("class"))

    try:
        return any(_policy_applies_to(c, code) for c in classes_present)
    except Exception:
        return True


# --------- Declarative manifests (R1) ---------------------------------------

# Each entry is (ADR code, callable). Order is authoritative.
ORDERED_RULES_PER_FILE: List[Tuple[str, Callable]] = [
    # --- schema band (meta/front-matter) ---
    *SCHEMA_RULES_PER_FILE,
    # --- schema band (structure) ---
    # TOREVIEW: Removing this rule due to the new governance controls
    #           through new SCHEMA, GOVERN rules
    # ("ADR-SCHEMA-021", validate_schema_021_strategy_no_rollout),
    # --- link band (per-file) ---
    *LINK_RULES_PER_FILE,
    # --- delta band (per-file) ---
    ("ADR-DELTA-300", validate_delta_300_override_target_missing),
    # --- meta band (per-file) ---
    *META_RULES_PER_FILE,
    # --- norm band (per-file) ---
    ("ADR-NORM-101", validate_norm_101_rfc_outside_normative),
    ("ADR-NORM-102", validate_norm_102_vague_terms_in_normative),
    # --- template band (per-file) ---
    *TEMPLATE_RULES_PER_FILE,
]

# Order documentation for post-run. Execution still builds graphs below.

ORDERED_RULES_POST_RUN_PER_FILE: List[Tuple[str, Callable]] = [
    # ("ADR-LINK-320", validate_link_320_closure_info),
    # ("ADR-LINK-321", validate_link_321_cycle_detected),
    # ("ADR-LINK-322", validate_link_322_fork_no_rationale_for_meta),
    *LINK_RULES_POST_RUN,
]


# --------- Public API --------------------------------------------------------


def run_all(ctx, rpt) -> None:
    """
    Run per-file validators in the established order (manifest-driven).
    """

    doc_class = ctx.meta.get("class")
    attempted = 0
    skipped = 0
    for _code, fn in ORDERED_RULES_PER_FILE:
        attempted += 1
        if _should_run(doc_class, _code):
            fn(ctx, rpt)
        else:
            skipped += 1

    # Optional diagnostics (off by default). Set ADR_REGISTRY_DIAG=1 to see it.
    if os.getenv("ADR_REGISTRY_DIAG") == "1":
        # Keep this terse to avoid changing CLI summaries.
        print(
            f"[registry] class='{doc_class}' "
            f"attempted={attempted} skipped_by_policy={skipped}"
        )


def post_run(idx, rpt) -> None:
    """
    Run cross-file validations after per-file checks.

    Order matches ORDERED_RULES_POST_RUN. We still construct the graphs
    here because these callsites require them.
    """
    graph, reverse_graph = build_supersede_graph(idx)

    # R2: apply policy gating to post-run as well. A post-run code executes if
    # it applies to *any* class present in this run. (Current policy makes
    # LINK-220/221/222 effectively 'all', so behavior is unchanged.)

    # TOREVIEW: LLM drafted logic to have embedded def() within this def()
    #           Moved logic to 'external' _post_should_run() for now, but
    #           leaving a note for future review

    """
    classes_present: Set[str | None] = set()
    for _sid, info in idx.items():
        classes_present.add(info["meta"].get("class"))
    """

    for _code, fn in ORDERED_RULES_POST_RUN_PER_FILE:
        if not _post_should_run(idx, _code):
            continue

        if _code == "ADR-LINK-320":
            # ADR-0001 §10.4, §14
            fn(reverse_graph, idx, rpt)
        elif _code == "ADR-LINK-321":
            # ADR-0001 §10.4, §14
            fn(graph, idx, rpt)
        elif _code == "ADR-LINK-322":
            # ADR-0001 §10.4, §14
            for _sid, info in idx.items():
                fn(info["meta"], info["path"], rpt)


# --------- Manifest accessors (for tests / tooling) --------------------------
def manifest_codes_per_file() -> List[str]:
    return [code for code, _ in ORDERED_RULES_PER_FILE]


def manifest_codes_post_run() -> List[str]:
    return [code for code, _ in ORDERED_RULES_POST_RUN_PER_FILE]


def manifest_codes_all() -> List[str]:
    return manifest_codes_per_file() + manifest_codes_post_run()


# Optionally expose a callable list for meta tooling
def pipeline() -> Callable:
    return run_all
