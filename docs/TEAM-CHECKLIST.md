# Elktron — Master Team Checklist

> **Submissions closed:** March 12, 2026 | **Hackathon:** March 23–25 | **Demo Day:** March 26 (11am–2pm PT / 2pm–5pm ET)
> **Deliverable:** 2–3 min pre-recorded demo + optional slides + GitHub repo
> **Track:** Build with Velocity
> **Last updated:** 2026-03-11

---

## Team Roster

| Name | Role | Owns |
|------|------|------|
| **Romeo Patino** | Lead — architecture, software, demo story | System design, escort bot software, dashboard frontend, Pi setup |
| **Joshua Tapia** | Robot arm — CV, positioning, training | SO-101 assembly, calibration, ACT policy, optic seating demo |
| **Alex Murillo** | Escort bot hardware lead | Chassis build, wiring, motor/sensor integration, floor testing |
| **Parth Patel** | Backend lead | FastAPI server, Jira/NetBox data integration, WebSocket pipeline |
| **Talha Shakil** | Media & presentations | Demo video, pitch deck, logo, filming, editing |
| **Raphael Rodea** | Build crew + logistics | Assembly, parts inventory, batteries, wiring checks, packing, demo day "vendor" |
| **Andrew Westberg** | Observer | Watching and learning — not on active roster |

---

## How to Use This Checklist

- **Claim a task:** Put your name in the `Owner` column
- **Mark done:** Change `[ ]` to `[x]`
- **Blocked?** Add `BLOCKED:` + reason next to the task
- **Questions?** Drop them in `#more-faster-better-2026` or DM Romeo
- **Rule:** If a task takes >2 hours and you're stuck, ask for help. Don't spin.

---

## PHASE 0: ADMIN & SIGN-UP (by March 12 — TOMORROW)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 0.1 | Sign up team in `#more-faster-better-2026` | Romeo | [ ] | **DEADLINE MARCH 12** — list all 7 names |
| 0.2 | Confirm all team members have Slack access to hackathon channel | Romeo | [ ] | DM each person |
| 0.3 | Create shared GitHub repo for Elktron | Romeo | [ ] | Private repo, add all members as collaborators |
| 0.4 | Share this checklist with the team (link or copy) | Romeo | [ ] | Pin in hackathon channel |
| 0.5 | Confirm everyone has read VELOCITY.md | All | [ ] | Sets the pace expectation |
| 0.6 | Each person confirms their availability March 20-23 | All | [ ] | Note any conflicts |
| 0.7 | Identify who has a car / can pick up Home Depot items | All | [ ] | PVC pipe + T-connector still need pickup |
| 0.8 | Pick up PVC pipe 1" x 4ft + T-connector from Home Depot | Romeo or volunteer | [ ] | Already in HD cart ($8.09) |

---

## PHASE 1: HARDWARE INTAKE & INVENTORY (March 11–13)

### 1A: Receive & Verify Shipments

Every package that arrives — open it, verify contents, mark done.

| # | Task | Owner | ETA | Status | Notes |
|---|------|-------|-----|--------|-------|
| 1A.1 | Receive Pi 5 Active Cooler | Romeo | 3/11 | [ ] | Check box, verify fan + heatsink + thermal pad included |
| 1A.2 | Receive LK-COKOINO 4WD Chassis Kit | Alex | 3/11 | [ ] | Verify: 4 motors, 4 wheels, chassis plates, screws, standoffs |
| 1A.3 | Receive Samsung 30Q 18650 batteries + charger | Romeo | 3/11 | [ ] | Start charging batteries IMMEDIATELY — takes 4-6 hours |
| 1A.4 | Receive MakerFocus Pi battery pack 10000mAh | Romeo | 3/11 | [ ] | Verify USB-C output, charge to 100% |
| 1A.5 | Receive WWZMDiB L298N Motor Driver 2-pack | Romeo | 3/12 | [ ] | Test one board — LEDs light up when powered |
| 1A.6 | Receive ELEGOO HC-SR04 Ultrasonic 5-pack | Romeo | 3/12 | [ ] | Keep 2 for build, rest are spares |
| 1A.7 | Receive DIYables HC-SR04 2-pack | Romeo | 3/12 | [ ] | Backup ultrasonic sensors |
| 1A.8 | Receive QTEATAK 18650 Battery Holders 8-pack | Romeo | 3/12 | [ ] | Need 1 for chassis, rest are spares |
| 1A.9 | Receive Arducam Pan-Tilt Platform (2 servos + controller) | Romeo | 3/12 | [ ] | Verify 2 servos + mounting hardware included |
| 1A.10 | Receive Arducam 120° Wide Camera (IMX708) | Romeo | 3/14 | [ ] | **Camera is the last escort bot part** — verify CSI cable included |
| 1A.11 | Receive Freenove 4WD Smart Car Kit (backup/parts) | Romeo | 3/11 | [ ] | Originally ordered — may use parts or keep as backup |
| 1A.12 | Receive NexiGo N60 1080P Webcam | Romeo | 3/11 | [ ] | For SO-101 arm overhead camera |
| 1A.13 | SO-101 arm kit (HiWonder) — LONG POLE | Romeo | ~3/18 | [ ] | Ships from China. If delayed, arm demo uses pre-recorded video |

### 1B: Inventory & Organize

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 1B.1 | Gather owned hardware: Pi 4, Pi 5, Pico, SIM card, velcro | Romeo | [ ] | From home — put in one box |
| 1B.2 | Find or buy MicroSD card 32-64GB for Pi 5 | Romeo | [ ] | Check drawer first. If not: Samsung EVO Select 64GB ~$8 |
| 1B.3 | Find USB-C data cables (not charge-only) x3 | All | [ ] | Test each cable — plug into laptop, run `ls /dev/tty*` |
| 1B.4 | Find small Phillips screwdriver set | All | [ ] | For chassis + arm assembly |
| 1B.5 | Find wire strippers or scissors for jumper wire prep | All | [ ] | For voltage divider + custom wiring |
| 1B.6 | Collect jumper wires: 20x M-F, 10x M-M | Romeo | [ ] | If not enough: buy assorted pack ~$6 |
| 1B.7 | Get breadboard (half-size) | Romeo | [ ] | For prototyping ultrasonic voltage divider |
| 1B.8 | Get resistors: 1kΩ (x2) and 2kΩ (x2) | Romeo | [ ] | For HC-SR04 ECHO pin voltage divider (5V → 3.3V) |
| 1B.9 | Label all parts with masking tape — write what each thing is | Anyone | [ ] | Prevents confusion during assembly |
| 1B.10 | Create a "war room" table/area for assembly | Romeo | [ ] | Dedicated space, good lighting, power strips |

