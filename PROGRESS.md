# Elktron — Progress Log

## Project Overview
**Two robots for the CoreWeave Hackathon (March 23, 2026)**
1. **SO-101 Arm** — Imitation learning for DC tasks (optic seating)
2. **Escort Bot** — Person-following vendor escort on the DC floor

---

## Current Status

| Robot | Code | Hardware | Tested | Demo Ready |
|-------|------|----------|--------|------------|
| SO-101 Arm | Done | **Ordered 3/9** — ETA ~3/18 | No | No |
| Escort Bot | Done | **Assembled 3/16** — chassis built, L298N wired, camera connected | **YES — person detection working** | In progress |

## Slack Checklist — 10 Steps to Demo Day

Tracked in `#the-elks-2026` Slack list.

| Phase | Task | Status | Assignee | Due |
|-------|------|--------|----------|-----|
| 1 | Sign up + admin — register team, share repo, confirm availability | **Done** | Josh | 3/12 |
| 2 | Receive + inventory hardware — open packages, verify, label, organize | **Done** | Alex, Romeo | 3/13 |
| 3 | Flash Pi + install software — Bookworm Lite, deps, YOLOv8n model | **Done** | Romeo | 3/14 |
| 4 | Build escort bot — assemble chassis, wire L298N, build mast, mount camera | **~80% done** — chassis + L298N + camera done, mast + HC-SR04 + motor power remaining | Alex, Raphael | 3/16 |
| 5 | Test escort bot — person detection, floor test, tune steering and speed | **In progress** — detection working, motor test next | Romeo, Raphael | 3/17 |
| 6 | Build SO-101 arm — assemble, calibrate, install LeRobot | Not started — kit ETA 3/18 | Josh | 3/19 |
| 7 | Train arm — record 50 demos, train ACT policy | Not started | Josh | 3/21 |
| 8 | Dashboard integration — live feeds, telemetry, scan log | Not started — backend written, needs Pi connection | Parth, Romeo | 3/21 |
| 9 | Demo polish — clean wiring, signage, rehearse | Not started | Talha, Raphael | 3/22 |
| 10 | Record + submit — 2-3 min video, slides, GitHub | Not started | Talha | 3/23 |

## Team (6 active + 1 observer)

| Person | Role | Owns |
|--------|------|------|
| **Romeo Patino** | Lead — architecture, software, demo story | System design, escort bot software, dashboard frontend, Pi setup |
| **Joshua Tapia** | Robot arm — CV, positioning, training | SO-101 assembly, calibration, ACT policy, optic seating demo |
| **Alex Murillo** | Escort bot hardware lead | Chassis build, wiring, motor/sensor integration, floor testing |
| **Parth Patel** | Backend lead | FastAPI server, Jira/NetBox data, WebSocket pipeline |
| **Talha Shakil** | Media & presentations | Demo video, pitch deck, logo, filming, editing |
| **Raphael Rodea** | Build crew + logistics | Assembly, parts inventory, batteries, wiring checks, packing, demo day "vendor" |
| **Andrew Westberg** | Observer | Watching and learning — not on active roster |

---

## What's Been Done

### Session: 2026-03-16

**MAJOR MILESTONE: Escort Bot Hardware Assembled + Person Detection Working on DC Floor**

**Hardware Assembly (at DC — EVI01)**
- LK-COKOINO 4WD chassis fully assembled — all 4 motors mounted, wheels attached, yellow tape labels (FR, FL, RR, RL)
- L298N motor driver (WWZMDiB) wired to Pi 5 GPIO — blue control wires for direction, red power wires to motor terminals
- Arducam IMX708 wide-angle camera connected via CSI ribbon cable ("Standard - Mini 200mm")
- Pi 5 in red case with official active cooler — running off USB-C power bank
- All assembly done at the DC workbench (Cisco switches visible in photos)

