"""
Elktron Dashboard — FastAPI WebSocket Server
Bridges hardware interfaces (arm + escort bot) to the frontend via WebSocket.
Falls back to mock data when hardware is not connected.
"""

import sys
import os
# Ensure api/ is on sys.path so absolute imports (arm, escort, models) resolve
sys.path.insert(0, os.path.dirname(__file__))

import asyncio
import json
import logging
import math
import time
import threading
import psutil
import httpx
from datetime import datetime, timedelta
from pathlib import Path

from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from arm import arm
from escort import escort

# Pi 5 address — raw camera stream + motor commands
PI_BASE_URL = "http://192.168.3.56:5000"

logger = logging.getLogger("elktron.server")

# ── Camera + YOLO Detection ───────────────────────────────────
import cv2 as _cv2
import numpy as _np

_cam         = None   # cv2.VideoCapture pulling from Pi MJPEG stream
_cam_running = False
_cam_thread  = None

class _FrameBuffer:
    """Thread-safe frame store for the MJPEG stream."""
    def __init__(self):
        self.frame: bytes = b""
        self.event = threading.Event()

    def put(self, jpg: bytes):
        self.frame = jpg
        self.event.set()
        self.event.clear()

_frame_buf = _FrameBuffer()

# ── YOLO detection state ───────────────────────────────────────
_det_enabled    = False
_det_model      = None
_det_model_name = "yolov8n"
# Absolute path — model lives in escort-bot/, server runs from elktron-app/api/
_MODEL_PATH     = Path(__file__).parent.parent.parent / "escort-bot" / "yolov8n.pt"
_det_lock       = threading.Lock()
_det_state: dict = {
    "active":      False,
    "yolo_conf":   None,
    "yolo_fps":    0.0,
    "yolo_detections": 0,
    "yolo_model":  "yolov8n",
}

def _load_yolo():
    """Load YOLOv8n from the escort-bot model path in a background thread."""
    global _det_model
    try:
        from ultralytics import YOLO
        logger.info(f"Loading YOLO from {_MODEL_PATH}")
        _det_model = YOLO(str(_MODEL_PATH))
        # Warm-up pass so first inference isn't slow
        dummy = _np.zeros((640, 640, 3), dtype=_np.uint8)
        _det_model(dummy, classes=[0], verbose=False)
        logger.info(f"YOLOv8n ready ({_MODEL_PATH})")
    except Exception as e:
        logger.warning(f"YOLO load failed: {e}")
        _det_model = None


