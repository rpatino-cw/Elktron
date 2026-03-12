#!/usr/bin/env python3
"""
Elktron Escort Bot — Pan/Tilt Servo Control + Rack Scanning
Hackathon March 2026 | CoreWeave DCT

Controls pan/tilt servos via GPIO PWM to sweep the camera
vertically across a full 42U rack for scanning.
"""

import time
try:
    from gpiozero import AngularServo
except ImportError:
    AngularServo = None
    print("[pan_tilt] gpiozero not available — running in simulation mode")

# ─── CONFIG ────────────────────────────────────────────────────────
# GPIO pins (BCM) for the pan/tilt servos
PAN_PIN = 12    # Horizontal rotation
TILT_PIN = 13   # Vertical rotation (rack scanning)

# Servo angle limits (degrees)
PAN_MIN = -90
PAN_MAX = 90
TILT_MIN = -60   # Looking down (bottom of rack)
TILT_MAX = 60    # Looking up (top of rack)

# Scan settings
SCAN_STEP = 5          # Degrees per step during rack scan
SCAN_PAUSE = 0.8       # Seconds to pause at each step (for camera capture)
SCAN_SPEED_DELAY = 0.05  # Delay between servo movements for smooth motion


# ─── SERVO INIT ───────────────────────────────────────────────────

class PanTilt:
    """Controls pan/tilt servos for camera positioning and rack scanning."""

    def __init__(self, pan_pin=PAN_PIN, tilt_pin=TILT_PIN, simulate=False):
        self.simulate = simulate or AngularServo is None
        self.pan_angle = 0
        self.tilt_angle = 0

        if not self.simulate:
            self.pan_servo = AngularServo(
                pan_pin,
                min_angle=PAN_MIN,
                max_angle=PAN_MAX,
                min_pulse_width=0.0005,
                max_pulse_width=0.0025,
            )
            self.tilt_servo = AngularServo(
                tilt_pin,
                min_angle=TILT_MIN,
                max_angle=TILT_MAX,
                min_pulse_width=0.0005,
                max_pulse_width=0.0025,
            )
        else:
            self.pan_servo = None
            self.tilt_servo = None
            print("[pan_tilt] Simulation mode — no servos connected")

    def set_pan(self, angle):
        """Set horizontal angle. Clamped to PAN_MIN..PAN_MAX."""
        angle = max(PAN_MIN, min(PAN_MAX, angle))
        self.pan_angle = angle
        if not self.simulate:
            self.pan_servo.angle = angle
        else:
            print(f"  [SIM] pan → {angle}°")

    def set_tilt(self, angle):
        """Set vertical angle. Clamped to TILT_MIN..TILT_MAX."""
        angle = max(TILT_MIN, min(TILT_MAX, angle))
        self.tilt_angle = angle
        if not self.simulate:
            self.tilt_servo.angle = angle
        else:
            print(f"  [SIM] tilt → {angle}°")

    def center(self):
        """Reset both servos to center (0, 0)."""
        self.set_pan(0)
        self.set_tilt(0)

    def look_at(self, pan, tilt):
        """Move both servos to specified angles."""
        self.set_pan(pan)
        self.set_tilt(tilt)

    # ─── RACK SCANNING ────────────────────────────────────────────

    def scan_rack(self, on_position=None):
        """
        Sweep camera from bottom of rack to top, pausing at each step.

        Args:
            on_position: Optional callback(tilt_angle) called at each step.
                         Use this to capture a frame at each position.

        Returns:
            List of tilt angles where the scan paused.
        """
        print("[SCAN] Starting rack scan — bottom to top")
        positions = []

        # Center pan (face the rack straight on)
        self.set_pan(0)
        time.sleep(0.3)

        # Sweep tilt from bottom (TILT_MIN) to top (TILT_MAX)
        angle = TILT_MIN
        while angle <= TILT_MAX:
            self.set_tilt(angle)
            time.sleep(SCAN_SPEED_DELAY)

            positions.append(angle)
            print(f"[SCAN] tilt={angle}°")

            if on_position:
                on_position(angle)

            time.sleep(SCAN_PAUSE)
            angle += SCAN_STEP

        # Return to center after scan
        self.center()
        print(f"[SCAN] Complete — {len(positions)} positions captured")
        return positions

    def scan_rack_bounce(self, on_position=None):
        """
        Sweep bottom→top then top→bottom (round trip).
        Useful for a second pass or continuous monitoring.
        """
        print("[SCAN] Starting bounce scan")
        positions = []

        self.set_pan(0)
        time.sleep(0.3)

        # Bottom to top
        angle = TILT_MIN
        while angle <= TILT_MAX:
            self.set_tilt(angle)
            time.sleep(SCAN_SPEED_DELAY)
            positions.append(angle)
            if on_position:
                on_position(angle)
            time.sleep(SCAN_PAUSE)
            angle += SCAN_STEP

        # Top to bottom
        angle = TILT_MAX
        while angle >= TILT_MIN:
            self.set_tilt(angle)
            time.sleep(SCAN_SPEED_DELAY)
            positions.append(angle)
            if on_position:
                on_position(angle)
            time.sleep(SCAN_PAUSE)
            angle -= SCAN_STEP

        self.center()
        print(f"[SCAN] Bounce complete — {len(positions)} positions captured")
        return positions

    def cleanup(self):
        """Release servo resources."""
        if not self.simulate:
            self.pan_servo.close()
            self.tilt_servo.close()
        print("[pan_tilt] Cleaned up")


# ─── STANDALONE TEST ──────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test pan/tilt servos")
    parser.add_argument("--simulate", action="store_true", help="Run without hardware")
    parser.add_argument("--scan", action="store_true", help="Run a full rack scan")
    parser.add_argument("--bounce", action="store_true", help="Run a bounce scan")
    args = parser.parse_args()

    pt = PanTilt(simulate=args.simulate)

    try:
        if args.scan:
            pt.scan_rack()
        elif args.bounce:
            pt.scan_rack_bounce()
        else:
            # Manual test: sweep through positions
            print("[TEST] Center")
            pt.center()
            time.sleep(1)

            print("[TEST] Look down (bottom of rack)")
            pt.look_at(0, TILT_MIN)
            time.sleep(1)

            print("[TEST] Look up (top of rack)")
            pt.look_at(0, TILT_MAX)
            time.sleep(1)

            print("[TEST] Pan left")
            pt.look_at(PAN_MIN, 0)
            time.sleep(1)

            print("[TEST] Pan right")
            pt.look_at(PAN_MAX, 0)
            time.sleep(1)

            print("[TEST] Back to center")
            pt.center()
            time.sleep(0.5)

            print("[TEST] Done")
    except KeyboardInterrupt:
        print("\nInterrupted")
    finally:
        pt.cleanup()
