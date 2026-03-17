#!/usr/bin/env python3
"""Sonar test — verify HC-SR04 wiring and distance readings.

Wiring (HC-SR04 → Pi 5):
  VCC  → 5V
  GND  → GND
  TRIG → GPIO25
  ECHO → 1kΩ → junction → GPIO24
                junction → 2kΩ → GND
  (voltage divider: 5V ECHO → 3.3V safe for Pi)
"""
from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=24, trigger=25, max_distance=4.0)

print("Sonar Test — HC-SR04 via gpiozero")
print("=" * 40)
print("Move hand/object in front of sensor.\nCtrl+C to stop.\n")

try:
    while True:
        d = sensor.distance * 100  # meters → cm
        bar = "█" * int(min(d, 200) / 5)
        status = "TOO CLOSE" if d < 30 else "OK"
        print(f"  {d:6.1f} cm  {bar:40s}  [{status}]", end="\r", flush=True)
        sleep(0.1)
except KeyboardInterrupt:
    print("\n\nDone.")
    sensor.close()
