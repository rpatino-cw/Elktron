"""
FloorCrew Dashboard — FastAPI WebSocket Server
Bridges hardware interfaces (arm + escort bot) to the frontend via WebSocket.
Falls back to mock data when hardware is not connected.
"""

import asyncio
import json
import logging
import math
import random
import time
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from arm import arm
from escort import escort

logger = logging.getLogger("floorcrew.server")

app = FastAPI(title="FloorCrew Dashboard")

# Serve frontend
ROOT = Path(__file__).parent.parent

@app.get("/")
async def index():
    return FileResponse(ROOT / "index.html")


# ── Hardware lifecycle ────────────────────────────────────────

USE_MOCK = True  # Set False when hardware is connected

@app.on_event("startup")
async def startup():
    global USE_MOCK
    # Try connecting to real hardware
    arm_ok = arm.connect()
    escort_ok = await escort.connect()
    if arm_ok or escort_ok:
        USE_MOCK = False
        logger.info(f"Hardware mode — arm:{arm_ok} escort:{escort_ok}")
    else:
        logger.info("No hardware detected — running in mock mode")

@app.on_event("shutdown")
async def shutdown():
    arm.disconnect()


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

# ── Mock Data Generators ────────────────────────────────────

def mock_arm_state(t: float) -> dict:
    """Simulate SO-ARM101 joint angles + gripper cycling through a pick sequence."""
    cycle = t % 12  # 12-second loop
    phase = "idle"
    gripper = "open"
    optic = False

    # Simulate a pick-place cycle
    if cycle < 2:
        phase = "idle"
        joints = [0, 0, 0, 0, 0, 0]
    elif cycle < 4:
        phase = "reaching"
        p = (cycle - 2) / 2
        joints = [
            -40 * p,
            -3 * p,
            -2 * p,
            5 * math.sin(p * math.pi) * 2,
            0,
            0,
        ]
    elif cycle < 5:
        phase = "gripping"
        gripper = "closing"
        joints = [-40, -3, -2, 0, 0, 0]
    elif cycle < 5.5:
        phase = "gripping"
        gripper = "closed"
        optic = True
        joints = [-40, -3, -2, 0, 0, 0]
    elif cycle < 8:
        phase = "transiting"
        p = (cycle - 5.5) / 2.5
        optic = True
        gripper = "closed"
        joints = [
            -40 + 88 * p,
            -3 + 6 * p,
            -2 + 4 * p,
            3 * math.sin(p * math.pi),
            0,
            0,
        ]
    elif cycle < 9:
        phase = "inserting"
        optic = True
        gripper = "closed"
        joints = [48, 3, 2, 0, 0, 0]
    elif cycle < 9.5:
        phase = "releasing"
        gripper = "open"
        optic = False
        joints = [48, 3, 2, 0, 0, 0]
    else:
        phase = "retracting"
        p = (cycle - 9.5) / 2.5
        joints = [48 * (1 - p), 3 * (1 - p), 2 * (1 - p), 0, 0, 0]

    # Add slight noise for realism
    joints = [round(j + random.uniform(-0.3, 0.3), 1) for j in joints]

    return {
        "type": "arm",
        "phase": phase,
        "gripper": gripper,
        "holding_optic": optic,
        "joints": {
            "base": joints[0],
            "shoulder": joints[1],
            "elbow": joints[2],
            "wrist_pitch": joints[3],
            "wrist_roll": joints[4],
            "wrist_yaw": joints[5],
        },
        "torque_avg": round(12 + random.uniform(-1, 1), 1),
        "temp_c": round(38 + random.uniform(-2, 3), 1),
        "cycle_count": int(t / 12),
        "accuracy_mm": round(0.8 + random.uniform(-0.1, 0.1), 2),
    }


def mock_escort_state(t: float) -> dict:
    """Simulate escort bot cycling through a vendor escort sequence."""
    cycle = t % 30  # 30-second loop
    phase = "idle"
    scan_pct = 0
    alert = None

    if cycle < 3:
        phase = "idle"
        location = "charging_bay"
        vendor = None
    elif cycle < 5:
        phase = "dispatched"
        location = "aisle_a"
        vendor = {"name": "TechCo Field Eng.", "ticket": "INC-40821"}
    elif cycle < 12:
        phase = "escorting"
        location = "aisle_a"
        vendor = {"name": "TechCo Field Eng.", "ticket": "INC-40821"}
    elif cycle < 14:
        phase = "arrived"
        location = "CAB-B3"
        vendor = {"name": "TechCo Field Eng.", "ticket": "INC-40821"}
    elif cycle < 20:
        phase = "scanning"
        location = "CAB-B3"
        vendor = {"name": "TechCo Field Eng.", "ticket": "INC-40821"}
        scan_pct = min(100, int(((cycle - 14) / 6) * 100))
    elif cycle < 22:
        phase = "monitoring"
        location = "CAB-B3"
        vendor = {"name": "TechCo Field Eng.", "ticket": "INC-40821"}
        scan_pct = 100
        if 20.5 < cycle < 21.5:
            alert = {"ru": "RU-25", "type": "brief_contact", "status": "checking"}
        elif 21.5 <= cycle < 22:
            alert = {"ru": "RU-25", "type": "brief_contact", "status": "cleared"}
    elif cycle < 24:
        phase = "verified"
        location = "CAB-B3"
        vendor = {"name": "TechCo Field Eng.", "ticket": "INC-40821"}
        scan_pct = 100
    else:
        phase = "returning"
        location = "aisle_a"
        vendor = None

    return {
        "type": "escort",
        "phase": phase,
        "location": location,
        "vendor": vendor,
        "target_rack": "CAB-B3",
        "authorized_ru": "RU-24",
        "scan_progress": scan_pct,
        "alert": alert,
        "battery_pct": max(20, 95 - int(t / 10)),
        "nodes_scanned": min(5, int(scan_pct / 20)),
    }


