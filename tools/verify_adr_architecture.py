# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tools/adr_verify__architecture.py
"""
Systematic verification scripts for ADR linter architecture gaps.
Targets actual patterns found in the refactored codebase.


**Critical assumption flaws Claude made:**

1. **"Orphaned Tests" category is fundamentally wrong** - The 12
   "orphaned" tests (POLICY, REGISTRY, SERVICES, FILTERS, PARSER)
   aren't orphaned at all. They're testing the linter's infrastructure
   components, not validation rules. This script assumed everything
   should map to `ORDERED_RULES_PER_FILE`, but the ADR linter has
   meta-tests for the architecture itself.

2. **Missing context about your refactoring scope** - I assumed all tests
   should correspond to validators in the registry, but you likely have:
   - Infrastructure tests (registry, policy, services)
   - Utility tests (filters, parser)
   - Meta-tests that verify the linter's own consistency

3. **Charset handling reveals real environment issues** - The `'charmap'
   codec can't decode` errors suggest actual file encoding problems, not
   architectural gaps.

4. **Template naming "inconsistencies" might be intentional**
   - `validate_templt_700` vs `template_700_template_of_required.py` could
     be deliberate shortening, not drift.

**What the script IS correctly identifying:**
- Placeholder tests (definitely real gaps)
- Missing tests for ADR-LINK-200 and ADR-DELTA-300 (likely real gaps)
- Registry files that reference codes without assertions (likely real problems)

**Better questions my script should answer:**
- Which validation rules have zero test coverage vs infrastructure components?
- Are there missing validators for codes referenced in your policy system?
- Do thest meta-tests (registry parity checks) actually validate what they
  claim to?
"""

import ast

# import os
import re
import sys

from pathlib import Path
from typing import Dict, List, Set, Optional  # Tuple,

# import importlib.util

from adr_linter.constants import CODES_INFRA


