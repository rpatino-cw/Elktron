# FloorCrew — Progress Log

## Project Overview
**Two robots for the CoreWeave Hackathon (March 23, 2026)**
1. **SO-101 Arm** — Imitation learning for DC tasks (optic seating)
2. **Escort Bot** — Person-following vendor escort on the DC floor

---

## Current Status

| Robot | Code | Hardware | Tested | Demo Ready |
|-------|------|----------|--------|------------|
| SO-101 Arm | Done | **Ordered 3/9** — ETA ~3/18 | No | No |
| Escort Bot | Done | **Ordered 3/9** — ETA ~3/11 | No | No |

---

## What's Been Done

### Session: 2026-03-09 (late night)

**Parts List Finalized + Verified**
- Created `PARTS-LIST.md` — detailed BOM with Amazon links, checkboxes, wiring diagrams, cost summary
- Verified Freenove 4WD kit (FNK0043) includes: integrated motor driver (Smart Car Board PCB), HC-SR04 ultrasonic + servo mount, Pi Camera (CSI), 2x servos for pan-tilt, IR line tracking, LEDs, buzzer
- Confirmed: L298N, HC-SR04P, USB webcam, camera mount are NOT needed separately — all in Freenove kit
- Savings: ~$37 off original estimate
- Added Raspberry Pi 5 Official Active Cooler (~$5) — REQUIRED to prevent thermal throttle under TFLite CV workload

**Pi 5 Setup Guide**
- Created `escort-bot/PI-SETUP.md` — complete SD flashing + first boot + software setup guide
- **OS choice: Raspberry Pi OS Lite (64-bit) — Bookworm** — only OS that supports Pi 5, 64-bit for TFLite perf, Lite for headless (saves ~500MB RAM), ships Python 3.11 + lgpio
- Covers: Imager download, pre-configured WiFi/SSH, first boot, install.sh, verification tests, troubleshooting, demo-day perf tips

**Updated Cost**
- Escort bot: ~$145 (down from ~$177 after removing kit duplicates + adding cooler)
- SO-101 arm: ~$311
- Shared/demo: ~$17-47
- Grand total: ~$468-498

---

### Session: 2026-03-09 (evening)

**Hardware Ordered**
- Freenove 4WD Smart Car Kit — Amazon — ETA 3/11
- Samsung 30Q 18650 batteries + charger — Amazon — ETA 3/11
- MakerFocus Pi Battery Pack 10000mAh — Amazon — ETA 3/11
- HiWonder LeRobot SO-ARM101 Kit — hiwonder.com — **ETA ~3/18 (long pole)**
- NexiGo N60 1080P Webcam — Amazon — ETA 3/11
- Total: ~$408

**Camera-Only Test Script**
- Created `escort-bot/test_camera.py` — runs person detection without motors or ultrasonic
- Two modes: headless (terminal only) and `--display` (live video with bounding boxes)
- Simulates steering output so you can validate detection + steering logic before chassis arrives
- Run: `python3 test_camera.py` (headless) or `python3 test_camera.py --display` (with video)

---

### Session: 2026-03-09

**Research**
- Found iRobot Create 3 repos (decided against — overkill for this use case)
- Evaluated chassis options: Freenove 4WD ($65), SunFounder PiCar-X ($82), Yahboom ($70)
- Chose Freenove 4WD as escort bot platform
- Evaluated detection approaches: MobileNet SSD v2 (TFLite) wins at ~20 FPS on Pi 5
- Decided to skip ROS 2 — too heavy for a single-Pi demo, gpiozero is enough
- Researched SO-101 arm: HiWonder kits ($270-$460), LeRobot framework, ACT policy
- Found forkable repos: mshakeelt/Human-Following-Robot, LeRobot hackathon repo

