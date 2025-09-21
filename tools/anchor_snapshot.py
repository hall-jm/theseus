# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# tools/2_anchor_snapshot.py

"""
Anchor Snapshot Tool - Rebuilt Implementation

Deterministic project state capture for effective LLM session handoffs.
Generates structured JSON snapshots with quality assessment and development
context.

Design Decisions:
- Git dependency accepted (always available for this project)
- Self-contained with configurable constants (no external YAML)
- Graceful degradation on errors (mark as unavailable, continue execution)
- Quality score transparency for LLM evaluation
- Deterministic output (UTC timestamps, sorted lists)
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple  # , Set,
import shutil

# === CONSTANTS & CONFIGURATION ===

ANCHOR_SCHEMA_VERSION = "2.1.0"
ANCHOR_VERSION = "10.2"

# -- .env debug overrides
DEBUG = bool(int(os.environ.get("ADR_REPO_SNAPSHOT_ANCHOR_DEBUG", "0")))

# File scanning limits
MAX_RECENT_FILES = 10
MAX_TODOS = 20
MAX_FILE_SIZE_READ = 10 * 1024 * 1024  # 10MB
RECENT_HOURS = 72
LOG_TAIL_CHARS = 400

# Git operation timeouts (seconds)
GIT_TIMEOUT = 10
PYTEST_TIMEOUT = 60
CACHE_TTL_SECONDS = 300  # 5 minutes

# Quality score weights (must sum to 1.0)
WEIGHT_TEST_HEALTH = 0.35
WEIGHT_SCOPE_APPROPRIATENESS = 0.20
WEIGHT_TECHNICAL_DEBT = 0.15
WEIGHT_CODE_QUALITY = 0.15
WEIGHT_DEVELOPMENT_MOMENTUM = 0.10
WEIGHT_CHANGE_RISK = 0.05

# File patterns
CODE_EXTENSIONS = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".rs", ".go"}
IGNORE_DIRS = {
    "__pycache__",
    "archive",
    "build",
    "dist",
    "node_modules",
    "venv",
    ".anchor_cache",
    ".git",
    ".pytest",
    ".pytest_cache",
    ".venv",
    ".venv_theseus",
}
IGNORE_PATTERNS = {"*.pyc", "*.pyo", "*.log", "*.tmp", "__init__.py"}

# Environment keys to hash (security)
ENV_KEYS_TO_HASH = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "GOOGLE_API_KEY",
    "AWS_SECRET_ACCESS_KEY",
    "HF_TOKEN",
]

# TODO detection patterns
TODO_PATTERNS = [
    r"\bTODO\b",
    r"\bFIXME\b",
    r"\bHACK\b",
    r"\bXXX\b",
    r"\bTOREVIEW\b",
]
TODO_CATEGORIES = {
    "blocking": [
        r"\b(FIXME|BROKEN|BUG|URGENT|CRITICAL|BLOCKER)\b",
        r"\b(must fix|blocks?|prevents?|stops?)\b",
    ],
    "debt": [
        r"\b(HACK|KLUDGE|WORKAROUND|TEMP)\b",
        r"\b(cleanup|refactor|improve)\b",
    ],
    "review": [
        r"\b(TOREVIEW|REVIEW|CHECK)\b",
        r"\b(verify|validate|confirm)\b",
    ],
    "improvement": [
        r"\b(enhance|optimize|performance)\b",
        r"\b(feature|add|implement)\b",
    ],
}

# === CORE UTILITIES ===


@dataclass
class TimedResult:
    """Container for timed operation results"""

    result: Any
    duration_ms: float
    available: bool = True
    error: Optional[str] = None


def _timer(func):
    """Decorator for timing operations"""

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            duration = (time.perf_counter() - start) * 1000
            if (
                isinstance(result, dict)
                and "available" in result
                and not result["available"]
            ):
                return TimedResult(
                    result, duration, False, result.get("error")
                )
            return TimedResult(result, duration, True)
        except Exception as e:
            duration = (time.perf_counter() - start) * 1000
            return TimedResult(
                {"available": False, "error": str(e)}, duration, False, str(e)
            )

    return wrapper


def _safe_hash(value: Optional[str]) -> Optional[str]:
    """Generate safe hash prefix for sensitive values"""
    if not value:
        return None
    return f"sha256[:8]={hashlib.sha256(value.encode()).hexdigest()[:8]}"


def _normalize_path(path: Path) -> str:
    """Normalize path to forward slashes for consistency"""
    return str(path).replace("\\", "/")


def _is_ignored(path: Path) -> bool:
    """Check if path should be ignored during scanning"""
    if path.name in IGNORE_DIRS:
        return True
    if any(part in IGNORE_DIRS for part in path.parts):
        return True
    if any(
        path.name.endswith(pat.replace("*", "")) for pat in IGNORE_PATTERNS
    ):
        return True
    return False


def _utc_timestamp() -> str:
    """Generate deterministic UTC timestamp"""
    return (
        dt.datetime.now(dt.timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )


def _debug(msg: str, level: str = "debug") -> None:
    if DEBUG:
        prefix = {"debug": "[D]", "warn": "[W]", "error": "[E]"}.get(
            level, "[DEBUG]"
        )
        print(f"{prefix} {msg}")


def _warn(msg: str) -> None:
    _debug(msg, "warn")


def _error(msg: str) -> None:
    _debug(msg, "error")


# === CACHE MANAGEMENT ===


def _get_cache_dir(root: Path) -> Path:
    """Get cache directory for git operations"""
    cache_dir = root / "logs" / ".anchor_snapshot"
    cache_dir.mkdir(exist_ok=True)
    return cache_dir


def _is_cache_valid(
    cache_file: Path, ttl_seconds: int = CACHE_TTL_SECONDS
) -> bool:
    """Check if cache file is still valid"""
    if not cache_file.exists():
        return False
    age = time.time() - cache_file.stat().st_mtime
    return age < ttl_seconds


def _load_cache(cache_file: Path) -> Optional[Dict]:
    """Load cached data if valid"""
    try:
        if _is_cache_valid(cache_file):
            return json.loads(cache_file.read_text())
    except Exception:
        pass
    return None


def _save_cache(cache_file: Path, data: Dict) -> None:
    """Save data to cache file"""
    try:
        cache_file.write_text(json.dumps(data, indent=2))
    except Exception:
        pass  # Cache failures are non-critical


def _clear_cache(root: Path) -> None:
    """Clear all cached data"""
    cache_dir = _get_cache_dir(root)
    try:
        for cache_file in cache_dir.glob("*.json"):
            cache_file.unlink()
        _debug(f"─ Cache cleared: {cache_dir}")
    except Exception as e:
        _debug(f"─ Cache clear failed: {e}")


# === GIT OPERATIONS ===


def _run_git_command(
    cmd: List[str], cwd: Path, timeout: int = GIT_TIMEOUT
) -> Dict[str, Any]:
    """Run git command with error handling"""
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        if result.returncode == 0:
            return {
                "available": True,
                "output": result.stdout.strip(),
                "stderr": result.stderr,
            }
        else:
            return {
                "available": False,
                "error": f"git rc={result.returncode}: {result.stderr}",
            }
    except subprocess.TimeoutExpired:
        return {"available": False, "error": f"git timeout after {timeout}s"}
    except FileNotFoundError:
        return {"available": False, "error": "git command not found"}
    except Exception as e:
        return {"available": False, "error": str(e)}


@_timer
def _get_git_basic_info(root: Path) -> Dict[str, Any]:
    """Get basic git repository information"""
    info = {}

    # Get commit hash
    result = _run_git_command(["git", "rev-parse", "--short", "HEAD"], root)
    if result["available"]:
        info["commit"] = result["output"]
    else:
        info["commit"] = None
        info["commit_error"] = result["error"]

    # Get branch name
    result = _run_git_command(["git", "branch", "--show-current"], root)
    if result["available"]:
        info["branch"] = result["output"]
    else:
        info["branch"] = None
        info["branch_error"] = result["error"]

    # Get dirty status
    result = _run_git_command(["git", "status", "--porcelain"], root)
    if result["available"]:
        info["dirty"] = bool(result["output"].strip())
    else:
        info["dirty"] = None
        info["dirty_error"] = result["error"]

    return info


@_timer
def _get_git_changes_detailed(root: Path) -> Dict[str, Any]:
    """Get detailed git change information with caching"""
    cache_file = _get_cache_dir(root) / "git_changes.json"
    cached = _load_cache(cache_file)

    if cached:
        _debug(f"─ git_changes.json cache file exists: {cache_file.exists()}")
        return cached

    changes = {
        "staged": [],
        "unstaged": [],
        "untracked": [],
        "file_stats": {},
        "recent_commits": [],
    }

    _debug("─ git (diff|ls-files|log) results:")

    # Get staged changes with status
    result = _run_git_command(
        ["git", "diff", "--name-status", "--cached", "--find-renames"], root
    )

    if result["available"]:
        _debug(
            "  ├─ git diff --name-status --cached --find-renames output "
            f"length: {len(result['output'])}"
        )
        for line in result["output"].splitlines():
            _debug(f"  ├─ processing line: '{line}'")
            if line.strip():
                parts = line.split("\t", 1)
                if len(parts) == 2:
                    status, filepath = parts
                    changes["staged"].append(
                        {"file": filepath, "status": status}
                    )

    # Get unstaged changes with status
    result = _run_git_command(
        ["git", "diff", "--name-status", "--find-renames"], root
    )
    if result["available"]:
        _debug(
            "  ├─ git diff --name-status --find-renames output length: "
            f"{len(result['output'])}"
        )
        for line in result["output"].splitlines():
            if line.strip():
                parts = line.split("\t", 1)
                if len(parts) == 2:
                    status, filepath = parts
                    changes["unstaged"].append(
                        {"file": filepath, "status": status}
                    )

    # Get untracked files
    result = _run_git_command(
        ["git", "ls-files", "--others", "--exclude-standard"], root
    )
    if result["available"]:
        _debug(
            "  ├─ git ls-files --others --exclude-standard output length: "
            f"{len(result['output'])}"
        )
        changes["untracked"] = [
            f.strip() for f in result["output"].splitlines() if f.strip()
        ]

    # Get numstat for churn analysis
    result = _run_git_command(
        ["git", "diff", "--numstat", "HEAD~10..HEAD"], root
    )
    if result["available"]:
        _debug(
            "  ├─ git diff --numstat HEAD~10..HEAD output length: "
            f"{len(result['output'])}"
        )
        for line in result["output"].splitlines():
            if line.strip():
                parts = line.split("\t")
                if len(parts) == 3:
                    adds, dels, filepath = parts
                    try:
                        changes["file_stats"][filepath] = {
                            "additions": int(adds) if adds != "-" else 0,
                            "deletions": int(dels) if dels != "-" else 0,
                        }
                    except ValueError:
                        pass

    # Get recent commits for context
    result = _run_git_command(["git", "log", "--oneline", "-5"], root)
    _debug(f"  ├─ git log --oneline -5 output length: {len(result['output'])}")
    if result["available"]:
        changes["recent_commits"] = [
            line.strip() for line in result["output"].splitlines()
        ]

    _debug("  └─ END OF git diff results")

    _save_cache(cache_file, changes)
    _debug(f"─ is cache valid: {str(_is_cache_valid(cache_file))}")
    return changes


# === FILE SYSTEM SCANNING ===


@_timer
def _scan_project_structure(root: Path) -> Dict[str, Any]:
    """Scan project for structure and recent activity"""
    structure = {
        "total_files": 0,
        "total_size": 0,
        "languages": {},
        "recent_files": [],
        "todos": [],
        "trees": {"src": [], "tests": [], "tools": []},
    }

    cutoff_time = dt.datetime.now() - dt.timedelta(hours=RECENT_HOURS)

    try:
        for file_path in root.rglob("*"):
            if not file_path.is_file() or _is_ignored(file_path):
                continue

            try:
                stat = file_path.stat()
                structure["total_files"] += 1
                structure["total_size"] += stat.st_size

                # Language detection
                suffix = file_path.suffix.lower()
                if suffix in CODE_EXTENSIONS:
                    lang = _get_language_name(suffix)
                    structure["languages"][lang] = (
                        structure["languages"].get(lang, 0) + 1
                    )

                # Recent file tracking
                mtime = dt.datetime.fromtimestamp(stat.st_mtime)
                if mtime > cutoff_time:
                    rel_path = _normalize_path(file_path.relative_to(root))
                    structure["recent_files"].append(
                        {
                            "path": rel_path,
                            "modified": mtime.isoformat(timespec="seconds"),
                            "size": stat.st_size,
                        }
                    )

                # Tree building for key directories - filter for relevance
                rel_path = file_path.relative_to(root)
                if rel_path.parts and rel_path.parts[0] in [
                    "src",
                    "tests",
                    "tools",
                ]:
                    tree_name = rel_path.parts[0]
                    should_include = False

                    if tree_name == "tools":
                        # Only include top-level standalone tools and key
                        # scripts
                        if (
                            len(rel_path.parts) == 2  # Top-level only
                            and suffix in CODE_EXTENSIONS
                            and not rel_path.name.startswith("__")
                        ):  # Exclude __main__.py etc
                            should_include = True
                    elif tree_name in ["src", "tests"]:
                        # Include all code files for src and tests
                        if suffix in CODE_EXTENSIONS:
                            should_include = True

                    if should_include:
                        entry = f"{_normalize_path(rel_path)} "
                        f"({_format_size(stat.st_size)})"
                        structure["trees"][tree_name].append(entry)

                # TODO scanning - always scan, truncate at the end
                if suffix in CODE_EXTENSIONS:
                    todos = _extract_todos_from_file(file_path, root)
                    structure["todos"].extend(todos)

            except (OSError, PermissionError):
                continue

    except Exception as e:
        return {"available": False, "error": str(e)}

    # Sort and format results
    priority_order = {"high": 0, "medium": 1, "low": 2}
    structure["todos"].sort(
        key=lambda todo: (
            priority_order.get(todo.get("priority", "low"), 2),
            todo.get("category", "improvement"),
            todo.get("file", ""),
        )
    )

    if len(structure["todos"]) > MAX_TODOS:
        structure["todos"] = structure["todos"][:MAX_TODOS]

    structure["recent_files"].sort(key=lambda x: x["modified"], reverse=True)
    structure["recent_files"] = structure["recent_files"][:MAX_RECENT_FILES]
    structure["languages"] = dict(
        sorted(
            structure["languages"].items(), key=lambda x: x[1], reverse=True
        )
    )

    for tree_name in structure["trees"]:
        structure["trees"][tree_name] = sorted(structure["trees"][tree_name])

    return structure


def _get_language_name(suffix: str) -> str:
    """Map file extension to language name"""
    mapping = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".rs": "Rust",
        ".go": "Go",
    }
    return mapping.get(suffix, suffix.upper().lstrip("."))


def _format_size(size: int) -> str:
    """Format file size in human readable format"""
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size // 1024}KB"
    else:
        return f"{size // (1024 * 1024)}MB"


def _extract_todos_from_file(
    file_path: Path, root: Path
) -> List[Dict[str, Any]]:
    """Extract TODO items from a single file"""
    todos = []
    try:
        if file_path.stat().st_size > MAX_FILE_SIZE_READ:
            return todos

        content = file_path.read_text(encoding="utf-8", errors="ignore")
        rel_path = _normalize_path(file_path.relative_to(root))

        for line_num, line in enumerate(content.splitlines(), 1):
            line_stripped = line.strip()

            # Skip regex pattern definitions and string literals
            if _is_pattern_definition(line_stripped):
                continue

            for pattern in TODO_PATTERNS:
                if re.search(pattern, line_stripped, re.IGNORECASE):
                    category, priority = _categorize_todo(line_stripped)
                    todos.append(
                        {
                            "file": rel_path,
                            "line": line_num,
                            "content": line_stripped[:200],
                            "category": category,
                            "priority": priority,
                        }
                    )
                    break

    except Exception:
        pass

    return todos


def _is_pattern_definition(line: str) -> bool:
    """
    Check if line is a regex pattern definition rather than actual TODO
    """
    line_lower = line.lower()

    # Skip string literals containing TODO keywords
    if any(
        marker in line_lower
        for marker in [
            'r"',
            "r'",
            '"""',
            "'''",  # Raw strings and docstrings
            "= [",
            "= {",
            ": [",
            ": {",  # Data structure definitions
            "patterns = ",
            "todo_patterns",  # Pattern variable definitions
            "blocking_patterns",
            "debt_patterns",  # Pattern list definitions
        ]
    ):
        return True

    # Skip lines that are clearly regex patterns
    if re.search(r'r["\'].*\\b.*\\b.*["\']', line):
        return True

    return False