MOCK_SCANS = [
    {
        "id": "scan-001",
        "timestamp": (datetime.now() - timedelta(hours=3)).isoformat(),
        "vendor": "TechCo Field Eng.",
        "ticket": "INC-40821",
        "rack": "CAB-B3",
        "authorized_ru": "RU-24",
        "result": "clean",
        "unauthorized": 0,
        "nodes_scanned": 5,
        "flags": ["RU-22 PSU amber"],
        "duration_s": 285,
    },
    {
        "id": "scan-002",
        "timestamp": (datetime.now() - timedelta(hours=7)).isoformat(),
        "vendor": "NetServ Inc.",
        "ticket": "INC-40798",
        "rack": "CAB-A2",
        "authorized_ru": "RU-16",
        "result": "clean",
        "unauthorized": 0,
        "nodes_scanned": 8,
        "flags": [],
        "duration_s": 340,
    },
    {
        "id": "scan-003",
        "timestamp": (datetime.now() - timedelta(days=1, hours=2)).isoformat(),
        "vendor": "DataLink Corp.",
        "ticket": "INC-40712",
        "rack": "CAB-B1",
        "authorized_ru": "RU-30",
        "result": "flagged",
        "unauthorized": 1,
        "nodes_scanned": 6,
        "flags": ["RU-29 unauthorized contact — not resolved", "RU-30 optic swapped"],
        "duration_s": 410,
    },
]


def mock_training_state(t: float) -> dict:
    """Simulate training pipeline state."""
    # Cycle through states over time
    stage_cycle = int(t / 60) % 4
    stages = ["idle", "recording", "uploading", "training"]
    stage = stages[stage_cycle]

    episodes = int(t / 15) % 50
    if stage == "recording":
        progress = (t % 60) / 60 * 100
    elif stage == "uploading":
        progress = min(100, (t % 60) / 30 * 100)
    elif stage == "training":
        progress = min(100, (t % 60) / 50 * 100)
    else:
        progress = 0

    return {
        "type": "training",
        "stage": stage,
        "episodes_recorded": episodes,
        "current_progress": round(progress, 1),
        "model": "ACT-v1",
        "policy": "act",
        "last_loss": round(0.15 - 0.001 * min(episodes, 40) + random.uniform(-0.005, 0.005), 4),
        "gpu": "A100-80G" if stage == "training" else None,
        "cost_so_far": round(episodes * 0.12, 2),
    }


# ── WebSocket endpoint ──────────────────────────────────────

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    start = time.time()

    # Send scan history once on connect
    scans = escort.load_scan_history() if not USE_MOCK else MOCK_SCANS
    await ws.send_json({"type": "scan_history", "scans": scans})

    # Send initial hardware status
    await ws.send_json({
        "type": "status",
        "arm_connected": arm.connected,
        "escort_connected": escort.connected,
        "mock_mode": USE_MOCK,
    })

    try:
        while True:
            t = time.time() - start

            if USE_MOCK:
                await ws.send_json(mock_arm_state(t))
                await ws.send_json(mock_escort_state(t))
            else:
                # Real hardware state
                if arm.connected:
                    arm_state = arm.get_state()
                    await ws.send_json(arm_state.model_dump())
                else:
                    await ws.send_json(mock_arm_state(t))

                if escort.connected:
                    escort_state = await escort.poll_state()
                    await ws.send_json(escort_state.model_dump())
                else:
                    await ws.send_json(mock_escort_state(t))

            await ws.send_json(mock_training_state(t))

            # Check for incoming commands from frontend
            try:
                data = await asyncio.wait_for(ws.receive_json(), timeout=0.09)
                await handle_ws_command(data)
            except asyncio.TimeoutError:
                pass

            await asyncio.sleep(0.01)  # ~10Hz with the timeout above
    except WebSocketDisconnect:
        pass


async def handle_ws_command(data: dict):
    """Route commands from the frontend to the right hardware interface."""
    target = data.get("target")
    action = data.get("action")
    params = data.get("params", {})

    if target == "arm":
        arm.handle_command(action, **params)
    elif target == "escort":
        await escort.handle_command(action, **params)
    else:
        logger.warning(f"Unknown command target: {target}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)
