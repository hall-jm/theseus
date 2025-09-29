#!/usr/bin/env bash
# tools/bash/commit_msg_reminder.sh
# Recency + inclusion visibility before every commit. Non-blocking unless STRICT.

# Fail on undefined vars; keep non-blocking flow otherwise.
set -u

# --- Configuration -----------------------------------------------------------

# Key files to track (repo-relative, or repo-relative to PROJECT_DIR below).
IMPORTANT_FILES=(
  "docs/focus_hints.yaml"
  "docs/END_OF_DAY.md"
  # "docs/START_OF_DAY.md"
  "docs/WORKPLAN.md"
  "docs/anchors/latest/anchor.md"
  "README.md"
)

# Monorepo subdir (repo-relative). Override with COMMIT_REMINDER_PROJECT_DIR.
# Default to repo root for single-repo setups.
PROJECT_DIR="${COMMIT_REMINDER_PROJECT_DIR:-.}"

# "Recent" window in hours. Override with COMMIT_REMINDER_FRESH_HOURS.
FRESH_HOURS="${COMMIT_REMINDER_FRESH_HOURS:-18}"

# Strict mode requires ACK_REMINDER=1 to proceed.
STRICT_MODE="${COMMIT_REMINDER_STRICT:-0}"

# Upstream to compare against for "already committed on this branch".
# Use @{u} if available; fall back to origin/HEAD or origin/main.
UPSTREAM="${COMMIT_REMINDER_UPSTREAM:-@{u}}"

# Quiet in CI or ad-hoc mute.
if [[ "${CI:-}" == "true" || "${PRECOMMIT_SILENCE_REMINDER:-0}" == "1" ]]; then
  exit 0
fi

# Ensure we run at the repo root (pre-commit may invoke from subdirs).
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || printf ".")"
cd "$REPO_ROOT" || true

# --- Helpers ----------------------------------------------------------------

# Resolve upstream fallback chain.
resolve_upstream() {
  local up="$1"
  if git rev-parse --verify -q "$up" >/dev/null 2>&1; then
    printf "%s" "$up"; return
  fi
  # Try origin/HEAD → strip "origin/"
  local def="$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@' || true)"
  [[ -z "$def" ]] && def="main"
  printf "%s" "origin/$def"
}

# Collect lists once (repo-relative paths).
# - Staged for this commit.
STAGED_LIST="$(git diff --name-only --cached 2>/dev/null || true)"

# - Ahead-of-upstream set (already committed on this branch since the fork point).
UPSTREAM_RESOLVED="$(resolve_upstream "$UPSTREAM")"
MERGE_BASE="$(git merge-base "$UPSTREAM_RESOLVED" HEAD 2>/dev/null || true)"
if [[ -n "$MERGE_BASE" ]]; then
  AHEAD_LIST="$(git diff --name-only "$MERGE_BASE" HEAD 2>/dev/null || true)"
else
  AHEAD_LIST=""   # No upstream configured; we’ll treat only "staged" as present.
fi

# Path presence against a list, allowing PROJECT_DIR prefix variant.
has_path() {
  local rel="$1" list="$2"
  grep -qxF -- "$rel" <<<"$list" || grep -qxF -- "${PROJECT_DIR%/}/$rel" <<<"$list"
}

is_staged()     { has_path "$1" "$STAGED_LIST"; }
is_committed()  { has_path "$1" "$AHEAD_LIST"; }

# Resolve an IMPORTANT_FILE to an actual on-disk path to stat (first match wins).
resolve_path() {
  local rel="$1"
  if [[ -e "$rel" ]]; then
    printf "%s" "$rel"
  elif [[ -e "$PROJECT_DIR/$rel" ]]; then
    printf "%s" "$PROJECT_DIR/$rel"
  else
    printf "%s" ""
  fi
}