**Person Detection Test — SUCCESS**
- Ran `python3 /home/elktron/escort-bot/camtest.py` on Pi 5
- YOLOv8n model loaded and detecting persons at **0.78 confidence**
- Camera: libcamera v0.7.0+rpt20260205, IMX708 wide, 640x360 sRGB + 1536x864 RAW
- 5/5 frames captured, all detecting 1 person with bounding boxes
- SCP'd test images from Pi (elktron@192.168.3.57) to Mac for review

**Claude Code on Pi**
- Claude Code installed and running directly on the Pi 5
- On-device AI development confirmed — can iterate on detection code without leaving the DC

**Build Evidence**
- 26 photos captured — assembly process, wiring details, detection output
- All photos in `progression/` folder with descriptive filenames
- Terminal screenshots showing YOLOv8n output and SCP transfers

---

### Session: 2026-03-10

**Team Formed**
- Alex Murillo — ordering LK-COKOINO 4WD chassis kit (same one Romeo found), using her own Pi. ETA tomorrow (3/11).
- Josh Tapia — wrote robot arm technical breakdown: Computer Vision → Inverse Kinematics → End Effector → Optic Ammo. Scoped to one switch, one optic.
- Romeo — recommended LeRobot imitation learning to collapse Josh's CV + IK layers into one step (teach by demonstration instead of coding each separately). End effector identified as critical risk.

**Escort Bot Redesign**
- Bot needs to be **tall** — must scan full 42U rack top to bottom while escorting vendors
- Added pan/tilt servo for camera vertical sweep
- Switching from Freenove 4WD to LK-COKOINO chassis (Alex ordering) + separate Arducam camera + pan/tilt platform
- Differential (tank) steering confirmed over 4-wheel steering — simpler, more stable for a tall bot in straight DC aisles
- Mast needed: ~3-4 ft PVC pipe mounted on chassis to raise camera to mid-rack height

**Revised Hardware — Escort Bot**
- See updated shopping list below (3 stores: Amazon, Home Depot, Best Buy)

---

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
- Updated `memory/MEMORY.md` — Elktron = two robots, Pi 4/5 as escort platform

---

## Hardware Shopping List

### Escort Bot — REVISED 2026-03-10

