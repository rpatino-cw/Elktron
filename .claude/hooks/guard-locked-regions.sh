#!/usr/bin/env bash
# ── Feature Lock Guard ──────────────────────────────────────
# Claude Code PreToolUse hook — blocks Edit/Write calls that
# touch code inside @LOCKED regions.
#
# Markers in source files:
#   // @LOCKED:feature-name
#   ... protected code ...
#   // @END-LOCKED:feature-name
#
# Exit codes:
#   0 = allow (not a locked region)
#   2 = block (touches locked code)
#
# Reads JSON from stdin: { tool_name, tool_input: { file_path, old_string, ... } }

set -euo pipefail

INPUT=$(cat)

TOOL=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null || echo "")

# Only guard Edit and Write tools
if [[ "$TOOL" != "Edit" && "$TOOL" != "Write" ]]; then
  exit 0
fi

FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null || echo "")

# Only guard files that actually have lock markers
if [[ -z "$FILE_PATH" || ! -f "$FILE_PATH" ]]; then
  exit 0
fi

# Fast path: only assembly.html has locks — skip grep for all other files
BASENAME=$(basename "$FILE_PATH")
if [[ "$BASENAME" != "assembly.html" ]]; then
  exit 0
fi

# Quick check: does the file even contain lock markers?
if ! grep -q '@LOCKED:' "$FILE_PATH" 2>/dev/null; then
  exit 0
fi

# For Write tool — block if file has ANY locked region (full overwrite = danger)
if [[ "$TOOL" == "Write" ]]; then
  LOCK_COUNT=$(grep -c '@LOCKED:' "$FILE_PATH" 2>/dev/null || echo "0")
  if [[ "$LOCK_COUNT" -gt "0" ]]; then
    LOCKED_NAMES=$(grep -oP '@LOCKED:\K[^\s]+' "$FILE_PATH" 2>/dev/null | sort -u | tr '\n' ', ' | sed 's/,$//')
    echo "BLOCKED: Cannot overwrite $FILE_PATH — it contains $LOCK_COUNT locked region(s): $LOCKED_NAMES. Use Edit tool to modify only unlocked sections." >&2
    exit 2
  fi
fi

# For Edit tool — check if old_string falls inside a locked region
OLD_STRING=$(echo "$INPUT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('tool_input',{}).get('old_string',''))
" 2>/dev/null || echo "")

if [[ -z "$OLD_STRING" ]]; then
  exit 0
fi

# Find all locked regions and check if old_string overlaps any
python3 -c "
import sys, re

file_path = sys.argv[1]
old_string = sys.argv[2]

with open(file_path, 'r') as f:
    content = f.read()

# Find all locked regions
regions = []
for m in re.finditer(r'// @LOCKED:(\S+)', content):
    name = m.group(1)
    start = m.start()
    end_pattern = f'// @END-LOCKED:{name}'
    end_pos = content.find(end_pattern, start)
    if end_pos == -1:
        end_pos = len(content)  # Unclosed = locked to EOF
    else:
        end_pos += len(end_pattern)
    regions.append((name, start, end_pos))

if not regions:
    sys.exit(0)

# Find where old_string appears in the file
pos = content.find(old_string)
if pos == -1:
    sys.exit(0)  # String not found — Edit will fail anyway, let it

edit_start = pos
edit_end = pos + len(old_string)

# Check overlap with any locked region
for name, lock_start, lock_end in regions:
    if edit_start < lock_end and edit_end > lock_start:
        line_num = content[:lock_start].count('\n') + 1
        print(f'BLOCKED: Edit touches locked region \"{name}\" (line {line_num}). This feature is locked and cannot be modified. Work around it or ask the user to unlock it first.', file=sys.stderr)
        sys.exit(2)

sys.exit(0)
" "$FILE_PATH" "$OLD_STRING"
