# Elktron — Team & Roles

## Team Roster (6 active + 1 observer)

### Romeo Patino — Project Management (PM)
**Title:** Data Center Technician, Channel Manager
**Objective:** Own the system architecture, LeRobot integration, and demo narrative. Make sure all three components (arm, bot, dashboard) connect into one coherent story.

**Scope:**
- Overall project architecture and technical decisions
- LeRobot framework integration for SO-101 arm
- Escort bot software (main.py, test_camera.py)
- Elktron dashboard (elktron-app) — initial template + frontend
- Pi 5 setup and configuration
- PROGRESS.md — single source of truth
- Hardware ordering (Amazon, Home Depot)

**Hardware:** Pi 4, Pi 5, Pico, MacBook (training + demo)

---

### Joshua Tapia — Integration Lead + Robot Arm
**Title:** Data Center Technician
**Objective:** Own the end-to-end integration — dashboard, API pipeline, escort bot testing — plus SO-101 arm when hardware is ready. Good with API work.

**Scope:**
- **Dashboard + API integration** (active as of 3/21) — testing Pi→dashboard pipeline, Xbox controller teleoperation, YOLOv8n + PID following
- Computer vision pipeline for optic detection
- Inverse kinematics and motion planning
- End effector design — gripper for SFP/QSFP optics
- LeRobot ACT policy training and evaluation
- Record 50 optic seating demonstrations
- Arm calibration and servo tuning

**Hardware:** His laptop (dashboard), Pi 5 onsite, arm kit

---

### Alex Murillo — Escort Bot Hardware Lead
**Title:** Data Center Technician
**Objective:** Own the physical escort bot build — chassis assembly, wiring, motor tuning, and field testing on the DC floor.

**Scope:**
- LK-COKOINO chassis assembly and wiring
- PVC mast construction and camera mounting
- Motor + ultrasonic sensor integration
- Physical testing — drive, steer, obstacle avoidance
- DC floor field testing during escort bot tuning
- Power system — battery charging, cable routing

**Hardware:** Her Raspberry Pi, LK-COKOINO chassis

---

### Parth Patel — Pi Setup + Integration Support
**Title:** Data Center Technician
**Objective:** Support onsite integration work alongside Josh. Set up the Pi environment for the team.

**Actual contributions (as of 3/21):**
- Pi terminal/CLI setup — installed powerlevel10k, shell tools, developer QoL
- Onsite support — working with Josh on integration testing
- Has not written project code (api_server.py, dashboard, etc. were all built by Romeo)

**Scope going forward:**
- Support Josh on dashboard + API integration testing onsite
- Help with hardware testing and debugging
- Jira/NetBox data integration (stretch goal)

**Confirmed:** 2026-03-18 — agreed in `#the-elks-2026`

**Hardware:** Laptop + onsite Pi 5 access

---

### Talha Shakil — Media & Presentations Lead
**Title:** Data Center Technician
**Objective:** Own all final deliverables — demo video, pitch deck, team logo, and presentation materials. Make sure Elktron looks polished for judges.

**Scope:**
- Team logo design
- Demo video production (filming, editing, narration support)
- Pitch deck / slides (5-7 slides)
- Screen recordings of dashboard for video
- Final video export and upload
- B-roll footage (wiring, assembly, Pi boot, terminal output)

**Hardware:** Phone/camera for filming, laptop for editing

---

### Raphael Rodea — Build Crew + Logistics Lead
**Title:** Data Center Technician
**Objective:** Own all physical assembly, parts inventory, battery management, and demo day logistics. The reason the robots are built clean, charged, and present on Demo Day (March 26).

**Scope:**
- Chassis assembly — mount motors, attach wheels, screw standoffs (pairs with Alex)
- PVC mast build — cut pipe, attach T-connector, mount to chassis
- Wiring checker — verify every connection against WIRING.md (second pair of eyes)
- Cable management — route wires, velcro, zip tie, label everything
- Parts inventory — open packages, verify contents, label with tape, organize war room
- Battery manager — charge all batteries night before, swap during testing, track charge levels
- Demo day packing — owns the checklist, makes sure nothing gets left behind
- Floor testing safety — stands near bot, ready to grab it
- B-roll camera assist — film assembly and floor tests for Talha's video edit
- Plays "vendor" role during escort bot demo

**Hardware:** None needed — works with Alex's hardware

---

### Andrew Westberg — Observer
**Title:** Data Center Technician
**Objective:** Watch and learn. Not on the active roster.

**Scope:**
- Observing the build process
- Learning robotics, Pi setup, and hackathon workflow
- Available to help if needed, but no assigned tasks

---

## Communication
- **Slack:** `#the-elks-2026` (team) · `#more-faster-better-2026` (hackathon)
- **Daily sync:** Share updates in team Slack each morning
- **Decisions:** Update PROGRESS.md — single source of truth
- **Rule:** Everyone owns their lane. Nobody waits for permission.
