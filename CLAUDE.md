# Elktron — Hackathon Project Config

## Key Info
- **Event:** March 23-25, 2026
- **Demo Day:** March 26 (2-5pm ET)
- **Team:** Elktron — signed up March 12 via `#more-better-faster-2026`
- **Deliverable:** 2-3 min pre-recorded demo + optional slides + GitHub repo
- **Track:** Build with Velocity
- **Git:** This folder is a git repo (`main` branch)

## Focus Check (run at session start)

> `Session: Hackathon | Status: LOCKED — Elktron (two robots) | Signed up`

---

## Feature Lock System — DO NOT MODIFY LOCKED REGIONS

`escort-bot/assembly.html` has **16 locked regions** protected by `@LOCKED:name` / `@END-LOCKED:name` markers. A PreToolUse hook (`guard-locked-regions.sh`) **deterministically blocks** any Edit or Write that touches locked code. This is enforced at the tool level — you cannot bypass it.

**Locked regions (do not modify):**
| Region | What it protects |
|--------|-----------------|
| `scene-setup` | Scene, camera, renderer, lights, controls, ground |
| `materials` | All shared MeshStandardMaterial definitions |
| `geometry-builders` | createMotorSet, createChassis, createMotorBrackets |
| `pi5-model` | Full Raspberry Pi 5 detailed 3D model |
| `crt-sound` | CRT boot sound effect |
| `monitor-osd` | Hovering monitor, boot terminal, holo-line |
| `catenary-and-cables` | Catenary helper, HDMI cable builder |
| `component-builders` | L298N, power bank, USB-C cable, PiSwitch, PVC mast, wiring harness |
| `assembly-steps` | All 15 assembly step definitions |
| `state-and-animation` | App state, animation helpers, step navigation, camera animation |
| `pi-setup-quest` | Interactive terminal quest system |
| `explode-collapse` | Explode/collapse toggle, step back |
| `virtual-filesystem` | Virtual Pi filesystem + terminal emulator |
| `event-listeners-edit-mode` | DOM listeners, keyboard, resize, edit mode, TransformControls |
| `wire-tool` | Wire tool v2 — creation, editing, undo, persistence, UI |
| `animate-and-init` | Animate loop, GLB loader, Pi/monitor init, SD card animation |

**To modify locked code:** Remove the `@LOCKED:name` and `@END-LOCKED:name` markers from the specific region, then edit freely. Re-add markers when done.

---

## Project: Elktron

Two robots for the DC floor. One project, three core components + supporting infrastructure:

| Component | Path | What It Does |
|-----------|------|-------------|
| **SO-101 Arm** | `robotics-site/so101/` | Imitation learning for DC tasks — optic seating, rack inspection. LeRobot + ACT policy. |
| **Escort Bot** | `escort-bot/` | Person-following vendor escort. Pi 5 + OpenCV DNN MobileNet SSD + LK-COKOINO 4WD chassis. **Claude Code installed on Pi** — on-device AI dev. |
| **Dashboard** | `elktron-app/` | Unified control panel — arm status, escort tracking, camera feeds, scan logs. FastAPI + vanilla JS. |
| **Landing Page** | `robotics-site/index.html` | Elktron pitch/showcase site |
| **Hub** | `hub.html` | Central navigation for all hackathon pages |

---

## Complete Directory Topology

