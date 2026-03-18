# Escort Bot — Full Build Checklist

> Elktron Hackathon | CoreWeave March 2026
> Platform: Raspberry Pi 5 + 4WD Chassis | CV: YOLOv8n (switched from OpenCV DNN MobileNet SSD v2)

---

## Phase 1: Procurement & Inventory

### Parts Sourcing
- [x] ~~Order 4WD chassis~~ — **LK-COKOINO 4WD kit — Alex has it**
- [x] ~~Order HC-SR04 ultrasonic sensor~~ — **DIYables 2-pack DELIVERED 3/12 + ELEGOO 5-pack arriving 3/13**
- [x] ~~Order Pi Camera Module 3 (CSI)~~ — **Arducam IMX708 Wide arriving Sat 3/15**
- [x] ~~Order motor driver~~ — **L298N 2-pack DELIVERED 3/12**
- [x] ~~Order battery holders~~ — **QTEATAK 8-pack DELIVERED 3/12**
- [x] ~~Order 18650 batteries~~ — **QOJH 4-pack arriving Sat 3/15**
- [x] ~~Order USB-C power bank~~ — **Anker PowerCore 10K arriving 3/13**
- [x] ~~Order pan/tilt platform~~ — **Arducam Pan Tilt DELIVERED 3/12**
- [x] ~~Order CSI ribbon extension cables~~ — **Arducam 7pc Flex Cable Set ORDERED 3/17, arriving 3/18** ($10.71)
- [x] ~~Order CanaKit Pi PSU~~ — **DELIVERED 3/12 (bench testing only)**
- [x] ~~Order USB-C right-angle adapter~~ — **Silkland 2-pack DELIVERED 3/12**
- [ ] Order jumper wires: 20x male-to-female, 10x male-to-male (ELEGOO 5-pack comes with 20 dupont cables — may suffice)
- [ ] Order breadboard (half-size) — for prototyping sensor connections
- [ ] Order 1kΩ and 2kΩ resistors (2 each) — voltage divider for HC-SR04 ECHO pin
- [ ] Optional: LED strip or indicator LEDs — visual status feedback
- [ ] Optional: small speaker/buzzer — audio alerts

### Inventory Check (before assembly day)
- [x] Raspberry Pi 5 — Alex has it, confirmed working
- [x] MicroSD card (32GB+) — Romeo has one, needs flashing with Bookworm Lite 64-bit
- [x] USB-C power supply for Pi 5 — CanaKit 3.5A DELIVERED 3/12 (bench testing)
- [ ] USB-C power bank for mobile operation — Anker arriving 3/13
- [x] 4WD chassis kit — Alex has it (LK-COKOINO)
- [x] L298N motor driver board — DELIVERED 3/12 (2-pack, have spare)
- [x] HC-SR04 ultrasonic sensor — DIYables 2-pack DELIVERED 3/12
- [x] ~~Camera (Arducam IMX708 Wide)~~ — **DELIVERED + WORKING 3/16**
- [ ] 18650 batteries — arriving Sat 3/15
- [ ] Jumper wires (male-to-female, male-to-male)
- [ ] Breadboard
- [ ] Resistors (1kΩ, 2kΩ) for voltage divider
- [ ] Small Phillips and flathead screwdrivers
- [ ] Wire strippers (if using raw wire)
- [ ] Electrical tape or heat shrink tubing
- [ ] Velcro strips for cable management
- [ ] Double-sided tape or mounting brackets for Pi + camera

---

## Phase 2: Raspberry Pi Setup

### OS Installation
- [ ] Download Raspberry Pi OS (64-bit, Bookworm) — use Raspberry Pi Imager
- [ ] Flash to MicroSD card
- [ ] Pre-configure WiFi + SSH in Imager settings (for headless access)
- [ ] Set hostname: `elktron-escort`
- [ ] Set username/password
- [ ] Insert MicroSD into Pi 5, boot up
- [ ] Verify boot — SSH in: `ssh <user>@elktron-escort.local`
- [ ] Run system update: `sudo apt update && sudo apt upgrade -y`
- [ ] Verify Python 3.11+: `python3 --version`

