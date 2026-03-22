# ESP-NOW RC Controller Setup

## What You Have
- 2x ESP32-CAM modules
- 1x ESP32-CAM-MB programmer (clip-on cradle)
- 5x tactile push buttons + wires (for controller)

## Flashing Steps

### 1. Install Arduino IDE + ESP32 Board Support
```bash
# Arduino IDE → File → Preferences → Additional Board URLs:
# https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
# Then: Tools → Board Manager → search "esp32" → install
```

### 2. Get Receiver MAC Address
1. Clip **receiver** ESP32-CAM into programmer cradle
2. Arduino IDE → Tools → Board: **AI Thinker ESP32-CAM**
3. Open `get_mac/get_mac.ino` → Upload
4. Open Serial Monitor (115200 baud)
5. Copy MAC address (e.g., `24:6F:28:AB:CD:EF`)

### 3. Flash Controller
1. Open `controller/controller.ino`
2. Replace `RECEIVER_MAC` with the MAC from step 2:
   ```c
   uint8_t RECEIVER_MAC[] = {0x24, 0x6F, 0x28, 0xAB, 0xCD, 0xEF};
   ```
3. Clip **controller** ESP32-CAM into programmer → Upload

### 4. Flash Receiver
1. Clip **receiver** ESP32-CAM back into programmer
2. Open `receiver/receiver.ino` → Upload
3. Remove from programmer

### 5. Wire Controller Buttons
```
GPIO 13 ──┤ FWD button  ├── GND
GPIO 15 ──┤ BACK button ├── GND
GPIO 14 ──┤ LEFT button ├── GND
GPIO 2  ──┤ RIGHT button├── GND
GPIO 4  ──┤ TURBO button├── GND
```
Power controller from USB power bank (micro USB into programmer cradle).

### 6. Wire Receiver to Pi 5
```
ESP32-CAM          Pi 5
─────────          ────
GPIO 1 (TX)  →  GPIO 15 (RXD)
GND          →  GND
```
Power receiver from Pi's 3.3V or 5V pin.

### 7. Enable UART on Pi 5
```bash
sudo raspi-config
# Interface Options → Serial Port
# Login shell over serial: NO
# Serial port hardware enabled: YES
sudo reboot
```

### 8. Run Motor Control
```bash
cd ~/hackathon/escort-bot/esp32
python3 rc_drive.py           # listen for commands
python3 rc_drive.py --test    # test motors without ESP32
```

## Troubleshooting
- **No serial data:** Check TX→RX wiring (crossed). Verify UART enabled.
- **Motors don't move:** Check L298N 12V power (batteries), verify GND shared between L298N and Pi.
- **ESP-NOW timeout:** Both ESP32-CAMs must be on same WiFi channel (default 0 = auto).
- **Flash fails:** Hold IO0 button while pressing RST on programmer, then release IO0.

## Emergency Stop
Press **Forward + Backward** simultaneously on controller = E-STOP.
