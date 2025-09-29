# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/parser/__init__.py

"""
Pure text parsing helpers only. (no file IO).

FOR_LLMS: parser/* must not import from io.py or validators/*.
"""

from .front_matter import parse_front_matter
from .structure import parse_document_structure

__all__ = ["parse_front_matter", "parse_document_structure"]
