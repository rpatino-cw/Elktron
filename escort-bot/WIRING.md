# Elktron Escort Bot — Wiring Guide

## GPIO Pin Map (BCM numbering)

```
┌─────────────────────────────────────────────┐
│              RASPBERRY PI 5                  │
│                                              │
│  Pin  │ BCM │ Function        │ Connects To  │
│───────┼─────┼─────────────────┼──────────────│
│  11   │  17 │ Left Motor FWD  │ L298N IN1    │
│  13   │  27 │ Left Motor BWD  │ L298N IN2    │
│  15   │  22 │ Right Motor FWD │ L298N IN3    │
│  16   │  23 │ Right Motor BWD │ L298N IN4    │
│  18   │  24 │ Ultrasonic ECHO │ HC-SR04 ECHO │
│  22   │  25 │ Ultrasonic TRIG │ HC-SR04 TRIG │
│   2   │  5V │ Sensor Power    │ HC-SR04 VCC  │
│   6   │ GND │ Common Ground   │ HC-SR04 GND  │
└─────────────────────────────────────────────┘
```

## L298N Motor Driver Wiring

```
BATTERY (7.4V)                 L298N                    MOTORS
─────────────┐          ┌──────────────┐
  (+) ───────┼──────────┤ +12V (VIN)   │
  (-) ───────┼──────────┤ GND          ├──── Left Motor (+/-)
             │          │              ├──── Right Motor (+/-)
             │     Pi ──┤ IN1 ← GPIO17 │
             │     Pi ──┤ IN2 ← GPIO27 │
             │     Pi ──┤ IN3 ← GPIO22 │
             │     Pi ──┤ IN4 ← GPIO23 │
             │          │              │
             │     Pi ──┤ ENA (jumper) │  ← Leave jumper ON for full speed
             │     Pi ──┤ ENB (jumper) │  ← Or connect to PWM pins for speed control
             │          │              │
             │  Pi GND ─┤ GND          │  ← COMMON GROUND (critical!)
             │          └──────────────┘
```

## HC-SR04 Ultrasonic Sensor

```
HC-SR04          Pi 5
────────         ─────
VCC ──────────── 5V (Pin 2)
TRIG ─────────── GPIO25 (Pin 22)
ECHO ──┬── 1kΩ ── GPIO24 (Pin 18)    ← VOLTAGE DIVIDER (5V → 3.3V)
       └── 2kΩ ── GND                ← Protects Pi GPIO from 5V
GND ──────────── GND (Pin 6)
```

> **IMPORTANT:** The HC-SR04 ECHO pin outputs 5V. Pi 5 GPIO is 3.3V tolerant.
> Use the voltage divider (1kΩ + 2kΩ resistors) or you risk frying the GPIO pin.
> If you don't have resistors, use an HC-SR04P (3.3V version) instead.

## Camera

Pi Camera Module connects via the CSI ribbon cable to the CAM port on the Pi 5.
If using the Freenove kit camera (USB), just plug into a USB port — picamera2
will detect it, but you may need to adjust `init_camera()` in main.py.

## Power (Fully Portable — Two Separate Sources)

```
USB-C Power Bank (5V/3A+) ──── Pi 5 USB-C port
  └── right-angle USB-C adapter → inline power switch → Pi
  └── Backup power bank ready for hot-swap

18650 x2 in series (7.4V) ──── Smart Car Board battery holder
  └── Powers motors via Smart Car Board
  └── 2 spare 18650s charged and ready

Pi 5V rail ──── Connection Board ──── Sensors + Servos
  └── HC-SR04 VCC (via Connection Board)
  └── Pan/tilt servos (~150mA each)
  └── Camera (CSI, powered internally by Pi)

CRITICAL: Common GND between Pi and Smart Car Board!
```

Two separate power sources:
1. Pi runs off USB-C power bank (5V/3A minimum — Pi 5 brownouts on weak banks)
2. Motors run off 18650 battery pack through Smart Car Board

Do NOT power the Pi from the Smart Car Board's 5V regulator — it can't supply enough current for Pi 5 under CV load (~3A).

## Quick Test Commands

```bash
# Test camera
libcamera-hello --timeout 5000

# Test ultrasonic (Python)
python3 -c "from gpiozero import DistanceSensor; s=DistanceSensor(echo=24,trigger=25); print(f'{s.distance*100:.1f}cm')"

# Test motors (Python) — wheels will spin!
python3 -c "from gpiozero import Robot; r=Robot(left=(17,27),right=(22,23)); r.forward(0.3); import time; time.sleep(1); r.stop()"
```
