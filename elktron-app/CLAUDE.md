# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Elktron Dashboard

Real-time operations dashboard for two DC floor robots: SO-ARM101 (optic seating arm) and Escort Bot (vendor escort + rack scanner). This is the working app — not the pitch page (that's in `../robotics-site/`).

## What It Does

1. Connects to SO-ARM101 via LeRobot serial interface — shows arm state, joint angles, gripper status
2. Connects to Escort Bot — shows location, scan results, vendor escort logs
3. Displays live camera feeds (webcam over USB or WebSocket stream)
4. Training controls — start/stop teleoperation recording, trigger cloud training, monitor progress
5. Rack scan log — every vendor escort produces a scan report: node health, contact events, before/after state

## Architecture

```
elktron-app/
├── CLAUDE.md
├── index.html              # Main dashboard — single-page app
├── api/                    # Python backend (FastAPI)
│   ├── server.py           # WebSocket server — bridges hardware to frontend
│   ├── arm.py              # SO-ARM101 serial interface (LeRobot/feetech)
│   ├── escort.py           # Escort bot control + scan processing
│   └── models.py           # Data models — scan reports, training runs, logs
├── static/                 # Frontend assets
│   ├── dashboard.js        # Main UI logic — WebSocket client, state management
│   └── styles.css          # Dashboard styles
└── data/
    ├── scans/              # Rack scan JSON reports
    ├── training/           # Training run configs + status
    └── logs/               # Activity logs (vendor escorts, arm operations)
```

**Frontend:** Single HTML page + vanilla JS. No framework. WebSocket connection to backend for live data.

**Backend:** Python FastAPI server. Bridges hardware (serial USB for arm, GPIO/motor for escort bot) to WebSocket for the frontend. Also serves REST endpoints for scan history and training management.

**Hardware layer:** LeRobot's `MotorsBus` for arm servo control. Escort bot uses direct GPIO (Pi) or ROS2 (iRobot Create 3) depending on platform chosen.

## Build & Run

```bash
# Backend
cd api/
pip install fastapi uvicorn websockets pyserial lerobot
uvicorn server:app --reload --port 8080

# Frontend
# Just open index.html or serve via the FastAPI static mount
open http://localhost:8080
```

## Key Decisions

- **WebSocket, not polling** — arm state updates at ~10Hz, polling would lag. Single persistent WS connection.
- **No React/Vue** — this ships in 48 hours. Vanilla JS + DOM manipulation. CSS Grid for layout.
- **LeRobot as the arm interface** — don't write custom servo code. Use `lerobot.common.robot_devices.motors.feetech` directly.
- **Scan reports are JSON files** — no database. Each vendor escort produces one `scans/{timestamp}.json`. Simple, portable, demo-friendly.
- **Privacy-first escort logging** — the bot monitors rack state (node health, contact events), never captures or stores images of people. Camera feed is live-only, not recorded.

## Hardware Context

- **SO-ARM101:** 6-DOF, Feetech STS3215 servos, USB serial via driver board. LeRobot handles all motor comms.
- **Escort Bot platform:** TBD — either iRobot Create 3 (ROS2), RC chassis + Pi (GPIO), or phone-on-wheels. The `escort.py` module should abstract the platform behind a common interface.
- **MacBook M4** is the dev machine. MPS backend for local inference. USB-C hub for servo + webcam connections.

## Scan Report Schema

```json
{
  "timestamp": "2026-03-23T14:35:00Z",
  "vendor": "TechCo Field Eng.",
  "ticket": "INC-40821",
  "rack": "CAB-B3",
  "authorized_ru": "RU-24",
  "baseline": {
    "RU-26": { "status": "healthy", "optics": "ok", "psu": "ok" },
    "RU-25": { "status": "healthy", "optics": "ok", "psu": "ok" },
    "RU-24": { "status": "healthy", "optics": "ok", "psu": "ok" },
    "RU-23": { "status": "healthy", "optics": "ok", "psu": "ok" },
    "RU-22": { "status": "amber", "optics": "ok", "psu": "amber" }
  },
  "events": [
    { "time": "+2m14s", "ru": "RU-25", "type": "brief_contact", "resolved": true },
    { "time": "+4m30s", "ru": "RU-24", "type": "optic_swap", "authorized": true }
  ],
  "result": "clean",
  "unauthorized_changes": 0
}
```

## Dashboard Panels

1. **Arm Status** — joint angles (6 servos), gripper state (open/closed/holding), current task, training mode toggle
2. **Escort Bot** — location in aisle, current vendor/ticket, scan progress bar, live alerts
3. **Camera Feeds** — 1-2 live feeds (wrist cam + overhead or escort cam). WebSocket binary frames.
4. **Rack Scan Log** — table of past scans with status (clean/flagged), expandable detail per scan
5. **Training Console** — start recording, episode counter, upload to cloud, training progress, download model

## Judging Track

Build with Velocity

## Status

- [ ] FastAPI server scaffolded
- [ ] WebSocket connection working
- [ ] Arm status panel (mock data first, then real serial)
- [ ] Escort bot panel (mock data first)
- [ ] Camera feed integration
- [ ] Rack scan log viewer
- [ ] Training controls
- [ ] Live hardware connected
- [ ] Demo scenarios rehearsed
