"""
RC Drive — Pi 5 Motor Control from ESP-NOW Receiver
=====================================================
Reads serial commands from ESP32-CAM receiver on UART (/dev/ttyAMA0)
and drives 4WD motors via L298N.

Serial format from ESP32: "forward,turn,turbo,estop\n"
  forward: -1 (back), 0 (stop), 1 (forward)
  turn:    -1 (left), 0 (straight), 1 (right)
  turbo:   0 (normal), 1 (fast)
  estop:   0 (normal), 1 (emergency stop)

WIRING:
  ESP32-CAM GPIO 1 (TX) → Pi 5 GPIO 15 (RXD)
  ESP32-CAM GND         → Pi 5 GND

  L298N:
    ENA (left speed)  → Pi GPIO 12 (PWM0)
    ENB (right speed) → Pi GPIO 13 (PWM1)
    IN1 (left fwd)    → Pi GPIO 18
    IN2 (left back)   → Pi GPIO 19
    IN3 (right fwd)   → Pi GPIO 20
    IN4 (right back)  → Pi GPIO 21

USAGE:
  python3 rc_drive.py              # normal mode
  python3 rc_drive.py --test       # test motors without ESP32
  python3 rc_drive.py --port /dev/ttyUSB0  # custom serial port
"""

import serial
import time
import sys
import signal
import argparse

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("[WARN] RPi.GPIO not available — running in dry-run mode")
    GPIO = None

# Motor pins (L298N)
ENA = 12   # left motor speed (PWM)
ENB = 13   # right motor speed (PWM)
IN1 = 18   # left forward
IN2 = 19   # left backward
IN3 = 20   # right forward
IN4 = 21   # right backward

# Speed settings (PWM duty cycle 0-100)
SPEED_NORMAL = 60
SPEED_TURBO = 90
SPEED_TURN = 40   # inner wheel speed during turns

# Serial config
DEFAULT_PORT = "/dev/ttyAMA0"
BAUD = 115200

# Globals
pwm_left = None
pwm_right = None
running = True


def setup_gpio():
    global pwm_left, pwm_right
    if GPIO is None:
        return

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for pin in [ENA, ENB, IN1, IN2, IN3, IN4]:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    pwm_left = GPIO.PWM(ENA, 1000)   # 1kHz PWM
    pwm_right = GPIO.PWM(ENB, 1000)
    pwm_left.start(0)
    pwm_right.start(0)


def stop_motors():
    """Kill all motor output."""
    if GPIO is None:
        print("[DRY] STOP")
        return
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_left.ChangeDutyCycle(0)
    pwm_right.ChangeDutyCycle(0)


def drive(forward, turn, turbo):
    """
    Set motor direction and speed.
    forward: -1/0/1, turn: -1/0/1, turbo: 0/1
    """
    speed = SPEED_TURBO if turbo else SPEED_NORMAL

    if GPIO is None:
        print(f"[DRY] fwd={forward} turn={turn} turbo={turbo} speed={speed}")
        return

    # Direction
    if forward == 1:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
    elif forward == -1:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
    else:
        # No forward/back — if turning, do pivot turn (spin in place)
        if turn == -1:
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)
            GPIO.output(IN3, GPIO.HIGH)
            GPIO.output(IN4, GPIO.LOW)
        elif turn == 1:
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.HIGH)
        else:
            stop_motors()
            return

    # Speed — differential for turns while moving
    if turn == 0:
        pwm_left.ChangeDutyCycle(speed)
        pwm_right.ChangeDutyCycle(speed)
    elif turn == -1:
        # Left turn: slow left, full right
        pwm_left.ChangeDutyCycle(SPEED_TURN)
        pwm_right.ChangeDutyCycle(speed)
    elif turn == 1:
        # Right turn: full left, slow right
        pwm_left.ChangeDutyCycle(speed)
        pwm_right.ChangeDutyCycle(SPEED_TURN)


def parse_command(line):
    """Parse CSV line: 'forward,turn,turbo,estop' → tuple or None."""
    line = line.strip()
    if not line or line.startswith('#') or line.startswith('ESP-NOW'):
        return None
    try:
        parts = line.split(',')
        if len(parts) != 4:
            return None
        return (int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))
    except (ValueError, IndexError):
        return None


def run_serial(port):
    """Main loop — read serial from ESP32, drive motors."""
    global running

    print(f"[RC] Opening {port} at {BAUD} baud...")
    try:
        ser = serial.Serial(port, BAUD, timeout=0.1)
    except serial.SerialException as e:
        print(f"[RC] Serial error: {e}")
        print(f"[RC] Make sure UART is enabled: sudo raspi-config → Interface Options → Serial Port")
        print(f"[RC] Disable serial console: 'console=serial0,115200' should NOT be in /boot/cmdline.txt")
        return

    ser.reset_input_buffer()
    print("[RC] Listening for ESP-NOW commands...")

    last_cmd_time = time.time()
    timeout = 1.0  # seconds without command = stop

    while running:
        try:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='ignore')
                cmd = parse_command(line)
                if cmd:
                    fwd, turn, turbo, estop = cmd
                    last_cmd_time = time.time()
                    if estop:
                        stop_motors()
                        print("[RC] ESTOP")
                    else:
                        drive(fwd, turn, turbo)

            # Safety timeout
            if time.time() - last_cmd_time > timeout:
                stop_motors()

            time.sleep(0.01)  # prevent CPU spin

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[RC] Error: {e}")
            stop_motors()
            time.sleep(0.5)

    ser.close()


def run_test():
    """Test motors without ESP32 — runs each direction for 1 second."""
    print("[TEST] Motor test sequence — each direction for 1s")
    tests = [
        ("Forward",       1,  0, 0),
        ("Backward",     -1,  0, 0),
        ("Left pivot",    0, -1, 0),
        ("Right pivot",   0,  1, 0),
        ("Forward+Left",  1, -1, 0),
        ("Forward+Right", 1,  1, 0),
        ("Turbo forward", 1,  0, 1),
    ]
    for name, fwd, turn, turbo in tests:
        print(f"  {name}...")
        drive(fwd, turn, turbo)
        time.sleep(1)
        stop_motors()
        time.sleep(0.3)
    print("[TEST] Done")


def cleanup(*_):
    global running
    running = False
    stop_motors()
    if GPIO:
        GPIO.cleanup()
    print("\n[RC] Shutdown")
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RC Drive — ESP-NOW to motor control")
    parser.add_argument("--port", default=DEFAULT_PORT, help="Serial port")
    parser.add_argument("--test", action="store_true", help="Test motors without ESP32")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    setup_gpio()

    if args.test:
        run_test()
        cleanup()
    else:
        run_serial(args.port)
        cleanup()
