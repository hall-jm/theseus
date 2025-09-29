cat > .git/hooks/commit-msg <<'SH'
#!/usr/bin/env bash
# Wrapper so the reminder always shows and never blocks the commit.
# Git passes the commit message file as $1. We forward it (unused is fine).

"$(git rev-parse --show-toplevel)/tools/bash/commit_msg_reminder.sh" "$1"

# Always allow the commit to proceed
exit 0
SH

chmod +x .git/hooks/commit-msg

