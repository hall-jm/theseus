# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/template/__init__.py

from .template_600_template_of_required import (
    validate_template_600_template_of_required,
)
from .template_601_status_proposed import (
    validate_template_601_status_proposed,
)
from .template_602_filename_template import (
    validate_template_602_filename_template,
)
from .template_603_no_link_graph import validate_template_603_no_link_graph
from .template_604_rfc_only_in_examples import (
    validate_template_604_rfc_only_in_examples,
)
from .template_605_mirror_section_order import (
    validate_template_605_mirror_section_order,
)

# single source for registry
TEMPLATE_RULES_PER_FILE = [
    ("ADR-TEMPLATE-600", validate_template_600_template_of_required),
    ("ADR-TEMPLATE-601", validate_template_601_status_proposed),
    ("ADR-TEMPLATE-602", validate_template_602_filename_template),
    ("ADR-TEMPLATE-603", validate_template_603_no_link_graph),
    ("ADR-TEMPLATE-604", validate_template_604_rfc_only_in_examples),
    ("ADR-TEMPLATE-605", validate_template_605_mirror_section_order),
]

TEMPLATE_RULES_POST_RUN = []

__all__ = [
    "TEMPLATE_RULES_PER_FILE",
    "TEMPLATE_RULES_POST_RUN",
]
