# Escort Bot — Person-Following Vendor Escort + Rack Scanner

## What This Is
The Escort Bot is one of two robots in the Elktron hackathon project (CoreWeave, March 23 2026). It is a mobile robot that autonomously follows vendors on the data center floor during maintenance visits. While escorting, it performs rack scans — sweeping its camera bottom-to-top across 42U racks to capture visual state before, during, and after vendor work. The goal is to create an audit trail of rack condition tied to each vendor visit, replacing the current manual process where DCTs walk alongside vendors and eyeball things.

The other robot is the SO-101 Arm (see `../robotics-site/`). The dashboard that connects both is in `../elktron-app/`.

## Hardware Platform

The bot is built on the **LK-COKOINO 4WD chassis** (CKK0011) — a basic 4-wheel-drive car kit with TT DC motors and an acrylic frame. Alex Murillo is providing her own chassis and Raspberry Pi. The full kit tutorial and drivers are in `../CKK0011-main/` (CH340 USB-serial driver, Arduino/Pi tutorials, assembly PDFs, and example Python code including `Demo1.py` for L298N motor control and `Demo2.py` for the Cokoino Robot Hat).

**Key components:**
- **Compute:** Raspberry Pi 5 (4GB or 8GB). Must run **Raspberry Pi OS Bookworm Lite 64-bit** — the only OS that supports Pi 5 + provides lgpio + picamera2 + Python 3.11. See `PI-SETUP.md` for full flashing and first-boot guide.
- **Motors:** 4x TT DC motors driven by an **L298N dual H-bridge** motor driver. Differential (tank) steering — left pair and right pair controlled independently. GPIO pins: left motor (17 fwd, 27 bwd), right motor (22 fwd, 23 bwd). Full wiring in `WIRING.md`.
- **Camera:** Arducam 120-degree wide-angle autofocus (IMX708), connected via CSI ribbon cable. Used for both person detection (FOLLOW mode) and rack scanning (SCAN mode).
- **Pan/Tilt:** Arducam pan/tilt platform with 2 MG90S micro servos. Pan on GPIO 12, tilt on GPIO 13. Controlled by `pan_tilt.py`. The tilt servo sweeps -60 to +60 degrees for rack scans.
- **Ultrasonic:** HC-SR04 on GPIO 24 (echo) and 25 (trigger). Provides obstacle avoidance — bot stops if anything is within 30cm. **Critical:** ECHO pin is 5V; Pi 5 GPIO is 3.3V tolerant. A voltage divider (1k + 2k resistors) is required or use HC-SR04P (3.3V version).
- **Power:** Dual power — USB-C power bank (5V/3A, e.g. Anker 10K) for the Pi, separate 7.4V battery pack (2x 18650) for motors through Freenove Smart Car Board. Inline USB-C power switch for clean on/off. Right-angle USB-C adapter to keep cable flush. Backup power bank + 2 spare 18650s for hot-swap during demo. Never power the Pi from the Smart Car Board's 5V regulator.
- **Mast:** ~3-4 ft PVC pipe (1 inch Schedule 40) mounted vertically on the chassis to raise the camera to mid-rack height. PVC T-connector attaches to chassis. This is critical — without height the camera can only see the bottom few rack units.

## Software Architecture

```
escort-bot/
├── CLAUDE.md              # THIS FILE — full project context
├── main.py                # Robot brain — 327 lines, complete
│                            Three modes: FOLLOW, SCAN, IDLE
│                            TFLite MobileNet SSD v2 for person detection
│                            Proportional steering with obstacle override
│                            Triggers rack scan when person is stationary 3s
├── pan_tilt.py            # Pan/tilt servo controller — 226 lines, complete
│                            PanTilt class: center(), look_at(), scan_rack(), scan_rack_bounce()
│                            Supports --simulate flag for testing without hardware
│                            Rack scan: sweeps TILT_MIN to TILT_MAX in 5-degree steps
├── test_camera.py         # Camera-only test — runs detection without motors
│                            Two modes: headless (terminal) and --display (live video)
│                            Use this to validate TFLite before assembling the chassis
├── install.sh             # One-command Pi 5 setup — apt, pip, model download
├── requirements.txt       # picamera2, tflite-runtime, gpiozero, numpy, lgpio, Pillow
├── WIRING.md              # GPIO pin map, L298N wiring, HC-SR04 voltage divider, test commands
├── PI-SETUP.md            # Complete Pi 5 OS flashing + first boot + troubleshooting guide
├── scans/                 # Output dir — one subfolder per rack scan with JPEG frames
├── models/                # TFLite model + COCO labels (created by install.sh)
│   ├── ssd_mobilenet_v2.tflite
│   └── coco_labels.txt
├── showcase.html          # Project scope page (presentation)
├── simulation.html        # 3D escort bot simulation (Three.js)
├── assembly.html          # Assembly instructions page
├── BUILD-GUIDE.html       # Step-by-step build guide
├── hardware-showcase.html # Hardware showcase page
├── hardware.html          # Hardware reference
├── mast-hardware.html     # Mast assembly details
└── Soldier.glb            # 3D model for simulation
```

