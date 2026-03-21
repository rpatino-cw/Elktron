#!/usr/bin/env python3
"""
GPIO Test Script — Escort Bot Pin Verification & Manual Control

Tests all GPIO pins per GPIO_Current.csv (2026-03-20):
  Motors:  IN1=GPIO17, IN2=GPIO22, IN3=GPIO5, IN4=GPIO6
  Sensor:  TRIG=GPIO23, ECHO=GPIO24
  I2C:     SDA=GPIO2, SCL=GPIO3 (pan/tilt)

Run on the Pi:
  python3 tests/gpio_test.py           # Full pin test
  python3 tests/gpio_test.py --drive   # Interactive keyboard drive mode
"""

import argparse
import sys
import time

try:
    from gpiozero import Robot, DistanceSensor, OutputDevice, Device
    from gpiozero.pins.lgpio import LGPIOFactory
    Device.pin_factory = LGPIOFactory()
    ON_PI = True
except (ImportError, Exception):
    ON_PI = False

# ─── CURRENT GPIO ASSIGNMENTS (per GPIO_Current.csv 2026-03-20) ───
LEFT_FORWARD  = 17   # IN1 — Pin 11
LEFT_BACKWARD = 22   # IN2 — Pin 15
RIGHT_FORWARD = 5    # IN3 — Pin 29
RIGHT_BACKWARD = 6   # IN4 — Pin 31
ULTRASONIC_TRIG = 23 # Pin 16
ULTRASONIC_ECHO = 24 # Pin 18


def test_pins():
    """Test each GPIO pin individually."""
    if not ON_PI:
        print("Not on Pi — simulating pin test")
        pins = {
            "IN1 (Left Fwd)":  LEFT_FORWARD,
            "IN2 (Left Bwd)":  LEFT_BACKWARD,
            "IN3 (Right Fwd)": RIGHT_FORWARD,
            "IN4 (Right Bwd)": RIGHT_BACKWARD,
            "TRIG":            ULTRASONIC_TRIG,
            "ECHO":            ULTRASONIC_ECHO,
        }
        for name, pin in pins.items():
            print(f"  [SIM] GPIO {pin:>2} — {name}")
        return

    print("=== GPIO Pin Test ===\n")

    # Test motor pins one at a time
    motor_pins = [
        ("IN1 (Left Fwd)",  LEFT_FORWARD),
        ("IN2 (Left Bwd)",  LEFT_BACKWARD),
        ("IN3 (Right Fwd)", RIGHT_FORWARD),
        ("IN4 (Right Bwd)", RIGHT_BACKWARD),
    ]

    for name, pin in motor_pins:
        print(f"Testing GPIO {pin:>2} — {name}...", end=" ", flush=True)
        dev = OutputDevice(pin)
        dev.on()
        time.sleep(0.3)
        dev.off()
        dev.close()
        print("OK")
        time.sleep(0.2)

    # Test ultrasonic sensor
    print(f"\nTesting ultrasonic (TRIG=GPIO{ULTRASONIC_TRIG}, ECHO=GPIO{ULTRASONIC_ECHO})...", end=" ", flush=True)
    try:
        sensor = DistanceSensor(echo=ULTRASONIC_ECHO, trigger=ULTRASONIC_TRIG, max_distance=4)
        readings = []
        for _ in range(3):
            readings.append(sensor.distance * 100)  # cm
            time.sleep(0.1)
        sensor.close()
        avg = sum(readings) / len(readings)
        print(f"OK — {avg:.1f} cm (avg of 3)")
    except Exception as e:
        print(f"FAIL — {e}")

    print("\n=== All pins tested ===")


def drive_mode():
    """Interactive keyboard control. WASD + Q to quit."""
    if not ON_PI:
        print("Drive mode requires Pi hardware. Exiting.")
        return

    import tty
    import termios

    robot = Robot(
        left=(LEFT_BACKWARD, LEFT_FORWARD),
        right=(RIGHT_BACKWARD, RIGHT_FORWARD),
    )
    sensor = DistanceSensor(echo=ULTRASONIC_ECHO, trigger=ULTRASONIC_TRIG, max_distance=4)

    speed = 1.0
    print("=== Drive Mode ===")
    print("  W = forward    S = backward")
    print("  A = left        D = right")
    print("  + = speed up   - = speed down")
    print("  SPACE = stop    Q = quit")
    print(f"  Speed: {speed}")

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1).lower()
            dist = sensor.distance * 100

            if ch == "q":
                break
            elif ch == "w":
                if dist < 30:
                    robot.stop()
                    sys.stdout.write(f"\r  BLOCKED — obstacle at {dist:.0f}cm     \r")
                else:
                    robot.forward(speed)
                    sys.stdout.write(f"\r  FWD {speed:.1f} | {dist:.0f}cm          \r")
            elif ch == "s":
                robot.backward(speed)
                sys.stdout.write(f"\r  BWD {speed:.1f} | {dist:.0f}cm          \r")
            elif ch == "a":
                robot.right(speed)
                sys.stdout.write(f"\r  LEFT {speed:.1f} | {dist:.0f}cm         \r")
            elif ch == "d":
                robot.left(speed)
                sys.stdout.write(f"\r  RIGHT {speed:.1f} | {dist:.0f}cm        \r")
            elif ch == " ":
                robot.stop()
                sys.stdout.write(f"\r  STOP | {dist:.0f}cm                \r")
            elif ch == "+":
                speed = min(1.0, speed + 0.1)
                sys.stdout.write(f"\r  Speed: {speed:.1f}                  \r")
            elif ch == "-":
                speed = max(0.1, speed - 0.1)
                sys.stdout.write(f"\r  Speed: {speed:.1f}                  \r")

            sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        robot.stop()
        robot.close()
        sensor.close()
        print("\nDrive mode ended.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Escort Bot GPIO Test & Drive")
    parser.add_argument("--drive", action="store_true", help="Interactive WASD drive mode")
    args = parser.parse_args()

    if args.drive:
        drive_mode()
    else:
        test_pins()