def _categorize_todo(content: str) -> Tuple[str, str]:
    """
    Categorize TODO item and assign priority based on enhanced focus detection
    """
    content_lower = content.lower()

    # Category detection patterns from documentation
    blocking_patterns = [
        r"\b(fixme|bug|broken|urgent|critical|blocker)\b",
        r"\b(must fix|blocks?|prevents?|stops?)\b",
        r"\btodo:.*\b(crashes?|fails?|throws?|timeout|exception)\b",
        r"\btodo:.*\b(blocks?|prevents?|stops?)\b",
    ]

    debt_patterns = [
        r"\b(hack|kludge|workaround|temp)\b",
        r"\b(cleanup|refactor|improve)\b",
        r"\btodo:.*\b(technical debt|legacy|replace)\b",
    ]

    review_patterns = [
        r"\b(toreview|review|check)\b",
        r"\b(verify|validate|confirm)\b",
        r"\btodo:.*\b(test|testing|validate|verify)\b",
    ]

    improvement_patterns = [
        r"\b(enhance|optimize|performance)\b",
        r"\b(feature|add|implement)\b",
        r"\btodo:.*\b(could|might|should consider)\b",
    ]

    question_patterns = [
        r"\btodo:.*\b(why|how|what|when|where)\b",
        r"\btodo:.*\b(unclear|confusing|ask|discuss|clarify)\b",
    ]

    # Determine category
    category = "improvement"  # default
    priority = "low"  # default

    for pattern in blocking_patterns:
        if re.search(pattern, content_lower):
            category = "blocking"
            priority = "high"
            break

    # Define pattern groups with priorities (higher priority checked first)
    pattern_groups = [
        ("debt", debt_patterns),
        ("review", review_patterns),
        ("question", question_patterns),
        ("improvement", improvement_patterns),
    ]

    if category == "improvement":  # Only check others if not already blocking
        for cat_name, patterns in pattern_groups:
            if any(re.search(pattern, content_lower) for pattern in patterns):
                category = cat_name
                break

    # Priority detection (independent of category)
    high_priority_terms = [
        "urgent",
        "critical",
        "blocker",
        "broken",
        "fixme",
        "bug",
        "must",
        "fix",
        "crashes",
        "fails",
        "stops",
        "blocks",
        "prevents",
    ]

    medium_priority_terms = [
        "should",
        "important",
        "review",
        "test",
        "toreview",
        "check",
        "verify",
        "validate",
        "confirm",
        "needs testing",
        "test",
    ]

    # Final review of priority if the priority is still 'low'
    if priority == "low" and any(
        term in content_lower for term in high_priority_terms
    ):
        priority = "high"
    elif priority == "low" and any(
        term in content_lower for term in medium_priority_terms
    ):
        priority = "medium"
    else:
        priority = "low"

    return category, priority


