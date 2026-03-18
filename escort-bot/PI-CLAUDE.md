# Escort Bot — Raspberry Pi 5 Context

You are Claude Code running directly on a **Raspberry Pi 5 (8GB)** inside a mobile robot called the **Escort Bot**. This is one of two robots in the **Elktron** hackathon project for **CoreWeave's "More. Better. Faster." hackathon** (March 23-26, 2026).

---

## What You're Running On

- **Board:** Raspberry Pi 5, 8GB RAM, Broadcom BCM2712 (quad Cortex-A76 @ 2.4GHz)
- **OS:** Raspberry Pi OS Lite 64-bit (Debian Bookworm) — headless, no desktop
- **Python:** 3.11+ (system)
- **Hostname:** `escort-bot`
- **User:** `pi`
- **SSH:** `ssh pi@escort-bot.local`
- **Cooling:** Official Pi 5 active cooler (aluminum heatsink + PWM blower fan)
- **Power (bench):** CanaKit 3.5A USB-C PSU with PiSwitch inline toggle
- **Power (mobile):** Anker PowerCore 10K USB-C power bank (5V/3A, ~3-4 hour runtime)
- **Storage:** MicroSD card (32GB+ Class 10)

### Pi 5 Specifics You Must Know
- **GPIO library:** `gpiozero 2.0+` with `lgpio` backend. RPi.GPIO does NOT work on Pi 5.
- **Camera library:** `picamera2` + `libcamera`. Legacy `raspivid`/`raspistill` do NOT work.
- **GPIO is 3.3V tolerant.** Any 5V signal (like HC-SR04 echo) needs a voltage divider.
- **No desktop environment.** All output is terminal/headless. No GUI windows.

---

## What This Robot Does

The Escort Bot **autonomously follows a vendor** walking the data center floor. When the vendor stops at a rack, the bot performs a **vertical camera sweep** (bottom to top) to scan all 42U rack units, creating a visual audit trail of rack condition before/during/after vendor work. It replaces the manual process where a DCT walks alongside and eyeballs things.

### Three Operating Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **IDLE** | No person detected | Stationary, camera centered, waiting |
| **FOLLOW** | Person detected (confidence >= 0.5) | Proportional steering to keep person centered. Ultrasonic obstacle override at < 30cm. Lost timeout: 1.5s → IDLE |
| **SCAN** | Person stationary for 3+ seconds | Stop motors, sweep tilt servo bottom-to-top in 5-degree increments, save JPEG at each position to `scans/{timestamp}/`. Return to FOLLOW after sweep |

---

## Hardware Connected to This Pi

### GPIO Pin Map (BCM numbering)

| BCM Pin | Function | Connected To |
|---------|----------|--------------|
| 17 | Left Motor FWD | L298N IN1 |
| 27 | Left Motor BWD | L298N IN2 |
| 22 | Right Motor FWD | L298N IN3 |
| 23 | Right Motor BWD | L298N IN4 |
| 24 | Ultrasonic ECHO | HC-SR04 ECHO (via 1kΩ + 2kΩ voltage divider) |
| 25 | Ultrasonic TRIG | HC-SR04 TRIG |
| 12 | Pan Servo PWM | Arducam Pan/Tilt — horizontal rotation |
| 13 | Tilt Servo PWM | Arducam Pan/Tilt — vertical sweep |
| 5V | Sensor Power | HC-SR04 VCC |
| GND | Common Ground | All components share ground |

### Motor System
- **Chassis:** LK-COKOINO 4WD (CKK0011) — acrylic frame, 4x TT DC motors (1:90 ratio), rubber wheels
- **Driver:** L298N dual H-bridge — 1 board drives all 4 motors
  - Channel A (OUT1/OUT2): Left pair (front-left + rear-left in parallel)
  - Channel B (OUT3/OUT4): Right pair (front-right + rear-right in parallel)
- **Steering:** Differential/tank drive — left and right pairs controlled independently
- **Motor power:** 2x 18650 Li-ion batteries in series (7.4V) through L298N. Separate from Pi power. Common GND only.

### Camera
- **Model:** Arducam Camera Module 3 Wide (IMX708 sensor)
- **FOV:** 120 degrees (wide angle)
- **Focus:** PDAF + CDAF autofocus, min 5cm
- **Interface:** MIPI CSI-2 ribbon cable to Pi 5 CSI port
- **Resolution for inference:** 640x480 @ 20 FPS
- **Software:** `picamera2` + `libcamera` stack only

### Pan/Tilt
- **Platform:** Arducam B0283 with 2x GH-S37D digital servos
- **Pan:** GPIO 12 — horizontal, ±90 degrees
- **Tilt:** GPIO 13 — vertical, -60 to +60 degrees (rack scan range)
- **Controller:** `pan_tilt.py` — `PanTilt` class with `center()`, `look_at()`, `scan_rack()`, `scan_rack_bounce()`
- **Known issue:** Platform can shake/wobble. Use slower servo speeds. Secure base with screws or tape.

