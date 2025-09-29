# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/template/template_609_governance_real_values.py

from __future__ import annotations
import re
import yaml

from ...constants.validation import (
    CONSTRAINT_RULES_KEY_PATTERN_RX,
    detect_real_governance_values,
)

_ERROR_CODE = "ADR-TEMPLATE-609"


def validate_template_609_governance_real_values(ctx, rpt) -> None:
    """
    ADR-TEMPLATE-609 — Template contains real governance values instead of
                       placeholders.

    Ref: ADR-0001 §5.3 · ADR-TEMPLATE-609
    """
    meta = ctx.meta
    if meta.get("class") != "template":
        return

    template_of = meta.get("template_of")
    if template_of != "governance":
        return

    # Find constraint_rules section
    match = CONSTRAINT_RULES_KEY_PATTERN_RX.search(ctx.body)
    if not match:
        return  # Let TEMPLATE-607 handle missing sections

    constraint_section = match.group(1).strip()

    # Extract YAML content from fenced blocks
    yaml_pattern = re.compile(r"```yaml\s*\n(.*?)\n```", re.DOTALL)
    yaml_match = yaml_pattern.search(constraint_section)

    if not yaml_match:
        return  # No YAML constraint block found

    yaml_content = yaml_match.group(1)

    try:
        # Parse YAML content
        constraint_data = yaml.safe_load(yaml_content)
        if not isinstance(constraint_data, dict):
            return

        # Look for constraint_rules key
        if "constraint_rules" in constraint_data:
            rules = constraint_data["constraint_rules"]
            violations = detect_real_governance_values(rules)

            if violations:
                rpt.add(
                    _ERROR_CODE,
                    ctx.path,
                    "governance template contains real "
                    f"values: {violations[0]}",
                )

    except yaml.YAMLError:
        # Let other validators handle YAML syntax errors
        return
