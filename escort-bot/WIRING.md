# Elktron Escort Bot — Wiring Guide

## GPIO Pin Map (BCM numbering)

```
┌─────────────────────────────────────────────────┐
│              RASPBERRY PI 5                      │
│                                                  │
│  Pin  │ BCM │ Function        │ Connects To      │
│───────┼─────┼─────────────────┼──────────────────│
│  11   │  17 │ Left Motor FWD  │ L298N IN1        │
│  13   │  27 │ Left Motor BWD  │ L298N IN2        │
│  15   │  22 │ Right Motor FWD │ L298N IN3        │
│  16   │  23 │ Right Motor BWD │ L298N IN4        │
│  18   │  24 │ Ultrasonic ECHO │ HC-SR04 ECHO     │
│  22   │  25 │ Ultrasonic TRIG │ HC-SR04 TRIG     │
│  32   │  12 │ Pan Servo PWM   │ Pan-Tilt PAN     │
│  33   │  13 │ Tilt Servo PWM  │ Pan-Tilt TILT    │
│   3   │   2 │ I2C SDA         │ LCD SDA          │
│   5   │   3 │ I2C SCL         │ LCD SCL          │
│   2   │  5V │ Sensor Power    │ HC-SR04 VCC      │
│   4   │  5V │ LCD Power       │ LCD VCC          │
│   6   │ GND │ Common Ground   │ L298N GND        │
│   9   │ GND │ Sensor Ground   │ HC-SR04 GND      │
│  14   │ GND │ LCD Ground      │ LCD GND          │
└─────────────────────────────────────────────────┘
```

## L298N Motor Driver Wiring

> **One L298N handles all 4 motors.** The L298N is a dual H-bridge (2 channels).
> The 4 TT motors wire as 2 parallel pairs — no second driver needed.
> - **Channel A** (OUT1/OUT2) → Left pair (Front-Left + Rear-Left) wired in parallel
> - **Channel B** (OUT3/OUT4) → Right pair (Front-Right + Rear-Right) wired in parallel
> Each channel's output wires reverse polarity for direction — they are NOT separate ground/hot.

```
BATTERY (7.4V)                 L298N                    MOTORS
─────────────┐          ┌──────────────┐
  (+) ───────┼──────────┤ +12V (VIN)   │         ┌── Front-Left
             │          │              ├── OUT1/2 ┤                (Channel A — LEFT)
  (-) ───────┼──────────┤ GND          │         └── Rear-Left
             │          │              │
             │          │              │         ┌── Front-Right
             │          │              ├── OUT3/4 ┤                (Channel B — RIGHT)
             │          │              │         └── Rear-Right
             │     Pi ──┤ IN1 ← GPIO17 │
             │     Pi ──┤ IN2 ← GPIO27 │
             │     Pi ──┤ IN3 ← GPIO22 │
             │     Pi ──┤ IN4 ← GPIO23 │
             │          │              │
             │     5V ──┤ +5V (logic)  │  ← REQUIRED — see ENA/ENB note below
             │          │              │
             │  Pi GND ─┤ GND          │  ← COMMON GROUND (critical!)
             │          └──────────────┘
```

### ENA / ENB Jumpers — CRITICAL

The L298N has **two enable pins** (ENA for Channel A, ENB for Channel B). Each enable pin sits between a pair of **dual header pins** on the board edge.

**To get motors spinning, you MUST jumper ENA and ENB:**

```
L298N Board Edge (top view)
┌────────────────────────────────────┐
│                                    │
│   [ENA•─•]  ← jumper these two    │
│                pins together       │
│   OUT1  OUT2   IN1  IN2           │
│                                    │
│   OUT3  OUT4   IN3  IN4           │
│                                    │
│   [ENB•─•]  ← jumper these two    │
│                pins together       │
│                                    │
│   +12V  GND  +5V                  │
└────────────────────────────────────┘
```

**How to jumper:** Use a **female-to-female dupont wire** to loop each enable pin's two header pins to each other. This connects enable HIGH, giving full speed on that channel.

**Without these jumpers, motors will NOT spin** — GPIO signals reach IN1-IN4 but the H-bridge outputs stay disabled. This is the #1 reason for "GPIO works but wheels don't move."

