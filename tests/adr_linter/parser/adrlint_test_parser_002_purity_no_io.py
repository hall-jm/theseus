# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tests/adr_linter/parser/adrlint_test_parser_002_purity_no_io.py

"""
ADR-0001 · §<XXX> Linter Rules Reference
ADR-XXXX-YYYY (E? W? I?): parser/ must not perform I/O or read env.
Linting Tests: ADRLINT-990
"""

from __future__ import annotations


import ast
from pathlib import Path

# FIXME: These _DISALLOWED* declarations needs to be centralized along with the
#        class `V` logic; avoid nesting defs() in defs();
_DISALLOWED_BUILTIN_CALLS = {"open"}
_DISALLOWED_ATTR_CALLS = {"read_text", "write_text", "open"}


def _discover_repo_root(start: Path) -> Path:
    start = start.resolve()
    for d in [start] + list(start.parents):
        if (d / "src" / "adr_linter" / "parser").is_dir():
            return d
    return start.parent


def _find_violations(py_path: Path):
    src = py_path.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(py_path))
    bad = []

    # FIXME: This class `V` logic needs to be centralized;
    #        avoid nesting defs() in defs();
    class V(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call):
            if (
                isinstance(node.func, ast.Name)
                and node.func.id in _DISALLOWED_BUILTIN_CALLS
            ):
                bad.append((py_path, node.lineno, f"{node.func.id}("))
            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr in _DISALLOWED_ATTR_CALLS
            ):
                bad.append((py_path, node.lineno, f".{node.func.attr}("))
            self.generic_visit(node)

        def visit_Attribute(self, node: ast.Attribute):
            if (
                node.attr == "environ"
                and isinstance(node.value, ast.Name)
                and node.value.id == "os"
            ):
                bad.append((py_path, node.lineno, "os.environ"))
            self.generic_visit(node)

        def visit_Subscript(self, node: ast.Subscript):
            v = node.value
            if (
                isinstance(v, ast.Attribute)
                and v.attr == "environ"
                and isinstance(v.value, ast.Name)
                and v.value.id == "os"
            ):
                bad.append((py_path, node.lineno, "os.environ[...]"))
            self.generic_visit(node)

    V().visit(tree)
    return bad


def test_adrlint990_parser_is_pure_no_io():
    repo_root = _discover_repo_root(Path(__file__))
    parser_dir = repo_root / "src" / "adr_linter" / "parser"
    assert parser_dir.is_dir(), f"Missing parser dir: {parser_dir}"

    violations = []
    for py in parser_dir.rglob("*.py"):
        if py.name == "__init__.py":
            continue
        violations.extend(_find_violations(py))

    if violations:
        lines = "\n".join(f"{p}:{ln}: {what}" for p, ln, what in violations)
        raise AssertionError("Disallowed I/O in parser/*:\n" + lines)
