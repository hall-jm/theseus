# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/template/__init__.py

from .template_600_template_of_required import (
    validate_template_600_template_of_required,
)
from .template_601_status_proposed import (
    validate_template_601_status_proposed,
)


# single source for registry
TEMPLATE_RULES_PER_FILE = [
    ("ADR-TEMPLATE-600", validate_template_600_template_of_required),
    ("ADR-TEMPLATE-601", validate_template_601_status_proposed),
]

TEMPLATE_RULES_POST_RUN = []

__all__ = [
    "TEMPLATE_RULES_PER_FILE",
    "TEMPLATE_RULES_POST_RUN",
]