### Claude Code (AI Dev on Pi)
- [x] Install Claude Code CLI on Pi 5 — **DONE 2026-03-15**
- [ ] Verify: `ssh pi@escort-bot.local` → `cd ~/escort-bot` → `claude` launches successfully
- [ ] Test: ask Claude to read a sensor value or run `test_camera.py` from within the CLI

### Enable Interfaces
- [ ] Enable Camera (CSI): `sudo raspi-config` → Interface Options → Camera → Enable
- [ ] Enable I2C (if using I2C sensors): `sudo raspi-config` → Interface Options → I2C → Enable
- [ ] Enable SPI (if needed): same path
- [ ] Reboot after interface changes: `sudo reboot`

### Camera Test
- [x] ~~Pi Camera Module: `libcamera-hello --timeout 5000`~~ — **WORKING, libcamera v0.7.0**
- [ ] USB webcam: `ls /dev/video*` — should show device
- [ ] Python test: `python3 -c "import cv2; cap=cv2.VideoCapture(0); ret,f=cap.read(); print(ret, f.shape); cap.release()"`
- [x] ~~Verify resolution: at least 640x480~~ — **CONFIRMED**
- [x] ~~Verify FPS: at least 15 FPS (20+ preferred)~~ — **CONFIRMED**
- [x] ~~If using picamera2: `python3 -c "from picamera2 import Picamera2; cam=Picamera2(); cam.start(); print('OK'); cam.stop()"`~~ — **WORKING**

### GPIO Test
- [ ] Install gpiozero: `pip3 install gpiozero lgpio`
- [ ] Test basic GPIO: `python3 -c "from gpiozero import LED; import time; led=LED(17); led.on(); time.sleep(1); led.off()"` (connect an LED to GPIO17 to verify)
- [ ] If GPIO permission error: add user to gpio group: `sudo usermod -aG gpio $USER`
- [ ] Verify lgpio backend works (Pi 5 uses lgpio, not RPi.GPIO)

---

## Phase 3: Chassis Assembly

### Base Chassis
- [ ] Identify top and bottom chassis plates
- [x] Mount 4 DC motors to bottom plate using brackets + screws
- [x] Verify motor shafts face outward (toward wheels)
- [x] Attach 4 wheels to motor shafts — press fit, should be snug
- [x] Spin each wheel by hand — motors should spin freely, no grinding
- [ ] Label motors: FL (front-left), FR (front-right), RL (rear-left), RR (rear-right)
- [ ] Mount standoffs between bottom and top plates (4–6 standoffs typical)
- [ ] Attach top plate — leave enough clearance for wires between plates

### Motor Wiring
- [ ] Solder or connect motor leads (2 wires per motor, 8 total)
- [ ] Route motor wires to center of chassis where L298N will mount
- [x] Left motors (FL + RL): wire in parallel — red to red, black to black
- [x] Right motors (FR + RR): wire in parallel — red to red, black to black
- [x] Result: 2 wire pairs — LEFT pair and RIGHT pair
- [ ] Verify polarity: when positive voltage applied, wheels spin FORWARD (test with battery briefly)
- [ ] If wheels spin backward: swap the two wires for that motor pair

### L298N Motor Driver Mounting
- [ ] Mount L298N board on top plate using standoffs or double-sided tape
- [ ] Connect LEFT motor pair to L298N OUT1 + OUT2 terminals
- [ ] Connect RIGHT motor pair to L298N OUT3 + OUT4 terminals
- [ ] Tighten screw terminals firmly — loose connections = intermittent motor failure
- [x] Connect battery pack positive to L298N +12V (VCC) terminal
- [x] Connect battery pack negative to L298N GND terminal
- [ ] Verify 5V jumper on L298N:
  - If jumper IN: L298N regulates 5V from motor battery (can power Pi — risky, noisy)
  - If jumper OUT: L298N only gets motor power, Pi needs separate power (RECOMMENDED)