# === TEST EXECUTION ===


@_timer
def _run_pytest(root: Path) -> Dict[str, Any]:
    """Run pytest with caching and offline mode"""
    cache_file = _get_cache_dir(root) / "pytest_results.json"
    cached = _load_cache(cache_file)
    if cached:
        cached["from_cache"] = True
        return cached

    try:
        env = os.environ.copy()
        # Remove API keys for offline testing
        for key in ENV_KEYS_TO_HASH:
            env.pop(key, None)
        env["MIRROR_LIVE_API"] = "0"
        env["MIRROR_ALLOW_NETWORK"] = "0"

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/adrlinter/",
                "-q",
                "-m",
                "not live",
            ],
            cwd=str(root),
            env=env,
            capture_output=True,
            text=True,
            timeout=PYTEST_TIMEOUT,
            check=False,
        )

        counters = _parse_pytest_output(result.stdout)

        test_result = {
            "available": True,
            "return_code": result.returncode,
            "stdout_tail": result.stdout[-1000:] if result.stdout else "",
            "stderr_tail": result.stderr[-500:] if result.stderr else "",
            "counters": counters,
            "health": "passing" if result.returncode == 0 else "failing",
            "from_cache": False,
        }

        _save_cache(cache_file, test_result)
        return test_result

    except subprocess.TimeoutExpired:
        return {
            "available": False,
            "error": f"pytest timeout after {PYTEST_TIMEOUT}s",
        }
    except Exception as e:
        return {"available": False, "error": str(e)}


