# Escort Bot — Raspberry Pi 5 Setup Guide

> **Target hardware:** Raspberry Pi 5 (4GB or 8GB)
> **Required OS:** Raspberry Pi OS Bookworm 64-bit (Lite recommended)
> **Last updated:** 2026-03-09

---

## Why This OS?

| Requirement | Why Bookworm 64-bit Lite |
|-------------|--------------------------|
| **Pi 5 support** | Bookworm is the **only** official OS for Pi 5. Bullseye does NOT support Pi 5. |
| **64-bit** | Required for OpenCV DNN performance. 32-bit halves inference speed on Pi 5's Cortex-A76 cores. |
| **Lite (no desktop)** | Robot runs headless. No GPU wasted on desktop compositor. All resources go to CV + motor control. Saves ~500MB RAM. |
| **picamera2** | Pre-installed on Bookworm. Uses libcamera stack (not legacy raspistill). |
| **gpiozero 2.0+** | Bookworm ships with lgpio backend (not RPi.GPIO), which is the only GPIO lib that works on Pi 5. |
| **Python 3.11+** | Bookworm ships Python 3.11. OpenCV wheels are built for 3.11+. |

**Do NOT use:**
- Bullseye (no Pi 5 support)
- Ubuntu (GPIO support is worse, picamera2 setup is painful)
- 32-bit (halves inference performance)
- Desktop version (wastes RAM/GPU on a headless robot)

---

## What You Need

- [ ] Raspberry Pi 5 (owned)
- [ ] MicroSD card — 32GB+ Class 10 / A2 (Samsung EVO Select or SanDisk Extreme recommended)
- [ ] SD card reader (USB or built-in)
- [ ] Your laptop/Mac
- [ ] WiFi network name + password (for headless SSH)

---

## Step 1: Download Raspberry Pi Imager

**macOS direct download:**
https://downloads.raspberrypi.com/imager/imager_latest.dmg

Or install via Homebrew:
```bash
brew install --cask raspberry-pi-imager
```

**Official page:** https://www.raspberrypi.com/software/

---

## Step 2: Flash the SD Card

1. Insert MicroSD card into your Mac
2. Open **Raspberry Pi Imager**
3. Click **CHOOSE DEVICE** → select **Raspberry Pi 5**
4. Click **CHOOSE OS** → select:
   ```
   Raspberry Pi OS (other)
     → Raspberry Pi OS Lite (64-bit)
         Debian Bookworm, no desktop
   ```
5. Click **CHOOSE STORAGE** → select your MicroSD card
6. Click **NEXT**

### IMPORTANT: Configure Settings (DO THIS!)

When prompted "Would you like to apply OS customisation settings?", click **EDIT SETTINGS**:

