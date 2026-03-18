#!/usr/bin/env python3
"""
Elktron Escort Bot — Pi 5 API Server
Streams camera with YOLOv8n detection overlay + exposes bot state for dashboard.

Run:  python3 api_server.py
Test: curl http://localhost:5000/health
Feed: open http://localhost:5000/video_feed in browser
"""

import time
import threading
import logging
from datetime import datetime

import cv2
import numpy as np
from flask import Flask, Response, jsonify, request

# ─── CONFIG ────────────────────────────────────────────────────────
HOST = "0.0.0.0"
PORT = 5000
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
JPEG_QUALITY = 70
CONFIDENCE_THRESHOLD = 0.5

# GPIO pins (BCM) — ultrasonic only, motors controlled by main.py
ULTRASONIC_ECHO = 24
ULTRASONIC_TRIG = 25

# ─── APP ───────────────────────────────────────────────────────────
app = Flask(__name__)
log = logging.getLogger("elktron.api")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

start_time = time.time()

# ─── SHARED STATE ──────────────────────────────────────────────────
# Thread-safe: GIL protects dict reference swaps. main.py can import
# and update bot_state when running alongside this server.

bot_state = {
    "phase": "idle",
    "location": "charging_bay",
    "vendor": None,
    "target_rack": None,
    "authorized_ru": None,
    "scan_progress": 0,
    "alert": None,
    "battery_pct": 100,
    "nodes_scanned": 0,
    # Extra telemetry (dashboard ignores unknown fields)
    "detection": {
        "person_detected": False,
        "confidence": 0.0,
        "bbox": None,
    },
    "distance_cm": None,
    "fps": 0.0,
}

# ─── FRAME BUFFER ──────────────────────────────────────────────────
frame_lock = threading.Lock()
latest_frame = None  # JPEG bytes
running = True

# ─── CAMERA + DETECTION THREAD ─────────────────────────────────────