## How It Works — Three Modes

**IDLE:** No person detected. Bot is stationary, camera is centered, waiting. Transitions to FOLLOW when a person is detected with confidence >= 0.5.

**FOLLOW:** Person detected. The bot uses proportional steering to keep the person centered in frame. `compute_steering()` calculates left/right motor speeds based on the person's bounding box position (horizontal centering) and size (distance control — stops advancing when the person fills ~15% of the frame). Obstacle override: if ultrasonic reads < 30cm, motors stop immediately regardless of detection state. If person is lost for > 1.5 seconds, transitions to IDLE.

**SCAN:** Triggered when the person has been stationary for 3+ seconds (they've stopped at a rack). Bot stops, camera sweeps bottom-to-top via pan/tilt servo in 5-degree increments, capturing a JPEG at each position. Frames are saved to `scans/{timestamp}/`. After scan completes, camera returns to center and mode transitions back to FOLLOW.

## Detection Pipeline

MobileNet SSD v2 (quantized TFLite) runs at ~20 FPS on Pi 5. Input: 300x300 RGB. Output: bounding boxes, class IDs, confidence scores. Only class 0 (person) is used. The largest detected person is tracked (handles multiple people in frame by following the closest/biggest one).

## Simulation Rules

The simulation (`simulation.html`) models a DC floor with 10 racks (2 rows of 5) in hot-aisle/cold-aisle configuration. `AISLE_WIDTH = 7`, `RACK_SPACING = 4.5`. The bot must respect collision detection at every frame during FOLLOW mode — it must never drive through a rack. After a scan completes, the bot must check for obstacles before resuming movement.

## Data Integration (Stretch Goal)

The escort bot can connect to **Jira** and **NetBox** via the CW MCP server to become context-aware during vendor escorts. It can look up which rack/device the vendor is there to work on, what state the device is in (staged, provisioned, decom'd), and cross-reference with open Jira tickets. The tokens (`JIRA_API_TOKEN`, `NETBOX_TOKEN`) are already set in `~/.config/keys/global.env`.

## Key Tuning Parameters (in main.py)

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| `KP` | 1.0 | Proportional steering gain — higher = more aggressive turning |
| `BASE_SPEED` | 0.5 | Forward speed (0.0–1.0) — start low on a real floor |
| `STOP_DISTANCE` | 0.30m | Ultrasonic cutoff — stop if obstacle closer than this |
| `TARGET_AREA_RATIO` | 0.15 | How close to follow — higher = closer following distance |
| `CONFIDENCE_THRESHOLD` | 0.5 | Min TFLite detection score to consider a person |
| `SCAN_IDLE_TIME` | 3.0s | How long person must be still before triggering scan |
| `LOST_TIMEOUT` | 1.5s | How long with no detection before switching to IDLE |

## Run Commands

```bash
# On Pi (after install.sh):
python3 main.py                  # Full escort + scan mode
python3 main.py --simulate       # Simulate servos (no pan/tilt hardware)
python3 main.py --scan-only      # Run one rack scan and exit (testing)
python3 test_camera.py           # Camera-only detection test (no motors)
python3 test_camera.py --display # Same but with live video window
python3 pan_tilt.py --simulate   # Test pan/tilt positions (simulated)
python3 pan_tilt.py --scan       # Test full rack scan (real servos)
```

## Team

| Person | Role |
|--------|------|
| **Romeo Patino** | Architecture, software, integration |
| **Alex Murillo** | Hardware build, her own chassis + Pi |

## What's NOT Done Yet

- Hardware assembly (chassis arrives 3/11, camera 3/14)
- Flash Pi 5 SD card
- Camera-only detection test on real Pi
- First motor test with L298N
- Mast construction (PVC from Home Depot)
- Pan/tilt mount on mast
- Full integration test (follow + scan)
- Tuning on real DC floor (KP, speed, thresholds)
- Demo recording