**Amazon**
| Item | Price | Who Orders | ETA | Link |
|------|-------|-----------|-----|------|
| LK-COKOINO 4WD Chassis Kit | ~$25 | **Alex Murillo** | 3/11 | [Amazon](https://www.amazon.com/Arduino-LK-COKOINO-Raspberry-Building/dp/B0B5JPJ9R4) |
| Arducam 120° Wide Autofocus Camera (IMX708) | $59.99 | Romeo | **Ordered 3/10** — ETA 3/14 | [Amazon](https://www.amazon.com/Arducam-Raspberry-Camera-Autofocus-Acrylic/dp/B0BX7VFT8Q) |
| Arducam Pan Tilt Platform (2 servos + controller) | $26.99 | Romeo | **Ordered 3/10** — ETA 3/12 | [Amazon](https://www.amazon.com/Arducam-Upgraded-Camera-Platform-Raspberry/dp/B08PK9N9T4) |
| Pi 5 Active Cooler (Official) | $9.98 | Romeo | **Ordered 3/10** — ETA 3/11 | [Amazon](https://www.amazon.com/Raspberry-Pi-Active-Cooler/dp/B0CLXZBR5P) |
| WWZMDiB L298N Motor Driver 2-Pack | $6.98 | Romeo | **Ordered 3/10** — ETA 3/12 | [Amazon](https://www.amazon.com/WWZMDiB-L298N-H-Bridge-Controller-Raspberry/dp/B0CR6BX5QL) |
| ELEGOO HC-SR04 Ultrasonic 5-Pack | $8.99 | Romeo | **Ordered 3/10** — ETA 3/12 | [Amazon](https://www.amazon.com/ELEGOO-HC-SR04-Ultrasonic-Distance-MEGA2560/dp/B01COSN7O6) |
| DIYables HC-SR04 Ultrasonic 2-Pack | $6.99 | Romeo | **Ordered 3/10** — ETA 3/12 | [Amazon](https://www.amazon.com/Ultrasonic-Sensor-Arduino-ESP8266-Raspberry/dp/B0CKS867QC) |
| QTEATAK 18650 Battery Holder 8-Pack | $9.99 | Romeo | **Ordered 3/10** — ETA 3/12 | [Amazon](https://www.amazon.com/QTEATAK-18650-Battery-Holder-Bundle/dp/B08B86KHB2) |

**Home Depot (in-store pickup)**
| Item | Price | Link |
|------|-------|------|
| PVC Pipe 1" Schedule 40 (cut to ~4 ft for mast) | ~$5 | [Home Depot](https://www.homedepot.com/b/Plumbing-Pipe-Fittings-Pipe-PVC-Pipe/N-5yc1vZ1z18i41) |
| PVC T-connector (mount mast to chassis) | ~$2 | In-store |
| Velcro cable ties / strips (reusable) | ~$5 | Amazon |

**Best Buy (if needed)**
| Item | Price | Link |
|------|-------|------|
| USB-C Power Bank 20000mAh (powers Pi on bot) | ~$25 | [Best Buy](https://www.bestbuy.com/site/searchpage.jsp?st=power+bank) |
| MicroSD Card 32-64GB | ~$10 | [Best Buy](https://www.bestbuy.com/site/shop/raspberry-pi-micro-sd) |

**Already Owned**
- Raspberry Pi 4 and 5 (Romeo)
- Raspberry Pi (Alex)
- Pico (Romeo, backup)
- SIM card (Romeo)
- Velcro strips (Romeo)

**Arrival Tracker (updated 3/12)**
| Item | Ordered | ETA | Status |
|------|---------|-----|--------|
| Pi Active Fan | 3/10 | 3/10 | **Arrived** — confirm in hand |
| LK-COKOINO 4WD Chassis (Alex) | 3/10 | 3/11 | **Arrived** — confirm with Alex |
| 18650 batteries + charger | 3/9 | 3/11 | **Arrived** — confirm in hand |
| MakerFocus Pi battery pack | 3/9 | 3/11 | **Arrived** — confirm in hand |
| WWZMDiB L298N 2-Pack | 3/10 | 3/11 | **Arrived** — confirm in hand |
| ELEGOO HC-SR04 5-Pack | 3/10 | 3/11 | **Arrived** — confirm in hand |
| DIYables HC-SR04 2-Pack | 3/10 | 3/11 | **Arrived** — confirm in hand |
| QTEATAK 18650 holders 8-Pack | 3/10 | 3/11 | **Arrived** — confirm in hand |
| Arducam Pan Tilt Platform | 3/10 | 3/12 | **Arriving today** |
| Arducam Camera Module 3 Wide (IMX708) | 3/10 | 3/14 | In transit (Saturday) |
| PVC Pipe 1" x 10ft + Tee fitting | — | **Pickup ready** | In HD cart ($8.09) — pick up today |
| Raspberry Pi + SIM + Velcro | — | **Have** | Gather from home |

**Backup / Alternatives**
- [ ] ALAMSCN L293D Motor Driver + TT Motor Kit — [Amazon](https://www.amazon.com/ALAMSCN-Controller-Control-Expansion-Arduino/dp/B08Y24QBX3) — L293D shield (600mA/ch, lower than L298N's 2A). Backup if L298N doesn't work out.

**Still Needed**
- [x] ~~Motor driver board~~ — **Ordered 3/10** (WWZMDiB L298N 2-pack)
- [x] ~~Ultrasonic sensor~~ — **Ordered 3/10** (ELEGOO 5-pack + DIYables 2-pack)
- [x] ~~Battery holders~~ — **Ordered 3/10** (QTEATAK 8-pack)
- [x] ~~Power bank for Pi~~ — MakerFocus ordered 3/9
- [ ] **MicroSD card 32-64GB** — Check if Romeo has one. If not: [Samsung EVO Select 64GB ~$8](https://www.amazon.com/Samsung-microSDXC-Memory-Adapter-MB-ME64KA/dp/B0CWPPMD8K)

**Escort Bot Total: ~$103** (Romeo: ~$88 Amazon + ~$8 Home Depot. Alex covers chassis.)

### SO-101 Arm (~$295) — Ordered 2026-03-09
- [x] HiWonder LeRobot SO-ARM101 Kit — ~$270 (hiwonder.com) — **ETA ~3/18 (ships from China, 6 biz days)**
- [x] NexiGo N60 1080P Webcam — ~$25 (Amazon) — ETA 3/11
- [x] Raspberry Pi 5 or laptop — already owned

### Previously Ordered (3/9) — may overlap / backup
- [x] Freenove 4WD Smart Car Kit — ~$65 (Amazon) — ETA 3/11
- [x] Samsung 30Q 18650 batteries + charger — ~$18 (Amazon) — ETA 3/11
- [x] MakerFocus Pi Battery Pack 10000mAh — ~$30 (Amazon) — ETA 3/11

---

## Design Notes

### Escort Bot — Data Integration
The escort bot needs to connect to **Jira** and **NetBox** so it knows what devices are in what status. This enables the bot to be context-aware during vendor escorts — it can identify which rack/device the vendor is there to work on, what state the device is in (staged, provisioned, decommissioned, etc.), and cross-reference with open Jira tickets for that location. Romeo already has `JIRA_API_TOKEN` and `NETBOX_TOKEN` set in `~/.config/keys/global.env`, and the CW MCP server exposes `jira_search`, `netbox_find_device`, `netbox_rack_devices`, and `netbox_interfaces`.

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
6. [x] **Sign up for hackathon** — **Done 3/12** via `#more-better-faster-2026`
7. [x] Order Pi 5 Active Cooler (~$10) — **Ordered 3/10, ETA 3/11**
7b. [x] Order Arducam Camera + Pan-Tilt — **Ordered 3/10, ETA 3/12-3/14**
8. [ ] Flash Pi 5 SD card (Bookworm Lite 64-bit) — see `PI-SETUP.md`
9. [ ] Camera-only detection test on Pi 5 (`python3 test_camera.py`)

### Week of March 11-15 (Escort Bot assembly)
10. [ ] Assemble Freenove chassis + connect motors/sensors (~2 hrs, kit has instructions)
11. [ ] Run escort-bot `install.sh` on Pi 5 (~45 min)
12. [ ] First escort bot test — person detection + motor control
13. [x] Write `elktron-app/api/arm.py` — LeRobot serial interface — **Done 3/10**
14. [x] Write `elktron-app/api/escort.py` — escort telemetry — **Done 3/10**
15. [x] Write `elktron-app/api/models.py` — Pydantic schemas — **Done 3/10**
16. [x] Build dashboard panels in `elktron-app/index.html` — **Already complete** (all 5 panels + JS + WebSocket)

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
│   ├── index.html                     # Elktron landing page
│   ├── CLAUDE.md                      # Robotics site config
│   └── so101/
│       ├── record.py                  # Record demos (scaffolded, ready)
│       ├── train.py                   # Train ACT policy (scaffolded, ready)
│       ├── deploy.py                  # Deploy autonomous (scaffolded, ready)
│       ├── install.sh                 # LeRobot setup
│       ├── requirements.txt
│       ├── HARDWARE.md                # BOM + assembly
│       └── showcase.html              # Scope page
└── elktron-app/
    ├── CLAUDE.md                      # Dashboard architecture spec
    ├── index.html                     # Dashboard UI (layout only, needs panels)
    └── api/
        ├── server.py                  # FastAPI + WebSocket (mock data, working)
        ├── arm.py                     # ✅ LeRobot Feetech motor bus interface
        ├── escort.py                  # ✅ Pi 5 telemetry + scan management
        └── models.py                  # ✅ Pydantic schemas (arm, escort, scan, training)
```