def _parse_pytest_output(output: str) -> Dict[str, int]:
    """Parse pytest output for test counts"""
    counters = {}
    if not output:
        return counters

    patterns = [
        (r"(\d+) passed", "passed"),
        (r"(\d+) failed", "failed"),
        (r"(\d+) skipped", "skipped"),
        (r"(\d+) xfailed", "xfailed"),
        (r"(\d+) xpassed", "xpassed"),
        (r"(\d+) error", "errors"),
        (r"(\d+) warning", "warnings"),
    ]

    for pattern, key in patterns:
        match = re.search(pattern, output)
        if match:
            counters[key] = int(match.group(1))

    return counters


@_timer
def _run_adr_verification(root: Path) -> Dict[str, Any]:
    """Run ADR architecture verification with caching"""
    cache_file = _get_cache_dir(root) / "adr_verification.json"
    cached = _load_cache(cache_file)
    if cached:
        cached["from_cache"] = True
        return cached

    try:
        verify_script = root / "tools" / "verify_adr_architecture.py"
        if not verify_script.exists():
            return {
                "available": False,
                "error": "verify_adr_architecture.py not found in tools/",
            }

        result = subprocess.run(
            [sys.executable, str(verify_script), str(root), "--json"],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=30,  # ADR verification should be fast
            check=False,
        )

        if result.returncode != 0:
            # Script failed, but might still have JSON output
            if result.stdout.strip():
                try:
                    verification_data = json.loads(result.stdout)
                    verification_data["available"] = True
                    verification_data["from_cache"] = False
                    _save_cache(cache_file, verification_data)
                    return verification_data
                except json.JSONDecodeError:
                    pass

            return {
                "available": False,
                "error": f"verification failed (rc={result.returncode}): "
                f"{result.stderr[-500:]}",
            }

        # Parse JSON output
        try:
            verification_data = json.loads(result.stdout)
            verification_data["available"] = True
            verification_data["from_cache"] = False
            _save_cache(cache_file, verification_data)
            return verification_data
        except json.JSONDecodeError as e:
            return {"available": False, "error": f"invalid JSON output: {e}"}

    except subprocess.TimeoutExpired:
        return {
            "available": False,
            "error": "ADR verification timeout after 30s",
        }
    except Exception as e:
        return {"available": False, "error": str(e)}


# === QUALITY ASSESSMENT ===