**Escort Bot — Scaffolded**
- `hackathon/escort-bot/main.py` — Full person-following logic (~150 lines). TFLite MobileNet SSD + gpiozero + HC-SR04 ultrasonic. Proportional steering with distance control.
- `hackathon/escort-bot/install.sh` — One-command Pi 5 setup (apt + pip + model download)
- `hackathon/escort-bot/requirements.txt` — picamera2, tflite-runtime, gpiozero, numpy, lgpio
- `hackathon/escort-bot/WIRING.md` — GPIO pin map, L298N wiring, HC-SR04 voltage divider, test commands
- `hackathon/escort-bot/showcase.html` — Project scope page (white/navy theme, animations, 3D)

**SO-101 Arm — Scaffolded**
- `hackathon/robotics-site/so101/record.py` — Record demos via leader-follower teleoperation. 3 tasks defined: optic_seating (50 eps), rack_inspection (30), cable_management (100).
- `hackathon/robotics-site/so101/train.py` — Train ACT policy. Supports cuda/mps/cpu.
- `hackathon/robotics-site/so101/deploy.py` — Deploy trained model for autonomous execution.
- `hackathon/robotics-site/so101/install.sh` — venv + LeRobot from source + deps
- `hackathon/robotics-site/so101/requirements.txt` — lerobot, torch, opencv, numpy, tensorboard
- `hackathon/robotics-site/so101/HARDWARE.md` — BOM, assembly notes, kit tiers, compute options
- `hackathon/robotics-site/so101/showcase.html` — Project scope page (white/navy, 3D image, animations)

**Config Updates**
- Updated `hackathon/CLAUDE.md` — registered escort-bot, updated focus check to show both robots
- Updated `memory/MEMORY.md` — FloorCrew = two robots, Pi 4/5 as escort platform

---

## Hardware Shopping List

### Escort Bot (~$113) — Ordered 2026-03-09
- [x] Freenove 4WD Smart Car Kit — ~$65 (Amazon) — ETA 3/11
- [x] Samsung 30Q 18650 batteries + charger (2-pack) — ~$18 (Amazon) — ETA 3/11
- [x] MakerFocus Pi Battery Pack 10000mAh — ~$30 (Amazon) — ETA 3/11
- [x] Raspberry Pi 5 — already owned

### SO-101 Arm (~$295) — Ordered 2026-03-09
- [x] HiWonder LeRobot SO-ARM101 Kit — ~$270 (hiwonder.com) — **ETA ~3/18 (ships from China, 6 biz days)**
- [x] NexiGo N60 1080P Webcam — ~$25 (Amazon) — ETA 3/11
- [x] Raspberry Pi 5 or laptop — already owned

### Total: ~$408 (ordered)

---

## Key Decisions Made

| Decision | Chose | Over | Why |
|----------|-------|------|-----|
| Escort platform | Pi 5 + Freenove chassis | iRobot Create 3 | Already own Pi, $65 vs $300 |
| Detection model | MobileNet SSD v2 (TFLite) | YOLO, HOG | 20 FPS on Pi 5, no training needed |
| Motor framework | gpiozero | ROS 2 | One file, zero setup overhead |
| Arm kit | HiWonder SO-ARM101 | Seeed Studio + 3D print | Faster, all parts included |
| Training policy | ACT (Action Chunking) | Diffusion, RL | LeRobot default, works with 50 demos |
| Demo task | Optic seating | Cable management, rack inspection | Most tractable, clear success/fail |

---

## What's Next

### Immediate (before March 12)
1. [x] Order Freenove kit + batteries + power bank — **Done 3/9**
2. [x] Order SO-ARM101 DIY kit + webcam — **Done 3/9**
3. [x] Create detailed parts list with Amazon links — **Done 3/9** (`PARTS-LIST.md`)
4. [x] Verify Freenove kit contents (motor driver, sensor, camera) — **Done 3/9**
5. [x] Create Pi 5 setup guide — **Done 3/9** (`escort-bot/PI-SETUP.md`)
6. [ ] **Sign up for hackathon (deadline: March 12) — 3 DAYS LEFT**
7. [ ] Order Pi 5 Active Cooler (~$5) — Amazon
8. [ ] Flash Pi 5 SD card (Bookworm Lite 64-bit) — see `PI-SETUP.md`
9. [ ] Camera-only detection test on Pi 5 (`python3 test_camera.py`)

