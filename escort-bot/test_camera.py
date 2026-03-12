#!/usr/bin/env python3
"""
Elktron Escort Bot — Camera-Only Detection Test
Run on Pi 5 with just a camera (no motors, no ultrasonic).
Validates the person detection pipeline before hardware arrives.

Usage:
  python3 test_camera.py              # headless — prints detections to terminal
  python3 test_camera.py --display    # shows live video with bounding boxes (needs display)

Requirements:
  pip install --break-system-packages tflite-runtime numpy
  (picamera2 is pre-installed on Pi OS Bookworm)
  Run install.sh first to download the TFLite model.
"""

import sys
import time
import argparse
import numpy as np
from picamera2 import Picamera2
from tflite_runtime.interpreter import Interpreter

# ─── CONFIG ────────────────────────────────────────────────────────
MODEL_PATH = "models/ssd_mobilenet_v2.tflite"
LABELS_PATH = "models/coco_labels.txt"
PERSON_CLASS_ID = 0
CONFIDENCE_THRESHOLD = 0.5
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
INPUT_SIZE = (300, 300)

# Steering params (simulated — no motors)
KP = 1.0
BASE_SPEED = 0.5
TARGET_AREA_RATIO = 0.15
AREA_TOLERANCE = 0.05


# ─── SETUP ─────────────────────────────────────────────────────────

def load_labels(path):
    with open(path, "r") as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}


def init_camera():
    cam = Picamera2()
    config = cam.create_preview_configuration(
        main={"size": (FRAME_WIDTH, FRAME_HEIGHT), "format": "RGB888"}
    )
    cam.configure(config)
    cam.start()
    time.sleep(1)
    return cam


def init_tflite(model_path):
    interpreter = Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return interpreter, input_details, output_details


# ─── DETECTION ─────────────────────────────────────────────────────

def detect_person(frame, interpreter, input_details, output_details):
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


def compute_steering_sim(bbox):
    """Simulate steering output without motors."""
    x, y, w, h = bbox
    center_x = x + w / 2
    frame_center = FRAME_WIDTH / 2
    error = (center_x - frame_center) / FRAME_WIDTH

    area_ratio = (w * h) / (FRAME_WIDTH * FRAME_HEIGHT)
    if area_ratio > TARGET_AREA_RATIO + AREA_TOLERANCE:
        speed = 0.0
        action = "TOO CLOSE — would stop"
    elif area_ratio < TARGET_AREA_RATIO - AREA_TOLERANCE:
        speed = BASE_SPEED
        action = "FOLLOWING"
    else:
        speed = BASE_SPEED * 0.3
        action = "CREEPING"

    left = max(-1.0, min(1.0, speed + error * KP))
    right = max(-1.0, min(1.0, speed - error * KP))

    return left, right, action, area_ratio


# ─── MAIN ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Escort Bot — Camera-only detection test")
    parser.add_argument("--display", action="store_true", help="Show live video with bounding boxes")
    parser.add_argument("--fps", action="store_true", help="Show FPS counter")
    args = parser.parse_args()

    cv2 = None
    if args.display:
        try:
            import cv2 as _cv2
            cv2 = _cv2
        except ImportError:
            print("[WARN] opencv-python not installed. Run: pip install --break-system-packages opencv-python")
            print("[WARN] Falling back to headless mode.")

    print("[Elktron] Camera-only detection test")
    print(f"[Elktron] Model: {MODEL_PATH}")
    print(f"[Elktron] Confidence threshold: {CONFIDENCE_THRESHOLD}")
    print(f"[Elktron] Display mode: {'ON' if cv2 else 'OFF'}")
    print()

    camera = init_camera()
    interpreter, input_det, output_det = init_tflite(MODEL_PATH)

    print("[Elktron] Ready. Point camera at a person.")
    print("[Elktron] Press Ctrl+C to stop.\n")

    frame_count = 0
    fps_start = time.time()
    last_seen = time.time()
    detections = 0

    try:
        while True:
            frame = camera.capture_array()
            bbox = detect_person(frame, interpreter, input_det, output_det)

            frame_count += 1
            elapsed = time.time() - fps_start
            fps = frame_count / elapsed if elapsed > 0 else 0

            if bbox is not None:
                last_seen = time.time()
                detections += 1
                x, y, w, h = bbox
                left, right, action, area = compute_steering_sim(bbox)
                fps_str = f" | {fps:.1f} FPS" if args.fps else ""
                print(f"[DETECT] person@({x},{y}) {w}x{h} area={area:.3f} → L={left:.2f} R={right:.2f} {action}{fps_str}")

                if cv2 is not None:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, f"{action} L={left:.2f} R={right:.2f}",
                                (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            else:
                gap = time.time() - last_seen
                if gap > 2.0 and frame_count % 20 == 0:
                    print(f"[WAIT] No person for {gap:.1f}s...")

            if cv2 is not None:
                cv2.imshow("Elktron Escort Bot — Detection Test", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            time.sleep(0.05)

    except KeyboardInterrupt:
        pass
    finally:
        camera.stop()
        if cv2 is not None:
            cv2.destroyAllWindows()

        total_time = time.time() - fps_start
        print(f"\n[Elktron] Test complete.")
        print(f"  Frames: {frame_count}")
        print(f"  Detections: {detections}")
        print(f"  Avg FPS: {frame_count / total_time:.1f}")
        print(f"  Detection rate: {detections / frame_count * 100:.1f}%" if frame_count > 0 else "")


if __name__ == "__main__":
    main()
