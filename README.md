# Elktron — Two Robots for the DC Floor

> CoreWeave Hackathon 2026 · "More. Better. Faster." · Build with Velocity

## What Is This

Two robots that automate repetitive data center floor tasks:

1. **SO-101 Robot Arm** — Learns DC tasks (optic seating, rack inspection) via imitation learning. You demonstrate, it repeats autonomously.
2. **Escort Bot** — Follows vendors through the DC floor using computer vision. Monitors rack interactions, logs everything.
3. **Elktron Dashboard** — Unified control panel showing arm status, escort tracking, camera feeds, and scan logs.

## Why

DCTs spend hours on tasks that are mechanical, repetitive, and physically demanding. Vendor escorts tie up a technician who could be doing real work. Elktron puts robots on those tasks so humans focus on what requires judgment.

## Tech Stack

| Component | Stack |
|-----------|-------|
| SO-101 Arm | LeRobot (HuggingFace) · ACT policy · Feetech servos · Python |
| Escort Bot | Raspberry Pi 5 · TFLite MobileNet SSD v2 · gpiozero · 4WD chassis |
| Dashboard | FastAPI · WebSocket · Vanilla JS · CSS Grid |

## Repo Structure

```
├── robotics-site/          # SO-101 arm — landing page + code
│   └── so101/              # record.py, train.py, deploy.py, install.sh
├── escort-bot/             # Escort bot — main.py, wiring, setup
├── elktron-app/          # Dashboard — FastAPI + WebSocket UI
│   └── api/server.py
├── CHECKLIST-SO101.md       # Full build checklist (10 phases, ~150 items)
├── CHECKLIST-ESCORT-BOT.md  # Full build checklist (11 phases, ~160 items)
├── PROGRESS.md              # What's done, what's next, hardware status
├── PARTS-LIST.md            # Hardware shopping list + costs
├── VELOCITY.md              # Engineering philosophy
├── WORKFLOW.md              # Day-of timeline
└── TEAM.md                  # Team info
```

## Key Dates

| Date | Event |
|------|-------|
| **March 12** | Sign-up deadline |
| **March 23–25** | Hackathon build days |
| **March 26** | Demo Day (2–5pm ET) |

## Getting Started

**Escort Bot (Pi 5):**
```bash
cd escort-bot
chmod +x install.sh && ./install.sh
# Wire motors + ultrasonic per WIRING.md
python3 main.py
```

**SO-101 Arm (Mac/Linux):**
```bash
cd robotics-site/so101
chmod +x install.sh && ./install.sh
# Assemble arms per HARDWARE.md
python record.py    # Record demos
python train.py     # Train policy
python deploy.py    # Run autonomous
```

## Hardware Cost

| Item | Cost | Status |
|------|------|--------|
| Freenove 4WD Kit | $65 | Ordered 3/9 |
| HiWonder SO-ARM101 | $270 | Ordered 3/9 |
| Batteries + power bank | $48 | Ordered 3/9 |
| Webcam | $25 | Ordered 3/9 |
| **Total** | **$408** | All ordered |

## Demo Story (3 minutes)

1. **Arm** (60s) — SO-101 picks optic from tray, seats it into switch port. Dashboard shows live joint angles.
2. **Escort** (60s) — Bot follows "vendor" through aisle, stops at rack, monitors work. Dashboard shows tracking.
3. **Review** (30s) — Scan log shows vendor visits, flagged events, clean/flagged status.

## Team

See `TEAM.md`