```
hackathon/
├── CLAUDE.md                          # THIS FILE — master project config
├── PROGRESS.md                        # Single source of truth — what's done, what's next
├── README.md                          # Project overview for GitHub
├── design-system.css                  # Shared CSS design tokens (colors, fonts)
├── .gitignore                         # Git ignore rules
│
├── docs/                              # PROJECT DOCUMENTATION
│   ├── PARTS-LIST.md                  # Hardware BOM with Amazon links + costs
│   ├── CHECKLIST-SO101.md             # 10-phase SO-101 arm build checklist
│   ├── CHECKLIST-ESCORT-BOT.md        # 11-phase escort bot build checklist
│   ├── TEAM.md                        # Team roster — Romeo, Alex, Josh + roles
│   ├── TEAM-CHECKLIST.md              # Master team task list (700+ lines, 10 phases)
│   ├── VELOCITY.md                    # Engineering philosophy / pace manifesto
│   ├── WORKFLOW.md                    # Demo day timeline template
│   ├── DEMO-SCRIPT.md                # Full 3-min demo video narration + shot list
│   ├── DEMO-CREATIVE-BRIEF.md        # Demo creative brief
│   ├── ADW-SUMMARY.md                # CoreWeave IDP Agentic Developer Workflows summary
│   ├── hackathon-sites.md             # Site inventory
│   └── reference/                     # External references
│       └── slack-evi01-build-dct-2026-03-12.md
│
├── hub.html                           # ★ THREE.JS — Hackathon navigation hub
├── daily.html                         # ★ THREE.JS — Daily standup page
│
├── robotics-site/                     # SO-101 ARM + LANDING PAGE
│   ├── CLAUDE.md                      # Robotics site config — arm overview, status, resources
│   ├── index.html                     # Elktron landing page (dark luxury-tech, CSS only)
│   ├── topology.html                  # ★ THREE.JS — System topology visualization
│   ├── elktron-robots.blend         # Blender 3D scene — both robots
│   ├── elktron-robots.blend1        # Blender auto-backup
│   ├── optic-staging-tray.blend       # Blender — optic staging tray model
│   ├── optic-staging-tray.blend1      # Blender auto-backup
│   ├── optic-staging-tray.obj         # OBJ export of optic tray
│   ├── optic-staging-tray.mtl         # OBJ material file
│   ├── hero-render.png                # Hero render image (from Blender)
│   ├── arm-render.png                 # SO-101 arm render
│   ├── guide-render.png               # Guide render
│   ├── so101-real.png                 # Real SO-101 photo
│   └── so101/                         # ARM CODE
│       ├── showcase.html              # SO-101 showcase page (CSS animations, no Three.js)
│       ├── record.py                  # Record demos via leader-follower teleoperation
│       ├── train.py                   # Train ACT policy (cuda/mps/cpu)
│       ├── deploy.py                  # Deploy trained model for autonomous execution
│       ├── install.sh                 # venv + LeRobot from source + deps
│       ├── requirements.txt           # lerobot, torch, opencv, numpy, tensorboard
│       └── HARDWARE.md                # BOM, assembly notes, kit tiers, compute options
│
├── escort-bot/                        # ESCORT BOT — PERSON-FOLLOWING ROBOT
│   ├── CLAUDE.md                      # Deep escort bot context — hardware, software, tuning
│   ├── main.py                        # Robot brain — 327 lines, 3 modes (FOLLOW/SCAN/IDLE)
│   ├── pan_tilt.py                    # Pan/tilt servo controller (226 lines)
│   ├── test_camera.py                 # Camera-only detection test (no motors)
│   ├── install.sh                     # One-command Pi 5 setup
│   ├── requirements.txt               # picamera2, opencv-python, gpiozero, numpy, lgpio
│   ├── WIRING.md                      # GPIO pin map, L298N wiring, HC-SR04 voltage divider
│   ├── PI-SETUP.md                    # Pi 5 OS flashing + first boot guide (Bookworm Lite 64-bit)
│   ├── Soldier.glb                    # 3D model (GLB) used in simulation
│   ├── door-open-phase.png            # Escort workflow diagram
│   ├── scan-verification.png          # Scan verification diagram
│   ├── showcase.html                  # Escort bot scope page (CSS animations, no Three.js)
│   ├── simulation.html                # ★ THREE.JS — DC floor simulation (10 racks, bot AI)
│   ├── assembly.html                  # ★ THREE.JS — Assembly instructions with 3D models
│   ├── BUILD-GUIDE.html               # ★ THREE.JS — Step-by-step build guide with 3D
│   ├── hardware-showcase.html         # ★ THREE.JS — Hardware showcase with 3D components
│   ├── hardware.html                  # ★ THREE.JS — Hardware reference with 3D models
│   ├── mast-hardware.html             # ★ THREE.JS — Mast assembly details with 3D
│   └── wiring-guide.html             # ★ THREE.JS — Interactive 3D wiring guide (GPIO, L298N, HC-SR04, servos, power)
│
├── elktron-app/                     # DASHBOARD — FASTAPI + VANILLA JS
│   ├── CLAUDE.md                      # Dashboard architecture spec — 5 panels, WebSocket
│   ├── README.md                      # Dashboard quick start
│   ├── DEMO-SCRIPT.md                 # Dashboard-specific demo script
│   ├── index.html                     # Main dashboard UI (single-page app, no Three.js)
│   ├── guide.html                     # Dashboard usage guide (no Three.js)
│   ├── requirements.txt               # fastapi, uvicorn, websockets, pyserial, lerobot
│   ├── .venv/                         # Python virtual environment (FastAPI + deps)
│   └── api/
│       ├── server.py                  # FastAPI + WebSocket server (mock data, working)
│       ├── arm.py                     # LeRobot Feetech motor bus serial interface
│       ├── escort.py                  # Pi 5 telemetry + scan management
│       └── models.py                  # Pydantic schemas (arm, escort, scan, training)
│
├── 3d-reference/                      # 3D MODEL REFERENCES + ASSETS
│   ├── CLAUDE.md                      # Workflow rules — file naming, format guide, pipeline
│   └── pi5-3d-model.html             # ★ THREE.JS — Raspberry Pi 5 interactive 3D model
│
├── 2d_manual_3d/                      # 2D-TO-3D CONVERSION WORKSPACE
│   ├── CLAUDE.md                      # Pipeline: 2D blueprint → approval → 3D model
│   └── pi5-layout.json               # Pi 5 component layout data
│
├── CKK0011-main/                      # VENDOR REPO — LK-COKOINO CHASSIS KIT
│   ├── CLAUDE.md                      # Context — assembly PDFs, L298N code, CH340 driver
│   ├── README.md                      # Manufacturer README (cokoino@outlook.com)
│   ├── CH340 Driver/                  # USB-serial driver (Windows only, not needed for Pi + L298N)
│   └── Tutorial/
│       ├── Arduino/                   # Arduino tutorials + sketches (5 experiments)
│       │   └── Sketches/             # .ino source files (motor, LED, ultrasonic, tracking)
│       └── RaspberryPi/              # ★ MOST RELEVANT — Pi tutorials + Python code
│           ├── Code/
│           │   ├── Demo1.py          # L298N motor control (RPi.GPIO — not Pi 5 compatible)
│           │   ├── Demo2.py          # Cokoino Robot Hat motor control (I2C/smbus)
│           │   └── Servo_test.py     # MG90S servo PWM test
│           └── *.pdf                 # Assembly guides, wiring tutorials (6 PDFs)
│
├── img/                               # REFERENCE IMAGES + DOCUMENTATION
│   ├── CLAUDE.md                      # Asset manifest — categorized photo inventory
│   ├── car_*.jpg (x10)               # LK-COKOINO chassis photos (measurements, angles, parts)
│   ├── frame_overall_view.jpg         # Acrylic frame top-down (hole patterns)
│   ├── raspberry pi above vew.jpg     # Pi 5 top-down reference
│   ├── cable-net.png                  # Network cable reference
│   ├── *.pdf (x3)                     # Amazon listing + reviews + Cokoino official docs
│   ├── 2d_car                         # 2D reference (missing file extension)
│   └── 2d_drawing/                    # 2D BLUEPRINT WORKSPACE
│       ├── CLAUDE.md                  # Strict workflow: trace → draft → approval → 3D
│       ├── frame_trace.html           # Frame tracing tool (canvas-based, no Three.js)
│       ├── 2d_car_reference.png       # Car reference for tracing
│       └── rc_chassis_frame_lines.png # Traced frame lines
│
└── taskboard/                         # TEAM TASK BOARD
    └── index.html                     # ★ THREE.JS — Interactive task board with 3D elements
```

