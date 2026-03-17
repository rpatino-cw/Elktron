#!/bin/bash
# ============================================================
# ELKTRON — SAVE & UPLOAD YOUR CHANGES
# Run from inside the Elktron folder:
#   bash push.sh
# ============================================================

echo ""
echo "=============================="
echo "  ELKTRON — Save & Upload"
echo "=============================="
echo ""

# Make sure we're in a git repo
if [ ! -d ".git" ]; then
    echo "ERROR: You're not inside the Elktron folder."
    echo ""
    echo "FIX: Run this first:"
    echo "  cd Elktron"
    echo "  bash push.sh"
    echo ""
    exit 1
fi

# Show what changed
echo "Files you changed:"
echo "-------------------"
git status --short
echo ""

# Check if there's anything to push
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    echo "Nothing to upload — you haven't changed anything."
    exit 0
fi

# Ask for a message
echo "What did you change? (one sentence)"
printf "> "
read -r MSG

if [ -z "$MSG" ]; then
    MSG="Update from $(whoami)"
fi

# Pull first to avoid conflicts
echo ""
echo "Getting latest from team..."
git pull --rebase 2>/dev/null || git pull

# Stage, commit, push
git add -A
git commit -m "$MSG"
git push

echo ""
echo "=============================="
echo "  UPLOADED"
echo "=============================="
echo "Your changes are live on GitHub."
echo ""
