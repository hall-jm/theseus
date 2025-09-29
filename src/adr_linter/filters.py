# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/parser/structure.py

"""
Reusable helpers for file selection and predicates (pytest-like -k).

Behavior is intentionally identical to the legacy implementation:
- supports and/or/not, parentheses, bare/quoted tokens
- tokens match case-insensitive substrings of full path OR filename
- falls back to simple substring match if parse fails
"""

from __future__ import annotations
import re
from pathlib import Path
from typing import Callable, List


def _tokenize_k(expr: str) -> List[str]:
    """
    Split into tokens: (, ), and, or, not, quoted strings, bare words.
    """
    if not expr:
        return []
    rx = re.compile(
        r'\(|\)|\band\b|\bor\b|\bnot\b|"(?:[^"\\]|\\.)*"|'
        r"'(?:[^'\\]|\\.)*'|[^()\s]+",
        re.I,
    )
    return rx.findall(expr)


def _strip_quotes(tok: str) -> str:
    if len(tok) >= 2 and tok[0] in {'"', "'"} and tok[-1] == tok[0]:
        return tok[1:-1]
    return tok


def compile_k(expr: str) -> Callable[[Path], bool]:
    """
    Compile a pytest-like -k boolean expression into a predicate Path->bool.
    """
    tokens = _tokenize_k(expr)
    if not tokens:
        return lambda _p: True

    def _combine_or(left_pred, right_pred):
        def predicate(path_obj: Path) -> bool:
            return left_pred(path_obj) or right_pred(path_obj)

        return predicate

    def _combine_and(left_pred, right_pred):
        def predicate(path_obj: Path) -> bool:
            return left_pred(path_obj) and right_pred(path_obj)

        return predicate

    def _negate(pred):
        def predicate(path_obj: Path) -> bool:
            return not pred(path_obj)

        return predicate

    pos = 0

    def peek():
        return tokens[pos].lower() if pos < len(tokens) else None

    def get():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        return tok

    def parse_or():
        node = parse_and()
        while True:
            t = peek()
            if t == "or":
                get()
                rhs = parse_and()
                lhs = node
                node = _combine_or(lhs, rhs)
            else:
                break
        return node

    def parse_and():
        node = parse_not()
        while True:
            t = peek()
            if t == "and":
                get()
                rhs = parse_not()
                lhs = node
                node = _combine_and(lhs, rhs)
            else:
                break
        return node

    def parse_not():
        t = peek()
        if t == "not":
            get()
            sub = parse_not()
            return _negate(sub)
        return parse_term()

    def parse_term():
        t = peek()
        if t == "(":
            get()
            node = parse_or()
            if peek() != ")":
                raise ValueError("Unbalanced parentheses in -k expression")
            get()  # consume ')'
            return node
        raw = get()
        tok = _strip_quotes(raw).lower()

        def pred(path_obj: Path) -> bool:
            s = path_obj.as_posix().lower()
            n = path_obj.name.lower()
            return tok in s or tok in n

        return pred

    try:
        tree = parse_or()
        if pos != len(tokens):
            raise ValueError("Unexpected tokens at end of -k expression")
        return tree
    except Exception:
        needle = (expr or "").lower()
        return lambda p: (
            needle in p.as_posix().lower() or needle in p.name.lower()
        )