---

## All Markdown Files — Quick Reference

### Root Level (hackathon/)
| File | Purpose | Read When |
|------|---------|-----------|
| **`PROGRESS.md`** | **READ FIRST EVERY SESSION** — hardware status, what's done, what's next | Always |
| `CLAUDE.md` | This file — master config and topology | Session start |
| `README.md` | GitHub-facing project overview, tech stack, getting started | Sharing project |

### docs/ (hackathon/docs/)
| File | Purpose | Read When |
|------|---------|-----------|
| `docs/PARTS-LIST.md` | Hardware BOM — Amazon links, costs, arrival tracker | Ordering or receiving parts |
| `docs/CHECKLIST-SO101.md` | 10-phase arm build checklist (~150 items) | Building the SO-101 arm |
| `docs/CHECKLIST-ESCORT-BOT.md` | 11-phase bot build checklist (~160 items) | Building the escort bot |
| `docs/TEAM.md` | Team roster — Romeo (lead), Alex (bot hardware), Josh (arm CV/IK) | Assigning work |
| `docs/TEAM-CHECKLIST.md` | Master task list with phases 0-10, ~700 lines | Coordinating team work |
| `docs/VELOCITY.md` | Engineering philosophy — pace, momentum, constraints | Motivation / team alignment |
| `docs/WORKFLOW.md` | Demo day timeline template (kickoff → present) | Day-of planning |
| `docs/DEMO-SCRIPT.md` | Full 3-min demo narration, shot list, filming notes | Recording demo video |
| `docs/DEMO-CREATIVE-BRIEF.md` | Demo creative brief | Pre-production planning |
| `docs/ADW-SUMMARY.md` | CoreWeave IDP Agentic Developer Workflows (reference only) | Understanding CW agent platform |

