# Elktron — All Hackathon Sites

> Complete index of every HTML page in `/Users/rpatino/hackathon/`.

---

## Quick Open

| Page | URL |
|------|-----|
| Hub | `file:///Users/rpatino/hackathon/index.html` |
| Landing | `file:///Users/rpatino/hackathon/robotics-site/index.html` |
| Dashboard | `http://localhost:8080` |
| Simulation | `file:///Users/rpatino/hackathon/escort-bot/simulation.html` |

---

## Three.js 3D Pages (9)

| # | File | Description | Three.js | Status |
|---|------|-------------|----------|--------|
| 1 | `index.html` | Hub with 3D background, 5-phase timeline | v0.170.0 | Working |
| 2 | `escort-bot/simulation.html` | DC floor simulation (10 racks, bot AI, Soldier.glb model) | v0.162.0 | Working |
| 3 | `escort-bot/assembly.html` | Assembly instructions, 3D exploded view | v0.162.0 | Working |
| 4 | `escort-bot/BUILD-GUIDE.html` | Step-by-step build guide with 3D models | v0.170.0 | Working |
| 5 | `escort-bot/hardware-showcase.html` | All escort bot components in 3D | v0.170.0 | Working |
| 6 | `escort-bot/mast-hardware.html` | Mast assembly details (PVC, T-connector, pan-tilt) | v0.162.0 | Working |
| 7 | `escort-bot/wiring-guide.html` | Interactive wiring (GPIO, L298N, HC-SR04, servos, power) | v0.170.0 | Working |
| 8 | `robotics-site/topology.html` | System topology visualization | — | Working |
| 9 | `3d-reference/pi5-3d-model.html` | Interactive Raspberry Pi 5 3D model | v0.162.0 | Reference |

---

## Static Pages (6)

| # | File | Description | Status |
|---|------|-------------|--------|
| 1 | `robotics-site/index.html` | Elktron landing page (dark luxury-tech) | Working |
| 2 | `robotics-site/so101/showcase.html` | SO-101 robot arm scope page | Working |
| 3 | `escort-bot/showcase.html` | Escort bot scope page | Working |
| 4 | `parts-status.html` | Hardware inventory, shopping list, and status tracker | Working |
| 5 | `pitch-deck.html` | Pitch deck for presentation | Working |
| 6 | `taskboard/index.html` | Interactive task board | Working |

---

## Dashboard (Needs Server)

| # | File | Description | Status |
|---|------|-------------|--------|
| 1 | `elktron-app/index.html` | Dashboard app (FastAPI + vanilla JS + WebSocket) | Needs Server |
| 2 | `elktron-app/guide.html` | Dashboard usage guide | Working |

> Start the dashboard server before opening: requires FastAPI running on port 8080.

---

## Summary

| Category | Count |
|----------|-------|
| Three.js 3D Pages | 9 |
| Static Pages | 6 |
| Dashboard (server-dependent) | 2 |
| **Total** | **17** |
