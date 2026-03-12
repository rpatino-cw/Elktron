# CKK0011 — LK-COKOINO 4WD Car Chassis Kit (Manufacturer Repo)

## What This Is

This is the **official manufacturer repository** for the LK-COKOINO 4WD Robot Car Chassis Kit (product code CKK0011), cloned from GitHub. It contains CH340 USB-serial drivers, assembly tutorials (PDF), and example code for both Arduino and Raspberry Pi platforms. This is NOT code written by the Elktron team — it is vendor-provided reference material.

The LK-COKOINO chassis is the **physical platform for the Escort Bot** — one of two robots in the Elktron hackathon project. Alex Murillo ordered this chassis kit (ETA March 11, 2026) and will assemble it with her own Raspberry Pi. The escort bot software that runs on the assembled chassis lives in `../escort-bot/`.

## Why This Repo Matters

The CKK0011 repo is the ground truth for three things:

1. **Assembly instructions** — The Tutorial PDFs walk through physically building the chassis step by step, including how to mount motors, attach wheels, wire the motor driver, and route power. Without these, you are guessing at assembly.

2. **Motor driver code** — The Raspberry Pi tutorials include working Python examples for two different motor driver configurations (L298N standalone and the Cokoino Robot Hat). The Elktron `escort-bot/main.py` uses L298N + gpiozero, but if debugging motor issues, cross-reference with `Demo1.py` (L298N approach) and `Demo2.py` (Robot Hat approach) here.

3. **CH340 driver** — The Cokoino Robot Hat uses a CH340 USB-serial chip. If using the hat instead of standalone L298N, the CH340 driver in this repo must be installed on the host machine. The Elktron project currently uses standalone L298N (no hat), so the CH340 driver is likely unnecessary — but keep it as a backup option.

## Folder Structure

```
CKK0011-main/
├── CLAUDE.md                    # THIS FILE
├── README.md                    # Manufacturer README — download instructions, contact info
│                                  Email: cokoino@outlook.com | Web: cokoino.com
│                                  Facebook: facebook.com/cokoino.lk
│
├── CH340 Driver/
│   └── Windows/                 # CH340 USB-serial driver (Windows only)
│                                  NOT needed for Pi + L298N setup
│                                  Only needed if using Cokoino Robot Hat via USB
│
├── Tutorial/
│   ├── Arduino/                 # Arduino-based tutorials and sketches
│   │   ├── 0 Read me first(important).pdf     # Start here — prerequisites
│   │   ├── 1 Introduction of 4WD Car Chassis.pdf  # Chassis overview, specs, parts
│   │   ├── 2 Install the Arduino IDE and Driver.pdf  # Arduino IDE + CH340 setup
│   │   ├── 3 How to Assemble the 4WD Car Chassis.pdf  # ★ ASSEMBLY GUIDE — photos + steps
│   │   ├── Experiment 1-How to use MG90S Micro Servo.pdf  # Servo control tutorial
│   │   ├── Experiment 2-Drive TT Motor to run the 4WD car.pdf  # Motor driving
│   │   ├── Experiment 3-Testing WS2812 LED Module.pdf  # LED strip control
│   │   ├── Experiment 4-Testing Ultrasonic Ranging Module.pdf  # HC-SR04 ultrasonic
│   │   ├── Experiment 5-Testing Line Tracking Module.pdf  # IR line tracking
│   │   └── Sketches/            # Arduino .ino source files
│   │       ├── 02.1_Testing_TT_Motor/
│   │       ├── 03.1_Testing_WS2812_LED/
│   │       ├── 04.1_Testing_Ultrasonic_Ranging_Module/
│   │       ├── 05.1_Testing_Tracking_Sensor/
│   │       └── 05.2_Line_Tracking_Car/
│   │
│   └── RaspberryPi/             # ★ RASPBERRY PI TUTORIALS — most relevant to Elktron
│       ├── 0 Read me first.pdf              # Prerequisites for Pi setup
│       ├── 1 Introduction of 4WD Car Chassis.pdf  # Same chassis overview as Arduino version
│       ├── 2 Installing and Configuring Raspberry Pi System.pdf  # Pi OS setup guide
│       ├── 3 How to Assemble the 4WD Car Chassis for Raspberry Pi.pdf  # ★ Pi-specific assembly
│       ├── 4 How to use MG90S Micro Servo.pdf  # Servo tutorial (pan/tilt reference)
│       ├── Demo1 Drive L298N motor modules to run the 4WD car.pdf  # ★ L298N wiring + code
│       ├── Demo2 Drive Cokoino 4WD Robot Hat to run the 4WD car.pdf  # Robot Hat alternative
│       └── Code/
│           ├── Demo1.py          # ★ L298N motor control — Python, uses RPi.GPIO
│           │                      #   Elktron uses gpiozero instead, but pin logic is the same
│           ├── Demo2.py          # Robot Hat motor control — Python
│           │                      #   Uses I2C (smbus) instead of direct GPIO
│           └── Servo_test.py     # MG90S servo test — basic PWM angle control
```