---

## PHASE 2: RASPBERRY PI SETUP (March 11–12)

This can start immediately — only needs Pi 5 + MicroSD + power.

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 2.1 | Download Raspberry Pi Imager on Mac | Romeo | [ ] | https://downloads.raspberrypi.com/imager/imager_latest.dmg |
| 2.2 | Flash MicroSD: Raspberry Pi OS Lite (64-bit, Bookworm) | Romeo | [ ] | In Imager: set hostname `elktron-escort`, enable SSH, set WiFi |
| 2.3 | Set username: `elktron` / password: [choose one, share with team] | Romeo | [ ] | Everyone needs SSH access |
| 2.4 | Insert MicroSD into Pi 5, connect USB-C power, boot | Romeo | [ ] | Green LED blinks = booting. Wait 60 seconds. |
| 2.5 | SSH into Pi: `ssh elktron@elktron-escort.local` | Romeo | [ ] | If .local doesn't resolve: find IP from router or `nmap -sn 192.168.x.0/24` |
| 2.6 | Run system update: `sudo apt update && sudo apt upgrade -y` | Romeo | [ ] | Takes 5–15 min depending on network |
| 2.7 | Verify Python version: `python3 --version` → should be 3.11+ | Romeo | [ ] | Bookworm ships 3.11 |
| 2.8 | Install Pi 5 Active Cooler (physical install) | Romeo | [ ] | 4 screws, thermal pad, plug fan into Pi 5 header |
| 2.9 | Verify cooler works: `cat /sys/class/thermal/thermal_zone0/temp` → should drop under load | Romeo | [ ] | Run `stress --cpu 4 --timeout 30s` and check temp stays <70°C |
| 2.10 | Enable Camera interface: `sudo raspi-config` → Interface → Camera | Romeo | [ ] | Reboot after |
| 2.11 | Enable I2C: `sudo raspi-config` → Interface → I2C | Romeo | [ ] | For pan-tilt servo controller |
| 2.12 | Install system deps: `sudo apt install -y python3-pip python3-venv libatlas-base-dev libjpeg-dev python3-opencv libcamera-apps` | Romeo | [ ] | One command, ~5 min |
| 2.13 | Create Python venv: `python3 -m venv ~/escort-env` | Romeo | [ ] | Isolated from system Python |
| 2.14 | Activate + install requirements: `source ~/escort-env/bin/activate && pip install -r requirements.txt` | Romeo | [ ] | Copy requirements.txt to Pi first |
| 2.15 | Install OpenCV: `sudo apt install python3-opencv` | Romeo | [ ] | System package preferred over pip on Pi |
| 2.16 | Download MobileNet SSD v2 model to Pi: run `install.sh` | Romeo | [ ] | Creates `~/models/` with `.pb` + `.pbtxt` |
| 2.17 | Test Python imports work: `python3 -c "import cv2, numpy, gpiozero; print('OK')"` | Romeo | [ ] | All should import cleanly |
| 2.18 | Set Pi to auto-connect to phone hotspot (backup WiFi) | Romeo | [ ] | `sudo nmcli dev wifi connect "iPhone" password "xxx"` |
| 2.19 | **Alex's Pi:** Repeat steps 2.1–2.17 on Alex's Raspberry Pi | Alex | [ ] | Same OS + software, hostname `elktron-alex` |

---

## PHASE 3: ESCORT BOT — HARDWARE BUILD (March 11–15)

### 3A: Chassis Assembly (~2 hours)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 3A.1 | Unbox LK-COKOINO kit — lay out all parts, verify nothing missing | Alex | [ ] | Compare against Amazon listing photos |
| 3A.2 | Identify top and bottom chassis plates | Alex | [ ] | Bottom plate = motor mounts |
| 3A.3 | Mount 4 DC motors to bottom plate using brackets + screws | Alex + Raphael | [ ] | Motor shafts face OUTWARD (toward wheels) |
| 3A.4 | Attach 4 wheels to motor shafts | Alex | [ ] | Press fit — should be snug, not loose |
| 3A.5 | Spin each wheel by hand — verify free rotation, no grinding | Alex | [ ] | If grinding: re-seat motor in bracket |
| 3A.6 | Label motors with tape: FL (front-left), FR, RL, RR | Alex | [ ] | Critical for wiring — wrong labels = reversed steering |
| 3A.7 | Mount standoffs between bottom and top plates | Alex | [ ] | 4-6 standoffs, leave clearance for wires between plates |
| 3A.8 | Attach top plate | Alex | [ ] | Don't fully tighten yet — need access for wiring |

### 3B: Motor Wiring (~1 hour)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 3B.1 | Solder or connect motor leads (2 wires per motor, 8 total) | Alex | [ ] | If no soldering iron: twist + electrical tape works for prototype |
| 3B.2 | Route all motor wires to center of chassis | Alex | [ ] | Where L298N will mount |
| 3B.3 | Wire LEFT motors in parallel: FL red→RL red, FL black→RL black | Alex | [ ] | Result: one wire pair for LEFT side |
| 3B.4 | Wire RIGHT motors in parallel: FR red→RR red, FR black→RR black | Alex | [ ] | Result: one wire pair for RIGHT side |
| 3B.5 | Quick polarity test: touch 7.4V battery briefly to LEFT pair | Alex | [ ] | Wheels should spin FORWARD. If backward: swap wires. |
| 3B.6 | Repeat polarity test for RIGHT pair | Alex | [ ] | Same direction as LEFT |
| 3B.7 | Mount L298N motor driver on top plate | Alex | [ ] | Double-sided tape or standoffs |
| 3B.8 | Connect LEFT motor pair → L298N OUT1 + OUT2 screw terminals | Alex | [ ] | Tighten firmly — loose = intermittent failure |
| 3B.9 | Connect RIGHT motor pair → L298N OUT3 + OUT4 screw terminals | Alex | [ ] | Tighten firmly |
| 3B.10 | Connect 18650 battery holder → L298N +12V (VCC) + GND terminals | Alex | [ ] | **Do NOT insert batteries yet** |
| 3B.11 | **Remove L298N 5V jumper** — Pi gets separate power via USB-C | Alex | [ ] | Jumper OUT = safer, cleaner power |