- [ ] Remove 5V jumper — power Pi separately via USB-C power bank

### L298N to Pi GPIO Connections
```
L298N Pin    →    Pi GPIO (BCM)    Purpose
─────────────────────────────────────────────
IN1          →    GPIO 17          Left motor forward
IN2          →    GPIO 24          Left motor backward
IN3          →    GPIO 22          Right motor forward
IN4          →    GPIO 23          Right motor backward
ENA          →    GPIO 12 (PWM)    Left motor speed (optional)
ENB          →    GPIO 13 (PWM)    Right motor speed (optional)
GND          →    Pi GND           Common ground (CRITICAL)
```

- [ ] Connect IN1 → GPIO 17 (jumper wire)
- [ ] Connect IN2 → GPIO 24
- [ ] Connect IN3 → GPIO 22
- [ ] Connect IN4 → GPIO 23
- [ ] Connect L298N GND → Pi GND pin (pin 6, 9, 14, 20, 25, 30, 34, or 39)
- [ ] **CRITICAL:** Common ground between L298N and Pi — without this, GPIO signals are unreliable
- [ ] Optional: Connect ENA → GPIO 12, ENB → GPIO 13 for PWM speed control
- [ ] If ENA/ENB not used: leave jumpers on ENA/ENB pins (full speed always)

### Motor Test (after wiring)
- [ ] Power on Pi + motor battery
- [ ] Run quick test script:
```python
from gpiozero import Robot
robot = Robot(left=(17, 24), right=(22, 23))
robot.forward(speed=0.3)   # slow forward, 2 seconds
import time; time.sleep(2)
robot.stop()
```
- [ ] Verify: all 4 wheels spin forward
- [ ] Test: `robot.backward(0.3)` — all wheels spin backward
- [ ] Test: `robot.left(0.3)` — left wheels stop/reverse, right wheels forward (turns left)
- [ ] Test: `robot.right(0.3)` — right wheels stop/reverse, left wheels forward (turns right)
- [ ] If turning is reversed: swap LEFT and RIGHT motor pair connections on L298N
- [ ] If one side spins wrong direction: swap the two wires for that motor pair

---

## Phase 4: Sensor Integration

### Ultrasonic Sensor (HC-SR04)
```
HC-SR04 Pin    →    Connection              Purpose
──────────────────────────────────────────────────
VCC            →    Pi 5V (pin 2 or 4)      Power
GND            →    Pi GND                   Ground
TRIG           →    GPIO 25                  Trigger pulse (output)
ECHO           →    Voltage divider → GPIO 24   Echo return (input)
```

**IMPORTANT:** HC-SR04 ECHO pin outputs 5V. Pi 5 GPIO is 3.3V tolerant only. You MUST use a voltage divider.

#### Voltage Divider Wiring
- [ ] Connect ECHO pin → 1kΩ resistor → junction point
- [ ] Connect junction point → 2kΩ resistor → GND
- [ ] Connect junction point → GPIO 24
- [ ] This divides 5V to ~3.3V (safe for Pi GPIO)
- [ ] Double-check resistor values: 1kΩ (brown-black-red) and 2kΩ (red-black-red)

#### HC-SR04 Assembly
- [ ] Mount HC-SR04 on front of chassis — facing forward, slightly angled down
- [ ] Sensor should be ~5–10cm above ground level
- [ ] Secure with hot glue, mounting bracket, or velcro
- [ ] Connect VCC → Pi 5V
- [ ] Connect GND → Pi GND
- [ ] Connect TRIG → GPIO 25
- [ ] Connect ECHO → voltage divider → GPIO 24
- [ ] Verify wiring 3 times before powering on (wrong connection can damage Pi)

