#!/usr/bin/env python3
"""Motor test — verify L298N wiring before running main.py.
Run with wheels OFF THE GROUND first!

Wiring (L298N → Pi 5 GPIO):
  IN1 → GPIO17  IN2 → GPIO27  (left motors)
  IN3 → GPIO22  IN4 → GPIO23  (right motors)
  L298N GND → Pi GND (CRITICAL — common ground)
  Remove 5V jumper on L298N (Pi powered separately via USB-C)
"""
from gpiozero import Robot
from time import sleep
import sys

bot = Robot(left=(17, 27), right=(22, 23))

tests = [
    ("FORWARD",  bot.forward,  0.3),
    ("BACKWARD", bot.backward, 0.3),
    ("LEFT",     bot.left,     0.3),
    ("RIGHT",    bot.right,    0.3),
]

print("Motor Test — L298N via gpiozero")
print("=" * 40)
print("Wheels should be OFF THE GROUND!\n")

for name, fn, speed in tests:
    print(f"  {name} at {int(speed*100)}% ...", end=" ", flush=True)
    fn(speed)
    sleep(1.5)
    bot.stop()
    sleep(0.5)
    print("OK")

print("\nAll directions tested.")
print("If any direction was wrong, swap the IN1/IN2 or IN3/IN4 wires for that side.")
bot.close()
