#!/usr/bin/env python3
"""
Elktron Escort Bot — Person-Following Robot + Rack Scanner
Hackathon March 2026 | CoreWeave DCT

Pi 5 + LK-COKOINO 4WD + YOLO11n (ultralytics) + Arducam IMX708 Wide
Follows a vendor on the DC floor, stops at racks to scan top-to-bottom.

Modes:
  FOLLOW  — track and follow a person (vendor escort)
  SCAN    — stopped at a rack, sweep camera bottom→top capturing frames
  IDLE    — no person detected, waiting
"""

import os
import time
import argparse
import numpy as np
import cv2
from datetime import datetime
from gpiozero import Robot, DistanceSensor
from pan_tilt import PanTilt
from pid import PIDController

# ─── CONFIG ────────────────────────────────────────────────────────
MODEL_NAME = "yolo11n.pt"    # smallest ultralytics model — auto-downloads on first run
INFER_SIZE = 320             # input resolution — half of 640 = 4× faster, enough for follow
CONFIDENCE_THRESHOLD = 0.5   # Min detection confidence
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Motor GPIO pins (BCM) — single L298N drives all 4 motors as 2 parallel pairs
# Channel A (OUT1/OUT2): FL+RL in parallel — left pair
# Channel B (OUT3/OUT4): FR+RR in parallel — right pair
LEFT_MOTOR = (17, 24)       # IN1/IN2 (forward, backward)
RIGHT_MOTOR = (22, 23)      # IN3/IN4 (forward, backward)

# Ultrasonic sensor pins (BCM)
ULTRASONIC_ECHO = 26
ULTRASONIC_TRIG = 25

# Steering
BASE_SPEED = 0.5            # 0.0–1.0
STOP_DISTANCE = 0.30        # meters — stop if obstacle closer than this
TARGET_AREA_RATIO = 0.15    # target bbox area / frame area (how close to follow)
LOST_TIMEOUT = 1.5          # seconds with no detection before stopping

# PID — Lateral (steering: keeps person centered in frame)
KP_LATERAL = 1.0            # Proportional — immediate turn response
KI_LATERAL = 0.1            # Integral — eliminates steady drift
KD_LATERAL = 0.3            # Derivative — dampens oscillation
MAX_INTEGRAL_LATERAL = 0.5  # Anti-windup clamp

# PID — Distance (speed: keeps person at target follow distance)
KP_DISTANCE = 1.2           # Proportional — speed up/slow down
KI_DISTANCE = 0.05          # Integral — eliminates steady-state gap
KD_DISTANCE = 0.2           # Derivative — smooth braking
MAX_INTEGRAL_DISTANCE = 0.3 # Anti-windup clamp

# Feed-forward
KFF = 0.15                  # Feed-forward gain — predict target motion

# Scan mode
SCAN_TRIGGER_DISTANCE = 0.50  # meters — if person stops near rack, trigger scan
SCAN_IDLE_TIME = 3.0          # seconds person must be stationary to trigger scan
SCAN_OUTPUT_DIR = "scans"     # where captured frames are saved

# Bot modes
MODE_FOLLOW = "FOLLOW"
MODE_SCAN = "SCAN"
MODE_IDLE = "IDLE"

# ─── SETUP ─────────────────────────────────────────────────────────

STREAM_URL = "http://localhost:8888/video_feed"

def init_camera():
    """Connect to the dashboard MJPEG stream instead of opening picamera2 directly.
    This lets the dashboard server and main.py share the camera without conflict."""
    cap = cv2.VideoCapture(STREAM_URL)
    if not cap.isOpened():
        raise RuntimeError(
            f"Cannot connect to camera stream at {STREAM_URL}\n"
            "Make sure the dashboard server is running: sudo systemctl start elktron"
        )
    print(f"[Camera] Connected to MJPEG stream at {STREAM_URL}")
    return cap


def init_detector():
    """Load YOLO11n — auto-downloads ~5MB on first run."""
    from ultralytics import YOLO
    model = YOLO(MODEL_NAME)
    # Warm-up pass so first real frame isn't slow
    dummy = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
    model(dummy, imgsz=INFER_SIZE, classes=[0], verbose=False)
    print(f"[Detector] YOLO11n ready (imgsz={INFER_SIZE}, person-only)")
    return model


def init_robot():
    """Initialize motors and ultrasonic sensor."""
    robot = Robot(left=LEFT_MOTOR, right=RIGHT_MOTOR)
    sonar = DistanceSensor(echo=ULTRASONIC_ECHO, trigger=ULTRASONIC_TRIG)
    return robot, sonar