### 3C: L298N → Pi GPIO Wiring (~30 min)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 3C.1 | Connect L298N IN1 → Pi GPIO 17 (jumper wire) | Alex | [ ] | Left motor forward |
| 3C.2 | Connect L298N IN2 → Pi GPIO 27 | Alex | [ ] | Left motor backward |
| 3C.3 | Connect L298N IN3 → Pi GPIO 22 | Alex | [ ] | Right motor forward |
| 3C.4 | Connect L298N IN4 → Pi GPIO 23 | Alex | [ ] | Right motor backward |
| 3C.5 | **CRITICAL: Connect L298N GND → Pi GND (pin 6)** | Alex | [ ] | Common ground — without this, motors won't respond to GPIO |
| 3C.6 | Optional: Connect ENA → GPIO 12, ENB → GPIO 13 for PWM speed | Alex | [ ] | If not using: leave jumpers on ENA/ENB for full speed |
| 3C.7 | Double-check all 5 connections against wiring diagram in `WIRING.md` | Alex + Raphael | [ ] | Two sets of eyes — one wrong wire can fry the Pi |
| 3C.8 | Take a photo of the completed wiring | Alex | [ ] | For troubleshooting + documentation |

### 3D: Motor Test (~15 min)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 3D.1 | Insert 18650 batteries into holder | Alex | [ ] | Charged batteries only |
| 3D.2 | Power on Pi via USB-C power bank | Alex | [ ] | Wait for boot — 30 sec |
| 3D.3 | SSH into Pi | Romeo or Alex | [ ] | `ssh elktron@elktron-escort.local` |
| 3D.4 | Run motor test script: | Romeo | [ ] | See script below |

```python
# motor_test.py — run on Pi
from gpiozero import Robot
import time
robot = Robot(left=(17, 27), right=(22, 23))
print("Forward..."); robot.forward(0.3); time.sleep(2)
print("Stop"); robot.stop(); time.sleep(1)
print("Backward..."); robot.backward(0.3); time.sleep(2)
print("Stop"); robot.stop(); time.sleep(1)
print("Left turn..."); robot.left(0.3); time.sleep(2)
print("Stop"); robot.stop(); time.sleep(1)
print("Right turn..."); robot.right(0.3); time.sleep(2)
print("Stop"); robot.stop()
print("DONE — all 4 directions tested")
```

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 3D.5 | Verify forward: all 4 wheels spin forward | Alex | [ ] | Prop chassis on box so wheels are off ground |
| 3D.6 | Verify backward: all 4 wheels spin backward | Alex | [ ] | |
| 3D.7 | Verify left turn: right wheels forward, left slow/reverse | Alex | [ ] | If reversed: swap LEFT/RIGHT pairs on L298N |
| 3D.8 | Verify right turn: left wheels forward, right slow/reverse | Alex | [ ] | |
| 3D.9 | If any direction wrong: check wiring, swap motor pair wires | Alex | [ ] | Most common issue: forward/backward swapped on one side |

### 3E: Ultrasonic Sensor (HC-SR04) (~30 min)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 3E.1 | Build voltage divider on breadboard: ECHO → 1kΩ → junction → 2kΩ → GND | Alex or Raphael | [ ] | Junction point connects to GPIO 24 |
| 3E.2 | Connect HC-SR04 VCC → Pi 5V (pin 2) | Alex | [ ] | |
| 3E.3 | Connect HC-SR04 GND → Pi GND | Alex | [ ] | |
| 3E.4 | Connect HC-SR04 TRIG → GPIO 25 | Alex | [ ] | |
| 3E.5 | Connect voltage divider junction → GPIO 24 | Alex | [ ] | **Do NOT connect ECHO directly to Pi — 5V will damage it** |
| 3E.6 | Mount HC-SR04 on front of chassis, facing forward | Alex | [ ] | Hot glue, velcro, or mounting bracket |
| 3E.7 | Run ultrasonic test: | Romeo | [ ] | See script below |

```python
# sonar_test.py — run on Pi
from gpiozero import DistanceSensor
import time
sonar = DistanceSensor(echo=24, trigger=25, max_distance=2)
for i in range(20):
    print(f"Distance: {sonar.distance * 100:.1f} cm")
    time.sleep(0.5)
```

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 3E.8 | Hold hand at 30cm → reading ~30cm (±5cm) | Alex | [ ] | |
| 3E.9 | Hold hand at 100cm → reading ~100cm | Alex | [ ] | |
| 3E.10 | Remove hand → reading >150cm | Alex | [ ] | |
| 3E.11 | If readings always 0 or max: check voltage divider wiring | Alex | [ ] | Most common issue |

### 3F: Camera + Pan-Tilt Mount (~1 hour, after 3/12 delivery)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 3F.1 | Assemble Arducam pan-tilt platform (2 servos + bracket) | Alex or Raphael | [ ] | Follow Arducam instructions |
| 3F.2 | Mount pan-tilt on TOP of chassis using standoffs or bracket | Alex | [ ] | Needs to be stable — camera shake ruins detection |
| 3F.3 | Connect pan-tilt servo controller to Pi (I2C or GPIO PWM) | Alex | [ ] | Check Arducam docs for pin assignment |
| 3F.4 | Mount camera on pan-tilt bracket | Alex | [ ] | Camera arrives 3/14 — use USB webcam for testing until then |
| 3F.5 | Connect Arducam IMX708 via CSI ribbon cable to Pi 5 | Alex | [ ] | Pi 5 has different CSI connector than Pi 4 — use correct cable |
| 3F.6 | Test camera: `libcamera-hello --timeout 5000` | Romeo | [ ] | Should show live preview |
| 3F.7 | Test pan-tilt servos sweep (write quick test script) | Romeo | [ ] | Pan: ±45°, Tilt: -30° to +60° |
| 3F.8 | Verify 120° FOV captures full aisle width at 2m distance | Alex | [ ] | Stand 2m away, walk side to side — should stay in frame |

### 3G: Mast Construction (~30 min, Home Depot parts)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 3G.1 | Cut PVC pipe to ~3.5 ft (adjust based on chassis height) | Anyone | [ ] | Goal: camera at mid-rack height (~3-4 ft from floor) |
| 3G.2 | Attach PVC T-connector to base of mast | Anyone | [ ] | T-connector mounts horizontally to chassis |
| 3G.3 | Secure T-connector to chassis with zip ties or bolts | Anyone | [ ] | Must be rigid — wobble = unusable camera feed |
| 3G.4 | Mount pan-tilt + camera at top of mast | Alex | [ ] | Velcro + zip ties — needs to be removable for transport |
| 3G.5 | Route CSI ribbon cable down mast, secure with velcro | Alex | [ ] | Keep away from motor wires — EMI interference |
| 3G.6 | Stability test: push mast gently — should not sway more than 1cm | Alex | [ ] | If wobbly: add cross-brace with PVC elbow |