def _calculate_quality_score(
    test_data: Dict[str, Any],
    git_changes: Dict[str, Any],
    todos: List[Dict[str, Any]],
    adr_verification: Dict[str, Any],
) -> Dict[str, Any]:
    """Calculate composite quality score using actual git evidence"""

    components = {}

    _debug("─ git Quality Details")
    _debug(f"  ├─ git_changes keys: {list(git_changes.keys())}")
    if "staged" in git_changes:
        _debug(f"  ├─ staged count: {len(git_changes.get('staged', []))}")
        _debug(f"  ├─ unstaged count: {len(git_changes.get('unstaged', []))}")
    else:
        _debug("  ├─ staged count: NaN ('staged' not in git_changes)")
        _debug("  ├─ unstaged count: NaN ('staged' not in git_changes)")
    _debug(
        f"  └─ git_changes.get('available'): "
        f"{git_changes.get('available')}"
    )

    # Calculate all component scores
    components["test_health"] = _assess_test_health(test_data)
    components["scope_appropriateness"] = _assess_scope_appropriateness(
        git_changes
    )
    components["technical_debt"] = _assess_technical_debt(todos, git_changes)
    components["code_quality"] = _assess_code_quality(adr_verification)
    components["development_momentum"] = _assess_development_momentum(
        git_changes
    )
    components["change_risk"] = _assess_change_risk(git_changes)

    # Calculate weighted overall score (keep full precision)
    overall_score_raw = (
        components["test_health"]["score"] * WEIGHT_TEST_HEALTH
        + components["scope_appropriateness"]["score"]
        * WEIGHT_SCOPE_APPROPRIATENESS
        + components["technical_debt"]["score"] * WEIGHT_TECHNICAL_DEBT
        + components["code_quality"]["score"] * WEIGHT_CODE_QUALITY
        + components["development_momentum"]["score"]
        * WEIGHT_DEVELOPMENT_MOMENTUM
        + components["change_risk"]["score"] * WEIGHT_CHANGE_RISK
    )

    # Calculate impact-weighted issues (impact = weight × (1 - score))
    impacts = []
    weights = {
        "test_health": WEIGHT_TEST_HEALTH,
        "scope_appropriateness": WEIGHT_SCOPE_APPROPRIATENESS,
        "technical_debt": WEIGHT_TECHNICAL_DEBT,
        "code_quality": WEIGHT_CODE_QUALITY,
        "development_momentum": WEIGHT_DEVELOPMENT_MOMENTUM,
        "change_risk": WEIGHT_CHANGE_RISK,
    }

    for component_name, component_data in components.items():
        impact = weights[component_name] * (1.0 - component_data["score"])
        if impact > 0.01:  # Only include meaningful impacts
            impacts.append(
                {
                    "component": component_name,
                    "impact": round(impact, 3),
                    "note": component_data["reason"],
                }
            )

    # Sort by impact (highest first)
    impacts.sort(key=lambda x: x["impact"], reverse=True)

    # Generate explanation based on highest impact issues
    if not impacts:
        explanation = "All quality metrics are strong"
    elif len(impacts) == 1:
        explanation = (
            f"Primary concern: {impacts[0]['component'].replace('_', ' ')}"
        )
    else:
        top_two = [
            impact["component"].replace("_", " ") for impact in impacts[:2]
        ]
        explanation = f"Key concerns: {', '.join(top_two)}"

    return {
        "quality_version": "1.0",
        "calculation_method": "evidence_based_weighted_sum",
        "calculated_at_utc": _utc_timestamp(),
        "overall_score_raw": round(overall_score_raw, 3),
        # HACK: Python's round() uses "round half to even" behavior.
        #       For 0.845, it rounds down to 0.84 instead of up to
        #       0.85.
        "overall_score": round((overall_score_raw + 0.0001), 2),
        "components": components,
        "top_issues_by_impact": impacts[:3],  # Top 3 issues
        "explanation": explanation,
        "weights": {
            "test_health": WEIGHT_TEST_HEALTH,
            "scope_appropriateness": WEIGHT_SCOPE_APPROPRIATENESS,
            "technical_debt": WEIGHT_TECHNICAL_DEBT,
            "code_quality": WEIGHT_CODE_QUALITY,
            "development_momentum": WEIGHT_DEVELOPMENT_MOMENTUM,
            "change_risk": WEIGHT_CHANGE_RISK,
        },
    }