## Key Files for Elktron

**Assembly (read in this order):**
1. `Tutorial/RaspberryPi/1 Introduction of 4WD Car Chassis.pdf` — understand what's in the box
2. `Tutorial/RaspberryPi/3 How to Assemble the 4WD Car Chassis for Raspberry Pi.pdf` — step-by-step build
3. `Tutorial/RaspberryPi/Demo1 Drive L298N motor modules to run the 4WD car.pdf` — wiring the L298N

**Code reference (for debugging motor issues):**
- `Tutorial/RaspberryPi/Code/Demo1.py` — L298N motor control using RPi.GPIO. The Elktron `escort-bot/main.py` does the same thing but uses gpiozero's `Robot` class instead. If motors don't work with gpiozero, try running Demo1.py directly to isolate whether the issue is wiring or software.
- `Tutorial/RaspberryPi/Code/Servo_test.py` — Basic servo PWM test. Useful if the pan/tilt servos misbehave — run this to test raw servo control before debugging `pan_tilt.py`.

**Ultrasonic reference:**
- `Tutorial/Arduino/Experiment 4-Testing Ultrasonic Ranging Module.pdf` — HC-SR04 wiring and code. The Arduino version, but the wiring principle is the same for Pi. Cross-reference with `escort-bot/WIRING.md`.

## Differences Between CKK0011 Code and Elktron Code

| Aspect | CKK0011 (this repo) | Elktron (`escort-bot/`) |
|--------|---------------------|---------------------------|
| **GPIO lib** | RPi.GPIO | gpiozero (required for Pi 5 — lgpio backend) |
| **Motor control** | `GPIO.output()` + `GPIO.PWM()` | `Robot(left=(17,27), right=(22,23))` |
| **Servo control** | Raw PWM via `GPIO.PWM()` | `AngularServo` from gpiozero |
| **Camera** | Not included | picamera2 + TFLite MobileNet SSD |
| **Purpose** | Basic driving demos | Autonomous person-following + rack scanning |
| **Pi version** | Pi 3/4 era (RPi.GPIO) | Pi 5 only (lgpio) |

**Important:** The CKK0011 code uses `RPi.GPIO`, which does **NOT work on Pi 5**. Pi 5 requires `lgpio` as the GPIO backend. The Elktron code uses gpiozero which auto-detects lgpio on Pi 5. Do not try to run Demo1.py or Demo2.py on a Pi 5 without first switching them from `RPi.GPIO` to gpiozero or lgpio.

## Chassis Specs (from documentation)

- **Frame:** Acrylic plates (upper + lower deck), ~25cm x 15cm
- **Motors:** 4x TT DC gear motors (3-6V, ~200 RPM no-load)
- **Wheels:** 4x 65mm rubber wheels
- **Steering:** Differential (tank) — left pair vs right pair, no Ackermann
- **Mounting:** Multiple M3 standoff holes for Pi, motor driver, sensors
- **Weight:** ~300g assembled (without Pi or batteries)
- **Power:** 2x 18650 LiPo cells (7.4V) for motors, separate USB-C for Pi

## When to Reference This Repo

- **During assembly** — follow the PDF guides step by step
- **Motor troubleshooting** — if `escort-bot/main.py` can't drive motors, test with `Demo1.py` (adapted to gpiozero) to isolate wiring vs code issues
- **Wiring verification** — compare `escort-bot/WIRING.md` against the L298N tutorial PDF diagrams
- **Servo issues** — run `Servo_test.py` (adapted to gpiozero) to verify servo hardware before debugging `pan_tilt.py`
- **Understanding the chassis** — the introduction PDF has photos and specs not available in the Amazon listing

## Do NOT

- Do not modify files in this repo — it is a vendor reference copy
- Do not try to run the Python code on Pi 5 without porting from RPi.GPIO to gpiozero/lgpio
- Do not install the CH340 driver unless switching to the Cokoino Robot Hat (currently not planned)
- Do not confuse the Arduino tutorials with the Pi tutorials — Elktron uses Pi only