#### Ultrasonic Test
- [ ] Run test:
```python
from gpiozero import DistanceSensor
sonar = DistanceSensor(echo=26, trigger=25, max_distance=2)
while True:
    print(f"Distance: {sonar.distance * 100:.1f} cm")
    import time; time.sleep(0.5)
```
- [ ] Hold hand at 30cm → reading should be ~30cm (±5cm)
- [ ] Hold hand at 100cm → reading should be ~100cm
- [ ] Remove hand → reading should be >150cm or max
- [ ] Verify readings are stable (not jumping wildly)
- [ ] If readings are always 0 or max: check wiring, especially voltage divider

### Camera Mounting
- [ ] Mount camera on TOP of chassis, facing forward
- [ ] Angle: slightly downward (~10–15 degrees) to see both floor and standing person
- [ ] Secure camera with bracket, velcro, or double-sided tape
- [ ] Verify camera has clear FOV — no chassis parts blocking view
- [ ] Camera cable routed cleanly — not near motor wires (EMI interference)
- [x] ~~Test camera still works after mounting: `libcamera-hello` or OpenCV test~~ — **CONFIRMED via camtest.py**

---

## Phase 5: Software Setup

### System Dependencies
- [ ] Run: `sudo apt install -y python3-pip python3-venv libatlas-base-dev libjpeg-dev libopenjp2-7-dev`
- [ ] Run: `sudo apt install -y python3-opencv` (system OpenCV, faster than pip)
- [ ] Run: `sudo apt install -y libcamera-apps` (if using Pi Camera Module)

### Python Environment
- [ ] Create venv: `python3 -m venv ~/escort-env`
- [ ] Activate: `source ~/escort-env/bin/activate`
- [ ] Install deps from `requirements.txt`: `pip install -r ~/hackathon/escort-bot/requirements.txt`
- [ ] Expected packages: `numpy`, `opencv-python` (or `python3-opencv`), `gpiozero`, `lgpio`, `picamera2`
- [ ] If `opencv-python` fails on Pi 5: use system package instead: `sudo apt install python3-opencv`

### Model Setup
- [ ] Download MobileNet SSD v2 (COCO) for OpenCV DNN:
```bash
mkdir -p ~/models
wget -O ~/models/frozen_inference_graph.pb http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz
# Extract the .pb from the tarball, or use escort-bot/install.sh
wget -O ~/models/ssd_mobilenet_v2_coco.pbtxt https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/ssd_mobilenet_v2_coco_2018_03_29.pbtxt
```
- [ ] Run `escort-bot/install.sh` — it downloads model + COCO labels
- [ ] Verify model files exist: `ls -la ~/models/frozen_inference_graph.pb ~/models/ssd_mobilenet_v2_coco.pbtxt`
- [ ] Download COCO labels file: `~/models/coco_labels.txt`
- [ ] Verify "person" is class 1 in labels file (COCO class IDs)

### Model Test (no motors)
- [ ] Run detection test:
```python
import cv2
import numpy as np

net = cv2.dnn.readNetFromTensorflow(
    "models/frozen_inference_graph.pb",
    "models/ssd_mobilenet_v2_coco.pbtxt"
)

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
blob = cv2.dnn.blobFromImage(frame, size=(300, 300), swapRB=True)
net.setInput(blob)
detections = net.forward()
# ... check detections for person class (class_id == 1) with confidence > 0.5
print("Person detected!" if person_found else "No person")
cap.release()
```
- [x] ~~Stand in front of camera (~1-2m away)~~ — **DONE**
- [x] ~~Verify: "person" class detected with confidence >0.5~~ — **YOLOv8n, 0.78 confidence at DC floor conditions**
- [x] ~~Check inference time: should be <100ms per frame on Pi 5~~ — **CONFIRMED <100ms**
- [ ] If too slow: ensure using quantized (uint8) model, not float32

---

