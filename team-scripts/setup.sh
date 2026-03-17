#!/bin/bash
# ============================================================
# ELKTRON TEAM SETUP
# Run this ONCE to get the project on your laptop.
# Open Terminal, paste this, hit Enter:
#   bash setup.sh
# ============================================================

set -e

REPO_URL="https://github.com/rpatino-cw/Elktron.git"
FOLDER="Elktron"

echo ""
echo "=============================="
echo "  ELKTRON — Team Setup"
echo "=============================="
echo ""

# Check for git
if ! command -v git &> /dev/null; then
    echo "Git is not installed."
    echo ""
    echo "TO FIX (Mac):"
    echo "  1. Open Terminal"
    echo "  2. Type: xcode-select --install"
    echo "  3. Click Install in the popup"
    echo "  4. Wait for it to finish, then run this script again"
    echo ""
    exit 1
fi

# Check if already cloned
if [ -d "$FOLDER" ]; then
    echo "Folder '$FOLDER' already exists. Pulling latest..."
    cd "$FOLDER"
    git pull
    echo ""
    echo "DONE — You're up to date."
    exit 0
fi

# Clone
echo "Downloading the project..."
git clone "$REPO_URL"
cd "$FOLDER"

echo ""
echo "=============================="
echo "  SETUP COMPLETE"
echo "=============================="
echo ""
echo "Your project is in the '$FOLDER' folder."
echo ""
echo "NEXT STEPS:"
echo "  cd $FOLDER"
echo "  bash push.sh        ← to save and upload your changes"
echo "  bash pull.sh         ← to get everyone else's changes"
echo ""
