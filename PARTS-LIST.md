# Elktron — Complete Parts List

> **Last updated:** 2026-03-09
> **Budget estimate:** ~$430–$455 total (before owned items)
> **Hackathon date:** March 23, 2026

Legend: ✅ = Owned | 🛒 = Need to buy | ⏳ = Ordered, waiting

---

## ROBOT 1: SO-101 Arm (Manipulation Bot)

### Option A: HiWonder Pre-Built Kit (RECOMMENDED)

- [ ] 🛒 **SO-ARM101 DIY Kit** — ~$270
  - Source: https://www.hiwonder.com/products/lerobot-so-101
  - Includes ALL of the following:
    - 6x Follower arm servos (HX-30HM / STS3215) — 30kg.cm @ 12V
    - 6x Leader arm servos (HX-10HM) — lighter, for teleoperation
    - 2x BusLinker V3.0 servo controller (USB-to-serial)
    - 1x 12V 5A power supply (barrel jack, follower arm)
    - 1x 5V power supply (leader arm)
    - 4x Table clamps (2 per arm)
    - Full set 3D-printed structural parts (ABS/PLA arm links + brackets)
    - Screws, cables, assembly hardware (M2/M3)

### Option B: DIY Build (requires 3D printer)

- [ ] 🛒 Feetech STS3215 servos x6 (follower) — ~$120 — AliExpress / RobotShop
- [ ] 🛒 Feetech STS3215 servos x6 (leader) — ~$100 — AliExpress
- [ ] 🛒 BusLinker V3.0 board x2 — ~$30 — HiWonder / AliExpress
- [ ] 🛒 3D-printed parts (STLs from https://github.com/TheRobotStudio/SO-ARM100) — ~$35 filament
- [ ] 🛒 12V 5A DC power supply — ~$12 — Amazon
- [ ] 🛒 5V 3A power supply — ~$8 — Amazon
- [ ] 🛒 Table C-clamps x4 (2" opening min) — ~$10 — Amazon / hardware store
- [ ] 🛒 M2 + M3 screw assortment kit — ~$8 — Amazon
- [ ] 🛒 Servo extension cables x6 (3-pin, 20cm) — ~$5 — Amazon

### Arm Add-ons (needed regardless of option)

- [ ] 🛒 **USB webcam (arm-mounted)** — ~$25 — Logitech C270 or similar, 1080p, OpenCV-compatible
- [ ] 🛒 USB-C data cable (to laptop, 6ft) — ~$8 — Amazon
- [ ] 🛒 Webcam mount/bracket — ~$5 — 3D-print or flex gooseneck clamp
- [ ] 🛒 Velcro cable ties / strips — ~$5 — Amazon (reusable, easier to reposition during prototyping)

**Arm subtotal (Option A + add-ons): ~$311**

---

## ROBOT 2: Escort Bot (Person-Following Mobile Robot)

### Compute (OWNED)

- [x] ✅ **Raspberry Pi 5** (8GB) — OWNED
- [x] ✅ **Raspberry Pi 4** — OWNED (backup)
- [x] ✅ **Raspberry Pi Pico** — OWNED (not ideal for CV)
- [x] ✅ **MicroSD card** — OWNED
- [x] ✅ **Raspberry Pi 5 Active Cooler (OFFICIAL)** — DELIVERED 3/11
  - PWM temp-controlled blower + aluminum heatsink + thermal tape
  - REQUIRED — TFLite CV workload will thermal throttle Pi 5 without cooling

> **Pi 5 OS Setup Guide:** See [`escort-bot/PI-SETUP.md`](escort-bot/PI-SETUP.md)
> **OS:** Raspberry Pi OS Lite (64-bit) — Bookworm. Only official OS for Pi 5. Lite = headless, no desktop wasting RAM.
> **Imager download:** https://downloads.raspberrypi.com/imager/imager_latest.dmg

### Chassis + Drivetrain

- [x] ✅ **LK-COKOINO 4WD Chassis Kit** — $26.99 — Alex ordering
  - Amazon: https://www.amazon.com/Arduino-LK-COKOINO-Raspberry-Building/dp/B0B5JPJ9R4
  - Kit includes (BARE CHASSIS ONLY):
    - Acrylic frame pieces
    - 4x TT DC geared motors + dupont wires
    - 4x metal motor brackets
    - 4x wheels (rubber, 2.56" diameter)
    - 1x 18650 battery holder (2-slot)
    - Screws, nuts, copper standoffs, zip ties
    - Screwdriver + wrench
  - **NOT included:** motor driver, sensors, camera, servos, Pi, batteries
  - **Docs:** `CKK0011-main/` — assembly PDFs, wiring tutorials

### Motor Control

- [x] ✅ **L298N motor driver (2-pack)** — ORDERED 3/10, arriving 3/12
  - WWZMDiB 2x L298N DC Dual H-Bridge — have a spare
  - Wiring: GPIO 17/27 (left motor), 22/23 (right motor). See WIRING.md.
- [ ] 🛒 Jumper wires M-F x20 (20cm) — ~$5 — Amazon (GPIO → L298N)
- [ ] 🛒 Jumper wires M-M x10 (20cm) — ~$3 — Amazon

### Sensors

- [x] ✅ **HC-SR04 ultrasonic sensors** — ORDERED 3/10
  - DIYables 2-pack (arriving 3/12) + ELEGOO 5-pack (arriving 3/14) — plenty of spares
  - ⚠️ ECHO pin is 5V — needs voltage divider (1kΩ + 2kΩ) or use HC-SR04P
- [ ] 🛒 Resistor kit (1kΩ + 2kΩ for voltage divider) — ~$3 — Amazon

### Vision

- [x] ✅ **Arducam Camera Module 3 Wide (IMX708, 120°)** — ORDERED 3/10, arriving Saturday 3/15
  - Autofocus, Pi 5 compatible, includes 15cm 15-22 pin FFC cable + acrylic case
- [x] ✅ **Arducam Pan/Tilt Platform** — ORDERED 3/10, arriving 3/12
  - Compatible with Pi Camera Module 3/V1/V2
  - Pan on GPIO 12, tilt on GPIO 13. Controlled by `pan_tilt.py`.

### Power (ALL PORTABLE — no wall outlets on DC floor)

- [x] ✅ **18650 Li-ion batteries (4-pack)** — $33.86 — ORDERED 3/11, arriving Saturday 3/15
  - QOJH 3.7V 3000mAh, button top, protected
  - WHY 4-PACK: 2 in the bot, 2 charged and ready to hot-swap during demo
- [x] ✅ **18650 dual-slot charger** — (in same order) — ORDERED 3/11, arriving Saturday 3/15
  - ACEBOTT smart charger, auto-shutoff, US plug
  - CHARGE NIGHT BEFORE DEMO — full charge takes ~4 hours
- [x] ✅ **18650 battery holder bundle (8-pack)** — ORDERED 3/10, arriving 3/12
  - QTEATAK — 1-slot (3.7V), 2-slot (7.4V), 3-slot (11.1V), 4-slot (14.8V) — 2 of each
  - Gives flexibility if chassis holder breaks or need different voltage configs
- [x] ✅ **USB-C power bank (Pi power)** — $22 — ORDERED 3/11, arriving Friday 3/14
  - Anker PowerCore 10K, 10000mAh, 5V/3A USB-C
  - MUST support 5V/3A output — Pi 5 will brownout on weak banks
  - Runtime: ~3-4 hours continuous CV workload
- [ ] 🛒 **Second USB-C power bank (backup/swap)** — ~$22
  - Same model. Demo runs 2-5pm — one bank may not last. Swap takes 10 seconds.
- [ ] 🛒 Short USB-C cable (6-12 inches, power bank → Pi) — ~$5 — Amazon
- [x] ✅ **USB-C right-angle adapter (2-pack)** — $9.11 — ORDERED 3/11, arriving 3/12
  - Silkland 90° adapter, 240W/40Gbps — overkill specs but keeps cable flush on chassis
- [x] ✅ **CanaKit 3.5A Pi Power Supply with PiSwitch** — $13.93 — ORDERED 3/11, arriving 3/12
  - Wall adapter with inline on/off switch — USE FOR BENCH TESTING + DEVELOPMENT
  - NOT portable — still need USB-C power bank for untethered DC floor demo

### Power — SO-101 Arm (Demo Day)

- [ ] 🛒 **Extension cord / power strip** — ~$0 (bring from home)
  - The arm's 12V/5V power supplies need wall power — arm is NOT portable
  - Confirm demo area has outlets or bring a 20ft extension cord

**Power architecture (escort bot — fully portable):**
```
Pi 5       ← USB-C power bank (5V/3A, mounted on chassis)
Motors     ← 18650 x2 in series (7.4V) through L298N
Sensors    ← Pi 5V rail (HC-SR04 VCC)
Pan/Tilt   ← Pi 5V rail (2x MG90S servos, ~150mA each)
Camera     ← Pi CSI port (powered by Pi internally)
CRITICAL   → Common GND between Pi and L298N!
```

**Power checklist for demo day:**
- [ ] All 4x 18650s fully charged night before
- [ ] Both power banks fully charged night before
- [ ] Test runtime: time how long the bot runs on one set of batteries
- [ ] Bring the 18650 charger to venue (charge spares during other demos)
- [ ] Extension cord for SO-101 arm wall power

### Mast (Camera Height — CRITICAL for Rack Scans)

- [ ] 🛒 **1" Schedule 40 PVC pipe, 3-4 ft** — ~$3 — Home Depot
  - Raises camera from chassis height (~4") to mid-rack height (~36-48")
  - Without this, camera only sees bottom 2-3 rack units — rack scans useless
  - Cut to length at Home Depot (free cuts)
- [ ] 🛒 **1" PVC T-connector x1** — ~$1 — Home Depot
  - Mounts pipe vertically to chassis frame
  - Horizontal arm bolts/zip-ties to acrylic frame mounting holes
- [ ] 🛒 **1" PVC elbow x1** — ~$1 — Home Depot
  - Top of mast — angles camera toward rack face
  - Pan/tilt platform mounts here
- [ ] 🛒 **1" PVC end cap x1** — ~$0.50 — Home Depot
  - Bottom of T-connector, optional stability
- [ ] 🛒 **PVC cement (small can)** — ~$4 — Home Depot
  - Glues T-connector and elbow permanently
  - OR skip cement and use friction fit + zip ties (faster, adjustable during prototyping)
- [ ] 🛒 **Hose clamps x2 (1" diameter)** — ~$2 — Home Depot
  - Secures PVC T-connector to chassis frame
  - Alternative: heavy-duty zip ties through chassis mounting holes

### Misc Hardware

- [ ] 🛒 Velcro strips / cable ties (reusable) — ~$5
- [ ] 🛒 Double-sided foam tape (1 roll) — ~$5
- [ ] 🛒 Half-size breadboard — ~$4
- [ ] 🛒 Electrical tape (1 roll) — ~$3
- [ ] 🛒 Heat shrink tubing assortment — ~$5 — Home Depot / Amazon (for voltage divider solder joints, cleaner than tape)
- [ ] 🛒 Rubber bumper pads (self-adhesive) — ~$3 — Home Depot (chassis corner protection for demo day)
- [ ] Rubber bands x5 — ~$0 (around the house)

**Escort bot subtotal: ~$202** (chassis from Alex, all electronics bought separately — L298N, HC-SR04, camera, pan/tilt, power, mast)

---

## SHARED / DEMO EQUIPMENT

- [x] ✅ **Laptop** (Mac M-series for training + demo) — OWNED
- [ ] 🛒 USB-A hub (4-port, if laptop is USB-C only) — ~$12 — Amazon
- [ ] 🛒 Ethernet cable (for SSH into Pi) — ~$5 — Amazon
- [ ] 🛒 HDMI cable + portable monitor (optional, Pi debug) — ~$0-30
- [ ] 🛒 **Extension cord (25ft)** — ~$10 — Home Depot / Amazon
  - SO-101 arm needs wall power (12V + 5V supplies). Demo area may not have outlets nearby.
- [ ] 🛒 **Power strip (6-outlet, surge protector)** — ~$10 — Amazon
  - Arm 12V supply + arm 5V supply + laptop charger + 18650 charger (charging spares during demo)
- [ ] Sample optic / fiber tray (arm demo task) — grab from DC floor
- [ ] Hard hat / safety vest (demo realism) — already have from DC

**Shared subtotal: ~$37-67**

---

## COST SUMMARY

| Category | Estimate |
|----------|----------|
| SO-101 Arm (HiWonder kit + add-ons) | ~$311 |
| Escort Bot (all parts — kit covers driver/sensor/camera) | ~$175 |
| Shared / Demo gear | ~$37-67 |
| **GRAND TOTAL** | **~$523-553** |
| Minus owned items (Pi 5, Pi 4, laptop, DC gear) | -$0 saved (no price on owned) |

### Savings:
- Alex providing chassis kit (~$27 saved)
- CanaKit PiSwitch replaces standalone power switch (~$7 saved)

---

## ORDER PRIORITY (what to buy first)

1. **HiWonder SO-101 Kit** — longest ship time (~5-7 days), order ASAP
2. **Freenove 4WD Kit** — Amazon Prime, 1-2 days
3. **Batteries + charger** — need charged before demo day
4. **Everything else** — Amazon Prime, order by March 18 latest

---

## RESOURCE LINKS

| Resource | URL |
|----------|-----|
| HiWonder SO-101 Kit | https://www.hiwonder.com/products/lerobot-so-101 |
| SO-ARM100 STLs (3D print) | https://github.com/TheRobotStudio/SO-ARM100 |
| LeRobot (HuggingFace) | https://github.com/huggingface/lerobot |
| LeRobot SO-101 docs | https://huggingface.co/docs/lerobot/en/so101 |
| Freenove 4WD GitHub | https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi |
| Haoran Xu build log | https://www.linkedin.com/pulse/lets-build-ai-hack-lerobot-so101-haoran-xu-onaqc/ |
| iRobot Create 3 (alt escort) | https://github.com/iRobotEducation/create3_docs |
