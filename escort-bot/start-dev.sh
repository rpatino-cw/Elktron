#!/usr/bin/env bash
# Launch browser-sync with file watching for escort-bot dev
# Watches all HTML/CSS/JS files, auto-reloads on save
cd "$(dirname "$0")" || exit 1

# Kill stale processes on configured ports
lsof -ti:8081,8082 | xargs kill 2>/dev/null
sleep 0.5

exec browser-sync start --config bs-config.js
