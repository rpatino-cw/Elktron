# Progression — Build Evidence

Photos and screenshots documenting the Elktron escort bot build process at the DC floor.

---

## 2026-03-16 — Full Hardware Assembly + Person Detection Working

Major milestone: chassis assembled, L298N wired to Pi 5 GPIO, Arducam IMX708 connected via CSI ribbon, and **YOLOv8n person detection confirmed working on the DC floor** at 78% confidence. Claude Code installed directly on the Pi for on-device AI development.

### Hardware Assembly Photos

| File | What |
|------|------|
| `pi5-active-cooler-dc.jpg` | Pi 5 in red case with active cooler, powered at DC workbench (Cisco switch visible) |
| `pi5-camera-ribbon.jpg` | Pi 5 close-up showing CSI ribbon cable ("Standard - Mini 200mm") to Arducam IMX708 |
| `pi5-camera-dc-floor.jpg` | Pi 5 with camera connected, Cisco equipment in background |
| `chassis-wiring-overview.jpg` | Full bot: Pi 5 + LK-COKOINO 4WD chassis + L298N motor driver, all wired |
| `chassis-l298n-full.jpg` | Overhead view — chassis with L298N and motor wiring visible |
| `l298n-wiring-closeup.jpg` | L298N motor driver close-up — blue GPIO wires + red power to motors |
| `l298n-gpio-wires.jpg` | L298N with GPIO control wires (blue/green/black) and motor power (red) |
| `motor-wiring-detail.jpg` | Motor wiring detail — labeled motor connectors, L298N output terminals |

### Person Detection Test (on Pi 5 at DC)

| File | What |
|------|------|
| `camtest-person-detect-01.jpg` | Detection output — "person 0.78" bounding box on camera frame |
| `camtest-person-detect-03.jpg` | Second detection frame — same confidence, different pose |
| `camtest_01-05.jpg` | All 5 test frames with detection bounding boxes |
| `yolov8n-terminal-output.jpg` | Terminal: YOLOv8n loading, 5/5 frames captured, all detecting 1 person |
| `scp-transfer-pi.jpg` | SCP transfer of camtest images from Pi (elktron@192.168.3.57) to Mac |

### Technical Details
- **Model:** YOLOv8n (ultralytics)
- **Camera:** Arducam IMX708 wide-angle (libcamera v0.7.0+rpt20260205)
- **Resolution:** 640x360 sRGB + 1536x864 RAW
- **Confidence:** 0.78 (person class)
- **Pi hostname:** elktron@192.168.3.57
- **Location:** CoreWeave EVI01 DC floor
- **Claude Code:** Installed on Pi — on-device AI development confirmed
- **Chassis:** LK-COKOINO 4WD with yellow-tape motor labels (FR, FL, RR, RL)
- **Motor driver:** L298N (WWZMDiB) — GPIO control wires (blue) + motor power (red)
- **Power:** USB-C power bank visible in assembly photos
