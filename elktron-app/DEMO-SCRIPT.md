# Elktron — Demo Script (2-3 min)

## Setup
- Dashboard open on laptop: `file:///Users/rpatino/hackathon/elktron-app/index.html`
- Escort bot assembled on table (if hardware arrived)
- SO-101 arm assembled on table (if hardware arrived)
- Phone ready for backup video if live demo fails

---

## Script

### Opening — The Problem (30 sec)

"Every day in a CoreWeave data center, DCTs do hundreds of repetitive physical tasks — seating optics, escorting vendors to racks, scanning equipment before and after maintenance. These tasks are manual, time-consuming, and error-prone.

One misseated optic can take down a node. One unauthorized rack touch can go unnoticed for hours. We do these tasks well — but we shouldn't have to do them at all."

### The Solution — Elktron (15 sec)

"Elktron is two robots purpose-built for the DC floor. Not a dashboard. Not an LLM wrapper. Physical robots that do physical work."

### Robot 1: SO-101 Arm (45 sec)

*[Point to arm on table or show video]*

"This is the SO-101 — a 6-axis robot arm running on the LeRobot framework from HuggingFace. We trained it using imitation learning. A human demonstrates the task with a leader arm, the follower watches and learns. After 50 demonstrations, it executes autonomously.

Our first task: optic seating. The arm picks a transceiver from a tray, carries it to the switch, and seats it into the port. Every cycle is logged — joint angles, torque, accuracy down to the millimeter."

*[Gesture to dashboard — Arm Status panel showing live cycle]*

"You can see it cycling right now — reaching, gripping, transiting, inserting, releasing. Sub-millimeter accuracy. Consistent every time."

### Robot 2: Escort Bot (45 sec)

*[Point to bot on table or show video]*

"This is the Escort Bot — a Raspberry Pi 5 on a Freenove chassis with MobileNet SSD for person detection. It follows vendors to their assigned rack, then scans every node top to bottom before and after the work.

It monitors for unauthorized contact — if someone touches a rack unit they're not supposed to, it flags it immediately. When the vendor is done, it verifies the rack state matches the pre-scan. All logged, all timestamped."

*[Point to dashboard — Escort Bot panel showing live escort sequence]*

"Here you can see the escort cycle — dispatched, walking, scanning, monitoring. That amber alert? It detected contact on RU-25, verified it was incidental, and cleared it. Fully automated accountability."

### Dashboard (15 sec)

*[Show full dashboard]*

"Everything feeds into one real-time dashboard — arm status, escort tracking, camera feeds, rack scan history, and the training console. WebSocket-connected at 10Hz. No database — scan reports are JSON files, portable and auditable."

### Closing — Why This Matters (15 sec)

"Elktron isn't about replacing DCTs. It's about giving us tools that match the precision of the infrastructure we maintain. Every CoreWeave data center does these exact tasks hundreds of times a day. Two robots, trained in an afternoon, running 24/7. That's the pitch."

---

## Backup Plans

| Scenario | Backup |
|----------|--------|
| Arm not assembled | Pre-recorded video of training cycle |
| Bot not working | Dashboard demo mode shows full cycle |
| WiFi issues | Dashboard runs standalone (no server needed) |
| Projector issues | Phone screen share |

## Key Numbers to Mention
- SO-101: ~$270/arm, 6-DOF, 50 training demos, sub-mm accuracy
- Escort Bot: ~$145, MobileNet SSD at 20 FPS on Pi 5, 5-node scan in under 5 min
- Total project cost: ~$408
- Training time: ~2 hours (recording) + ~4 hours (model training, unattended)
- Framework: LeRobot (HuggingFace), OpenCV DNN, FastAPI, vanilla JS

## Judging Track
**Build with Velocity** — AI to accelerate DC construction and operations