**+5V logic pin:** The L298N's **+5V pin** must be connected to **Pi 5V** (pin 2 or 4). When battery voltage is >7V, the onboard regulator can supply 5V — but it's more reliable to feed 5V from the Pi. **Remove the onboard regulator jumper** (the jumper near the +5V pin) if you're feeding external 5V.

## HC-SR04 Ultrasonic Sensor

```
HC-SR04          Pi 5
────────         ─────
VCC ──────────── 5V (Pin 2)
TRIG ─────────── GPIO25 (Pin 22)
ECHO ──┬── 1kΩ ── GPIO24 (Pin 18)   ← VOLTAGE DIVIDER (5V → 3.3V)
       └── 2kΩ ── GND               ← Protects Pi GPIO from 5V
GND ──────────── GND (Pin 9)
```

> **IMPORTANT:** The HC-SR04 ECHO pin outputs 5V. Pi 5 GPIO is 3.3V tolerant.
> Use the voltage divider (1kΩ + 2kΩ resistors) — 1:2 ratio gives ~3.33V output.
> Without the divider you risk frying the GPIO pin.
> Alternative: use HC-SR04P (3.3V version) and skip the divider.

## I2C LCD Screen

```
LCD Module       Pi 5
──────────       ─────
GND ──────────── GND (Pin 14)
VCC ──────────── 5V  (Pin 4)
SDA ──────────── GPIO2 / SDA1 (Pin 3)
SCL ──────────── GPIO3 / SCL1 (Pin 5)
```

> The LCD uses the **I2C bus** (dedicated pins, no conflict with motor/sensor GPIOs).
> Most I2C LCD modules have a default address of `0x27` or `0x3F`.
> Scan for the address after wiring:
> ```bash
> sudo i2cdetect -y 1
> ```
> Enable I2C on the Pi if not already:
> ```bash
> sudo raspi-config nonint do_i2c 0
> ```

## Pan/Tilt Servos

```
Pan Servo        Pi 5
─────────        ─────
Signal ────────── GPIO12 (Pin 32)
VCC ──────────── 5V (Pi 5V rail or external)
GND ──────────── GND

Tilt Servo       Pi 5
──────────       ─────
Signal ────────── GPIO13 (Pin 33)
VCC ──────────── 5V
GND ──────────── GND
```

> MG90S servos draw ~150mA each. Two servos = ~300mA from the 5V rail.
> If the Pi brownouts under load, power servos from the battery pack through a 5V BEC instead.

## Camera

Arducam IMX708 120° wide-angle connects via **CSI ribbon cable** to the CAM port on the Pi 5.
Powered internally by the Pi — no external wiring needed.

## Power (Fully Portable — Two Separate Sources)

```
USB-C Power Bank (5V/3A+) ──── Pi 5 USB-C port
  └── right-angle USB-C adapter → inline power switch → Pi
  └── Backup power bank ready for hot-swap

18650 x2 in series (7.4V) ──── L298N +12V (VIN)
  └── Powers motors through L298N
  └── 2 spare 18650s charged and ready

Pi 5V rail ──── Sensors + Servos + LCD
  └── HC-SR04 VCC
  └── Pan/tilt servos (~300mA total)
  └── LCD VCC
  └── Camera (CSI, powered internally by Pi)

CRITICAL: Common GND between Pi and L298N!
```

Two separate power sources:
1. Pi runs off USB-C power bank (5V/3A minimum — Pi 5 brownouts on weak banks)
2. Motors run off 18650 battery pack through L298N

Do NOT power the Pi from the L298N's 5V regulator — it can't supply enough current for Pi 5 under CV load (~3A).

## Quick Test Commands

```bash
# Test camera
libcamera-hello --timeout 5000

# Test ultrasonic (Python)
python3 -c "from gpiozero import DistanceSensor; s=DistanceSensor(echo=24,trigger=25); print(f'{s.distance*100:.1f}cm')"

# Test motors (Python) — wheels will spin!
python3 -c "from gpiozero import Robot; r=Robot(left=(17,27),right=(22,23)); r.forward(0.3); import time; time.sleep(1); r.stop()"

# Scan I2C bus for LCD address
sudo i2cdetect -y 1

# Test LCD (after installing RPLCD)
python3 -c "from RPLCD.i2c import CharLCD; lcd=CharLCD('PCF8574',0x27); lcd.write_string('Elktron Bot')"

# Test pan/tilt servos
python3 pan_tilt.py --simulate
```