def _assess_test_health(test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Assess test health component"""
    if not test_data.get("available", False):
        return {
            "score": 0.0,
            "reason": "test execution failed",
            "status": "unknown",
            "metrics": {"available": False},
        }

    counters = test_data.get("counters", {})
    passed = counters.get("passed", 0)
    failed = counters.get("failed", 0)
    total_tests = passed + failed

    if total_tests == 0:
        return {
            "score": 0.5,
            "reason": "no tests found",
            "status": "unknown",
            "metrics": {"passed": 0, "failed": 0, "total": 0},
        }

    pass_rate = passed / total_tests
    coverage_boost = min(0.1, total_tests / 1000)
    final_score = min(1.0, pass_rate + coverage_boost)

    if final_score >= 0.9:
        status = "good"
    elif final_score >= 0.7:
        status = "warn"
    else:
        status = "poor"

    return {
        "score": final_score,
        "reason": f"{passed} passed, {failed} failed ({total_tests} total)",
        "status": status,
        "metrics": {"passed": passed, "failed": failed, "total": total_tests},
    }


def _assess_scope_appropriateness(
    git_changes: Dict[str, Any],
) -> Dict[str, Any]:
    """Assess scope appropriateness using git change analysis"""
    if not git_changes.get("available", False):
        return {
            "score": 0.5,
            "reason": "git changes unavailable",
            "status": "unknown",
            "metrics": {"available": False},
        }

    # Count total changed files
    staged_count = len(git_changes.get("staged", []))
    unstaged_count = len(git_changes.get("unstaged", []))
    untracked_count = len(git_changes.get("untracked", []))
    total_changed = staged_count + unstaged_count + untracked_count

    # Calculate directories affected
    all_files = []
    for item in git_changes.get("staged", []) + git_changes.get(
        "unstaged", []
    ):
        all_files.append(item.get("file", ""))
    all_files.extend(git_changes.get("untracked", []))

    dirs_affected = len(set(Path(f).parent for f in all_files if f))

    # Scope assessment based on breadth only
    if total_changed <= 3:
        base_score = 1.0
        scope_desc = "highly focused"
    elif total_changed <= 8:
        base_score = 0.8
        scope_desc = "focused"
    elif total_changed <= 20:
        base_score = 0.6
        scope_desc = "moderate"
    else:
        base_score = 0.4
        scope_desc = "broad"

    # Boost for refactoring patterns (high rename ratio)
    rename_count = sum(
        1
        for item in git_changes.get("staged", [])
        + git_changes.get("unstaged", [])
        if item.get("status", "").startswith("R")
    )
    rename_ratio = rename_count / max(total_changed, 1)

    if rename_ratio > 0.3:
        base_score = min(1.0, base_score + 0.2)
        scope_desc += " with refactoring"

    status = (
        "good"
        if base_score >= 0.7
        else "warn" if base_score >= 0.5 else "poor"
    )

    return {
        "score": base_score,
        "reason": f"{scope_desc} ({total_changed} files)",
        "status": status,
        "metrics": {
            "files_changed": total_changed,
            "dirs_affected": dirs_affected,
            "rename_ratio": round(rename_ratio, 2),
        },
    }


def _assess_technical_debt(
    todos: List[Dict[str, Any]], git_changes: Dict[str, Any]
) -> Dict[str, Any]:
    """Assess technical debt relative to changed files"""
    blocking_todos = sum(1 for todo in todos if todo.get("priority") == "high")

    # print ("DEBUGGING todos: ", str(todos))

    if git_changes.get("available", False):
        total_changed = (
            len(git_changes.get("staged", []))
            + len(git_changes.get("unstaged", []))
            + len(git_changes.get("untracked", []))
        )
        active_files = max(total_changed, 1)
    else:
        active_files = 1

    debt_density = blocking_todos / active_files

    if debt_density == 0:
        score = 1.0
        reason = "no blocking TODOs"
        status = "good"
    elif debt_density < 0.5:
        score = 0.8
        reason = f"{blocking_todos} blocking TODOs, manageable density"
        status = "good"
    elif debt_density < 1.0:
        score = 0.5
        reason = f"{blocking_todos} blocking TODOs, moderate density"
        status = "warn"
    else:
        score = 0.2
        reason = f"{blocking_todos} blocking TODOs, high density"
        status = "poor"

    return {
        "score": score,
        "reason": reason,
        "status": status,
        "metrics": {
            "blocking_todos": blocking_todos,
            "debt_density": round(debt_density, 2),
        },
    }


def _assess_code_quality(adr_verification: Dict[str, Any]) -> Dict[str, Any]:
    """Assess code quality using detailed verification results"""
    if not adr_verification.get("available", False):
        return {
            "score": 0.5,
            "reason": "ADR verification unavailable",
            "status": "unknown",
            "metrics": {"verification_status": "unavailable"},
        }

    summary = adr_verification.get("summary", {})
    total_issues = summary.get("total_issues", 0)

    # Score based on issue density, not binary pass/fail
    if total_issues == 0:
        score = 1.0
        status = "good"
        reason = "no architectural issues detected"
    elif total_issues <= 5:
        score = 0.8
        status = "good"
        reason = f"{total_issues} minor architectural issues"
    elif total_issues <= 15:
        score = 0.5
        status = "warn"
        reason = f"{total_issues} architectural issues need attention"
    else:
        score = 0.2
        status = "poor"
        reason = f"{total_issues} significant architectural problems"

    return {
        "score": score,
        "reason": reason,
        "status": status,
        "metrics": {
            "total_issues": total_issues,
            "checks_with_issues": summary.get("checks_with_issues", 0),
        },
    }


def _assess_development_momentum(
    git_changes: Dict[str, Any],
) -> Dict[str, Any]:
    """Assess development momentum from recent commits and changes"""
    if not git_changes.get("available", False):
        return {"score": 0.5, "reason": "git data unavailable"}

    # Analyze recent commits
    recent_commits = git_changes.get("recent_commits", [])
    commit_count = len(recent_commits)

    # Analyze current changes
    total_changes = (
        len(git_changes.get("staged", []))
        + len(git_changes.get("unstaged", []))
        + len(git_changes.get("untracked", []))
    )

    # Score based on activity level
    if commit_count >= 3 and total_changes >= 5:
        score = 0.9
        reason = (
            f"high activity ({commit_count} recent commits, "
            f"{total_changes} changed files)"
        )
        status = "good"
    elif commit_count >= 2 or total_changes >= 3:
        score = 0.7
        reason = (
            f"moderate activity ({commit_count} recent commits, "
            f"{total_changes} changed files)"
        )
        status = "good"
    elif commit_count >= 1 or total_changes >= 1:
        score = 0.5
        reason = (
            f"low activity ({commit_count} recent commits, "
            f"{total_changes} changed files)"
        )
        status = "warn"
    else:
        score = 0.2
        reason = "minimal activity detected"
        status = "poor"

    return {
        "score": score,
        "reason": reason,
        "status": status,
        "metrics": {
            "recent_commits": commit_count,
            "changed_files": total_changes,
        },
    }


def _assess_change_risk(git_changes: Dict[str, Any]) -> Dict[str, Any]:
    """Assess change risk using churn and rename analysis"""
    if not git_changes.get("available", False):
        return {
            "score": 0.5,
            "reason": "git data unavailable",
            "status": "unknown",
            "metrics": {"available": False},
        }

    file_stats = git_changes.get("file_stats", {})
    if not file_stats:
        return {
            "score": 0.7,
            "reason": "no churn data available",
            "status": "unknown",
            "metrics": {"churn_data_available": False},
        }

    total_additions = sum(
        stats.get("additions", 0) for stats in file_stats.values()
    )
    total_deletions = sum(
        stats.get("deletions", 0) for stats in file_stats.values()
    )
    total_churn = total_additions + total_deletions

    all_changes = git_changes.get("staged", []) + git_changes.get(
        "unstaged", []
    )
    rename_count = sum(
        1 for item in all_changes if item.get("status", "").startswith("R")
    )
    total_changed = len(all_changes)
    rename_ratio = rename_count / max(total_changed, 1)

    if total_churn < 100:
        churn_risk = 0.9
    elif total_churn < 500:
        churn_risk = 0.7
    else:
        churn_risk = 0.4

    rename_boost = min(0.3, rename_ratio * 0.5)
    final_score = min(1.0, churn_risk + rename_boost)

    if final_score >= 0.7:
        status = "good"
    elif final_score >= 0.5:
        status = "warn"
    else:
        status = "poor"

    return {
        "score": final_score,
        "reason": f"{total_churn} total churn",
        "status": status,
        "metrics": {
            "total_churn": total_churn,
            "rename_ratio": round(rename_ratio, 2),
            "additions": total_additions,
            "deletions": total_deletions,
        },
    }


# === OUTPUT GENERATION ===


def _build_snapshot(root: Path, debug: bool = False) -> Dict[str, Any]:
    """Build complete project snapshot with timing"""
    start_time = time.perf_counter()

    # Collect all data with timing
    git_basic = _get_git_basic_info(root)
    # git_changes = _get_git_changes_detailed(root)

    git_changes_timed = _get_git_changes_detailed(root)
    git_data_for_quality = (
        git_changes_timed.result.copy()
        if git_changes_timed.available
        else {"available": False, "error": git_changes_timed.error}
    )
    git_data_for_quality["available"] = git_changes_timed.available

    project_structure = _scan_project_structure(root)
    test_results = _run_pytest(root)

    _debug(
        "─ Git changes available: "
        f"{git_data_for_quality.get('available', False)}"
    )
    if git_data_for_quality.get("available", False):
        # git_data_for_quality IS the changes dict now
        changes = git_data_for_quality
        _debug(f"  ├─ Staged: {len(changes.get('staged', []))}")
        _debug(f"  ├─ Unstaged: {len(changes.get('unstaged', []))}")
        _debug(
            f"  └─ Recent commits: "
            f"{len(changes.get('recent_commits', []))}"
        )

    adr_verification_timed = _run_adr_verification(root)
    adr_verification = (
        adr_verification_timed.result
        if adr_verification_timed.available
        else {"available": False, "error": adr_verification_timed.error}
    )

    if test_results.available:
        test_data_for_quality = test_results.result.copy()
        test_data_for_quality["available"] = True
    else:
        test_data_for_quality = {
            "available": False,
            "error": test_results.error,
        }

    # Calculate quality score - FIX: pass the actual result data
    todos = (
        project_structure.result.get("todos", [])
        if project_structure.available
        else []
    )
    quality_assessment = _calculate_quality_score(
        (
            test_data_for_quality
            if test_data_for_quality["available"]
            else {"available": False}
        ),
        (
            git_data_for_quality
            if git_data_for_quality["available"]
            else {"available": False}
        ),
        todos,
        adr_verification,
    )

    # Environment security hashes
    env_hashes = {
        key: _safe_hash(os.environ.get(key)) for key in ENV_KEYS_TO_HASH
    }

    # Project hash for change detection
    project_hash = _calculate_project_hash(root)

    total_elapsed = (time.perf_counter() - start_time) * 1000

    return {
        "meta": {
            "schema_version": ANCHOR_SCHEMA_VERSION,
            "tool_version": ANCHOR_VERSION,
            "timestamp": _utc_timestamp(),
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "project_hash": project_hash,
            "total_elapsed_ms": round(total_elapsed, 1),
        },
        "git": {
            "basic": (
                git_basic.result
                if git_basic.available
                else {"available": False, "error": git_basic.error}
            ),
            "changes": (
                git_changes_timed.result
                if git_changes_timed.available
                else {"available": False, "error": git_changes_timed.error}
            ),
            "timing_ms": {
                "basic_info": git_basic.duration_ms,
                "detailed_changes": git_changes_timed.duration_ms,
            },
        },
        "project": {
            "structure": (
                project_structure.result
                if project_structure.available
                else {"available": False, "error": project_structure.error}
            ),
            "timing_ms": project_structure.duration_ms,
        },
        "tests": {
            "results": (
                test_results.result
                if test_results.available
                else {"available": False, "error": test_results.error}
            ),
            "timing_ms": test_results.duration_ms,
        },
        "quality_assessment": quality_assessment,
        "security": {"env_hashes": env_hashes},
        "adr_verification": adr_verification,
    }


def _calculate_project_hash(root: Path) -> str:
    """Calculate deterministic hash of project state for change detection"""
    hasher = hashlib.md5()

    try:
        # Sort paths for deterministic ordering
        file_paths = sorted(
            [p for p in root.rglob("*") if p.is_file() and not _is_ignored(p)]
        )

        for file_path in file_paths:
            try:
                stat = file_path.stat()
                rel_path = _normalize_path(file_path.relative_to(root))
                hasher.update(rel_path.encode("utf-8"))
                hasher.update(str(stat.st_mtime_ns).encode("utf-8"))
                hasher.update(str(stat.st_size).encode("utf-8"))
            except (OSError, PermissionError):
                continue
    except Exception:
        # Fallback to timestamp-based hash if file scanning fails
        hasher.update(str(time.time()).encode("utf-8"))

    return hasher.hexdigest()[:12]


def _write_output_files(
    root: Path, snapshot: Dict[str, Any]
) -> Tuple[Path, Path]:
    """Write JSON and Markdown output files to dated and latest directories"""
    date_str = dt.date.today().isoformat()
    anchor_dir = root / "docs" / "anchors" / date_str
    latest_dir = root / "docs" / "anchors" / "latest"

    # Create directories
    for directory in [anchor_dir, latest_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    # Write JSON with deterministic formatting
    json_content = json.dumps(
        snapshot, indent=2, ensure_ascii=False, sort_keys=True
    )
    json_path = anchor_dir / "anchor.json"
    json_path.write_text(json_content, encoding="utf-8")

    # Write Markdown summary
    md_content = _generate_markdown_summary(snapshot)
    md_path = anchor_dir / "anchor.md"
    md_path.write_text(md_content, encoding="utf-8")

    # Copy to latest (overwrite existing)
    latest_json = latest_dir / "anchor.json"
    latest_md = latest_dir / "anchor.md"
    shutil.copy2(json_path, latest_json)
    shutil.copy2(md_path, latest_md)

    return json_path, md_path


def _generate_markdown_summary(snapshot: Dict[str, Any]) -> str:
    """
    Generate concise human-readable Markdown summary optimized for LLM
    consumption
    """
    meta = snapshot["meta"]
    git_basic = snapshot["git"]["basic"]
    quality = snapshot["quality_assessment"]
    tests = snapshot["tests"]["results"]

    # Build executive summary for quick LLM scanning
    lines = [
        f"# Project Snapshot - {meta['timestamp']}",
        "",
        "## Executive Summary (LLM Quick Start)",
        f"- **Quality Score**: {quality['overall_score']}/1.0 - "
        f"{quality['explanation']}",
        f"- **Git**: `{git_basic.get('commit', 'unknown')}` on "
        f"`{git_basic.get('branch', 'unknown')}`",
        f"- **Dirty**: {'Yes' if git_basic.get('dirty') else 'No'}",
        f"- **Test Health**: {tests.get('health', 'unknown')} "
        f"({tests.get('counters', {}).get('passed', 0)} passed)",
        f"- **Generated**: {meta['total_elapsed_ms']}ms",
        "",
        "## Quality Component Breakdown",
    ]

    # Quality details for LLM evaluation
    for component, details in quality["components"].items():
        score = details["score"]
        reason = details["reason"]
        component_name = component.replace("_", " ").title()
        lines.append(f"- **{component_name}**: {score:.2f} - {reason}")

    # Recent activity summary
    lines.extend(["", "## Recent Activity"])

    project_data = snapshot["project"]["structure"]
    if project_data.get("available", False):
        recent_files = project_data.get("recent_files", [])
        if recent_files:
            lines.append(
                f"**Recent Files** ({len(recent_files)} in "
                f"last {RECENT_HOURS}h):"
            )
            for file_info in recent_files[:5]:  # Show top 5
                lines.append(
                    f"- `{file_info['path']}` ({file_info['modified']})"
                )
            if len(recent_files) > 5:
                lines.append(f"- ... and {len(recent_files) - 5} more")
        else:
            lines.append("No recent file activity detected")

    # Git changes summary
    git_changes = snapshot["git"]["changes"]
    if git_changes.get("available", False):
        staged = len(git_changes.get("staged", []))
        unstaged = len(git_changes.get("unstaged", []))
        untracked = len(git_changes.get("untracked", []))

        if staged + unstaged + untracked > 0:
            lines.extend(
                [
                    "",
                    "## Git Status",
                    f"- **Staged**: {staged} files",
                    f"- **Unstaged**: {unstaged} files",
                    f"- **Untracked**: {untracked} files",
                ]
            )

    lines.extend(
        [
            "",
            f"_Full data available in anchor.json "
            f"({meta['schema_version']})_",
        ]
    )

    return "\n".join(lines)


# === MAIN EXECUTION ===


def _create_argument_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser"""
    parser = argparse.ArgumentParser(
        description="Generate deterministic project snapshot for LLM handoffs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  {sys.argv[0]}                    # Generate snapshot for current directory
  {sys.argv[0]} --root /path       # Generate for specific directory
  {sys.argv[0]} --emit-eod         # Also generate END_OF_DAY.md file

Quality Score Components:
  Test Health (35%), Scope Appropriateness (20%), Technical Debt (15%),
  Code Quality (15%), Development Momentum (10%), Change Risk (5%)
        """,
    )

    parser.add_argument(
        "--root",
        type=Path,
        help="Project root directory (default: auto-detect from script "
        "location)",
    )
    parser.add_argument(
        "--emit-eod",
        action="store_true",
        help="Also generate docs/END_OF_DAY.md file",
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear cache and force fresh data collection",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output and timing information",
    )

    return parser


def _determine_project_root(
    script_path: Path, provided_root: Optional[Path]
) -> Path:
    """Determine project root directory using heuristics"""
    if provided_root:
        root = provided_root.resolve()
        if not root.exists():
            raise ValueError(f"Provided root directory does not exist: {root}")
        return root

    # Auto-detect: if script is in tools/, use parent directory
    script_dir = script_path.parent
    if script_dir.name == "tools":
        return script_dir.parent
    else:
        return script_dir


def main() -> None:
    """Main execution function"""
    parser = _create_argument_parser()
    args = parser.parse_args()

    global DEBUG
    if args.debug:
        DEBUG = True

    try:
        # Determine project root
        script_path = Path(__file__).resolve()
        root = _determine_project_root(script_path, args.root)

        if args.clear_cache:
            _debug("─ Cache disabled by --no-cache flag")
            _clear_cache(root)

        _debug(f"─ Schema version: {ANCHOR_SCHEMA_VERSION}")

        # Generate snapshot
        snapshot = _build_snapshot(root, args.debug)

        # Write output files
        json_path, md_path = _write_output_files(root, snapshot)

        # Generate END_OF_DAY.md if requested
        if args.emit_eod:
            eod_path = _generate_end_of_day(root, snapshot)
            print(f"Generated END_OF_DAY: {eod_path}")

        # Output summary
        quality_score = snapshot["quality_assessment"]["overall_score"]
        elapsed_ms = snapshot["meta"]["total_elapsed_ms"]

        print("Generated snapshot:")
        # print(f"  JSON: {json_path}")
        # print(f"  Markdown: {md_path}")

        latest_dir = root / "docs" / "anchors" / "latest"

        print("Wrote:")
        print(f"  - {md_path}")
        print(f"  - {json_path}")
        print("Copied to:")
        print(f"  - {latest_dir}\\anchor.md")
        print(f"  - {latest_dir}\\anchor.json")

        print(f"  Quality Score: {quality_score}/1.0")
        print(f"  Completed in: {elapsed_ms}ms")

        # Quick summary for immediate context
        git_info = snapshot["git"]["basic"]
        commit = git_info.get("commit", "unknown")
        branch = git_info.get("branch", "unknown")
        dirty = git_info.get("dirty", False)

        print("\nQuick Context:")
        print(f"  Git: {commit} on {branch} {'(dirty)' if dirty else ''}")
        print(
            f"  Tests: {snapshot['tests']['results'].get('health', 'unknown')}"
        )
        print(f"  Quality: {snapshot['quality_assessment']['explanation']}")

    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        _error(e)
        if DEBUG:
            import traceback

            traceback.print_exc()
        sys.exit(1)


def _generate_end_of_day(root: Path, snapshot: Dict[str, Any]) -> Path:
    """Generate END_OF_DAY.md file (placeholder implementation)"""
    # This would need actual implementation based on your current EOD format
    eod_content = f"""# END OF DAY - {snapshot['meta']['timestamp']}

Quality Score: {snapshot['quality_assessment']['overall_score']}/1.0
{snapshot['quality_assessment']['explanation']}

See anchor.json for full details.
"""

    eod_path = root / "docs" / "END_OF_DAY.md"
    eod_path.parent.mkdir(exist_ok=True)
    eod_path.write_text(eod_content, encoding="utf-8")
    return eod_path


if __name__ == "__main__":
    main()