### 3H: Power System Assembly (~30 min)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 3H.1 | Insert charged 18650 batteries into battery holder | Alex | [ ] | 2 batteries in series = 7.4V for motors |
| 3H.2 | Connect battery holder to L298N VCC + GND | Alex | [ ] | Already done in 3B.10 |
| 3H.3 | Connect USB-C power bank to Pi 5 via short USB-C cable | Alex | [ ] | Mount power bank on chassis with velcro |
| 3H.4 | Verify Pi boots on battery power (not wall plug) | Alex | [ ] | Green LED blinks, SSH works |
| 3H.5 | Verify motors spin on battery power | Alex | [ ] | Run motor_test.py again |
| 3H.6 | Run full system for 5 min — check for brown-outs | Alex | [ ] | If Pi reboots: power bank can't supply enough amps |
| 3H.7 | Measure battery life: run motors continuously, time until weak | Alex | [ ] | Target: 30+ min for demo day |
| 3H.8 | Label all power connections with tape | Alex | [ ] | So you can swap batteries quickly on demo day |

---

## PHASE 4: ESCORT BOT — SOFTWARE TESTING (March 12–16)

### 4A: Camera-Only Detection (no motors needed)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 4A.1 | Copy `test_camera.py` to Pi: `scp test_camera.py elktron@elktron-escort.local:~/` | Romeo | [ ] | |
| 4A.2 | Run: `python3 test_camera.py` (headless mode) | Romeo | [ ] | Terminal output: "Person detected at (x,y) conf=0.XX" |
| 4A.3 | Stand 1m from camera → verify person detection confidence >0.5 | Romeo | [ ] | |
| 4A.4 | Stand 3m from camera → verify still detects (may be lower confidence) | Romeo | [ ] | |
| 4A.5 | Walk side to side → verify bounding box tracks correctly | Romeo | [ ] | |
| 4A.6 | Test with 2 people in frame → should track the largest (closest) | Romeo + anyone | [ ] | |
| 4A.7 | Check inference speed: should be <100ms per frame on Pi 5 | Romeo | [ ] | If >200ms: check model is quantized (uint8) |
| 4A.8 | Test in different lighting: bright, dim, fluorescent | Romeo | [ ] | DC floor is fluorescent — test under similar lighting |
| 4A.9 | Test with person in dark clothing | Romeo | [ ] | Common failure mode |
| 4A.10 | Test with person carrying a box (partial occlusion) | Romeo | [ ] | Vendor escort scenario |

### 4B: Full Software Integration (after motors + sonar tested)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 4B.1 | Copy `main.py` + `pan_tilt.py` to Pi | Romeo | [ ] | |
| 4B.2 | Edit `main.py` config: verify GPIO pins match wiring | Romeo | [ ] | LEFT_MOTOR, RIGHT_MOTOR, ECHO, TRIG |
| 4B.3 | Edit camera config: verify resolution + camera index | Romeo | [ ] | Use picamera2 for Arducam IMX708 |
| 4B.4 | Edit model path: verify `models/ssd_mobilenet_v2.pb` exists | Romeo | [ ] | |
| 4B.5 | **Bench test (wheels off ground):** run `main.py` | Romeo + Alex | [ ] | See checklist below |
| 4B.6 | Stand in front → wheels spin forward | Alex observes | [ ] | |
| 4B.7 | Move LEFT → right wheels speed up (bot tries to turn left) | Alex observes | [ ] | |
| 4B.8 | Move RIGHT → left wheels speed up (bot turns right) | Alex observes | [ ] | |
| 4B.9 | Walk closer → wheels slow down / stop (too close) | Alex observes | [ ] | |
| 4B.10 | Walk away → wheels speed up (trying to follow) | Alex observes | [ ] | |
| 4B.11 | Disappear from frame → wheels stop after 1.5 sec | Alex observes | [ ] | |
| 4B.12 | Hold hand in front of sonar (<30cm) → emergency stop | Alex observes | [ ] | |
| 4B.13 | If steering reversed: swap left/right GPIO in config | Romeo | [ ] | |
| 4B.14 | Test scan mode: stand still for 3+ seconds → scan triggers | Romeo | [ ] | Pan-tilt should sweep, capture frames to `scans/` |

### 4C: Floor Testing (after bench test passes)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 4C.1 | Find open indoor space (hallway, garage, empty room) | Anyone | [ ] | Smooth floor, not carpet |
| 4C.2 | Set `BASE_SPEED = 0.2` (start slow) | Romeo | [ ] | Safety first |
| 4C.3 | Place bot on floor, SSH in, run `main.py` | Romeo | [ ] | |
| 4C.4 | **Safety:** Someone stands near bot ready to pick it up | Alex or Raphael | [ ] | |
| 4C.5 | Stand 2m in front → bot moves toward you | Romeo | [ ] | |
| 4C.6 | Walk forward slowly → bot follows | Romeo | [ ] | |
| 4C.7 | Stop → bot stops within 0.5–1m | Romeo | [ ] | |
| 4C.8 | Turn left → bot turns left | Romeo | [ ] | |
| 4C.9 | Turn right → bot turns right | Romeo | [ ] | |
| 4C.10 | Walk behind a pillar/wall → bot stops after timeout | Romeo | [ ] | |
| 4C.11 | Walk for 30+ seconds continuously → bot follows the whole time | Romeo | [ ] | THIS is the demo shot |
| 4C.12 | Record a phone video of the floor test | Anyone | [ ] | Good for demo B-roll |

### 4D: Tuning (~1 hour, iterate on these)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 4D.1 | If oscillating left/right: reduce KP (1.0 → 0.6) | Romeo | [ ] | |
| 4D.2 | If not turning enough: increase KP (1.0 → 1.5) | Romeo | [ ] | |
| 4D.3 | If following too close: decrease TARGET_AREA_RATIO (0.15 → 0.10) | Romeo | [ ] | |
| 4D.4 | If too far: increase TARGET_AREA_RATIO (0.15 → 0.20) | Romeo | [ ] | |
| 4D.5 | If losing person too easily: decrease CONFIDENCE_THRESHOLD (0.5 → 0.35) | Romeo | [ ] | |
| 4D.6 | If tracking wrong objects: increase CONFIDENCE_THRESHOLD | Romeo | [ ] | |
| 4D.7 | Gradually increase BASE_SPEED (0.2 → 0.3 → 0.4 → 0.5) | Romeo | [ ] | |
| 4D.8 | Record final "golden config" values — write them in main.py | Romeo | [ ] | These are the demo settings |