### Subdirectory CLAUDE.md Files
| File | Purpose |
|------|---------|
| `robotics-site/CLAUDE.md` | SO-101 arm overview — problem, tech stack, LeRobot resources, status |
| `escort-bot/CLAUDE.md` | **Deep escort bot spec** — hardware platform, software architecture, 3 modes (FOLLOW/SCAN/IDLE), detection pipeline, tuning parameters, run commands |
| `elktron-app/CLAUDE.md` | Dashboard architecture — 5 panels, WebSocket, FastAPI, scan report JSON schema |
| `CKK0011-main/CLAUDE.md` | Vendor chassis kit context — assembly guides, motor code (Demo1.py), RPi.GPIO vs gpiozero differences |
| `3d-reference/CLAUDE.md` | 3D model pipeline — file naming, format guide (STL/OBJ/GLB/STEP), folder relationships |
| `2d_manual_3d/CLAUDE.md` | 2D-to-3D conversion workspace — pipeline steps, approval gate, conversion methods (Blender/OpenSCAD/FreeCAD) |
| `img/CLAUDE.md` | Image asset manifest — categorized photo inventory with descriptions, known issues |
| `img/2d_drawing/CLAUDE.md` | Strict 2D blueprint rules — trace faithfully, no guessing, approval required before 3D |

### Other Markdown in Subdirectories
| File | Purpose |
|------|---------|
| `escort-bot/WIRING.md` | GPIO pin map, L298N wiring diagram, HC-SR04 voltage divider |
| `escort-bot/PI-SETUP.md` | Complete Pi 5 SD flashing + first boot + troubleshooting guide |
| `robotics-site/so101/HARDWARE.md` | SO-101 BOM, assembly notes, kit tiers, compute options |
| `elktron-app/README.md` | Dashboard quick start |
| `elktron-app/DEMO-SCRIPT.md` | Dashboard-specific demo walkthrough |
| `CKK0011-main/README.md` | Manufacturer README |

---

## Three.js / 3D Websites — Complete Map

**12 HTML files use Three.js** (via CDN importmap). Here is every one:

