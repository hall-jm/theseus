# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/link/__init__.py

from .link_300_bidi_links import validate_link_300_bidi_links
from .link_301_unidi_required_pin import validate_link_301_unidi_required_pin
from .link_302_pointer_section_missing import (
    validate_link_302_pointer_section_missing,
)
from .link_303_pin_format_any_field import (
    validate_link_303_pin_format_any_field,
)
from .link_304_normative_ptr_missing import (
    validate_link_304_normative_ptr_missing,
)
from .link_305_ownership import validate_link_305_ownership

from .link_320_closure_info import validate_link_320_closure_info
from .link_321_cycle_detected import validate_link_321_cycle_detected
from .link_322_fork_no_rationale import (
    validate_link_322_fork_no_rationale_for_meta,
)

# single source for registry
LINK_RULES_PER_FILE = [
    ("ADR-LINK-300", validate_link_300_bidi_links),
    ("ADR-LINK-301", validate_link_301_unidi_required_pin),
    ("ADR-LINK-302", validate_link_302_pointer_section_missing),
    ("ADR-LINK-303", validate_link_303_pin_format_any_field),
    ("ADR-LINK-304", validate_link_304_normative_ptr_missing),
    ("ADR-LINK-305", validate_link_305_ownership),
]

LINK_RULES_POST_RUN = [
    ("ADR-LINK-320", validate_link_320_closure_info),
    ("ADR-LINK-321", validate_link_321_cycle_detected),
    ("ADR-LINK-322", validate_link_322_fork_no_rationale_for_meta),
]

__all__ = [
    "LINK_RULES_PER_FILE",
    "LINK_RULES_POST_RUN",
]