**General tab:**
- [x] Set hostname: `escort-bot`
- [x] Set username and password:
  - Username: `pi`
  - Password: (pick something — you'll SSH with this)
- [x] Configure wireless LAN:
  - SSID: (your WiFi network)
  - Password: (your WiFi password)
  - Country: US
- [x] Set locale:
  - Timezone: America/Chicago
  - Keyboard: us

**Services tab:**
- [x] Enable SSH → Use password authentication

Click **SAVE** → click **YES** to apply → click **YES** to confirm write.

Wait for write + verification to complete (~5-10 min).

---

## Step 3: First Boot

1. Eject SD card from Mac
2. Insert into Pi 5
3. Connect power (USB-C, 5V/3A minimum)
4. Wait ~60-90 seconds for first boot
5. Find Pi on your network:

```bash
# From your Mac terminal:
ping escort-bot.local

# If that doesn't resolve, scan the network:
arp -a | grep -i "raspberry\|dc:a6\|b8:27\|d8:3a\|2c:cf"
# Or use: brew install nmap && nmap -sn 192.168.1.0/24
```

6. SSH in:
```bash
ssh pi@escort-bot.local
# Enter your password when prompted
```

---

## Step 4: Run the Install Script

Once SSH'd into the Pi:

```bash
# Clone or copy the escort-bot code to Pi
# Option A: scp from your Mac
# (run this on your Mac, not the Pi)
scp -r ~/hackathon/escort-bot/ pi@escort-bot.local:~/escort-bot/

# Option B: git clone (if repo is pushed)
# git clone <repo-url> ~/escort-bot

# Then on the Pi:
cd ~/escort-bot
chmod +x install.sh
./install.sh
```

This installs: picamera2, OpenCV, gpiozero, lgpio, and downloads the MobileNet SSD model.

---

## Step 5: Verify Everything Works

```bash
# Test camera (should show 5 seconds of video output info)
libcamera-hello --timeout 5000

# Test GPIO (should print pin info without errors)
python3 -c "from gpiozero import Device; print('GPIO OK:', Device.pin_factory)"

# Test OpenCV DNN (should print model loaded)
python3 -c "
import cv2
net = cv2.dnn.readNetFromTensorflow('models/ssd_mobilenet_v2.pb', 'models/ssd_mobilenet_v2.pbtxt')
print('OpenCV DNN OK. Backend:', cv2.dnn.DNN_BACKEND_OPENCV)
"

# If all three pass, run the bot:
python3 main.py
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ssh: connect to host escort-bot.local port 22: Connection refused` | Pi hasn't finished booting. Wait 90s. Or WiFi creds were wrong — reflash with correct SSID/password. |
| `ModuleNotFoundError: No module named 'lgpio'` | Run `sudo apt install python3-lgpio` — Pi 5 needs lgpio, not RPi.GPIO |
| `libcamera-hello` shows no camera | Check CSI ribbon cable is seated firmly. Use the Pi 5 CSI port (between HDMI ports). |
| `python3-opencv` not found | Run `sudo apt install python3-opencv` (preferred over pip on Pi) |
| Pi throttles / gets hot | Attach heatsink or active cooler. Pi 5 throttles at 85°C under CV workload. |
| GPIO permission denied | Add user to gpio group: `sudo usermod -aG gpio pi && reboot` |

---

## Performance Tips for Demo Day

- **Overclock (optional):** Add `arm_freq=2800` to `/boot/firmware/config.txt` (up from 2400MHz default). Needs active cooling.
- **Disable Bluetooth** (saves CPU): `sudo systemctl disable bluetooth`
- **Disable swap** (SD card longevity): `sudo dphys-swapfile swapoff && sudo systemctl disable dphys-swapfile`
- **Pin CPU governor:** `echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor`

---

## Claude Code (AI-Assisted Dev on the Pi)

Claude Code CLI is installed on the Pi. This gives you an AI coding assistant directly on the robot hardware.

```bash
# SSH into Pi, then:
cd ~/escort-bot
claude
```

**What this unlocks:**
- Edit and debug `main.py`, `pan_tilt.py`, `test_camera.py` without leaving the Pi
- Ask Claude to read sensor output, inspect GPIO pins, and fix code in one loop
- Iterate on motor calibration, detection thresholds, and PID tuning with AI assistance
- On demo day: rapid on-site fixes without needing a laptop with the codebase

**Tip:** Run `claude` in the `~/escort-bot` directory so it picks up the project CLAUDE.md for full context.

---

## Quick Reference

| Item | Value |
|------|-------|
| OS | Raspberry Pi OS Lite (64-bit) — Bookworm |
| Hostname | `escort-bot` |
| Username | `pi` |
| SSH | `ssh pi@escort-bot.local` |
| Python | 3.11+ (system) |
| GPIO lib | lgpio (via gpiozero 2.0+) |
| Camera lib | picamera2 + libcamera |
| ML runtime | OpenCV DNN (MobileNet SSD v2) |
| AI dev tool | Claude Code CLI (installed) |
| Imager download | https://downloads.raspberrypi.com/imager/imager_latest.dmg |
| OS downloads | https://www.raspberrypi.com/software/operating-systems/ |