### Escort Bot — 3D Pages (7 files)
| File | Three.js Ver | What It Renders |
|------|-------------|-----------------|
| `escort-bot/simulation.html` | v0.162.0 | **DC floor simulation** — 10 racks (2 rows of 5), hot/cold aisle, escort bot AI with collision detection. Uses `Soldier.glb` model. Interactive: bot follows person through aisles. |
| `escort-bot/assembly.html` | v0.162.0 | **Assembly instructions** — 3D exploded view of chassis, step-by-step build with interactive 3D models |
| `escort-bot/BUILD-GUIDE.html` | v0.170.0 | **Build guide** — Comprehensive step-by-step with 3D models of each component, interactive assembly sequence |
| `escort-bot/hardware-showcase.html` | v0.162.0 | **Hardware showcase** — All escort bot components rendered in 3D: chassis, Pi 5, L298N, HC-SR04, camera, mast |
| `escort-bot/hardware.html` | v0.162.0 | **Hardware reference** — Interactive 3D models of individual components with specs and pin diagrams |
| `escort-bot/mast-hardware.html` | v0.162.0 | **Mast assembly** — 3D model of PVC mast, T-connector, pan-tilt mount, camera placement |
| `escort-bot/wiring-guide.html` | v0.170.0 | **Wiring guide** — Interactive 3D wiring: GPIO connections, L298N, HC-SR04 voltage divider, servos, power distribution |

### Navigation & Overview (2 files)
| File | Three.js Ver | What It Renders |
|------|-------------|-----------------|
| `hub.html` | v0.170.0 | **Hackathon hub** — Central navigation with 3D background/hero element. Links to all pages. |
| `daily.html` | v0.163.0 | **Daily standup** — Team sync page with 3D visual elements |

### System Architecture (1 file)
| File | Three.js Ver | What It Renders |
|------|-------------|-----------------|
| `robotics-site/topology.html` | varies | **System topology** — 3D visualization of how arm, bot, and dashboard connect |

### 3D Reference (1 file)
| File | Three.js Ver | What It Renders |
|------|-------------|-----------------|
| `3d-reference/pi5-3d-model.html` | v0.162.0 | **Raspberry Pi 5 model** — Interactive 3D model of the Pi 5 board, components labeled |

### Task Management (1 file)
| File | Three.js Ver | What It Renders |
|------|-------------|-----------------|
| `taskboard/index.html` | varies | **Task board** — Interactive team task tracker with 3D visual elements |

### NON-Three.js HTML Pages (6 files)
| File | What It Is |
|------|-----------|
| `robotics-site/index.html` | Elktron landing page — dark luxury-tech CSS, no Three.js |
| `robotics-site/so101/showcase.html` | SO-101 scope page — CSS animations, no Three.js |
| `escort-bot/showcase.html` | Escort bot scope page — CSS animations, no Three.js |
| `elktron-app/index.html` | Dashboard app — vanilla JS + WebSocket, no Three.js |
| `elktron-app/guide.html` | Dashboard usage guide, no Three.js |
| `img/2d_drawing/frame_trace.html` | Canvas-based frame tracing tool, no Three.js |

---

## 3D Asset Files

| File | Format | What |
|------|--------|------|
| `robotics-site/elktron-robots.blend` | Blender | Main 3D scene — both robots |
| `robotics-site/optic-staging-tray.blend` | Blender | Optic staging tray model |
| `robotics-site/optic-staging-tray.obj` | OBJ | Exported optic tray mesh |
| `robotics-site/optic-staging-tray.mtl` | MTL | Material file for OBJ |
| `escort-bot/Soldier.glb` | GLB | Person model for simulation |
| `2d_manual_3d/pi5-layout.json` | JSON | Pi 5 component positions |

---

## Three.js Version Note

The project uses **mixed Three.js versions** across files:
- v0.162.0 — Most escort-bot pages + 3d-reference
- v0.163.0 — daily.html
- v0.170.0 — hub.html, BUILD-GUIDE.html

Consider standardizing to **v0.170.0** (latest used) for consistency.

---

## Skills (invoke these)

| Skill | When to Use |
|-------|-------------|
| `/elktron-demo-commander` | Planning, prioritizing, deciding what to cut, demo strategy |
| `/elktron-robotics-debugger` | Hardware bring-up, sensor/motor/camera issues, training failures |
| `/elktron-pitch-writer` | Pitch, demo narration, slides, README, submission copy |
| `/frontend-design` | Before writing any frontend code |
| `threejs-*` (all 10) | Before any Three.js work — load all 10 skills |

## Key Docs — Read Order

1. **`PROGRESS.md`** — Always first. Hardware status, what's done, what's next.
2. **This file** — Topology, where everything is.
3. **`docs/TEAM-CHECKLIST.md`** — What needs to happen, who owns what.
4. **Component CLAUDE.md** — Deep context for whichever component you're working on.