## Phase 6: Person-Following Algorithm

### Core Logic (from `escort-bot/main.py`)
```
Loop:
  1. Capture frame from camera
  2. Run OpenCV DNN inference → detect persons
  3. Find largest person bounding box (closest person)
  4. Calculate error_x = (bbox_center_x - frame_center_x) / frame_width
  5. Calculate area_ratio = bbox_area / frame_area
  6. Steering: left_speed = BASE_SPEED - error_x * KP
              right_speed = BASE_SPEED + error_x * KP
  7. Distance: if area_ratio > TARGET → too close → slow down/stop
              if area_ratio < TARGET → too far → speed up
  8. Obstacle: if sonar < STOP_DISTANCE → emergency stop
  9. Lost: if no person for LOST_TIMEOUT → stop and wait
```

### Parameter Tuning Reference
| Parameter | Default | Range | What it does |
|-----------|---------|-------|-------------|
| `CONFIDENCE_THRESHOLD` | 0.5 | 0.3–0.7 | Min detection confidence (lower = more false positives) |
| `BASE_SPEED` | 0.5 | 0.2–0.8 | Forward speed (higher = faster but harder to steer) |
| `STOP_DISTANCE` | 0.30m | 0.15–0.50m | Ultrasonic emergency stop distance |
| `TARGET_AREA_RATIO` | 0.15 | 0.05–0.30 | How close to follow (bigger = closer) |
| `AREA_TOLERANCE` | 0.05 | 0.02–0.10 | Dead zone around target distance |
| `LOST_TIMEOUT` | 1.5s | 0.5–3.0s | Time without person before stopping |
| `KP` | 1.0 | 0.5–2.0 | Steering gain (higher = sharper turns) |
| `FRAME_WIDTH` | 320 | 160–640 | Detection resolution (lower = faster, less accurate) |

### Implementation Checklist
- [ ] Copy `escort-bot/main.py` to Pi: `scp main.py pi@elktron-escort.local:~/`
- [ ] Edit config section at top of `main.py` — set GPIO pins to match wiring
- [ ] Edit camera index (0 for USB, or picamera2 path for CSI)
- [ ] Edit model path to match where model was downloaded

### Bench Test (wheels off ground)
- [ ] Prop chassis up so wheels spin freely (put on a box)
- [ ] Run `main.py`
- [ ] Stand in front of camera → wheels should spin forward
- [ ] Move LEFT → right wheels should speed up (bot turns left to track you)
- [ ] Move RIGHT → left wheels should speed up (bot turns right)
- [ ] Walk away → wheels speed up (bot tries to close distance)
- [ ] Walk closer → wheels slow down or stop
- [ ] Disappear from frame → wheels stop after LOST_TIMEOUT
- [ ] Hold hand in front of ultrasonic (<30cm) → wheels stop immediately (emergency stop)
- [ ] If steering is reversed: swap left/right GPIO pins in config
- [ ] If forward/backward reversed: swap forward/backward GPIO pins

---

## Phase 7: Floor Testing

### Safety Precautions
- [ ] Test in open area first — no expensive equipment nearby
- [ ] Have someone ready to pick up the bot if it goes rogue
- [ ] Start with LOW speed: `BASE_SPEED = 0.2`
- [ ] Keep laptop nearby with SSH session open to kill the script: `Ctrl+C`
- [ ] Battery fully charged before floor test
- [ ] Test on smooth floor (not carpet — 4WD works but drains battery fast on carpet)

### Basic Movement Test
- [ ] Place bot on floor, run `main.py`
- [ ] Stand 2m in front → bot should move toward you slowly
- [ ] Walk forward slowly → bot follows
- [ ] Stop → bot stops (within 0.5–1m)
- [ ] Turn left → bot turns left
- [ ] Turn right → bot turns right
- [ ] Walk behind a pillar → bot stops after LOST_TIMEOUT