---

## PHASE 5: SO-101 ARM BUILD (March 18–21, after kit arrives)

### 5A: Assembly (~2-3 hours)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 5A.1 | Unbox HiWonder kit — inventory all parts against list | Josh + Talha | [ ] | 2 arms, 12 servos, 2 BusLinkers, PSUs, clamps, hardware |
| 5A.2 | Verify all 12 servos spin freely — none DOA | Josh | [ ] | Power each briefly to test |
| 5A.3 | **Leader arm assembly:** mount servos S1-S6 (base → gripper) | Josh | [ ] | Follow HiWonder assembly guide |
| 5A.4 | Route leader arm cables, velcro at each joint | Josh | [ ] | Clean routing prevents snags |
| 5A.5 | Connect leader servos to BusLinker V3.0 (daisy chain) | Josh | [ ] | |
| 5A.6 | Connect 5V PSU to leader BusLinker | Josh | [ ] | |
| 5A.7 | Connect USB-C from leader BusLinker to laptop | Josh | [ ] | Verify detected: `ls /dev/ttyACM*` or `ls /dev/cu.usbmodem*` |
| 5A.8 | **Follower arm assembly:** repeat S1-S6 (identical to leader) | Josh + Talha | [ ] | |
| 5A.9 | Route follower cables, velcro at joints | Josh + Talha | [ ] | |
| 5A.10 | Connect follower servos to BusLinker V3.0 | Josh | [ ] | |
| 5A.11 | Connect 12V 5A PSU to follower BusLinker | Josh | [ ] | Higher voltage = more torque |
| 5A.12 | Connect USB-C from follower BusLinker to laptop | Josh | [ ] | Should be second ttyACM device |
| 5A.13 | Clamp both arms to table ~30cm apart | Josh | [ ] | Firm — no wobble allowed |
| 5A.14 | Mount NexiGo webcam overhead or on gooseneck, pointing at follower workspace | Josh | [ ] | Verify webcam sees full arm workspace |

### 5B: Mechanical Verification (~30 min)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 5B.1 | Manually move each leader arm joint — smooth, no binding | Josh | [ ] | |
| 5B.2 | Manually move each follower arm joint — smooth, no binding | Josh | [ ] | |
| 5B.3 | Verify gripper opens/closes fully on both arms | Josh | [ ] | |
| 5B.4 | Confirm full range of motion — no table collisions | Josh | [ ] | |
| 5B.5 | Tighten all screws — loose screws = drift during training | Josh | [ ] | |
| 5B.6 | Verify cable routing doesn't snag during full sweep | Josh | [ ] | |

### 5C: Software Setup (~1 hour)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 5C.1 | Install Python 3.11 on training machine (Mac or Linux laptop) | Josh | [ ] | |
| 5C.2 | Create venv: `python3 -m venv ~/lerobot-env` | Josh | [ ] | |
| 5C.3 | Run `so101/install.sh` — installs LeRobot + deps | Josh | [ ] | |
| 5C.4 | Verify torch backend: `torch.backends.mps.is_available()` (Mac) | Josh | [ ] | |
| 5C.5 | Create LeRobot config YAML — set serial ports + camera index | Josh | [ ] | follower: ttyACM0, leader: ttyACM1, camera: 0 |
| 5C.6 | Test config loads: `python -c "from lerobot..."` | Josh | [ ] | |
| 5C.7 | Test webcam: `python -c "import cv2; cap=cv2.VideoCapture(0); print(cap.read()[0])"` | Josh | [ ] | |

### 5D: Calibration (~1 hour)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 5D.1 | Run LeRobot calibration: `python lerobot/scripts/control_robot.py calibrate` | Josh | [ ] | Move each joint to physical limits when prompted |
| 5D.2 | Record min/max angles for all 6 joints, both arms | Josh | [ ] | Write down on paper |
| 5D.3 | Save calibration file — back it up | Josh | [ ] | **Do NOT lose this** |
| 5D.4 | Test mirroring: move leader joint 1 to 90° → follower matches | Josh | [ ] | |
| 5D.5 | Test all 6 joints mirror within ~2° | Josh | [ ] | |
| 5D.6 | Mark workspace positions with tape: HOME, OPTIC TRAY, SWITCH PORT | Josh | [ ] | |
| 5D.7 | Verify follower can reach: home → tray → port → home | Josh | [ ] | |

### 5E: Teleoperation + Data Collection (~2-3 hours)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 5E.1 | Launch teleoperation mode — verify leader controls follower | Josh | [ ] | |
| 5E.2 | Practice optic seating manually 5+ times before recording | Josh | [ ] | Grab optic → lift → move to port → seat → release → retract |
| 5E.3 | Start recording: `python so101/record.py` | Josh | [ ] | |
| 5E.4 | Record episodes 1–10 (basic, clean motions) | Josh | [ ] | Each episode: 10–30 seconds |
| 5E.5 | Review episode 1 video — camera captures full action? | Josh | [ ] | |
| 5E.6 | Record episodes 11–30 (consistent, smooth) | Josh + Talha | [ ] | Talha can take turns recording |
| 5E.7 | Record episodes 31–50 (add minor variations: angle, path) | Josh + Talha | [ ] | |
| 5E.8 | Verify dataset: video files exist, joint CSVs look correct | Josh | [ ] | |
| 5E.9 | Delete any episodes with collisions or drops | Josh | [ ] | |
| 5E.10 | Backup dataset to external drive or cloud | Josh | [ ] | |
| 5E.11 | **Stretch:** Record 50+ more episodes for robustness | Josh + Talha | [ ] | 100 total is ideal |

### 5F: Training (~2-4 hours, mostly unattended)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 5F.1 | Start training: `python so101/train.py` | Josh | [ ] | Mac MPS: 2-4 hrs, NVIDIA GPU: 1-2 hrs |
| 5F.2 | Open TensorBoard: `tensorboard --logdir outputs/` | Josh | [ ] | Monitor loss curve |
| 5F.3 | Verify loss decreases for first 50-100 epochs | Josh | [ ] | |
| 5F.4 | Watch for overfitting (val loss goes up while train goes down) | Josh | [ ] | Stop if overfitting |
| 5F.5 | Save best checkpoint (lowest val loss) | Josh | [ ] | |
| 5F.6 | Back up trained model | Josh | [ ] | |

