# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/post_run/adrlint_test_link_222_fork_no_rationale_graph.py

"""
ADR-0001 · §14 Linter Rules Reference
ADR-LINK-222 (W): Supersede closure: fork without rationale in
                  `change_history`.
Linting Tests: ADRLINT-030
"""

from __future__ import annotations

from adr_linter.report import Report
from adr_linter.services.index import load_files, build_index_from_files
from adr_linter.validators.registry import post_run
from adr_linter.validators.link.link_222_fork_no_rationale import (
    validate_link_222_fork_no_rationale_for_meta,
)

from ..conftest import (
    _write_text,
    _write_and_ctx,
    _good_meta_front_matter,
    _has_code,
    assert_warning_code,
)


"""
What sometimes looks like “two homes” is actually **two *levels of tests*
(unit vs integration) for the same rule**, which should still live in
**one home directory** that matches the **phase where the rule is executed**.

Here’s the mental model that keeps it straight:

## 1) Terms (so we don’t talk past each other)

* **Rule (atomic)** = one semantic predicate (e.g., “fork without rationale
  emits ADR-LINK-222”).
* **Predicate function** = the single callable that implements that rule
  (here: `validate_link_222_fork_no_rationale_for_meta`).
* **Orchestrator/Phase** = where the rule is executed in the pipeline:

  * **Per-file** phase → `run_all(ctx, rpt)`
  * **Post-run** phase → `post_run(idx, rpt)`

## 2) What makes a rule “atomic”

* **Exactly one predicate** (one testable truth).
* **Exactly one orchestrator phase** that invokes it in the runtime.
* Zero branching into different “modes” that change semantics.

If a predicate is invoked in **both** per-file **and** post-run phases, it’s
**not** atomic anymore; that’s two runtime contexts and likely two
responsibilities → it should be split into **two codes**. (But that’s *not*
the case for 222.)

## 3) Where ADR-LINK-222 *actually* runs

* The registry lists 222 **only** in `ORDERED_RULES_POST_RUN_PER_FILE`.
* `post_run(idx, rpt)` loops the index and applies the predicate.
* `run_all(ctx, rpt)` never calls 222.
  → Therefore, **222’s single home is the `post_run/` suite**.

## 4) Why you sometimes *see* “two homes”

Two different **test lenses** can create the illusion:

* **Integration lens**: call the **orchestrator** (`post_run`) to prove the
  pipeline wiring and index sweep work.
* **Unit lens**: call the **predicate function directly** to pin edge cases
  (rationale present, single supersede, dedupe).

Those are **two test levels**, not two homes. They both belong **under the
same home**: `tests/adrlinter/post_run/…` because that’s the rule’s runtime
phase.

## 5) Practical rule for your repo

* **Home = phase.** Put *all* ADR-LINK-222 tests in `post_run/`.
* It’s fine (and good) to have **both**:

  * an **integration** test that builds an index and calls `post_run`,
  * and **unit-ish** tests that call the predicate directly.
* Keep them in **one file** (or two small files) **within `post_run/`**. That
preserves atomicity and phase separation.

## 6) When would a rule truly need two homes?

Only if the codebase intentionally **executes the same semantic in two phases**
(per-file *and* post-run). That’s a design smell. The correct fix is **split
the semantics** and issue **two codes** (e.g., per-file quick check vs post-run
repo sweep). Until then, a single phase = a single home.

---

### TL;DR

An atomic rule can—and should—have **one home tied to its runtime phase**.
Different *test levels* (unit vs integration) for that same rule do **not**
imply different homes; they live side-by-side in the **post_run** suite for
ADR-LINK-222.
"""


# --- Integration Lens Testing ------------------------------------------------


def test_adrlint030_link222_fork_without_rationale_graph(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-030
    Rule being tested: ADR-LINK-222 — Supersede closure: fork without rationale
                                      in `change_history`.
    """
    md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-0003",
                "supersedes": ["ADR-0001", "ADR-0002"],
                "change_history": [],  # no rationale
            }
        )
        + "Body"
    )
    _write_text(
        _route_and_reset_workspace, "docs/adr-new/ADR-0003-fork.md", md
    )

    idx = build_index_from_files(load_files(_route_and_reset_workspace))
    rpt = Report()
    post_run(idx, rpt)
    assert _has_code(rpt, "ADR-LINK-222")


# --- Unit Lens Testing -------------------------------------------------------


def test_adrlint059_link222_fork_validation_consolidated_immediate(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-059
    Rule being tested: ADR-LINK-222 — fork (2+ supersedes) with empty
                       change_history → ADR-LINK-222 (warn).
    """
    md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-0003",
                "supersedes": ["ADR-0001", "ADR-0002"],
                "change_history": [],
            }
        )
        + "Body"
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "fork-immediate.md", md
    )

    rpt = Report()
    validate_link_222_fork_no_rationale_for_meta(ctx.meta, ctx.path, rpt)

    assert_warning_code(rpt, "ADR-LINK-222")


def test_adrlint060_link222_fork_validation_with_rationale(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-060
    Rule being tested: ADR-LINK-222 — fork with non-empty change_history →
                                      no ADR-LINK-222
    """
    md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-0003",
                "supersedes": ["ADR-0001", "ADR-0002"],
                "change_history": [
                    {
                        "date": "2025-09-08",
                        "by": "Engineer",
                        "note": "Rationale for the fork.",
                    }
                ],
            }
        )
        + "Body"
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "fork-with-rationale.md", md
    )

    rpt = Report()
    validate_link_222_fork_no_rationale_for_meta(ctx.meta, ctx.path, rpt)
    assert not _has_code(rpt, "ADR-LINK-222")


def test_adrlint061_link222_fork_validation_single_supersede(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-061
    Rule being tested: ADR-LINK-222 — single supersedes (not a fork) → no
                       ADR-LINK-222
    """
    md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-0002",
                "supersedes": "ADR-0001",
                "change_history": [],
            }
        )
        + "Body"
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "single-supersede.md", md
    )

    rpt = Report()
    validate_link_222_fork_no_rationale_for_meta(ctx.meta, ctx.path, rpt)

    assert not _has_code(rpt, "ADR-LINK-222")


def test_adrlint062_link222_fork_without_rationale_once(
    _route_and_reset_workspace,
):
    """
    Pre-refactored pytest: ADRLINT-063
    Rule being tested: ADR-LINK-222 — fork sans rationale → exactly one
                                      ADR-LINK-222 (warn)
    """
    md = (
        _good_meta_front_matter(
            **{
                "id": "ADR-9994",
                "title": "Fork Test",
                "class": "owner",
                "supersedes": ["ADR-0001", "ADR-0002"],
                "change_history": [],
            }
        )
        + "# Fork without rationale\nThis should trigger ADR-LINK-222 once.\n"
    )
    _, ctx = _write_and_ctx(
        _route_and_reset_workspace, "fork-without-rationale.md", md
    )

    rpt = Report()
    validate_link_222_fork_no_rationale_for_meta(ctx.meta, ctx.path, rpt)

    assert_warning_code(rpt, "ADR-LINK-222")
