# Elktron — All Hackathon Sites

> Complete index of every HTML page in `/Users/rpatino/hackathon/`.

---

## Quick Open

| Page | URL |
|------|-----|
| Hub | `file:///Users/rpatino/hackathon/hub.html` |
| Landing | `file:///Users/rpatino/hackathon/robotics-site/index.html` |
| Dashboard | `http://localhost:8080` |
| Simulation | `file:///Users/rpatino/hackathon/escort-bot/simulation.html` |
| Folder Topology | `file:///Users/rpatino/hackathon/topology-folders.html` |
| Context Topology | `file:///Users/rpatino/hackathon/topology-context.html` |
| Deep Topology | `file:///Users/rpatino/hackathon/topology-deep.html` |

---

## Three.js Version Note

Pages use a mix of Three.js versions: **v0.162.0**, **v0.163.0**, and **v0.170.0**. This should be unified to a single version before demo day to avoid subtle rendering differences or API breakage.

---

## Three.js 3D Pages (12)

| # | File | Description | Three.js | Status | URL |
|---|------|-------------|----------|--------|-----|
| 1 | `hub.html` | Central navigation hub with 3D background | v0.170.0 | Working | `file:///Users/rpatino/hackathon/hub.html` |
| 2 | `daily.html` | Daily standup page with 3D visuals | v0.163.0 | Working | `file:///Users/rpatino/hackathon/daily.html` |
| 3 | `escort-bot/simulation.html` | DC floor simulation (10 racks, bot AI, Soldier.glb model) | v0.162.0 | Working | `file:///Users/rpatino/hackathon/escort-bot/simulation.html` |
| 4 | `escort-bot/assembly.html` | Assembly instructions, 3D exploded view | v0.162.0 | Working | `file:///Users/rpatino/hackathon/escort-bot/assembly.html` |
| 5 | `escort-bot/BUILD-GUIDE.html` | Step-by-step build guide with 3D models | v0.170.0 | Working | `file:///Users/rpatino/hackathon/escort-bot/BUILD-GUIDE.html` |
| 6 | `escort-bot/hardware-showcase.html` | All escort bot components in 3D | v0.162.0 | Working | `file:///Users/rpatino/hackathon/escort-bot/hardware-showcase.html` |
| 7 | `escort-bot/hardware.html` | Interactive hardware reference with 3D | v0.162.0 | Working | `file:///Users/rpatino/hackathon/escort-bot/hardware.html` |
| 8 | `escort-bot/mast-hardware.html` | Mast assembly details (PVC, T-connector, pan-tilt) | v0.162.0 | Working | `file:///Users/rpatino/hackathon/escort-bot/mast-hardware.html` |
| 9 | `escort-bot/wiring-guide.html` | Interactive 3D wiring (GPIO, L298N, HC-SR04, servos, power) | v0.170.0 | Working | `file:///Users/rpatino/hackathon/escort-bot/wiring-guide.html` |
| 10 | `robotics-site/topology.html` | System topology visualization | — | Working | `file:///Users/rpatino/hackathon/robotics-site/topology.html` |
| 11 | `3d-reference/pi5-3d-model.html` | Interactive Raspberry Pi 5 3D model | v0.162.0 | Reference Only | `file:///Users/rpatino/hackathon/3d-reference/pi5-3d-model.html` |
| 12 | `taskboard/index.html` | Interactive task board with 3D elements | — | Working | `file:///Users/rpatino/hackathon/taskboard/index.html` |

---

## Static Pages (12)

| # | File | Description | Status | URL |
|---|------|-------------|--------|-----|
| 1 | `robotics-site/index.html` | Elktron landing page (dark luxury-tech, Hermes-inspired, CSS only) | Working | `file:///Users/rpatino/hackathon/robotics-site/index.html` |
| 2 | `robotics-site/so101/showcase.html` | SO-101 robot arm scope page (CSS animations) | Working | `file:///Users/rpatino/hackathon/robotics-site/so101/showcase.html` |
| 3 | `escort-bot/showcase.html` | Escort bot scope page (CSS animations) | Working | `file:///Users/rpatino/hackathon/escort-bot/showcase.html` |
| 4 | `parts-status.html` | Hardware inventory, shopping list, and status tracker | Working | `file:///Users/rpatino/hackathon/parts-status.html` |
| 5 | `pitch-deck.html` | Pitch deck for presentation | Working | `file:///Users/rpatino/hackathon/pitch-deck.html` |
| 6 | `pitch-playbook.html` | Pitch playbook and talking points | Working | `file:///Users/rpatino/hackathon/pitch-playbook.html` |
| 10 | `img/2d_drawing/frame_trace.html` | Canvas-based frame tracing tool | Reference Only | `file:///Users/rpatino/hackathon/img/2d_drawing/frame_trace.html` |

---

## Dashboard (Needs Server)

| # | File | Description | Status | URL |
|---|------|-------------|--------|-----|
| 1 | `elktron-app/index.html` | Dashboard app (FastAPI + vanilla JS + WebSocket) | Needs Server | `http://localhost:8080` |
| 2 | `elktron-app/guide.html` | Dashboard usage guide | Working | `file:///Users/rpatino/hackathon/elktron-app/guide.html` |

> Start the dashboard server before opening: requires FastAPI running on port 8080.

---

## Pipeline / Tools (2D-to-3D)

Located in `2d_manual_3d/` — intermediate HTML files used in the chassis and Pi 5 2D-to-3D conversion pipeline.

| File | Description | Status |
|------|-------------|--------|
| `2d_manual_3d/*.html` | Multiple intermediate conversion pages for chassis and Pi 5 | Reference Only |

---

## Topology Visualizations (NEW)

| # | File | Description | Status | URL |
|---|------|-------------|--------|-----|
| 1 | `topology-folders.html` | D3.js collapsible folder tree — color-coded, searchable | Working | `file:///Users/rpatino/hackathon/topology-folders.html` |
| 2 | `topology-context.html` | D3.js force graph — CLAUDE.md hierarchy, memory banks, skills, MCP | Working | `file:///Users/rpatino/hackathon/topology-context.html` |
| 3 | `topology-deep.html` | D3.js force graph — 90 nodes, 150+ edges, everything connected | Working | `file:///Users/rpatino/hackathon/topology-deep.html` |

---

## Summary

| Category | Count |
|----------|-------|
| Three.js 3D Pages | 12 |
| Static Pages | 10 |
| Dashboard (server-dependent) | 2 |
| Topology Visualizations | 3 |
| Pipeline / Tools | Multiple |
| **Total** | **27+** |