# Portable-ish mtime → epoch seconds.
mtime_epoch() {
  local p="$1"
  if [[ -z "$p" || ! -e "$p" ]]; then
    printf "%s" ""; return
  fi
  if date -r "$p" +%s >/dev/null 2>&1; then
    date -r "$p" +%s; return
  fi
  python - <<'PY' "$p" 2>/dev/null || true
import os, sys
p = sys.argv[1]
try:
    print(int(os.path.getmtime(p)))
except Exception:
    pass
PY
}

# Last commit timestamp for a path (epoch) or empty if none.
last_commit_epoch() {
  local p="$1"
  git log -1 --format=%ct -- "$p" 2>/dev/null || true
}

now_epoch() { date -u +%s; }

# Format a simple left/right line.
line() {
  # $1 label; $2 detail
  printf -- "%-40s %s\n" "$1" "$2"
}

# --- Report ------------------------------------------------------------------

echo
echo "───────────── Commit Reminder (inclusion + recency) ─────────────"
echo "Fresh window: < ${FRESH_HOURS}h considered 'Recent'"
echo

NOW="$(now_epoch)"

for rel in "${IMPORTANT_FILES[@]}"; do
  RESOLVED="$(resolve_path "$rel")"
  PRESENT="no"
  [[ -n "$RESOLVED" ]] && PRESENT="yes"

  INCLUDED="no"
  if is_staged "$rel" || is_committed "$rel"; then
    INCLUDED="yes"
  fi

  # Recency (Recent / Stale / Unknown)
  RECENCY="Unknown"
  NOTE=""
  if [[ "$PRESENT" == "yes" ]]; then
    MTIME="$(mtime_epoch "$RESOLVED")"
    LCMT="$(last_commit_epoch "$RESOLVED")"
    LAST_TS="$LCMT"
    if [[ -n "$MTIME" && -n "$LCMT" ]]; then
      (( MTIME > LCMT )) && LAST_TS="$MTIME"
    elif [[ -n "$MTIME" ]]; then
      LAST_TS="$MTIME"
    fi
    if [[ -n "$LAST_TS" ]]; then
      AGE_SEC=$(( NOW - LAST_TS ))
      AGE_HRS=$(( AGE_SEC / 3600 ))
      if (( AGE_HRS < FRESH_HOURS )); then
	    # Not a typo; keeping value to 5 characters
		# for formatting reasons;
        RECENCY="Recnt (<${FRESH_HOURS}h)"
      else
        RECENCY="Stale (≥${FRESH_HOURS}h)"
      fi
    fi
  else
    NOTE="missing on disk"
  fi

  # Label + symbol:
  # [✓] included in this commit (staged or ahead since fork)
  # [•] present on disk but not included this commit
  # [ ] missing on disk
  if [[ "$INCLUDED" == "yes" ]]; then
    line "- [✓] $rel" "Included · ${RECENCY}"
  elif [[ "$PRESENT" == "yes" ]]; then
    line "- [•] $rel" "      Present · Not in this commit · ${RECENCY}"
  else
    line "- [ ] $rel" "Not present · ${RECENCY}${NOTE:+ · $NOTE}"
  fi
done

echo
echo "Tips: COMMIT_REMINDER_FRESH_HOURS (default ${FRESH_HOURS})"
echo "      COMMIT_REMINDER_PROJECT_DIR (${PROJECT_DIR})"
echo "      PRECOMMIT_SILENCE_REMINDER=1 to mute"
echo "      COMMIT_REMINDER_STRICT=1 to require ACK"
echo "────────────────────────────────────────────────────────────────"
echo

# --- Optional strict gate ----------------------------------------------------

if [[ "$STRICT_MODE" == "1" && "${ACK_REMINDER:-}" != "1" ]]; then
  echo "⛔ Strict mode: set ACK_REMINDER=1 on the commit command to proceed." >&2
  echo "   Example: ACK_REMINDER=1 git commit -m 'feat: ...'" >&2
  exit 1
fi

exit 0
