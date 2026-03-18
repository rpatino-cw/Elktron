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

### Joshua Tapia — Robot Arm CV/IK Lead
**Title:** Data Center Technician
**Objective:** Own the SO-101 arm's task execution — from computer vision pipeline to inverse kinematics to end effector design. Make the optic seating demo work.

**Scope:**
- Computer vision pipeline for optic detection
- Inverse kinematics and motion planning
- End effector design — gripper for SFP/QSFP optics
- LeRobot ACT policy training and evaluation
- Record 50 optic seating demonstrations
- Arm calibration and servo tuning
- Risk owner: end effector is the critical unknown

**Hardware:** TBD — uses Romeo's laptop for training, arm kit arrives ~3/18

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

### Parth Patel — Backend Lead
**Title:** Data Center Technician
**Objective:** Own the dashboard backend — improve the FastAPI server, wire in mock/real data from Jira and NetBox, build out API endpoints.

**Scope:**
- FastAPI server improvements (`elktron-app/api/server.py`)
- Jira/NetBox data integration (mock data first, real data stretch)
- WebSocket data pipeline to frontend
- Scan report JSON generation
- Wire `arm.py` and `escort.py` to receive real telemetry

**Hardware:** Laptop

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
**Objective:** Own all physical assembly, parts inventory, battery management, and demo day logistics. The reason the robots are built clean, charged, and present on March 23.

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