### Ultrasonic Sensor
- **Model:** HC-SR04
- **Range:** 2-450cm, resolution 3mm
- **CRITICAL:** Echo pin outputs 5V. Pi GPIO is 3.3V. A voltage divider (1kΩ series + 2kΩ to GND) is wired between echo and GPIO 24.
- **Obstacle threshold:** 30cm — motors stop immediately when triggered

### Mast
- ~3-4 ft PVC pipe (1" Schedule 40) mounted vertically on chassis
- Raises camera to mid-rack height for full 42U scanning
- Pan/tilt platform at top, camera mounted on tilt bracket

---

## Software on This Pi

### Installed Dependencies
```
picamera2>=0.3.12
numpy>=1.24.0
opencv-python>=4.8.0
gpiozero>=2.0
lgpio>=0.2.2.0
Pillow
```

### Detection Stack
- **Current:** OpenCV DNN + MobileNet SSD v2 (`models/ssd_mobilenet_v2.pb` + `.pbtxt`)
  - ~20 FPS on Pi 5 CPU
  - Only detects person (class ID 1), tracks largest bounding box
  - Confidence threshold: 0.5
- **Planned upgrade:** YOLOv8n + ByteTrack (persistent person tracking by ID)
  - `pip install ultralytics`
  - Export to NCNN format for Pi 5 (~15-20 FPS)
  - Replaces `detect_person()` in main.py with `model.track()` API

### Project Files (on this Pi at ~/escort-bot/)

| File | Lines | Purpose |
|------|-------|---------|
| `main.py` | ~373 | Robot brain — FOLLOW/SCAN/IDLE modes, detection, motor control, obstacle avoidance |
| `pan_tilt.py` | ~225 | Pan/tilt servo controller, rack scan sweep logic |
| `pid.py` | ~86 | PID controller with anti-windup, derivative filtering, output clamping |
| `test_camera.py` | — | Camera-only detection test (no motors). `--display` flag for live video |
| `install.sh` | — | One-command setup: apt deps, pip deps, model download |
| `requirements.txt` | — | Python dependencies |
| `WIRING.md` | — | GPIO pin map, L298N wiring, HC-SR04 voltage divider diagram |

### Key Tuning Parameters (in main.py)

| Parameter | Default | Purpose |
|-----------|---------|---------|
| KP_LATERAL | 1.0 | Steering proportional gain |
| KI_LATERAL | 0.1 | Steering integral gain |
| KD_LATERAL | 0.3 | Steering derivative gain |
| KP_DISTANCE | 1.2 | Speed proportional gain |
| KI_DISTANCE | 0.05 | Speed integral gain |
| KD_DISTANCE | 0.2 | Speed derivative gain |
| KFF | 0.15 | Feed-forward gain (predict target motion) |
| BASE_SPEED | 0.5 | Max forward speed (0.0-1.0) |
| STOP_DISTANCE | 0.30 | Ultrasonic cutoff (meters) |
| TARGET_AREA_RATIO | 0.15 | Target follow distance (higher = closer) |
| CONFIDENCE_THRESHOLD | 0.5 | Min detection confidence |
| SCAN_IDLE_TIME | 3.0 | Seconds stationary before scan triggers |
| LOST_TIMEOUT | 1.5 | Seconds without detection before IDLE |

### PID Tuning (on the floor)
1. **P-only first:** Ki=0, Kd=0. Increase Kp until bot tracks but oscillates.
2. **Add D:** Increase Kd until oscillation stops. Too much = sluggish.
3. **Add I:** Increase Ki slowly until steady-state drift gone. Too much = windup.
4. **Feed-forward (KFF):** Increase until bot anticipates direction changes. Too much = overcorrection.

---

## Run Commands

```bash
# Full escort + scan mode
python3 main.py

# Simulate servos (no pan/tilt hardware)
python3 main.py --simulate

# Run one rack scan and exit
python3 main.py --scan-only

# Camera-only detection test (no motors)
python3 test_camera.py

# Detection with live video window (needs display)
python3 test_camera.py --display

# Test pan/tilt positions (simulated)
python3 pan_tilt.py --simulate

# Test full rack scan (real servos)
python3 pan_tilt.py --scan
```

---

## The Bigger Picture — Elktron Project

This bot is **one of two robots** in Elktron:

1. **Escort Bot (this robot)** — Mobile person-following vendor escort + rack scanner
2. **SO-101 Arm** — 6-DOF imitation learning arm for optic seating (pick transceiver from tray, seat into switch port). Uses HuggingFace LeRobot + ACT policy.

Both robots connect to a **Dashboard** (FastAPI + WebSocket + vanilla JS) that shows arm status, escort telemetry, camera feeds, and scan logs.

### Team
| Person | Role |
|--------|------|
| Romeo Patino | Architecture, software, integration, escort bot lead |
| Alex Murillo | Hardware build, provides chassis + Pi |
| Joshua Tapia | SO-101 arm, end effector |
| Parth Patel | Team member |
| Talha Shakil | Team member |
| Raphael Rodea | Team member |

---

## Reference Links (Real URLs)

### Project
- **GitHub repo:** https://github.com/rpatino-cw/Elktron
- **GitHub Pages (project site):** https://rpatino-cw.github.io/Elktron/

### Raspberry Pi
- **Pi 5 documentation:** https://www.raspberrypi.com/documentation/computers/raspberry-pi-5.html
- **Pi 5 GPIO pinout:** https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio
- **picamera2 docs:** https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
- **picamera2 GitHub:** https://github.com/raspberrypi/picamera2
- **libcamera docs:** https://libcamera.org/docs.html
- **gpiozero docs:** https://gpiozero.readthedocs.io/en/latest/
- **lgpio (Pi 5 GPIO backend):** https://abyz.me.uk/lg/py_lgpio.html
- **Pi OS downloads:** https://www.raspberrypi.com/software/operating-systems/
- **Pi Imager:** https://www.raspberrypi.com/software/

### Computer Vision
- **OpenCV DNN module:** https://docs.opencv.org/4.x/d2/d58/tutorial_table_of_content_dnn.html
- **MobileNet SSD v2 (TF model zoo):** https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md
- **YOLOv8 (Ultralytics):** https://docs.ultralytics.com/models/yolov8/
- **YOLOv8 on Raspberry Pi:** https://docs.ultralytics.com/guides/raspberry-pi/
- **ByteTrack paper:** https://arxiv.org/abs/2110.06864

### Imitation Learning (SO-101 Arm)
- **LeRobot (HuggingFace):** https://github.com/huggingface/lerobot
- **LeRobot SO-101 docs:** https://huggingface.co/docs/lerobot/en/so101
- **ACT policy paper:** https://arxiv.org/abs/2304.13705
- **Haoran Xu build log:** https://www.linkedin.com/pulse/lets-build-ai-hack-lerobot-so101-haoran-xu-onaqc/

### Hardware Components
- **LK-COKOINO 4WD chassis (CKK0011):** https://github.com/LK-COKOINO/CKK0011
- **L298N datasheet:** https://www.st.com/resource/en/datasheet/l298.pdf
- **HC-SR04 datasheet:** https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf
- **Arducam Camera Module 3 Wide:** https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/12MP-IMX708/
- **Arducam Pan/Tilt (B0283):** https://www.arducam.com/product/arducam-upgraded-camera-pan-tilt-platform-for-raspberry-pi/
- **HiWonder SO-ARM101:** https://www.hiwonder.com/products/so-arm101

### CoreWeave (Employer)
- **CoreWeave docs:** https://docs.coreweave.com/
- **Hackathon channel:** `#more-faster-better-2026` (Slack)

---

## What You Can Help With on This Pi

You are here to enable rapid, on-device development. Your primary jobs:

1. **Debug and iterate** on `main.py`, `pan_tilt.py`, `pid.py`, and `test_camera.py` — live, on the actual hardware
2. **Read sensor output** — camera frames, ultrasonic distances, GPIO states — and fix code in one loop
3. **Tune PID parameters** — adjust gains based on real-world behavior
4. **Troubleshoot hardware** — GPIO issues, camera not detected, motor direction wrong, servo jitter
5. **Run tests** — `test_camera.py` for detection, `pan_tilt.py --scan` for servos, full `main.py` for integration
6. **Demo day rapid fixes** — on-site debugging without needing a laptop with the full codebase

### Quick Diagnostic Commands

```bash
# Check camera is connected
libcamera-hello --timeout 2000

# Check GPIO access
python3 -c "from gpiozero import Device; print('GPIO OK:', Device.pin_factory)"

# Check OpenCV DNN model loads
python3 -c "import cv2; net = cv2.dnn.readNetFromTensorflow('models/ssd_mobilenet_v2.pb', 'models/ssd_mobilenet_v2.pbtxt'); print('Model loaded OK')"

# Check CPU temperature
vcgencmd measure_temp

# Check throttling status
vcgencmd get_throttled

# Check available memory
free -h

# Check disk space
df -h /

# Check Python version
python3 --version

# Check installed packages
pip3 list | grep -E "picamera2|opencv|gpiozero|lgpio|numpy|ultralytics"

# Test ultrasonic sensor
python3 -c "
from gpiozero import DistanceSensor
sensor = DistanceSensor(echo=24, trigger=25)
print(f'Distance: {sensor.distance * 100:.1f} cm')
"

# Test motors briefly (left forward 0.5s)
python3 -c "
from gpiozero import Motor
from time import sleep
left = Motor(forward=17, backward=27)
left.forward(0.3)
sleep(0.5)
left.stop()
print('Left motor test done')
"
```

### Performance Tips
- **Overclock:** Add `arm_freq=2800` to `/boot/firmware/config.txt` (needs active cooler)
- **Disable Bluetooth:** `sudo systemctl disable bluetooth`
- **Pin CPU governor:** `echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor`
- **Disable swap:** `sudo dphys-swapfile swapoff && sudo systemctl disable dphys-swapfile`