### Tuning Session (expect 30–60 minutes)
- [ ] If bot oscillates left-right: REDUCE `KP` (e.g., 1.0 → 0.6)
- [ ] If bot doesn't turn enough: INCREASE `KP` (e.g., 1.0 → 1.5)
- [ ] If bot follows too close: DECREASE `TARGET_AREA_RATIO` (e.g., 0.15 → 0.10)
- [ ] If bot stays too far: INCREASE `TARGET_AREA_RATIO` (e.g., 0.15 → 0.20)
- [ ] If bot loses person too easily: DECREASE `CONFIDENCE_THRESHOLD` (e.g., 0.5 → 0.35)
- [ ] If bot follows wrong things (not people): INCREASE `CONFIDENCE_THRESHOLD`
- [ ] If bot is too slow: INCREASE `BASE_SPEED` gradually (0.5 → 0.6 → 0.7)
- [ ] If bot is jerky: add smoothing to speed commands (exponential moving average)
- [ ] Tune until bot can follow a walking person for 30+ seconds continuously
- [ ] Note final parameter values — these are your "golden config"

### Edge Cases to Test
- [ ] Two people in frame → bot should follow the closest (largest bbox)
- [ ] Person walking fast → bot should try to keep up (may lose them — that's OK)
- [ ] Person standing still → bot should stop at target distance
- [ ] Obstacle between bot and person → ultrasonic stops bot, doesn't ram obstacle
- [ ] Lighting change (bright hallway → dim aisle) → detection still works?
- [ ] Person wearing dark clothing → detection still works?
- [ ] Person carrying a box (partially occluded) → detection still works?

### Battery Life Test
- [ ] Fully charge batteries
- [ ] Run continuous following test
- [ ] Time how long until motors weaken or Pi browns out
- [ ] Target: at least 30 minutes of operation for demo day
- [ ] If battery life too short: get higher capacity pack or carry spare

---

## Phase 8: DC-Specific Features

### Vendor Escort Scenario
- [ ] Define escort route: entrance → aisle → specific rack → back to entrance
- [ ] Bot follows vendor (person-following mode)
- [ ] At destination rack: bot stops and enters "monitoring mode"
- [ ] Monitoring mode: camera captures video of vendor working on rack
- [ ] Optional: log timestamp + rack ID + vendor name to scan report JSON

### Rack Contact Detection (stretch goal)
- [ ] Define rack zones in camera frame (if camera is static at rack)
- [ ] Detect if person's hands enter unauthorized rack unit zone
- [ ] Trigger alert (LED, buzzer, or dashboard notification)
- [ ] Log event to scan report JSON
- [ ] This is a STRETCH GOAL — skip if time is tight

### Status Indicators
- [ ] LED: Green = following, Yellow = searching, Red = obstacle stop
- [ ] Optional: buzzer beep on person lost
- [ ] Optional: buzzer pattern on escort complete
- [ ] If no LEDs: use print statements + dashboard for status

### Autonomous Navigation (stretch goal)
- [ ] Pre-program aisle waypoints (x, y coordinates or timed sequences)
- [ ] Bot navigates to rack autonomously using dead reckoning or waypoints
- [ ] This is a MAJOR stretch — only attempt if person-following works perfectly
- [ ] Simpler alternative: bot just follows vendor (no autonomous nav needed)

---

## Phase 9: Dashboard Integration

### WebSocket Connection
- [ ] `main.py` sends telemetry to Elktron dashboard via WebSocket
- [ ] Telemetry payload:
```json
{
  "type": "escort_status",
  "state": "following",        // following | searching | stopped | obstacle
  "person_detected": true,
  "confidence": 0.87,
  "bbox": [120, 80, 280, 400],
  "distance_m": 1.5,
  "sonar_cm": 95,
  "speed_left": 0.45,
  "speed_right": 0.52,
  "battery_v": 7.2,
  "uptime_s": 342
}
```
- [ ] Dashboard receives and displays: state, person detection, distance, sonar reading
- [ ] Dashboard shows live camera feed (WebSocket binary frames or MJPEG stream)
- [ ] If no live connection: use mock data for dashboard demo (JSON replay)

### Camera Streaming
- [ ] Option A: MJPEG over HTTP — `http://<pi-ip>:8080/stream`
  - Use `picamera2` with MJPEG server or `cv2` with Flask
  - Lower latency, simpler
- [ ] Option B: WebSocket binary frames
  - Encode each frame as JPEG, send via WebSocket
  - Integrates with existing dashboard WebSocket
- [ ] Test stream from another machine: open browser to MJPEG URL or check dashboard
- [ ] Verify latency: <500ms acceptable, <200ms ideal

---

## Phase 10: Demo Preparation

### Demo Setup
- [ ] Fully charged batteries (both motor pack and Pi power bank)
- [ ] Spare batteries on standby
- [ ] Clear demo area: 3m x 5m minimum, no tripping hazards
- [ ] Good lighting in demo area
- [ ] WiFi connection stable (for dashboard communication)
- [ ] Laptop showing Elktron dashboard nearby
- [ ] "Vendor" (team member) knows the walk route

### Demo Script (60 seconds)
- [ ] 0:00–0:10 — Show bot on floor, dashboard showing "IDLE"
- [ ] 0:10–0:15 — Narrate: "Escort bot autonomously follows vendors on the DC floor"
- [ ] 0:15–0:20 — "Vendor" starts walking, bot begins following
- [ ] 0:20–0:40 — Bot follows vendor through demo aisle (20 seconds of following)
- [ ] 0:40–0:50 — Vendor stops at "rack," bot stops at target distance
- [ ] 0:50–0:55 — Dashboard shows: escort status, camera feed, vendor position
- [ ] 0:55–1:00 — "Person detection using OpenCV DNN on Raspberry Pi 5, <100ms inference"

### Video Recording
- [ ] Record from a third-person angle — shows both vendor and bot moving
- [ ] Also record dashboard screen (screen capture or second camera)
- [ ] Record 5+ takes — pick the smoothest one
- [ ] Audio: clear narration explaining what's happening
- [ ] Video: 1080p, well-lit, shows bot's movement clearly
- [ ] Include a moment where bot successfully turns a corner following vendor
- [ ] Total escort bot segment: 60 seconds max for the 3-minute final video

### Failsafe Plan
- [ ] If bot won't follow: switch to manual RC control + narrate the vision
- [ ] If Pi camera fails: swap to USB webcam (bring both)
- [ ] If WiFi fails: run dashboard locally on Pi, screen-share via HDMI
- [ ] If motors die: show detection working on screen (person tracking without movement)
- [ ] If battery dies mid-demo: have spare fully charged pack ready to swap

---

## Phase 11: Pre-Hackathon Integration Test

### Full System Test (do this at least 2 days before demo day)
- [ ] Both robots running simultaneously
- [ ] Dashboard receiving telemetry from both (arm + escort bot)
- [ ] Camera feeds streaming from both
- [ ] Run full demo script end-to-end
- [ ] Time the full demo — must be under 3 minutes total
- [ ] Record a practice video — review for issues
- [ ] Fix any issues found
- [ ] Run full demo script again — confirm fixes

### Network Test
- [ ] Pi 5 and laptop on same WiFi network
- [ ] WebSocket connections stable for 5+ minutes
- [ ] No firewall blocking local traffic
- [ ] If venue WiFi is unreliable: bring a portable WiFi router or use Pi as hotspot

### Stress Test
- [ ] Run escort bot for 15+ minutes continuous
- [ ] Check: motors still responsive? Pi overheating? Battery holding?
- [ ] If Pi overheats: add heatsink or small fan
- [ ] If motors weaken: check battery voltage, swap if <6.5V (for 7.4V pack)
- [ ] Run through demo script 3x consecutively without stopping
