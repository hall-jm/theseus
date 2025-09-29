# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/validators/schema/__init__.py

from .schema_001_required_meta import validate_schema_001_required_meta
from .schema_002_class_value import validate_schema_002_class_value
from .schema_003_keys_order import validate_schema_003_keys_order
from .schema_004_status_field_requirements import (
    validate_schema_004_status_field_requirements,
)
from .schema_005_date_format import validate_schema_005_date_format
from .schema_006_governance_scope import validate_schema_006_governance_scope
from .schema_007_owner_governed_by import validate_schema_007_owner_governed_by
from .schema_008_invalid_scope_value import (
    validate_schema_008_invalid_scope_value,
)
from .schema_009_class_forbidden_field import (
    validate_schema_009_class_forbidden_field,
)
from .schema_010_governance_constraint_rules import (
    validate_schema_010_governance_constraint_rules,
)
from .schema_011_owner_no_extends import (
    validate_schema_011_owner_no_extends,
)
from .schema_012_non_owner_no_owners import (
    validate_schema_012_non_owner_no_owners,
)
from .schema_013_non_owner_identify_ownership import (
    validate_schema_013_non_owner_identify_ownership,
)
from .schema_014_invalid_relationship_combination import (
    validate_schema_014_invalid_relationship_combination,
)
from .schema_015_governance_constraint_violation import (
    validate_schema_015_governance_constraint_violation,
)
from .schema_016_decision_format import (
    validate_schema_016_decision_format,
)


# single source for registry
SCHEMA_RULES_PER_FILE = [
    ("ADR-SCHEMA-001", validate_schema_001_required_meta),
    ("ADR-SCHEMA-002", validate_schema_002_class_value),
    ("ADR-SCHEMA-003", validate_schema_003_keys_order),
    ("ADR-SCHEMA-004", validate_schema_004_status_field_requirements),
    ("ADR-SCHEMA-005", validate_schema_005_date_format),
    ("ADR-SCHEMA-006", validate_schema_006_governance_scope),
    ("ADR-SCHEMA-007", validate_schema_007_owner_governed_by),
    ("ADR-SCHEMA-008", validate_schema_008_invalid_scope_value),
    ("ADR-SCHEMA-009", validate_schema_009_class_forbidden_field),
    ("ADR-SCHEMA-010", validate_schema_010_governance_constraint_rules),
    ("ADR-SCHEMA-011", validate_schema_011_owner_no_extends),
    ("ADR-SCHEMA-012", validate_schema_012_non_owner_no_owners),
    ("ADR-SCHEMA-013", validate_schema_013_non_owner_identify_ownership),
    ("ADR-SCHEMA-014", validate_schema_014_invalid_relationship_combination),
    ("ADR-SCHEMA-015", validate_schema_015_governance_constraint_violation),
    ("ADR-SCHEMA-016", validate_schema_016_decision_format),
]

SCHEMA_RULES_POST_RUN = []

__all__ = [
    "SCHEMA_RULES_PER_FILE",
    "SCHEMA_RULES_POST_RUN",
]