def _camera_loop():
    """
    Software capture loop. Runs in a daemon thread.
    - When detection OFF: pass-through JPEG (fast, ~75% quality)
    - When detection ON:  run YOLO11n, draw boxes, push annotated JPEG
    """
    global _cam_running, _det_enabled, _det_model, _det_state

    fps_ema    = 0.0
    alpha      = 0.15
    t_last     = time.time()
    t_det_last = 0.0
    DET_MIN_MS = 0.2   # max 5 FPS for YOLO inference

    while _cam_running:
        if _cam is None:
            time.sleep(0.1)
            continue

        try:
            ret, bgr = _cam.read()   # BGR from cv2.VideoCapture (Pi MJPEG stream)
            if not ret:
                time.sleep(0.05)
                continue

            t_now  = time.time()
            dt     = max(t_now - t_last, 1e-6)
            t_last = t_now
            fps_ema = fps_ema * (1 - alpha) + (1.0 / dt) * alpha

            # Camera is physically mounted 180° — flip to correct orientation
            bgr = _cv2.flip(bgr, -1)

            if _det_enabled and _det_model is not None and (t_now - t_det_last) >= DET_MIN_MS:
                t_det_last = t_now
                rgb = bgr[:, :, ::-1]  # BGR→RGB for YOLO
                results = _det_model(rgb, classes=[0], conf=0.35, verbose=False)
                boxes   = results[0].boxes
                n       = len(boxes)
                best_conf = float(boxes.conf.max()) if n > 0 else 0.0

                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    c = float(box.conf[0])
                    _cv2.rectangle(bgr, (x1, y1), (x2, y2), (0, 220, 80), 3)
                    _cv2.rectangle(bgr, (x1, max(y1 - 24, 0)), (x1 + 130, y1), (0, 220, 80), -1)
                    _cv2.putText(bgr, f"person {c:.0%}", (x1 + 4, max(y1 - 6, 14)),
                                 _cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 2)

                # HUD: status bar
                hud = f"YOLO: {n} person{'s' if n != 1 else ''}  {fps_ema:.1f}fps"
                _cv2.rectangle(bgr, (0, 0), (280, 28), (0, 0, 0), -1)
                _cv2.putText(bgr, hud, (6, 20),
                             _cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 220, 80), 2)

                # Only write active=True if detection is still enabled (guard against
                # _det_enabled being cleared while YOLO inference was in-flight)
                with _det_lock:
                    if _det_enabled:
                        _det_state = {
                            "active":          True,
                            "yolo_conf":       round(best_conf, 2) if n > 0 else None,
                            "yolo_fps":        round(fps_ema, 1),
                            "yolo_detections": n,
                            "yolo_model":      _det_model_name,
                        }

                ok, jpg = _cv2.imencode(".jpg", bgr, [_cv2.IMWRITE_JPEG_QUALITY, 70])

            elif _det_enabled and _det_model is None:
                # Model still loading — show indicator
                _cv2.rectangle(bgr, (0, 0), (220, 28), (0, 0, 0), -1)
                _cv2.putText(bgr, "YOLO: LOADING...", (6, 20),
                             _cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 180, 255), 2)
                ok, jpg = _cv2.imencode(".jpg", bgr, [_cv2.IMWRITE_JPEG_QUALITY, 75])

            else:
                with _det_lock:
                    _det_state["active"]   = False
                    _det_state["yolo_fps"] = round(fps_ema, 1)

                ok, jpg = _cv2.imencode(".jpg", bgr, [_cv2.IMWRITE_JPEG_QUALITY, 75])

            if ok:
                _frame_buf.put(bytes(jpg.tobytes()))

        except Exception as e:
            logger.error(f"Camera loop error: {e}")
            time.sleep(0.05)


def _init_camera():
    global _cam, _cam_running, _cam_thread
    stream_url = f"{PI_BASE_URL}/video_feed"
    try:
        cap = _cv2.VideoCapture(stream_url)
        if not cap.isOpened():
            raise RuntimeError(f"stream not open at {stream_url}")
        _cam = cap
        _cam_running = True
        _cam_thread = threading.Thread(target=_camera_loop, daemon=True, name="cam-loop")
        _cam_thread.start()
        logger.info(f"Camera stream connected — {stream_url} (YOLO runs on this machine)")
    except Exception as e:
        logger.warning(f"Camera stream unavailable: {e}")
        _cam = None


async def _mjpeg_frames():
    """Async generator: yield MJPEG boundary frames to the client."""
    loop = asyncio.get_event_loop()
    while _cam is not None and _cam_running:
        await loop.run_in_executor(None, _frame_buf.event.wait, 0.1)
        jpg = _frame_buf.frame
        if jpg:
            yield (
                b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
                + jpg
                + b"\r\n"
            )


# ── Remote motor control (HTTP → Pi) ──────────────────────────
# Motors live on the Pi. We POST {l, r} to /drive instead of
# writing GPIO directly — YOLO + PID stay on this machine.
_drive_client: httpx.AsyncClient | None = None

async def _send_drive(l: float, r: float) -> None:
    """Send motor command to Pi. Fire-and-forget — drop on timeout."""
    if _drive_client is None:
        return
    try:
        await _drive_client.post(
            f"{PI_BASE_URL}/drive",
            json={"l": round(l, 3), "r": round(r, 3)},
            timeout=0.2,
        )
    except Exception:
        pass  # Pi watchdog stops motors if commands dry up


# ── Hardware lifecycle ────────────────────────────────────────
USE_MOCK = True  # Set False when hardware is connected

@asynccontextmanager
async def lifespan(app):
    global USE_MOCK, _cam_running, _drive_client
    arm_ok    = arm.connect()
    escort_ok = await escort.connect()
    if arm_ok or escort_ok:
        USE_MOCK = False
        logger.info(f"Hardware mode — arm:{arm_ok} escort:{escort_ok}")
    else:
        logger.info("No hardware detected — running in mock mode")
    _init_camera()
    _drive_client = httpx.AsyncClient()
    logger.info(f"Motor client ready — POSTing drive commands to {PI_BASE_URL}/drive")
    yield
    # Shutdown
    arm.disconnect()
    await _send_drive(0.0, 0.0)   # safe stop on server exit
    if _drive_client:
        await _drive_client.aclose()
        _drive_client = None
    global _cam
    _cam_running = False
    if _cam:
        _cam.release()
        _cam = None


