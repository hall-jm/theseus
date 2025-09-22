# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# src/adr_linter/cli.py

from __future__ import annotations
import argparse
import sys

from .engine import run

# from pathlib import Path
from . import __package__  # noqa: F401  (keep relative imports stable)

# TODO: Add versioning information from .env or pyproject.toml to support
#       versioning functions within the application (even if just as a
#       `--version` argument for now


def create_parser():
    """
    Create the argument parser for anchoring snapshot tools
    """
    parser = argparse.ArgumentParser(
        prog="theseus (adr-linter)",
        description="Linter for Theseus ADRs.",
    )

    parser.add_argument("--path", default=".")
    parser.add_argument("--fail-on", default="E", choices=["E", "W", "I"])
    parser.add_argument(
        "-k",
        "--keyword",
        default=None,
        help="pytest -k style boolean filter for filenames/paths",
    )
    parser.add_argument("--emit-metrics", action="store_true")
    parser.add_argument("--format", choices=["md", "jsonl"], default="md")
    return parser


def main(argv=None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    rc = run(
        path=args.path,
        fail_on=args.fail_on,
        k_expr=args.keyword,
        emit_metrics=args.emit_metrics,
        fmt=args.format,
    )
    return rc


if __name__ == "__main__":
    sys.exit(main())

"""
Future Enhancement:
- Take the chunked rules and consolidate them into a single file for easier
  review in total

+def _bundle_template_rules_md(out_path: Path) -> None:
+    ""
+    Concatenate all validators/template/*.py into a single Markdown file.
+    Output is intended for human/LLM consumption (not execution).
+    ""
+    import re
+    import datetime as dt
+    from .constants import CODES
+    from .validators import template as template_pkg
+    from pathlib import Path as _P
+
+    tpl_dir = _P(template_pkg.__file__).resolve().parent
+    files = sorted(
+        tpl_dir.glob("template_*.py"),
+        key=lambda p: int(re.search(r"template_(\\d{3})_", p.name).group(1)),
+    )
+
+    out_path.parent.mkdir(parents=True, exist_ok=True)
+
+    lines = []
+    lines.append("# Template Rules Bundle (ADR-0001 §7.5)\n")
+    lines.append(
         f"_Generated: {dt.datetime.now().isoformat(timespec='seconds')}_\\n"
     )
+    lines.append(
         "> This file is a non-executable mash-up of per-rule modules under "
         "`validators/template/`.\\n"
     )
+
+    for p in files:
+        m = re.search(r"template_(\\d{3})_", p.name)
+        num = m.group(1) if m else "???"
+        code = f\"ADR-TEMPLT-{num}\"
+        title = CODES.get(code, (\"?\", \"\"))[1] if code in CODES else \"\"
+        lines.append(f\"\\n## {code} — {title}\\n\")
+        lines.append(
             f\"_File: {p.relative_to(tpl_dir.parent.parent)}_\\n\\n\"
         )
+        src = p.read_text(encoding=\"utf-8\")
+        lines.append(\"```python\\n\" + src.rstrip() + \"\\n```\\n\")
+
+    out_path.write_text(\"\\n\".join(lines), encoding=\"utf-8\")

+    parser.add_argument("--path", default=".", help="Root path to scan")
+    parser.add_argument("-k", dest="k", default="", help="Filter expression")
+    # ---- New: bundle/mash helper (non-invasive) ---------------------------
+    parser.add_argument(
+        "--bundle-template-rules",
+        "--mash-template-rules",
+        dest="bundle_template_rules",
+        action="store_true",
+        help="Concatenate validators/template/*.py into a single Markdown "
         "file and exit.",
+    )
+    parser.add_argument(
+        "--bundle-out",
+        dest="bundle_out",
+        default="TEMPLT_RULES_BUNDLE.md",
+        help="Output path for --bundle-template-rules (default: "
         "TEMPLT_RULES_BUNDLE.md)",
+    )
 
     args = parser.parse_args(argv)
-    return run_engine(path=args.path, k=args.k)
+    # Fast-path: just produce the bundle and exit
+    if args.bundle_template_rules:
+        out = Path(args.bundle_out)
+        _bundle_template_rules_md(out)
+        print(f"Wrote template rule bundle → {out}")
+        return 0
+
+    # Normal linter execution
+    return run_engine(path=args.path, k=args.k)
"""