### 5G: Deployment + Testing (~2 hours)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 5G.1 | Load best checkpoint into `deploy.py` | Josh | [ ] | |
| 5G.2 | Set up identical workspace (same positions, lighting, camera) | Josh | [ ] | |
| 5G.3 | Place optic in tray, arm at home position | Josh | [ ] | |
| 5G.4 | Run: `python so101/deploy.py` | Josh | [ ] | **WATCH — be ready to Ctrl+C** |
| 5G.5 | Does arm move toward optic? | Josh | [ ] | Basic directional test |
| 5G.6 | Does arm grasp optic? | Josh | [ ] | |
| 5G.7 | Does arm seat optic in port? | Josh | [ ] | |
| 5G.8 | Does arm retract to home? | Josh | [ ] | |
| 5G.9 | Run 10 consecutive attempts — log success/failure | Josh | [ ] | Target: >60% success |
| 5G.10 | If <60%: record 20 more demos + retrain | Josh | [ ] | Fine-tune, don't start over |

---

## PHASE 6: DASHBOARD (March 14–20)

### 6A: Backend (FastAPI)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 6A.1 | Set up Python venv for dashboard: `python3 -m venv ~/fc-dashboard-env` | Parth | [ ] | |
| 6A.2 | Install deps: `pip install fastapi uvicorn websockets` | Parth | [ ] | |
| 6A.3 | Run mock server: `cd elktron-app/api && uvicorn server:app --reload --port 8080` | Parth | [ ] | |
| 6A.4 | Verify WebSocket mock data flows to frontend | Parth | [ ] | Open `http://localhost:8080` |
| 6A.5 | Add mock Jira data to server (vendor name, ticket ID, rack) | Parth | [ ] | Use Romeo's Jira MCP for real schema |
| 6A.6 | Add mock NetBox data to server (device name, status, rack unit) | Parth | [ ] | Use Romeo's NetBox MCP for real schema |
| 6A.7 | Create 5 sample scan report JSONs in `data/scans/` | Parth | [ ] | Follow schema in `elktron-app/CLAUDE.md` |
| 6A.8 | Wire `arm.py` to receive real arm telemetry when hardware connected | Romeo or Josh | [ ] | After arm is built |
| 6A.9 | Wire `escort.py` to receive real escort telemetry when bot connected | Romeo | [ ] | After bot passes floor test |

### 6B: Frontend (Dashboard UI)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 6B.1 | Review existing `index.html` — understand 5 panel layout | Parth | [ ] | Arm status, escort bot, camera feeds, scan log, training console |
| 6B.2 | Style dashboard: dark theme, CoreWeave-inspired (navy/white/accent) | Parth | [ ] | Match `robotics-site/index.html` aesthetic |
| 6B.3 | **Arm Status panel:** show 6 joint angles as animated gauges/bars | Parth | [ ] | Updates at 10Hz via WebSocket |
| 6B.4 | **Arm Status panel:** gripper state indicator (open/closed/holding) | Parth | [ ] | Color-coded |
| 6B.5 | **Arm Status panel:** current task name + status (IDLE/RUNNING/COMPLETE) | Parth | [ ] | |
| 6B.6 | **Escort Bot panel:** mode indicator (FOLLOW/SCAN/IDLE) | Parth | [ ] | Large, color-coded badge |
| 6B.7 | **Escort Bot panel:** sonar distance bar | Parth | [ ] | Red when <30cm |
| 6B.8 | **Escort Bot panel:** detection confidence + bbox overlay info | Parth | [ ] | |
| 6B.9 | **Escort Bot panel:** vendor name + ticket ID (from Jira mock) | Parth | [ ] | |
| 6B.10 | **Camera Feeds panel:** placeholder for 1-2 live video streams | Parth | [ ] | WebSocket binary or MJPEG `<img>` |
| 6B.11 | **Scan Log panel:** table of past scans — timestamp, rack, result, vendor | Parth | [ ] | Expandable rows for detail |
| 6B.12 | **Scan Log panel:** color-code results — green=clean, red=flagged | Parth | [ ] | |
| 6B.13 | **Training Console panel:** episode counter, status, progress bar | Parth | [ ] | Mock data is fine for demo |
| 6B.14 | Add "LIVE" badge that pulses when receiving real-time data | Parth | [ ] | Visual indicator for judges |
| 6B.15 | Responsive layout — works on laptop screen (1440px) + projector (1080p) | Parth | [ ] | |
| 6B.16 | Add Elktron logo/branding in header | Parth | [ ] | |

### 6C: Data Integration (stretch — connects to CW systems)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 6C.1 | Pull sample Jira tickets using `jira_search` MCP tool | Romeo | [ ] | Export 5-10 representative tickets as JSON |
| 6C.2 | Pull sample NetBox rack data using `netbox_rack_devices` | Romeo | [ ] | Export 2-3 racks with devices |
| 6C.3 | Embed Jira/NetBox data in mock server responses | Parth | [ ] | Real data, not fake — makes demo authentic |
| 6C.4 | Dashboard shows real rack device names from NetBox | Parth | [ ] | |
| 6C.5 | Dashboard shows real ticket IDs from Jira | Parth | [ ] | |

---

## PHASE 7: DEMO VIDEO PRODUCTION (March 20–22)

### 7A: Demo Script

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 7A.1 | Write full 3-minute demo narration script | Andrew | [ ] | Use `/elktron-pitch-writer` skill for draft |
| 7A.2 | Script structure — approved by Romeo: | | | |

