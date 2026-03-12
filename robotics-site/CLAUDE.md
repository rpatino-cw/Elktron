# Elktron — DC Robotics

## One-Line
SO-101 robot arm for autonomous DC floor tasks — optic seating, rack inspection, cable management.

## Problem
DCTs perform repetitive physical tasks (seating optics, inspecting racks, dressing cables) that are time-consuming, error-prone, and could be automated with a low-cost robot arm trained via imitation learning.

## What It Does
1. Build SO-101 robot arm (~$120/arm) using LeRobot framework
2. Train via imitation learning (leader-follower teleoperation)
3. Deploy on DC floor for targeted tasks (optic seating, visual inspection, cable routing)

## Demo Story
1. **Optic Seating** — Robot arm picks transceiver from tray, seats it into switch port
2. **Rack Inspection** — Arm-mounted camera scans rack face, flags unseated cables or LED faults
3. **Cable Dress** — Arm routes patch cable along rack rail, secures with velcro

## Tech Stack
- **Robot:** SO-101 (6-DOF, Feetech STS3215 servos)
- **Framework:** LeRobot (HuggingFace) — imitation learning + RL
- **Language:** Python
- **Hardware:** ~$120/arm + 3D printed parts + Bambu/Ender printer
- **Training:** ACT policy, Diffusion Policy, or SmolVLA

## Resources
- [SO-101 Assembly & Setup Guide](https://huggingface.co/docs/lerobot/en/so101) — official HuggingFace docs
- [Build & AI Hack the SO-101 (LinkedIn)](https://www.linkedin.com/pulse/lets-build-ai-hack-lerobot-so101-haoran-xu-onaqc/) — Haoran Xu's build log, keyboard teleop without leader arm
- [Teleop Branch (GitHub)](https://github.com/seanxu112/lerobot/tree/teleop) — keyboard teleoperation code for single-arm setup (no leader needed)
- [LeRobot Main Repo](https://github.com/huggingface/lerobot) — full framework: datasets, policies, training, eval
- [HiWonder SO-101 Kit (Pre-built)](https://www.hiwonder.com/products/lerobot-so-101) — buy pre-assembled instead of 3D printing, faster path to demo

## Key Insight from Haoran Xu's Article
- You can control the follower arm WITHOUT a leader arm using keyboard teleop
- `MotorsBus.sync_write()` sends serial commands to each servo
- Copilot Agent mode generated ~400 lines of teleop glue code in 5 min
- Next steps in article: Inverse Kinematics, ROS2 wrapper, MoveIt integration

## File Structure
```
robotics-site/
├── CLAUDE.md              # this file
├── index.html             # Elktron landing page (dark luxury-tech)
├── elktron-robots.blend # 3D assets
└── (future)
    ├── teleop/            # keyboard teleop scripts
    ├── training/          # imitation learning configs
    └── demo/              # recorded demo videos
```

## Status
- [x] Landing page built (index.html)
- [x] 3D assets created (elktron-robots.blend)
- [ ] SO-101 parts sourced
- [ ] Arms 3D printed
- [ ] Arms assembled & calibrated
- [ ] LeRobot installed & configured
- [ ] Keyboard teleop working (single arm)
- [ ] Leader-follower teleoperation working
- [ ] Imitation learning trained
- [ ] DC task demo recorded
- [ ] Slides done
- [ ] Video recorded

## Judging Track
Build with Velocity

## Winning Criteria Check
- [x] Closes a loop (trains and executes physical tasks autonomously)
- [x] Physical/DC-native angle (robot arm on the DC floor)
- [ ] Shippable in 48h with static data (hardware build required — tight)
- [x] Clear before/after story (manual optic seating vs. autonomous)
- [x] No finance data or politics needed
