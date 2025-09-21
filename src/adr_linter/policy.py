# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/policy.py

"""
Read-only policy view for ADR linter codes and applicability.

This module mirrors `constants.py` (codes, severities, titles, blocking sets)
and adds a conservative applicability matrix for documentation and gap
analysis. It is used for applicability gating in validators/registry.py.

TOREVIEW: [!?] - Need to confirm why this exists if not used in the actual
                 linter
          [??] - Need to confirm if this entry is still needed in this
                 file
"""

from __future__ import annotations

from typing import Dict, Set

from .constants import (
    CODES as _CODES,
    CODES_BLOCKING as _BLOCKING,
    CODES_WARNING as _WARNING,
    # VALID_ADR_CLASSES,  # [!?]
)

# Ordered classes for readability
CLASSES = ("owner", "delta", "strategy", "style-guide", "template")


# ---- Band policy (single source of truth for runtime expectations) ----------
# Bands that participate in the runtime validator pipeline (must be implemented
# and should have pytest coverage). Non-runtime bands (e.g. PROC) are
# documentation/telemetry only unless promoted here in the future.
BANDS_RUNTIME: Set[str] = {
    "SCHEMA",
    "NORM",
    "META",
    "LINK",
    "DELTA",
    "TEMPLATE",
}
BANDS_NON_RUNTIME: Set[str] = {"PROC"}

# ---- Codes table (mirror of constants.CODES) --------------------------------
# Shape: { "ADR-XXXX-nnn": {"severity": "E|W|I", "title": "Description"} }
CODES: Dict[str, Dict[str, str]] = {
    code: {"severity": sev, "title": title}
    for code, (sev, title) in _CODES.items()
}

# ---- Blocking / warning sets (mirror of constants) --------------------------
BLOCKING: Set[str] = set(_BLOCKING)
WARNING: Set[str] = set(_WARNING)


# ---- Applicability matrix (documentation-only) ------------------------------
# Start with "applies to all classes" then carve out obvious constraints
# that already align with current implementation:
#
# - TEMPLT-7xx apply only to class 'template' (validate_template_class early
#   returns for non-templates).
# - NORM-101 is skipped for style-guide (legacy facade early-returns).
# - SCHEMA-003 does not apply to style-guide (expected keys list is empty).
# - Link band (LINK-2xx) does not conceptually apply to style-guide per ADR,
#   but the runtime currently doesn't short-circuit; we still document the
#   intent here without wiring behavior.
#
APPLICABILITY: Dict[str, Set[str]] = {}

for code in CODES.keys():
    APPLICABILITY[code] = set(CLASSES)

    # Template-only codes
    if code.startswith("ADR-TEMPLATE-7"):
        APPLICABILITY[code] = {"template"}

    # Template-only codes
    if code.startswith("ADR-DELTA-3"):
        APPLICABILITY[code] = {"delta"}

    # Style-guide exemptions reflected in current behavior:
    if code == "ADR-NORM-101":
        APPLICABILITY[code].discard("style-guide")

    if code == "ADR-SCHEMA-003":
        APPLICABILITY[code].discard("style-guide")

    # Documented ADR intent (not enforced at runtime yet):
    if code.startswith("ADR-LINK-2"):
        APPLICABILITY[code].discard("style-guide")


def applies_to(adr_class: str, code: str) -> bool:
    """
    Return True if this code is documented as applicable to class.
    """
    classes = APPLICABILITY.get(code)
    if not classes:
        return False
    return adr_class in classes


def band_of(code: str) -> str | None:
    """
    Return the band portion of an ADR code, e.g., 'SCHEMA' for ADR-SCHEMA-001.
    """
    try:
        _adr, band, _num = code.split("-", 2)
        return band
    except Exception:
        return None


def is_runtime_code(code: str) -> bool:
    """
    True if this code belongs to a band that requires validators/tests.
    """
    b = band_of(code)
    return b in BANDS_RUNTIME if b else False