# ─── DETECTION ─────────────────────────────────────────────────────

def detect_person(frame, model):
    """
    Run YOLO11n inference on a frame.
    Returns the largest person bounding box as (x, y, w, h) in pixels,
    or None if no person detected above CONFIDENCE_THRESHOLD.
    """
    results = model(frame, imgsz=INFER_SIZE, classes=[0],
                    conf=CONFIDENCE_THRESHOLD, verbose=False)

    best_box = None
    best_area = 0

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        w, h = x2 - x1, y2 - y1
        area = w * h
        if area > best_area:
            best_area = area
            best_box = (x1, y1, w, h)

    return best_box


# ─── STEERING ──────────────────────────────────────────────────────

def compute_steering(bbox, lateral_pid, distance_pid, dt, prev_bbox=None):
    """
    PID-based steering with feed-forward.

    Two PID loops:
      1. Lateral — error = how far person is from frame center (steering)
      2. Distance — error = target area ratio - actual area ratio (speed)

    Feed-forward: uses frame-to-frame bbox center delta to predict
    where the person is heading, reducing tracking lag.

    Returns (left_speed, right_speed) each in range [-1, 1].
    """
    x, y, w, h = bbox
    person_center_x = x + w / 2
    frame_center_x = FRAME_WIDTH / 2

    # ── Lateral PID (steering) ──
    lateral_error = (person_center_x - frame_center_x) / FRAME_WIDTH
    steering = lateral_pid.update(lateral_error, dt)

    # ── Distance PID (speed) ──
    area_ratio = (w * h) / (FRAME_WIDTH * FRAME_HEIGHT)
    distance_error = TARGET_AREA_RATIO - area_ratio  # positive = too far, go forward
    speed = distance_pid.update(distance_error, dt)

    # Clamp speed to [0, BASE_SPEED] — no reversing toward person
    speed = max(0.0, min(BASE_SPEED, speed))

    # ── Feed-forward (predict target motion) ──
    ff = 0.0
    if prev_bbox is not None:
        px, py, pw, ph = prev_bbox
        prev_center_x = px + pw / 2
        delta_x = (person_center_x - prev_center_x) / FRAME_WIDTH
        ff = KFF * delta_x  # positive = person moving right

    # ── Combine into differential drive ──
    turn = steering + ff
    left_speed = max(-1.0, min(1.0, speed + turn))
    right_speed = max(-1.0, min(1.0, speed - turn))

    return left_speed, right_speed


def drive(robot, left_speed, right_speed):
    """Send speed commands to motors."""
    robot.value = (left_speed, right_speed)


# ─── SCAN MODE ─────────────────────────────────────────────────────

def run_scan(camera, pan_tilt, scan_id):
    """
    Execute a full rack scan: sweep camera bottom→top, capture a frame
    at each tilt position, save to disk.

    Returns list of saved file paths.
    """
    scan_dir = os.path.join(SCAN_OUTPUT_DIR, scan_id)
    os.makedirs(scan_dir, exist_ok=True)
    saved_files = []

    def capture_at_position(tilt_angle):
        """Callback: grab a frame and save it."""
        time.sleep(0.2)  # let servo settle
        ret, frame = camera.read()
        if not ret:
            print(f"  [WARN] Frame grab failed at {tilt_angle}°, skipping")
            return
        filename = f"rack_{tilt_angle:+04d}deg.jpg"
        filepath = os.path.join(scan_dir, filename)

        # Save as JPEG using picamera2's built-in helper
        try:
            from PIL import Image
            img = Image.fromarray(frame)
            img.save(filepath, quality=90)
            saved_files.append(filepath)
            print(f"  [CAPTURE] {filepath}")
        except ImportError:
            # Fallback: save raw numpy
            np.save(filepath.replace(".jpg", ".npy"), frame)
            saved_files.append(filepath.replace(".jpg", ".npy"))
            print(f"  [CAPTURE] {filepath} (numpy fallback — install Pillow for JPEG)")

    print(f"[SCAN] Starting rack scan — ID: {scan_id}")
    pan_tilt.scan_rack(on_position=capture_at_position)
    print(f"[SCAN] Done — {len(saved_files)} frames saved to {scan_dir}/")

    return saved_files


def person_is_stationary(bbox, prev_bbox, threshold=20):
    """Check if person bbox center hasn't moved much between frames."""
    if prev_bbox is None:
        return False
    cx = bbox[0] + bbox[2] / 2
    cy = bbox[1] + bbox[3] / 2
    pcx = prev_bbox[0] + prev_bbox[2] / 2
    pcy = prev_bbox[1] + prev_bbox[3] / 2
    return abs(cx - pcx) < threshold and abs(cy - pcy) < threshold


