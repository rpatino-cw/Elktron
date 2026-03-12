#!/usr/bin/env python3
"""
Elktron Escort Bot — Person-Following Robot + Rack Scanner
Hackathon March 2026 | CoreWeave DCT

Pi 5 + LK-COKOINO 4WD + TFLite MobileNet SSD v2 + Arducam 120° Wide
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
from datetime import datetime
from picamera2 import Picamera2
from gpiozero import Robot, DistanceSensor
from tflite_runtime.interpreter import Interpreter
from pan_tilt import PanTilt

# ─── CONFIG ────────────────────────────────────────────────────────
MODEL_PATH = "models/ssd_mobilenet_v2.tflite"
LABELS_PATH = "models/coco_labels.txt"
PERSON_CLASS_ID = 0          # COCO class 0 = person
CONFIDENCE_THRESHOLD = 0.5   # Min detection confidence
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
INPUT_SIZE = (300, 300)      # MobileNet SSD input size

# Motor GPIO pins (BCM) — adjust to LK-COKOINO / L298N wiring
LEFT_MOTOR = (17, 27)       # (forward, backward)
RIGHT_MOTOR = (22, 23)      # (forward, backward)

# Ultrasonic sensor pins (BCM)
ULTRASONIC_ECHO = 24
ULTRASONIC_TRIG = 25

# Steering
KP = 1.0                    # Proportional gain — tune on the floor
BASE_SPEED = 0.5            # 0.0–1.0
STOP_DISTANCE = 0.30        # meters — stop if obstacle closer than this
TARGET_AREA_RATIO = 0.15    # target bbox area / frame area (how close to follow)
AREA_TOLERANCE = 0.05       # dead zone around target area
LOST_TIMEOUT = 1.5          # seconds with no detection before stopping

# Scan mode
SCAN_TRIGGER_DISTANCE = 0.50  # meters — if person stops near rack, trigger scan
SCAN_IDLE_TIME = 3.0          # seconds person must be stationary to trigger scan
SCAN_OUTPUT_DIR = "scans"     # where captured frames are saved

# Bot modes
MODE_FOLLOW = "FOLLOW"
MODE_SCAN = "SCAN"
MODE_IDLE = "IDLE"

# ─── SETUP ─────────────────────────────────────────────────────────

def load_labels(path):
    """Load COCO label map."""
    with open(path, "r") as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}


def init_camera():
    """Initialize Pi Camera with picamera2."""
    cam = Picamera2()
    config = cam.create_preview_configuration(
        main={"size": (FRAME_WIDTH, FRAME_HEIGHT), "format": "RGB888"}
    )
    cam.configure(config)
    cam.start()
    time.sleep(1)  # warm-up
    return cam


def init_tflite(model_path):
    """Load TFLite model and allocate tensors."""
    interpreter = Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return interpreter, input_details, output_details


def init_robot():
    """Initialize motors and ultrasonic sensor."""
    robot = Robot(left=LEFT_MOTOR, right=RIGHT_MOTOR)
    sonar = DistanceSensor(echo=ULTRASONIC_ECHO, trigger=ULTRASONIC_TRIG)
    return robot, sonar


# ─── DETECTION ─────────────────────────────────────────────────────

def detect_person(frame, interpreter, input_details, output_details):
    """
    Run TFLite inference on a frame.
    Returns the largest person bounding box as (x, y, w, h) in pixels,
    or None if no person detected.
    """
    img = np.resize(frame, (1, INPUT_SIZE[0], INPUT_SIZE[1], 3)).astype(np.uint8)
    interpreter.set_tensor(input_details[0]["index"], img)
    interpreter.invoke()

    boxes = interpreter.get_tensor(output_details[0]["index"])[0]
    classes = interpreter.get_tensor(output_details[1]["index"])[0]
    scores = interpreter.get_tensor(output_details[2]["index"])[0]

    best_box = None
    best_area = 0

    for i in range(len(scores)):
        if int(classes[i]) == PERSON_CLASS_ID and scores[i] >= CONFIDENCE_THRESHOLD:
            ymin, xmin, ymax, xmax = boxes[i]
            x = int(xmin * FRAME_WIDTH)
            y = int(ymin * FRAME_HEIGHT)
            w = int((xmax - xmin) * FRAME_WIDTH)
            h = int((ymax - ymin) * FRAME_HEIGHT)
            area = w * h
            if area > best_area:
                best_area = area
                best_box = (x, y, w, h)

    return best_box


# ─── STEERING ──────────────────────────────────────────────────────

def compute_steering(bbox):
    """
    Given a person bounding box (x, y, w, h), compute left/right motor speeds.
    Returns (left_speed, right_speed) each in range [-1, 1].
    """
    x, y, w, h = bbox
    person_center_x = x + w / 2
    frame_center_x = FRAME_WIDTH / 2

    error = (person_center_x - frame_center_x) / FRAME_WIDTH

    area_ratio = (w * h) / (FRAME_WIDTH * FRAME_HEIGHT)
    if area_ratio > TARGET_AREA_RATIO + AREA_TOLERANCE:
        speed = 0.0
    elif area_ratio < TARGET_AREA_RATIO - AREA_TOLERANCE:
        speed = BASE_SPEED
    else:
        speed = BASE_SPEED * 0.3

    left_speed = max(-1.0, min(1.0, speed + (error * KP)))
    right_speed = max(-1.0, min(1.0, speed - (error * KP)))

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
        frame = camera.capture_array()
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
    interpreter, input_det, output_det = init_tflite(MODEL_PATH)
    robot, sonar = init_robot()
    pan_tilt = PanTilt(simulate=args.simulate)
    os.makedirs(SCAN_OUTPUT_DIR, exist_ok=True)

    # Scan-only mode for testing
    if args.scan_only:
        scan_id = datetime.now().strftime("scan_%Y%m%d_%H%M%S")
        run_scan(camera, pan_tilt, scan_id)
        pan_tilt.cleanup()
        camera.stop()
        return

    # State tracking
    mode = MODE_IDLE
    last_seen = time.time()
    prev_bbox = None
    stationary_since = None
    scan_count = 0

    # Center camera for follow mode
    pan_tilt.center()

    print("[Elktron] Ready. Modes: FOLLOW → SCAN → FOLLOW")
    print(f"  Scan triggers when person is stationary for {SCAN_IDLE_TIME}s")

    try:
        while True:
            frame = camera.capture_array()

            # ── Obstacle override (all modes) ──
            if sonar.distance < STOP_DISTANCE:
                robot.stop()
                print(f"[STOP] Obstacle at {sonar.distance:.2f}m")
                time.sleep(0.1)
                continue

            # ── Detect person ──
            bbox = detect_person(frame, interpreter, input_det, output_det)

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
                        stationary_since = None
                        print(f"[MODE] SCAN → FOLLOW\n")
                        continue
                else:
                    stationary_since = None

                # Normal follow mode
                mode = MODE_FOLLOW
                left, right = compute_steering(bbox)
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
                else:
                    print(f"[SEARCH] Lost person, waiting {LOST_TIMEOUT - elapsed:.1f}s...")

            time.sleep(0.05)  # ~20 FPS cap

    except KeyboardInterrupt:
        print("\n[Elktron] Shutting down.")
    finally:
        robot.stop()
        pan_tilt.cleanup()
        camera.stop()
        print(f"[Elktron] {scan_count} rack scans completed this session.")


if __name__ == "__main__":
    main()
