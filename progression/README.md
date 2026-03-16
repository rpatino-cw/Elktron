# Progression — Build Evidence

Photos and screenshots documenting the Elktron build process.

## 2026-03-16 — Person Detection Working

Camera test on Pi 5 at DC floor. YOLOv8n model detecting persons at 0.78 confidence.

| File | What |
|------|------|
| `camtest_01-05.jpg` | Detection output — bounding boxes on camera frames |
| `pi-terminal-detection.png` | Terminal output showing successful detection run |
| `scp-transfer.png` | SCP transfer of test images from Pi to Mac |

### Details
- Model: YOLOv8n
- Camera: Arducam IMX708 wide (libcamera v0.7.0)
- Resolution: 640x360 sRGB
- Confidence: 0.78
- Pi: elktron@192.168.3.57