app = FastAPI(title="Elktron Dashboard", lifespan=lifespan)

ROOT = Path(__file__).parent.parent

@app.get("/")
async def index():
    return FileResponse(ROOT / "index.html")

@app.get("/design-system.css")
async def design_system():
    return FileResponse(ROOT / "../design-system.css", media_type="text/css")

@app.get("/video_feed")
async def video_feed():
    """MJPEG stream — clean or YOLO-annotated depending on detection toggle."""
    if _cam is None:
        return {"error": "camera not available"}
    return StreamingResponse(
        _mjpeg_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


# ── REST endpoints ────────────────────────────────────────────

@app.get("/api/scans")
async def get_scans():
    return escort.load_scan_history()

@app.get("/api/status")
async def get_status():
    return {
        "arm_connected":    arm.connected,
        "escort_connected": escort.connected,
        "mock_mode":        USE_MOCK,
        "det_enabled":      _det_enabled,
    }


# ── Real System Stats ─────────────────────────────────────────

def system_stats() -> dict:
    try:
        temp = round(float(
            Path("/sys/class/thermal/thermal_zone0/temp").read_text()
        ) / 1000, 1)
    except Exception:
        temp = None
    return {
        "type":      "system",
        "cpu_pct":   round(psutil.cpu_percent(interval=None), 1),
        "mem_pct":   round(psutil.virtual_memory().percent, 1),
        "temp_c":    temp,
        "uptime_s":  int(time.time() - psutil.boot_time()),
        "cam_active": _cam is not None,
    }


# ── WebSocket endpoint ────────────────────────────────────────

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    await ws.send_json({"type": "scan_history", "scans": escort.load_scan_history()})
    await ws.send_json({
        "type":             "status",
        "escort_connected": escort.connected,
        "cam_active":       _cam is not None,
    })

    async def recv_loop():
        try:
            async for msg in ws.iter_json():
                await handle_ws_command(msg)
        except WebSocketDisconnect:
            pass
        except Exception:
            pass

    async def send_loop():
        try:
            while True:
                await ws.send_json(system_stats())

                if escort.connected:
                    escort_state = await escort.poll_state()
                    await ws.send_json(escort_state.model_dump())

                # Always push detection telemetry so the panel updates
                with _det_lock:
                    det = dict(_det_state)
                await ws.send_json({
                    "type":            "drive_detection",
                    "det_active":      det["active"],
                    "yolo_conf":       det["yolo_conf"],
                    "yolo_fps":        det["yolo_fps"],
                    "yolo_detections": det["yolo_detections"],
                    "yolo_model":      det["yolo_model"],
                    "motor_l":         0,
                    "motor_r":         0,
                })

                await asyncio.sleep(1.0)
        except Exception:
            pass

    recv_task = asyncio.create_task(recv_loop())
    send_task = asyncio.create_task(send_loop())

    done, pending = await asyncio.wait(
        [recv_task, send_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for t in pending:
        t.cancel()


async def handle_ws_command(data: dict):
    """Route commands from the frontend to the right hardware interface."""
    target = data.get("target")
    action = data.get("action")
    params = data.get("params", {})

    if target == "arm":
        arm.handle_command(action, **params)

    elif target == "escort":
        await escort.handle_command(action, **params)

    elif target == "teleop":
        if action == "drive":
            l = max(-1.0, min(1.0, float(params.get("l", 0.0))))
            r = max(-1.0, min(1.0, float(params.get("r", 0.0))))
            await _send_drive(l, r)
        elif action == "stop":
            await _send_drive(0.0, 0.0)

    elif target == "detection":
        global _det_enabled
        if action == "toggle":
            _det_enabled = bool(params.get("enabled", not _det_enabled))
            if not _det_enabled:
                with _det_lock:
                    _det_state["active"] = False
            if _det_enabled and _det_model is None:
                # Load YOLO in background so the toggle doesn't block
                threading.Thread(target=_load_yolo, daemon=True, name="yolo-load").start()
            logger.info(f"YOLO detection {'ON' if _det_enabled else 'OFF'}")

    else:
        logger.warning(f"Unknown command target: {target}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8888)
