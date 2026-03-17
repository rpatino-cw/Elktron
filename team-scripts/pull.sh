#!/bin/bash
# ============================================================
# ELKTRON — GET LATEST CHANGES
# Run from inside the Elktron folder:
#   bash pull.sh
# ============================================================

echo ""
echo "=============================="
echo "  ELKTRON — Get Latest"
echo "=============================="
echo ""

# Make sure we're in a git repo
if [ ! -d ".git" ]; then
    echo "ERROR: You're not inside the Elktron folder."
    echo ""
    echo "FIX: Run this first:"
    echo "  cd Elktron"
    echo "  bash pull.sh"
    echo ""
    exit 1
fi

# Stash any local changes so pull doesn't fail
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "Saving your local changes first..."
    git stash
    git pull
    echo "Restoring your local changes..."
    git stash pop
else
    git pull
fi

echo ""
echo "DONE — You have the latest version."
echo ""