### Week of March 11-15 (Escort Bot assembly)
10. [ ] Assemble Freenove chassis + connect motors/sensors (~2 hrs, kit has instructions)
11. [ ] Run escort-bot `install.sh` on Pi 5 (~45 min)
12. [ ] First escort bot test — person detection + motor control
13. [x] Write `floorcrew-app/api/arm.py` — LeRobot serial interface — **Done 3/10**
14. [x] Write `floorcrew-app/api/escort.py` — escort telemetry — **Done 3/10**
15. [x] Write `floorcrew-app/api/models.py` — Pydantic schemas — **Done 3/10**
16. [x] Build dashboard panels in `floorcrew-app/index.html` — **Already complete** (all 5 panels + JS + WebSocket)

### Week of March 16-19 (SO-101 Arm assembly)
17. [ ] Assemble SO-101 arms when kit arrives (~2-3 hrs)
18. [ ] Install LeRobot, calibrate servos (~1 hr)
19. [ ] First autonomous test — keyboard teleop if leader arm not working

### Week of March 20-22
9. [ ] Tune escort bot on DC floor (Kp, speed, thresholds) (~2-4 hrs)
10. [ ] Record 50 optic seating demonstrations (~1-2 hrs)
11. [ ] Train ACT policy (~2-4 hrs, runs unattended)
12. [ ] Evaluate + retrain if needed (~2 hrs)
13. [ ] Demo polish — clean wiring, signage, camera feeds
14. [ ] Record 2-3 min demo video

### March 23 — Demo Day

---

## File Map

```
hackathon/
├── CLAUDE.md                          # Hackathon root config
├── PROGRESS.md                        # THIS FILE — single source of truth
├── PARTS-LIST.md                      # Hardware BOM + Amazon links + costs
├── CHECKLIST-SO101.md                 # 10-phase arm build checklist
├── CHECKLIST-ESCORT-BOT.md            # 11-phase bot build checklist
├── VELOCITY.md                        # Engineering philosophy
├── WORKFLOW.md                        # Demo day timeline
├── escort-bot/
│   ├── main.py                        # Person-following robot brain (211 lines, complete)
│   ├── test_camera.py                 # Camera-only detection test (no motors)
│   ├── install.sh                     # Pi 5 software setup
│   ├── requirements.txt
│   ├── WIRING.md                      # GPIO + wiring diagrams
│   ├── PI-SETUP.md                    # Pi 5 OS flashing + first boot guide
│   └── showcase.html                  # Scope page
├── robotics-site/
│   ├── index.html                     # FloorCrew landing page
│   ├── CLAUDE.md                      # Robotics site config
│   └── so101/
│       ├── record.py                  # Record demos (scaffolded, ready)
│       ├── train.py                   # Train ACT policy (scaffolded, ready)
│       ├── deploy.py                  # Deploy autonomous (scaffolded, ready)
│       ├── install.sh                 # LeRobot setup
│       ├── requirements.txt
│       ├── HARDWARE.md                # BOM + assembly
│       └── showcase.html              # Scope page
└── floorcrew-app/
    ├── CLAUDE.md                      # Dashboard architecture spec
    ├── index.html                     # Dashboard UI (layout only, needs panels)
    └── api/
        ├── server.py                  # FastAPI + WebSocket (mock data, working)
        ├── arm.py                     # ✅ LeRobot Feetech motor bus interface
        ├── escort.py                  # ✅ Pi 5 telemetry + scan management
        └── models.py                  # ✅ Pydantic schemas (arm, escort, scan, training)
```
