# Elktron Dashboard

Real-time operations dashboard for the Elktron hackathon project — two DC floor robots controlled and monitored from a single interface.

## The Problem

DCTs manage robot arms and escort bots manually. There's no unified view of what the arm is doing, what the escort bot scanned, or whether a vendor touched something they shouldn't have. This dashboard is the control center.

## What It Does

- **Live arm status** — see joint angles, gripper state, and current task in real time
- **Escort monitoring** — watch the bot escort a vendor, scan a rack, and flag unauthorized contact
- **Scan history** — every vendor escort produces a JSON report. Browse, filter, drill in.
- **Training controls** — start/stop teleoperation recording, kick off cloud training, download models
- **Camera feeds** — live USB webcam streams from the arm wrist and escort bot

## Demo Story

1. **Arm demo** — open dashboard, show arm status "READY". Start teleoperation. Move arm to pick optic. Show joint angles updating live. Stop recording. Kick off training.
2. **Escort demo** — vendor arrives. Dashboard shows "Escorting to CAB-B3". Bot arrives, baseline scan runs. Vendor works on RU-24. Dashboard shows live node status. RU-25 gets a brief contact — amber alert, then clears. Work completes. Scan report saved.
3. **Review demo** — open scan log. Show 3 past scans: 2 clean, 1 flagged. Drill into the flagged one — unauthorized contact on RU-19 that didn't resolve.

## Tech Stack

- **Frontend:** HTML + vanilla JS + CSS Grid. WebSocket for live data.
- **Backend:** Python FastAPI. WebSocket bridge to hardware.
- **Hardware:** LeRobot (arm), ROS2 or GPIO (escort bot), USB webcams.