def detection_loop():
    """Background thread: capture frames, run YOLOv8n, encode JPEG."""
    global latest_frame, running

    # --- Camera init ---
    try:
        from picamera2 import Picamera2
        cam = Picamera2()
        config = cam.create_preview_configuration(
            main={"size": (FRAME_WIDTH, FRAME_HEIGHT), "format": "RGB888"}
        )
        cam.configure(config)
        cam.start()
        time.sleep(1)  # warm-up
        log.info("Camera started (picamera2, %dx%d)", FRAME_WIDTH, FRAME_HEIGHT)
    except Exception as e:
        log.error("Camera init failed: %s — streaming disabled", e)
        return

    # --- YOLOv8n model ---
    model = None
    try:
        from ultralytics import YOLO
        model = YOLO("yolov8n.pt")
        log.info("YOLOv8n loaded")
    except Exception as e:
        log.warning("YOLOv8n load failed: %s — streaming raw frames", e)

    # --- Ultrasonic sensor (optional) ---
    sonar = None
    try:
        from gpiozero import DistanceSensor
        sonar = DistanceSensor(echo=ULTRASONIC_ECHO, trigger=ULTRASONIC_TRIG)
        log.info("Ultrasonic sensor on GPIO %d/%d", ULTRASONIC_ECHO, ULTRASONIC_TRIG)
    except Exception as e:
        log.warning("Ultrasonic init failed: %s — distance disabled", e)

    fps_counter = 0
    fps_time = time.time()

    while running:
        try:
            frame = cam.capture_array()  # numpy RGB888

            # --- Detection ---
            person_detected = False
            confidence = 0.0
            bbox = None

            if model is not None:
                results = model(frame, classes=[0], conf=CONFIDENCE_THRESHOLD, verbose=False)
                for r in results:
                    if r.boxes is not None and len(r.boxes) > 0:
                        # Take highest-confidence person
                        best_idx = r.boxes.conf.argmax()
                        confidence = float(r.boxes.conf[best_idx])
                        x1, y1, x2, y2 = r.boxes.xyxy[best_idx].cpu().numpy().astype(int)
                        bbox = [int(x1), int(y1), int(x2), int(y2)]
                        person_detected = True

                        # Draw bbox on frame
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        label = f"person {confidence:.0%}"
                        cv2.putText(frame, label, (x1, y1 - 8),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # --- HUD overlay ---
            phase = bot_state["phase"].upper()
            cv2.putText(frame, f"ELKTRON | {phase}", (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # --- Ultrasonic ---
            distance_cm = None
            if sonar is not None:
                try:
                    distance_cm = round(sonar.distance * 100, 1)
                    cv2.putText(frame, f"{distance_cm}cm", (FRAME_WIDTH - 100, 25),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)
                except Exception:
                    pass

            # --- FPS ---
            fps_counter += 1
            elapsed = time.time() - fps_time
            if elapsed >= 1.0:
                fps = fps_counter / elapsed
                bot_state["fps"] = round(fps, 1)
                fps_counter = 0
                fps_time = time.time()

            # --- Update shared state ---
            bot_state["detection"] = {
                "person_detected": person_detected,
                "confidence": round(confidence, 3),
                "bbox": bbox,
            }
            bot_state["distance_cm"] = distance_cm

            # --- Encode JPEG ---
            # Convert RGB → BGR for cv2.imencode
            bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            ok, buf = cv2.imencode(".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
            if ok:
                with frame_lock:
                    latest_frame = buf.tobytes()

        except Exception as e:
            log.error("Detection loop error: %s", e)
            time.sleep(0.1)

    cam.stop()
    log.info("Camera stopped")


# ─── MJPEG GENERATOR ──────────────────────────────────────────────

def mjpeg_stream():
    """Yield MJPEG frames for the /video_feed endpoint."""
    while running:
        with frame_lock:
            frame = latest_frame
        if frame is None:
            time.sleep(0.05)
            continue
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )
        time.sleep(0.03)  # ~30fps cap (Pi will be slower anyway)


# ─── ROUTES ────────────────────────────────────────────────────────

@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.route("/health")
def health():
    return jsonify({"status": "ok", "uptime": round(time.time() - start_time, 1)})


@app.route("/state")
def state():
    return jsonify(bot_state)


@app.route("/video_feed")
def video_feed():
    return Response(
        mjpeg_stream(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/dispatch", methods=["POST"])
def dispatch():
    data = request.get_json(silent=True) or {}
    bot_state["phase"] = "dispatched"
    bot_state["vendor"] = data.get("vendor")
    bot_state["target_rack"] = data.get("target_rack")
    log.info("Dispatch: vendor=%s rack=%s", bot_state["vendor"], bot_state["target_rack"])
    return jsonify({"ok": True})


@app.route("/recall", methods=["POST"])
def recall():
    bot_state["phase"] = "returning"
    bot_state["vendor"] = None
    bot_state["target_rack"] = None
    log.info("Recall issued")
    return jsonify({"ok": True})


@app.route("/stop", methods=["POST"])
def stop():
    bot_state["phase"] = "idle"
    log.info("Emergency stop")
    # If motors are active, stop them
    try:
        from gpiozero import Robot
        robot = Robot(left=(17, 27), right=(22, 23))
        robot.stop()
    except Exception:
        pass
    return jsonify({"ok": True})


# ─── MAIN ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Starting Elktron API server on %s:%d", HOST, PORT)
    log.info("Endpoints:")
    log.info("  GET  /health     — connectivity check")
    log.info("  GET  /state      — bot telemetry JSON")
    log.info("  GET  /video_feed — MJPEG camera stream")
    log.info("  POST /dispatch   — send bot to rack")
    log.info("  POST /recall     — return to bay")
    log.info("  POST /stop       — emergency stop")

    # Start detection thread
    det_thread = threading.Thread(target=detection_loop, daemon=True)
    det_thread.start()

    # Run Flask (threaded for concurrent MJPEG clients)
    app.run(host=HOST, port=PORT, threaded=True)