## Judging Tracks
1. **Build with Velocity** — AI to accelerate dev or DC construction (OUR TRACK)
2. Productivity at Scale — 10x faster workflows
3. Win the Customer — speed to production

## Bonus Categories
- People's Choice
- Cross Functional Team
- Most Company OKRs

## Winning Formula
- Specificity beats generality
- Closed loop > visualization
- Physical world beats software toys
- Measurable delta beats vibes
- Authenticity > flash

## Photo-to-3D Pipeline (v2 — 6 Stages)

Converts reference photos into interactive 3D assembly pages. Multi-view aware. Full docs: `img/2d_drawing/CLAUDE.md`

| Stage | Name | Who | Tool | Output |
|-------|------|-----|------|--------|
| 1 | Trace | User (per view) | `~/dev/tracer/index.html` | JSON line data per view |
| 2 | Analyze | Claude (per view) | Canvas HTML | Annotated 2D canvas per view |
| 3 | Merge | Claude | HTML + table | Unified mm dimensions + multi-view blueprint |
| 4 | ASCII 3D Preview | Claude | HTML `<pre>` + JS | Isometric ASCII wireframe |
| 5 | 3D Model | Claude | Three.js v0.170.0 | Interactive 3D model |
| 6 | Assembly Page | Claude | Three.js + design-system.css | Build guide |

**Rules:** Three.js v0.170.0, inline geometry (no external models), design-system.css for assembly pages, approval gates between every stage. Stage 3 (Merge) combines all views — no Z-heights from imagination. Stage 4 (ASCII Preview) is mandatory — no Three.js build before ASCII preview is approved.

## Pipeline Relationships

```
img/ (reference photos)
  → img/2d_drawing/ (2D blueprints, approval gate)
    → 2d_manual_3d/ (conversion workspace)
      → 3d-reference/ (finished 3D models)
        → robotics-site/*.blend (Blender scenes)
          → escort-bot/*.html (Three.js web visualizations)

CKK0011-main/ (vendor chassis docs)
  → escort-bot/WIRING.md (our wiring, based on vendor tutorials)
    → escort-bot/main.py (software that drives the wired hardware)
      → elktron-app/api/escort.py (telemetry bridge to dashboard)
        → elktron-app/index.html (live dashboard UI)

robotics-site/so101/*.py (arm code)
  → elktron-app/api/arm.py (serial interface bridge)
    → elktron-app/index.html (arm panel in dashboard)
```

## URLs — Open in Incognito

```bash
# Hub (start here)
open -a "Google Chrome" --args --incognito "file:///Users/rpatino/hackathon/hub.html"

# Three.js Sites
open -a "Google Chrome" --args --incognito "file:///Users/rpatino/hackathon/escort-bot/simulation.html"
open -a "Google Chrome" --args --incognito "file:///Users/rpatino/hackathon/escort-bot/BUILD-GUIDE.html"
open -a "Google Chrome" --args --incognito "file:///Users/rpatino/hackathon/escort-bot/hardware-showcase.html"
open -a "Google Chrome" --args --incognito "file:///Users/rpatino/hackathon/escort-bot/hardware.html"
open -a "Google Chrome" --args --incognito "file:///Users/rpatino/hackathon/escort-bot/assembly.html"
open -a "Google Chrome" --args --incognito "file:///Users/rpatino/hackathon/escort-bot/mast-hardware.html"
open -a "Google Chrome" --args --incognito "file:///Users/rpatino/hackathon/3d-reference/pi5-3d-model.html"
open -a "Google Chrome" --args --incognito "file:///Users/rpatino/hackathon/robotics-site/topology.html"
open -a "Google Chrome" --args --incognito "file:///Users/rpatino/hackathon/taskboard/"

# Non-3D Pages
open -a "Google Chrome" --args --incognito "file:///Users/rpatino/hackathon/robotics-site/index.html"
open -a "Google Chrome" --args --incognito "file:///Users/rpatino/hackathon/elktron-app/index.html"

# Dashboard (needs server)
# cd elktron-app && source .venv/bin/activate && uvicorn api.server:app --reload --port 8080
```