# ─── MAIN LOOP ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Elktron Escort Bot")
    parser.add_argument("--simulate", action="store_true", help="Simulate servos (no hardware)")
    parser.add_argument("--scan-only", action="store_true", help="Run one rack scan and exit")
    args = parser.parse_args()

    print("[Elktron] Initializing escort bot...")
    camera = init_camera()
    net = init_detector()
    robot, sonar = init_robot()
    pan_tilt = PanTilt(simulate=args.simulate)
    os.makedirs(SCAN_OUTPUT_DIR, exist_ok=True)

    # PID controllers
    lateral_pid = PIDController(
        kp=KP_LATERAL, ki=KI_LATERAL, kd=KD_LATERAL,
        max_integral=MAX_INTEGRAL_LATERAL, max_output=1.0
    )
    distance_pid = PIDController(
        kp=KP_DISTANCE, ki=KI_DISTANCE, kd=KD_DISTANCE,
        max_integral=MAX_INTEGRAL_DISTANCE, max_output=BASE_SPEED
    )

    # Scan-only mode for testing
    if args.scan_only:
        scan_id = datetime.now().strftime("scan_%Y%m%d_%H%M%S")
        run_scan(camera, pan_tilt, scan_id)
        pan_tilt.cleanup()
        camera.release()
        return

    # State tracking
    mode = MODE_IDLE
    last_seen = time.time()
    prev_bbox = None
    stationary_since = None
    scan_count = 0
    last_time = time.time()

    # Center camera for follow mode
    pan_tilt.center()

    print("[Elktron] Ready. Modes: FOLLOW → SCAN → FOLLOW")
    print(f"  Scan triggers when person is stationary for {SCAN_IDLE_TIME}s")

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("[WARN] Stream frame drop, retrying...")
                time.sleep(0.05)
                continue
            now = time.time()
            dt = now - last_time
            last_time = now

            # ── Obstacle override (all modes) ──
            if sonar.distance < STOP_DISTANCE:
                robot.stop()
                print(f"[STOP] Obstacle at {sonar.distance:.2f}m")
                time.sleep(0.1)
                continue

            # ── Detect person ──
            bbox = detect_person(frame, net)

            if bbox is not None:
                last_seen = time.time()

                # Check if person is stationary (potential scan trigger)
                if person_is_stationary(bbox, prev_bbox):
                    if stationary_since is None:
                        stationary_since = time.time()
                    idle_duration = time.time() - stationary_since

                    # Person has been still long enough — trigger scan
                    if idle_duration >= SCAN_IDLE_TIME and mode != MODE_SCAN:
                        robot.stop()
                        mode = MODE_SCAN
                        scan_count += 1
                        scan_id = datetime.now().strftime(f"scan_%Y%m%d_%H%M%S_{scan_count:03d}")
                        print(f"\n[MODE] FOLLOW → SCAN (person stationary {idle_duration:.1f}s)")

                        run_scan(camera, pan_tilt, scan_id)

                        # Return camera to center for follow mode
                        pan_tilt.center()
                        mode = MODE_FOLLOW
                        lateral_pid.reset()
                        distance_pid.reset()
                        stationary_since = None
                        print(f"[MODE] SCAN → FOLLOW\n")
                        continue
                else:
                    stationary_since = None

                # Normal follow mode
                mode = MODE_FOLLOW
                left, right = compute_steering(bbox, lateral_pid, distance_pid, dt, prev_bbox)
                drive(robot, left, right)
                x, y, w, h = bbox
                print(f"[FOLLOW] person@({x},{y}) size={w}x{h} → L={left:.2f} R={right:.2f}")

                prev_bbox = bbox

            else:
                # No person detected
                prev_bbox = None
                stationary_since = None
                elapsed = time.time() - last_seen

                if elapsed > LOST_TIMEOUT:
                    robot.stop()
                    if mode != MODE_IDLE:
                        print(f"[MODE] {mode} → IDLE")
                        mode = MODE_IDLE
                        lateral_pid.reset()
                        distance_pid.reset()
                else:
                    print(f"[SEARCH] Lost person, waiting {LOST_TIMEOUT - elapsed:.1f}s...")

            time.sleep(0.05)  # ~20 FPS cap

    except KeyboardInterrupt:
        print("\n[Elktron] Shutting down.")
    finally:
        robot.stop()
        pan_tilt.cleanup()
        camera.release()
        print(f"[Elktron] {scan_count} rack scans completed this session.")


if __name__ == "__main__":
    main()