```
0:00–0:20  INTRO — "Elktron: AI-powered robots for the DC floor"
           Show both robots + dashboard. Set the scene.

0:20–0:40  PROBLEM — "Vendors on the DC floor are unmonitored.
           Rack contact goes unlogged. Optic seating is manual and slow."

0:40–1:20  ESCORT BOT DEMO — Bot follows a "vendor" through an aisle.
           Stops at rack. Camera sweeps rack. Dashboard updates live.
           Narrate: Pi 5, TFLite, <100ms inference, person detection.

1:20–2:00  SO-101 ARM DEMO — Arm picks optic from tray, seats it in port.
           Show autonomous run. Dashboard shows joint angles updating.
           Narrate: LeRobot, 50 demos, ACT policy, imitation learning.

2:00–2:30  DASHBOARD — Show all 5 panels. Scan log with real data.
           Jira ticket context. NetBox rack mapping.
           Narrate: "One dashboard for both robots."

2:30–2:50  IMPACT — "Reduces vendor escort time by X.
           Automates manual optic seating. Every rack contact logged."

2:50–3:00  CLOSE — "Elktron. Built for the floor. Built at CoreWeave."
```

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 7A.3 | Review script with full team — everyone understands the story | All | [ ] | |
| 7A.4 | Assign who narrates each section | Andrew + Romeo | [ ] | |
| 7A.5 | Time the script read-aloud — must be <3 min | Andrew | [ ] | |

### 7B: Recording Setup

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 7B.1 | Find a clean, well-lit room for recording | Andrew | [ ] | Preferably with white/neutral background |
| 7B.2 | Set up recording camera (phone on tripod or DSLR) | Andrew | [ ] | 1080p minimum |
| 7B.3 | Test audio: narrate a sentence, play back, check clarity | Andrew | [ ] | No echo, no background noise |
| 7B.4 | Set up screen recording for dashboard (OBS or QuickTime) | Andrew | [ ] | Capture dashboard panel updates |
| 7B.5 | Have spare batteries for everything (bot, Pi, camera) | Alex | [ ] | Nothing dies mid-take |
| 7B.6 | Print small "Elktron" sign to place near robots | Anyone | [ ] | Branding in video |