class ArchitectureVerifier:
    def __init__(self, root_path: str):
        self.root = Path(root_path)
        self.tools_path = self.root / "src" / "adr_linter"
        self.tests_path = self.root / "tests" / "adr_linter"

    def verify_all(self) -> Dict[str, List[str]]:
        """Run all verification checks and return issues found."""
        issues = {}

        print(
            "🔍 Running systematic architecture verification...",
            file=sys.stderr,
        )

        issues["registry_import_drift"] = self.check_registry_import_drift()
        issues["policy_constants_drift"] = self.check_policy_constants_drift()
        issues["placeholder_tests"] = self.find_placeholder_tests()
        issues["test_validator_pairing"] = self.check_test_validator_pairing()
        issues["missing_test_coverage"] = self.find_missing_test_coverage()
        issues["orphaned_tests"] = self.find_orphaned_tests()
        issues["phase_mismatches"] = self.check_phase_mismatches()
        issues["naming_inconsistencies"] = self.check_naming_inconsistencies()

        return issues

    def check_registry_import_drift(self) -> List[str]:
        """
        Verify all registry imports actually resolve to existing functions.
        """
        issues = []
        registry_path = self.tools_path / "validators" / "registry.py"

        if not registry_path.exists():
            return [f"Registry file not found: {registry_path}"]

        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            # Extract imports and their aliases
            imports = {}
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        for alias in node.names:
                            imports[alias.asname or alias.name] = {
                                "module": node.module,
                                "name": alias.name,
                            }

            # Extract registry entries
            registry_functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id in [
                            "ORDERED_RULES_PER_FILE",
                            "ORDERED_RULES_POST_RUN_PER_FILE",
                        ]:
                            if isinstance(node.value, ast.List):
                                for item in node.value.elts:
                                    if (
                                        isinstance(item, ast.Tuple)
                                        and len(item.elts) == 2
                                    ):
                                        func_name = item.elts[1]
                                        if isinstance(func_name, ast.Name):
                                            registry_functions.append(
                                                func_name.id
                                            )

            # Check if imported functions exist
            for func_name in registry_functions:
                if func_name not in imports:
                    issues.append(
                        f"Function '{func_name}' used in registry but not "
                        "imported"
                    )
                else:
                    # Try to resolve the actual file
                    import_info = imports[func_name]
                    expected_path = self._resolve_import_path(
                        import_info["module"]
                    )
                    if expected_path and not expected_path.exists():
                        issues.append(
                            f"Import '{func_name}' points to non-existent "
                            f"file: {expected_path}"
                        )

        except Exception as e:
            issues.append(f"Error parsing registry: {e}")

        return issues

    def check_policy_constants_drift(self) -> List[str]:
        """Check if policy.py mirrors constants.py correctly."""
        issues = []

        policy_path = self.tools_path / "policy.py"
        constants_path = self.tools_path / "constants.py"

        if not policy_path.exists():
            return [f"Policy file not found: {policy_path}"]

        if not constants_path.exists():
            return [f"Constants file not found: {constants_path}"]

        try:
            # Check if policy imports from constants correctly
            with open(policy_path, "r", encoding="utf-8") as f:
                policy_content = f.read()

            # Look for import statements
            if "from .constants import" not in policy_content:
                issues.append("Policy does not import from constants")

            # Check for expected imports
            expected_imports = ["CODES", "CODES_BLOCKING", "CODES_WARNING"]
            for imp in expected_imports:
                if (
                    f"{imp} as _" not in policy_content
                    and f"{imp}" not in policy_content
                ):
                    issues.append(f"Policy missing import: {imp}")

        except Exception as e:
            issues.append(f"Error checking policy-constants drift: {e}")

        return issues

    def find_placeholder_tests(self) -> List[str]:
        """Find test files that are placeholders with no real assertions."""
        placeholders = []

        for test_file in self.tests_path.rglob("*.py"):
            if not test_file.name.startswith(
                "test_"
            ) and not test_file.name.startswith("adrlint_test_"):
                continue

            try:
                with open(test_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check for placeholder markers
                is_placeholder = False
                placeholder_reasons = []

                if "@pytest.mark.adrlint_placeholder" in content:
                    is_placeholder = True
                    placeholder_reasons.append(
                        "has @pytest.mark.adrlint_placeholder"
                    )

                if 'reason="Placeholder:' in content:
                    is_placeholder = True
                    placeholder_reasons.append(
                        "has skip reason containing 'Placeholder:'"
                    )

                if "intentionally not implemented" in content:
                    is_placeholder = True
                    placeholder_reasons.append(
                        "contains 'intentionally not implemented'"
                    )

                # Check for minimal test content
                if "assert True" in content and content.count("assert") == 1:
                    is_placeholder = True
                    placeholder_reasons.append("only contains 'assert True'")

                if is_placeholder:
                    relative_path = test_file.relative_to(self.root)
                    placeholders.append(
                        f"{relative_path}: {', '.join(placeholder_reasons)}"
                    )

            except Exception as e:
                relative_path = test_file.relative_to(self.root)
                placeholders.append(
                    f"{relative_path}: Error reading file - {e}"
                )

        return placeholders

    def check_test_validator_pairing(self) -> List[str]:
        """Check if validators have corresponding test files."""
        issues = []

        # Get all validator codes from registry
        registry_codes = self._extract_registry_codes()

        # Get all test files and extract codes they test
        test_codes = self._extract_test_codes()

        # Find validators without tests
        missing_tests = registry_codes - test_codes
        for code in missing_tests:
            issues.append(f"Validator {code} has no corresponding test file")

        return issues

    def find_missing_test_coverage(self) -> List[str]:
        """
        Find test files that reference codes but don't actually test them.
        """
        issues = []

        for test_file in self.tests_path.rglob("*.py"):
            if not test_file.name.startswith("adrlint_test_"):
                continue

            try:
                with open(test_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extract ADR codes mentioned in filename or content
                filename_codes = re.findall(
                    r"ADR-[A-Z]+-\d+", test_file.name.upper()
                )
                content_codes = re.findall(r"ADR-[A-Z]+-\d+", content)

                all_mentioned_codes = set(filename_codes + content_codes)

                # Check if there are actual test functions
                tree = ast.parse(content)

                # TOREVIEW: Created code but never used.  Why?
                """
                test_functions = [
                    node.name
                    for node in ast.walk(tree)
                    if isinstance(node, ast.FunctionDef)
                    and node.name.startswith("test_")
                ]
                """

                # Check for assertions in test functions
                has_real_assertions = False
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assert):
                        # Skip trivial assertions
                        if (
                            isinstance(node.test, ast.Constant)
                            and node.test.value is True
                        ):
                            continue
                        has_real_assertions = True
                        break

                if all_mentioned_codes and not has_real_assertions:
                    relative_path = test_file.relative_to(self.root)
                    codes_str = ", ".join(sorted(all_mentioned_codes))
                    issues.append(
                        f"{relative_path}: mentions codes {codes_str} but has "
                        "no real assertions"
                    )

            except Exception as e:
                relative_path = test_file.relative_to(self.root)
                issues.append(f"{relative_path}: Error analyzing - {e}")

        return issues

    def find_orphaned_tests(self) -> List[str]:
        """
        Find test files that don't correspond to any validator in registry.

        For LLMs:
        "Orphaned Tests" category is fundamentally wrong - The "orphaned" tests
        (POLICY, REGISTRY, SERVICES, FILTERS, PARSER) aren't orphaned at all.
        They're testing the linter's infrastructure components, not validation
        rules.

        This script assumed everything should map to ORDERED_RULES_PER_FILE,
        but this ADR linter has meta-tests for the architecture itself.
        """
        issues = []

        registry_codes = self._extract_registry_codes()

        for test_file in self.tests_path.rglob("*.py"):
            if not test_file.name.startswith("adrlint_test_"):
                continue

            # Extract codes from test filename
            filename_codes = re.findall(
                r"ADR-[A-Z]+-\d+", test_file.name.upper()
            )

            # Convert schema_001 style to ADR-SCHEMA-001
            name_parts = test_file.stem.split("_")
            if len(name_parts) >= 4:  # adrlint_test_schema_001_...
                band = name_parts[2].upper()
                number = name_parts[3]
                potential_code = f"ADR-{band}-{number}"
                filename_codes.append(potential_code)

            # Check for codes that aren't in registry OR infrastructure
            unknown_codes = set(filename_codes) - registry_codes - CODES_INFRA
            if unknown_codes:
                relative_path = test_file.relative_to(self.root)
                codes_str = ", ".join(sorted(unknown_codes))
                issues.append(
                    f"{relative_path}: tests codes {codes_str} not in "
                    "registry or infrastructure"
                )

        return issues

    def check_phase_mismatches(self) -> List[str]:
        """
        Check if validators are in the correct execution phase and tests are in
        correct directories.
        """
        issues = []

        registry_path = self.tools_path / "validators" / "registry.py"
        if not registry_path.exists():
            return ["Registry file not found"]

        with open(registry_path, "r", encoding="utf-8") as f:
            content = f.read()

        per_file_codes = set()
        post_run_codes = set()

        # Extract per-file and post-run validators
        # Find the start of ORDERED_RULES_PER_FILE
        start_match = re.search(
            r"ORDERED_RULES_PER_FILE.*?=.*?\[", content, re.DOTALL
        )
        if start_match:
            remaining_content = content[start_match.end() :]
            # Find where this list ends (closing bracket followed by newline)
            end_match = re.search(r"\]\s*$", remaining_content, re.MULTILINE)
            if end_match:
                per_file_section = remaining_content[: end_match.start()]
                per_file_codes = set(
                    re.findall(r'"(ADR-[A-Z]+-\d+)"', per_file_section)
                )
            else:
                per_file_codes = set(
                    re.findall(r'"(ADR-[A-Z]+-\d+)"', remaining_content)
                )

        # Extract per-file and post-run validators
        # per_file_match = re.search(
        #     r"ORDERED_RULES_PER_FILE.*?=.*?\[(.*?)\]", content, re.DOTALL
        # )
        post_run_match = re.search(
            r"ORDERED_RULES_POST_RUN_PER_FILE.*?=.*?\[(.*?)\]",
            content,
            re.DOTALL,
        )

        # if per_file_match:
        #     per_file_codes = set(
        #         re.findall(r'"(ADR-[^"]+)"', per_file_match.group(1))
        #     )
        if post_run_match:
            post_run_codes = set(
                re.findall(r'"(ADR-[^"]+)"', post_run_match.group(1))
            )

        # Check for validators that might be in wrong phase
        for code in per_file_codes:
            if (
                "graph" in code.lower()
                or "cycle" in code.lower()
                or "closure" in code.lower()
            ):
                issues.append(
                    f"{code} in per-file phase but seems to need graph data"
                )

        # Check test directory placement
        for test_file in self.tests_path.rglob("*.py"):
            if not test_file.name.startswith("adrlint_test_"):
                continue

            try:
                with open(test_file, "r", encoding="utf-8") as f:
                    test_content = f.read()

                test_codes = set(re.findall(r"ADR-[A-Z]+-\d+", test_content))
                is_in_validators = "validators" in test_file.parts
                is_in_post_run = "post_run" in test_file.parts

                for code in test_codes:
                    if code in post_run_codes and is_in_validators:
                        relative_path = test_file.relative_to(self.root)
                        issues.append(
                            f"{relative_path}: tests {code} (post-run rule) "
                            "but in validators/ directory"
                        )
                    # Check for per-file codes in post_run directory
                    elif code in per_file_codes and is_in_post_run:
                        relative_path = test_file.relative_to(self.root)
                        issues.append(
                            f"{relative_path}: tests {code} (per-file rule) "
                            "but in post_run/ directory"
                        )

            except Exception as e:
                print(f"Exception: {e}")
                continue

        return issues

    def check_naming_inconsistencies(self) -> List[str]:
        """
        Find naming inconsistencies between imports and actual function names.
        """
        issues = []

        # This would require parsing validator files to check function names
        # vs registry imports - placeholder for now

        validators_path = self.tools_path / "validators"
        if not validators_path.exists():
            return ["Validators directory not found"]

        # Check for common naming patterns
        for validator_file in validators_path.rglob("*.py"):
            if validator_file.name == "__init__.py":
                continue

            try:
                with open(validator_file, "r", encoding="utf-8") as f:
                    content = f.read()

                tree = ast.parse(content)

                # Extract function definitions
                functions = [
                    node.name
                    for node in ast.walk(tree)
                    if isinstance(node, ast.FunctionDef)
                    and node.name.startswith("validate_")
                ]

                # Check if filename matches function name pattern
                expected_prefix = validator_file.stem.replace("-", "_")

                matching_functions = [
                    f for f in functions if expected_prefix in f
                ]
                if functions and not matching_functions:
                    relative_path = validator_file.relative_to(self.root)
                    issues.append(
                        f"{relative_path}: function names {functions} don't "
                        "match filename pattern"
                    )

            except Exception as e:
                relative_path = validator_file.relative_to(self.root)
                issues.append(f"{relative_path}: Error checking naming - {e}")

        return issues

    def _extract_registry_codes(self) -> Set[str]:
        """Extract all validator codes from registry manifests."""
        codes = set()

        registry_path = self.tools_path / "validators" / "registry.py"
        if not registry_path.exists():
            return codes

        with open(registry_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract codes from both manifests
        code_matches = re.findall(r'"(ADR-[A-Z]+-\d+)"', content)
        codes.update(code_matches)

        return codes

    def _extract_test_codes(self) -> Set[str]:
        """Extract all codes that have test files."""
        codes = set()

        for test_file in self.tests_path.rglob("*.py"):
            if not test_file.name.startswith("adrlint_test_"):
                continue

            # Extract from filename
            filename_codes = re.findall(
                r"ADR-[A-Z]+-\d+", test_file.name.upper()
            )
            codes.update(filename_codes)

            # Convert pattern like schema_001 to ADR-SCHEMA-001
            name_parts = test_file.stem.split("_")
            if len(name_parts) >= 4:  # adrlint_test_schema_001_...
                try:
                    band = name_parts[2].upper()
                    number = name_parts[3]
                    if number.isdigit():
                        code = f"ADR-{band}-{number.zfill(3)}"
                        codes.add(code)
                except (IndexError, ValueError):
                    pass

        return codes

    def _resolve_import_path(self, module_path: str) -> Optional[Path]:
        """Resolve a relative import to actual file path."""
        if module_path.startswith("."):
            # Relative import from validators/
            parts = module_path.split(".")
            if parts[0] == "":
                parts = parts[1:]  # Remove empty first element

            path = self.tools_path / "validators"
            for part in parts[1:]:  # Skip first dot
                path = path / part

            return path.with_suffix(".py")

        return None


def output_context_documentation():
    """
    Output context documentation for LLM consumption about this script.
    """
    context = {
        "script_purpose": "Detects architectural drift in refactored ADR "
        "linter codebase",
        "intended_audience": "LLMs like Claude, GPT, Copilot",
        "creation_context": "Built after discovering systematic gaps between "
        "assumed vs. actual test coverage during modular refactoring",
        "reliable_detections": [
            "Missing test files for implemented validators",
            "Placeholder tests that need real implementations",
            "Tests in wrong execution phase directories "
            "(per-file vs post-run)",
            "Infrastructure vs business validation code categorization",
        ],
        "known_limitations": [
            "Regex patterns are brittle and break on registry.py formatting "
            "changes",
            "Only works with specific ORDERED_RULES_* structure patterns",
            "Cannot detect semantic correctness of tests, only structural "
            "presence",
            "Requires manual updates when new code categories are added to "
            "constants.py",
        ],
        "llm_guidance": {
            "before_changes": "Run --json mode to get structured "
            "architectural health baseline",
            "prioritization": "If total_issues > 0, address structural gaps "
            "before adding features",
            "coverage_verification": "Don't assume test coverage exists just "
            "because files exist - check for placeholders",
            "issue_triage": "Distinguish business validation gaps (tier 1) vs "
            "style inconsistencies (tier 3)",
        },
        "red_flags": [
            "Script reports 0 issues but human reports incomplete coverage = "
            "script has blind spots",
            "Phase mismatch count suddenly changes = regex extraction broke",
            "New 'orphaned tests' appearing = CODES_INFRA categorization "
            "needs updating",
        ],
        "meta_lesson": "This script itself required multiple debugging rounds "
        "due to incorrect assumptions about data patterns. Verification "
        "tooling is not immune to the same drift problems it's designed to "
        "detect.",
        "debugging_history": [
            "Initially miscategorized infrastructure tests as 'orphaned'",
            "Regex extraction captured codes from wrong registry sections",
            "Phase mismatch logic had inverted classification",
            "UTF-8 encoding issues on Windows/mingw64 environments",
        ],
    }

    return context


def main():
    """Run verification and report issues."""
    import json
    import argparse

    parser = argparse.ArgumentParser(
        description="Verify ADR linter architecture"
    )
    parser.add_argument(
        "root_path", nargs="?", default=".", help="Root path to analyze"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON format for LLM consumption",
    )
    parser.add_argument(
        "--context-doc",
        action="store_true",
        help="Output context documentation for LLM consumption about this "
        "script's purpose and limitations",
    )

    args = parser.parse_args()

    if args.context_doc:
        print(json.dumps(output_context_documentation(), indent=2))
        sys.exit(0)

    verifier = ArchitectureVerifier(args.root_path)
    all_issues = verifier.verify_all()

    total_issues = sum(len(issues) for issues in all_issues.values())

    if args.json:
        # JSON output for LLM consumption
        output = {
            "timestamp": __import__("datetime").datetime.now().isoformat(),
            "root_path": str(args.root_path),
            "summary": {
                "total_issues": total_issues,
                "checks_with_issues": sum(
                    1 for issues in all_issues.values() if issues
                ),
                "total_checks": len(all_issues),
            },
            "checks": {},
        }

        for check_name, issues in all_issues.items():
            output["checks"][check_name] = {
                "count": len(issues),
                "status": "FAIL" if issues else "PASS",
                "issues": issues,
            }

        print(json.dumps(output, indent=2))
    else:
        # Human-friendly output
        print(
            f"\n📊 Architecture Verification Complete - {total_issues} issues "
            "found\n"
        )

        for check_name, issues in all_issues.items():
            if issues:
                print(
                    f"❌ {check_name.replace('_', ' ').title()} ({len(issues)} "
                    "issues):"
                )
                if check_name.replace("_", " ").title() in ["Orphaned Tests"]:
                    print(
                        "NOTE: 'Orphaned Tests' category is fundamentally "
                        "wrong. \n\n"
                        "The 'orphaned' tests (POLICY, REGISTRY, SERVICES, "
                        "FILTERS, PARSER) may not be orphaned at all.\n"
                        "They may be testing the linter's infrastructure "
                        "components, not validation rules."
                        "\n"
                        "This script assumed everything should map to "
                        "`ORDERED_RULES_PER_FILE`, but this ADR linter\nhas "
                        "meta-tests for the architecture itself."
                    )
                for issue in issues:
                    print(f"   • {issue}")
                print()
            else:
                print(f"✅ {check_name.replace('_', ' ').title()}: OK")

        if total_issues > 0:
            print(f"🔥 Total issues found: {total_issues}")
        else:
            print("🎉 No architectural issues detected!")

    # Exit code for scripts regardless of output format
    sys.exit(1 if total_issues > 0 else 0)


if __name__ == "__main__":
    main()
