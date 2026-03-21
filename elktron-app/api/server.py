"""
Elktron Dashboard — FastAPI WebSocket Server
Bridges hardware interfaces (arm + escort bot) to the frontend via WebSocket.
Falls back to mock data when hardware is not connected.
"""

import asyncio
import io as _io_mod
import json
import logging
import math
import time
import threading
import psutil
from datetime import datetime, timedelta
from pathlib import Path

from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from arm import arm
from escort import escort

# ── Camera (picamera2 hardware MJPEG stream) ─────────────────
import io as _io

class _FrameBuffer(_io.BufferedIOBase):
    """Output sink for MJPEGEncoder — stores latest encoded frame."""
    def __init__(self):
        self.frame: bytes = b""
        self.event = threading.Event()

    def write(self, buf):
        self.frame = bytes(buf)
        self.event.set()
        self.event.clear()
        return len(buf)

_cam = None
_frame_buf = _FrameBuffer()

def _init_camera():
    global _cam
    try:
        from picamera2 import Picamera2
        from picamera2.encoders import MJPEGEncoder
        from picamera2.outputs import FileOutput
        from libcamera import Transform
        _cam = Picamera2()
        config = _cam.create_video_configuration(
            main={"size": (640, 480)},
            transform=Transform(hflip=1, vflip=1),  # 180° rotation
            controls={"FrameRate": 30},
        )
        _cam.configure(config)
        encoder = MJPEGEncoder(2_000_000)  # 2 Mbps — slightly lower quality, much less CPU
        _cam.start_recording(encoder, FileOutput(_frame_buf))
        logger.info("Camera started (IMX708 wide, hardware MJPEG)")
    except Exception as e:
        logger.warning(f"Camera unavailable: {e}")
        _cam = None

async def _mjpeg_frames():
    """Async generator: stream hardware-encoded MJPEG frames to client."""
    loop = asyncio.get_event_loop()
    while _cam is not None:
        await loop.run_in_executor(None, _frame_buf.event.wait, 0.1)
        jpg = _frame_buf.frame
        if jpg:
            yield (
                b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
                + jpg
                + b"\r\n"
            )

logger = logging.getLogger("elktron.server")

# ── Motor teleop ──────────────────────────────────────────────

_robot = None

def _init_motors():
    global _robot
    try:
        from gpiozero import Robot
        # Pin order per gpio_test.py: gpiozero Robot(left=(fwd,bwd), right=(fwd,bwd))
        # L298N wiring (GPIO_Current.csv): IN2=22(L-fwd), IN1=17(L-bwd), IN4=6(R-fwd), IN3=5(R-bwd)
        _robot = Robot(left=(22, 17), right=(6, 5))
        _robot.stop()
        logger.info("Motors ready — gpiozero Robot (L=(22,17) R=(6,5))")
    except Exception as e:
        logger.warning(f"Motors unavailable: {e}")
        _robot = None

# ── Hardware lifecycle ────────────────────────────────────────

USE_MOCK = True  # Set False when hardware is connected

@asynccontextmanager
async def lifespan(app):
    global USE_MOCK
    # Startup: try connecting to real hardware
    arm_ok = arm.connect()
    escort_ok = await escort.connect()
    if arm_ok or escort_ok:
        USE_MOCK = False
        logger.info(f"Hardware mode — arm:{arm_ok} escort:{escort_ok}")
    else:
        logger.info("No hardware detected — running in mock mode")
    _init_camera()
    _init_motors()
    yield
    # Shutdown
    arm.disconnect()
    global _robot
    if _robot:
        _robot.stop()
        _robot.close()
        _robot = None
    global _cam
    if _cam:
        _cam.stop_recording()
        _cam.close()
        _cam = None

app = FastAPI(title="Elktron Dashboard", lifespan=lifespan)

# Serve frontend
ROOT = Path(__file__).parent.parent

@app.get("/")
async def index():
    return FileResponse(ROOT / "index.html")

@app.get("/design-system.css")
async def design_system():
    return FileResponse(ROOT / "../design-system.css", media_type="text/css")

@app.get("/video_feed")
async def video_feed():
    """MJPEG camera stream from the Pi Camera Module 3 Wide."""
    if _cam is None:
        return {"error": "camera not available"}
    return StreamingResponse(
        _mjpeg_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


# ── REST endpoints ────────────────────────────────────────────

@app.get("/api/scans")
async def get_scans():
    """Return scan history from disk."""
    return escort.load_scan_history()

@app.get("/api/status")
async def get_status():
    """Quick health check with hardware status."""
    return {
        "arm_connected": arm.connected,
        "escort_connected": escort.connected,
        "mock_mode": USE_MOCK,
    }

# ── Real System Stats ────────────────────────────────────────

def system_stats() -> dict:
    """Real Pi system telemetry — CPU, memory, temperature, uptime."""
    try:
        temp = round(float(
            Path("/sys/class/thermal/thermal_zone0/temp").read_text()
        ) / 1000, 1)
    except Exception:
        temp = None
    return {
        "type": "system",
        "cpu_pct":  round(psutil.cpu_percent(interval=None), 1),
        "mem_pct":  round(psutil.virtual_memory().percent, 1),
        "temp_c":   temp,
        "uptime_s": int(time.time() - psutil.boot_time()),
        "cam_active": _cam is not None,
    }


# ── WebSocket endpoint ──────────────────────────────────────

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    # Real scan history from disk only — no mock data
    await ws.send_json({"type": "scan_history", "scans": escort.load_scan_history()})

    # Hardware connection status
    await ws.send_json({
        "type": "status",
        "escort_connected": escort.connected,
        "cam_active": _cam is not None,
    })

    async def recv_loop():
        """Process incoming commands immediately as they arrive — no polling delay."""
        try:
            async for msg in ws.iter_json():
                await handle_ws_command(msg)
        except WebSocketDisconnect:
            pass
        except Exception:
            pass

    async def send_loop():
        """Push telemetry at 1 Hz — independent of receive."""
        try:
            while True:
                await ws.send_json(system_stats())
                if escort.connected:
                    escort_state = await escort.poll_state()
                    await ws.send_json(escort_state.model_dump())
                await asyncio.sleep(1.0)
        except Exception:
            pass

    recv_task = asyncio.create_task(recv_loop())
    send_task = asyncio.create_task(send_loop())

    # Run until either task ends (disconnect / error)
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
        if _robot is None:
            return
        if action == "drive":
            l = max(-1.0, min(1.0, float(params.get("l", 0.0))))
            r = max(-1.0, min(1.0, float(params.get("r", 0.0))))
            _robot.value = (l, r)
        elif action == "stop":
            _robot.stop()
    else:
        logger.warning(f"Unknown command target: {target}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8888)