### 7C: Filming

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 7C.1 | Record escort bot following vendor — 5+ takes | Andrew films, Romeo/Alex operate | [ ] | Pick smoothest |
| 7C.2 | Record escort bot scan mode — close-up of pan-tilt sweep | Andrew | [ ] | The "wow" moment |
| 7C.3 | Record SO-101 arm autonomous optic seating — 5+ takes | Andrew films, Josh operates | [ ] | Close-up of optic being seated |
| 7C.4 | Record dashboard screen — all panels updating live | Andrew (screen capture) | [ ] | |
| 7C.5 | Record team intro shot (optional but good for People's Choice) | Andrew | [ ] | 5-sec clip of team waving |
| 7C.6 | Record B-roll: wiring, assembly, Pi boot screen, terminal output | Andrew | [ ] | Fills gaps in edit |

### 7D: Editing

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 7D.1 | Import all footage into video editor (iMovie / DaVinci / Premiere) | Andrew | [ ] | |
| 7D.2 | Cut to 3-minute final edit following script structure | Andrew | [ ] | |
| 7D.3 | Add narration audio track | Andrew | [ ] | |
| 7D.4 | Add title card: "Elktron — CoreWeave Hackathon 2026" | Andrew | [ ] | |
| 7D.5 | Add text overlays: tech specs, metrics, labels | Andrew | [ ] | "Pi 5 + TFLite", "LeRobot ACT Policy" |
| 7D.6 | Add background music (optional, low volume) | Andrew | [ ] | Royalty-free, tech/ambient |
| 7D.7 | Export at 1080p, <100MB | Andrew | [ ] | |
| 7D.8 | Full team watches final cut — approve or request changes | All | [ ] | |
| 7D.9 | Upload final video to submission platform | Romeo | [ ] | |

---

## PHASE 8: PITCH DECK / SLIDES (March 20–22)

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 8.1 | Create slide deck (5-7 slides max) | Andrew + Romeo | [ ] | |
| 8.2 | Slide 1: Title — "Elktron" + team names + track | Andrew | [ ] | |
| 8.3 | Slide 2: Problem — vendor escorts unmonitored, manual optic seating | Andrew | [ ] | |
| 8.4 | Slide 3: Solution — two robots, one dashboard | Andrew | [ ] | Diagram showing both robots + dashboard |
| 8.5 | Slide 4: Escort Bot — architecture diagram, tech stack, demo screenshot | Andrew | [ ] | |
| 8.6 | Slide 5: SO-101 Arm — LeRobot pipeline, demo screenshot | Andrew | [ ] | |
| 8.7 | Slide 6: Dashboard — screenshot, Jira/NetBox integration | Andrew | [ ] | |
| 8.8 | Slide 7: Impact + What's Next — metrics, roadmap | Andrew | [ ] | |
| 8.9 | Review slides with team | All | [ ] | |

---

## PHASE 9: INTEGRATION & REHEARSAL (March 21–22)

### 9A: Full System Integration

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 9A.1 | Both robots running simultaneously | Romeo + Josh + Alex | [ ] | |
| 9A.2 | Dashboard receiving live telemetry from escort bot | Romeo | [ ] | WebSocket from Pi |
| 9A.3 | Dashboard receiving live telemetry from arm | Josh | [ ] | WebSocket from laptop |
| 9A.4 | Camera feeds streaming to dashboard | Romeo | [ ] | At least one feed working |
| 9A.5 | Scan report generates and appears in dashboard log | Romeo | [ ] | After bot scan completes |
| 9A.6 | If live hardware integration fails: switch to mock data | Romeo | [ ] | Dashboard still looks complete |

### 9B: Rehearsal

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 9B.1 | Run full demo script end-to-end (no camera) | All | [ ] | Identify any gaps |
| 9B.2 | Time the run — must be under 3 min | Andrew (timekeeper) | [ ] | |
| 9B.3 | Rehearse with camera rolling — practice take | Andrew | [ ] | |
| 9B.4 | Review practice video — note issues | All | [ ] | |
| 9B.5 | Fix issues found in rehearsal | Relevant owner | [ ] | |
| 9B.6 | Run demo 3x back-to-back without stopping | All | [ ] | Stress test everything |
| 9B.7 | Rehearse failsafe scenarios: | | | |
| 9B.7a | — What if escort bot won't follow? Switch to manual RC | Romeo + Alex | [ ] | |
| 9B.7b | — What if arm doesn't work? Switch to teleoperation | Josh | [ ] | |
| 9B.7c | — What if WiFi fails? Dashboard runs locally | Romeo | [ ] | |
| 9B.7d | — What if battery dies? Swap in spare | Alex | [ ] | |

---

## PHASE 10: DEMO DAY — MARCH 23

### 10A: Morning — Setup

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 10A.1 | Charge ALL batteries the night before | Alex | [ ] | Motor packs, power banks, phone |
| 10A.2 | Pack everything in labeled boxes | All | [ ] | Robots, cables, power, laptop, spare parts |
| 10A.3 | **Packing checklist — DO NOT FORGET:** | | | |
| 10A.3a | — Escort bot (fully assembled) | Alex | [ ] | |
| 10A.3b | — SO-101 arm (both arms, clamped to portable board?) | Josh | [ ] | |
| 10A.3c | — Laptop (charged) + charger | Romeo | [ ] | |
| 10A.3d | — USB-C hub | Romeo | [ ] | |
| 10A.3e | — USB-C cables x3 (arm leader, arm follower, webcam) | Josh | [ ] | |
| 10A.3f | — Power strips + extension cord | Romeo | [ ] | |
| 10A.3g | — 12V PSU + 5V PSU (arm power) | Josh | [ ] | |
| 10A.3h | — Motor batteries (charged) x2 sets | Alex | [ ] | |
| 10A.3i | — Pi power banks (charged) x2 | Alex | [ ] | |
| 10A.3j | — MicroSD card (with OS + software) | Romeo | [ ] | |
| 10A.3k | — Sample optic + fiber tray (demo prop) | Romeo | [ ] | Grab from DC floor |
| 10A.3l | — Screwdriver set + velcro + zip ties (emergency repair) | Alex | [ ] | |
| 10A.3m | — Phone tripod or camera for recording | Andrew | [ ] | |
| 10A.3n | — Spare jumper wires + breadboard | Alex | [ ] | |
| 10A.3o | — "Elktron" printed sign | Anyone | [ ] | |
| 10A.4 | Arrive early — set up table, test everything works in venue | All | [ ] | 30 min before start |
| 10A.5 | Connect to venue WiFi — test SSH to Pi, dashboard loads | Romeo | [ ] | |
| 10A.6 | If venue WiFi unreliable: set up phone hotspot | Romeo | [ ] | |
| 10A.7 | Do one full dry run at the venue | All | [ ] | |

### 10B: Demo Time

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 10B.1 | Romeo narrates / presents | Romeo | [ ] | |
| 10B.2 | Alex operates escort bot | Alex | [ ] | |
| 10B.3 | Josh operates SO-101 arm | Josh | [ ] | |
| 10B.4 | Andrew manages recording | Andrew | [ ] | |
| 10B.5 | Parth has dashboard on screen | Parth | [ ] | |
| 10B.6 | Raphael plays "vendor" for escort demo | Raphael | [ ] | Walk the route, stop at "rack" |
| 10B.7 | Talha monitors from audience perspective — signals if anything not visible | Talha | [ ] | |

### 10C: After Demo

| # | Task | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 10C.1 | Upload final demo video (if not pre-recorded) | Andrew + Romeo | [ ] | |
| 10C.2 | Push code to GitHub repo (clean up secrets first) | Romeo | [ ] | |
| 10C.3 | Submit to hackathon judges | Romeo | [ ] | |
| 10C.4 | Celebrate | All | [ ] | You built two robots in 2 weeks |

---

## QUICK REFERENCE — KEY FILES

| File | What | Who Needs It |
|------|------|-------------|
| `escort-bot/main.py` | Escort bot brain — person detection + motor control | Romeo, Alex |
| `escort-bot/test_camera.py` | Camera-only test (no motors) | Romeo |
| `escort-bot/install.sh` | Pi software setup (one command) | Romeo, Alex |
| `escort-bot/WIRING.md` | GPIO pinout + wiring diagrams | Alex, Raphael |
| `escort-bot/PI-SETUP.md` | Pi 5 OS flash + first boot guide | Romeo, Alex |
| `robotics-site/so101/record.py` | Record arm demos | Josh, Talha |
| `robotics-site/so101/train.py` | Train ACT policy | Josh |
| `robotics-site/so101/deploy.py` | Run trained arm autonomously | Josh |
| `robotics-site/so101/install.sh` | LeRobot + deps setup | Josh |
| `robotics-site/so101/HARDWARE.md` | Arm BOM + assembly notes | Josh, Talha |
| `elktron-app/index.html` | Dashboard UI | Parth |
| `elktron-app/api/server.py` | Dashboard backend (FastAPI) | Parth, Romeo |
| `elktron-app/api/arm.py` | Arm serial interface | Josh, Romeo |
| `elktron-app/api/escort.py` | Escort bot telemetry | Romeo |
| `elktron-app/api/models.py` | Data schemas | Parth |
| `PROGRESS.md` | Single source of truth — what's done, what's next | Everyone |
| `PARTS-LIST.md` | Hardware BOM + Amazon links | Alex, Romeo |
| `VELOCITY.md` | Engineering pace manifesto — read this | Everyone |

---

## TIMELINE SUMMARY

```
March 11 (TODAY)  ─── Hardware arrives, Pi setup, sign up
March 12          ─── SIGN-UP DEADLINE, more hardware, motor/sonar tests
March 13–14       ─── Escort bot assembly complete, camera test
March 15–16       ─── Floor testing + tuning, dashboard started
March 17          ─── Buffer day (catch up on anything behind)
March 18          ─── SO-101 arm kit arrives (hopefully)
March 19          ─── Arm assembly + calibration
March 20          ─── Arm data collection + training, dashboard polish
March 21          ─── Integration testing, demo script finalized
March 22          ─── Rehearsal, video recording, final polish
March 23–25       ─── HACKATHON DAYS
March 26          ─── DEMO DAY (11am–2pm PT / 2pm–5pm ET)
```

---

## RISK REGISTER

| Risk | Impact | Likelihood | Mitigation | Owner |
|------|--------|-----------|------------|-------|
| SO-101 kit delayed past 3/20 | High | Medium | Demo uses pre-recorded arm video + teleoperation live | Josh |
| Escort bot can't follow reliably | High | Low | Fallback: manual RC control + narrate vision | Romeo + Alex |
| Pi 5 overheats under CV load | Medium | Low | Active cooler ordered. If still hot: reduce resolution | Romeo |
| WiFi fails at venue | Medium | Medium | Phone hotspot backup, dashboard runs locally | Romeo |
| Battery dies mid-demo | Medium | Low | Spare charged packs on standby | Alex |
| Team member unavailable March 23–26 | Medium | Low | Cross-train: each robot has 2 people who can operate it | All |
| Camera arrives late (ETA 3/14) | Low | Low | Use USB webcam until Arducam arrives | Romeo |
| Training doesn't converge | Medium | Medium | More data (100+ episodes) or simpler task subset | Josh |

---

*Last updated by Romeo — 2026-03-11. Update this file as tasks complete.*
