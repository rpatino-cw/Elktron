"""
Elktron Dashboard — Escort Bot Telemetry Aggregator
Collects state from the Pi 5 escort bot (via HTTP or WebSocket),
manages scan reports, and exposes state for the dashboard.
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4

import httpx

from models import (
    EscortAlert,
    EscortPhase,
    EscortState,
    NodeBaseline,
    ScanEvent,
    ScanReport,
    ScanResult,
    Vendor,
)

logger = logging.getLogger("elktron.escort")

# Data directory for scan reports
DATA_DIR = Path(__file__).parent.parent / "data"
SCANS_DIR = DATA_DIR / "scans"
LOGS_DIR = DATA_DIR / "logs"

# Escort bot Pi 5 network address
DEFAULT_BOT_HOST = "192.168.3.56"
DEFAULT_BOT_PORT = 5000


class EscortInterface:
    """Interface to the escort bot running on Pi 5."""

    def __init__(self, host: str = DEFAULT_BOT_HOST, port: int = DEFAULT_BOT_PORT):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self._connected = False
        self._state = EscortState()
        self._current_scan: Optional[ScanReport] = None
        self._error: Optional[str] = None
        self._last_heartbeat: float = 0

        # Ensure data dirs exist
        SCANS_DIR.mkdir(parents=True, exist_ok=True)
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

    @property
    def connected(self) -> bool:
        return self._connected

    async def connect(self) -> bool:
        """Ping the escort bot to check connectivity."""
        try:
            async with httpx.AsyncClient(timeout=3) as client:
                resp = await client.get(f"{self.base_url}/health")
                if resp.status_code == 200:
                    self._connected = True
                    self._error = None
                    self._last_heartbeat = time.time()
                    logger.info(f"Escort bot connected at {self.base_url}")
                    return True
        except Exception as e:
            self._error = f"Cannot reach escort bot at {self.base_url}: {e}"
            logger.warning(self._error)
        self._connected = False
        return False

    async def poll_state(self) -> EscortState:
        """Fetch current state from the escort bot's API."""
        if not self._connected:
            return self._state

        try:
            async with httpx.AsyncClient(timeout=2) as client:
                resp = await client.get(f"{self.base_url}/state")
                if resp.status_code == 200:
                    data = resp.json()
                    self._last_heartbeat = time.time()
                    self._state = EscortState(
                        phase=data.get("phase", "idle"),
                        location=data.get("location", "unknown"),
                        vendor=Vendor(**data["vendor"]) if data.get("vendor") else None,
                        target_rack=data.get("target_rack"),
                        authorized_ru=data.get("authorized_ru"),
                        scan_progress=data.get("scan_progress", 0),
                        alert=EscortAlert(**data["alert"]) if data.get("alert") else None,
                        battery_pct=data.get("battery_pct", 0),
                        nodes_scanned=data.get("nodes_scanned", 0),
                        connected=True,
                    )
                    return self._state
        except Exception as e:
            # Check if heartbeat is stale
            if time.time() - self._last_heartbeat > 10:
                self._connected = False
                self._error = f"Lost connection: {e}"
                logger.warning(self._error)

        return self._state

    def get_state(self) -> EscortState:
        """Get current cached state for dashboard broadcast (sync version)."""
        self._state.connected = self._connected
        self._state.error = self._error
        return self._state

    # ── Scan Management ──────────────────────────────────────

    def start_scan(self, vendor: Vendor, rack: str, authorized_ru: str) -> ScanReport:
        """Begin a new scan report for a vendor escort."""
        scan = ScanReport(
            id=f"scan-{uuid4().hex[:8]}",
            timestamp=datetime.now(),
            vendor=vendor.name,
            ticket=vendor.ticket,
            rack=rack,
            authorized_ru=authorized_ru,
        )
        self._current_scan = scan
        logger.info(f"Scan started: {scan.id} | {vendor.name} @ {rack}")
        return scan

    def record_event(self, ru: str, event_type: str, authorized: Optional[bool] = None,
                     resolved: Optional[bool] = None):
        """Record a contact event during an active scan."""
        if self._current_scan is None:
            logger.warning("No active scan — ignoring event")
            return

        elapsed = (datetime.now() - self._current_scan.timestamp).total_seconds()
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)

        event = ScanEvent(
            time=f"+{minutes}m{seconds:02d}s",
            ru=ru,
            type=event_type,
            authorized=authorized,
            resolved=resolved,
        )
        self._current_scan.events.append(event)

        if authorized is False:
            self._current_scan.unauthorized_changes += 1

        logger.info(f"Scan event: {event_type} @ {ru}")

    def finish_scan(self) -> Optional[ScanReport]:
        """Finalize the current scan, save to disk, return the report."""
        if self._current_scan is None:
            return None

        scan = self._current_scan
        scan.duration_s = int((datetime.now() - scan.timestamp).total_seconds())

        # Determine result
        if scan.unauthorized_changes > 0:
            scan.result = ScanResult.flagged
        else:
            scan.result = ScanResult.clean

        # Build flags summary
        for event in scan.events:
            if event.authorized is False or event.resolved is False:
                scan.flags.append(f"{event.ru} {event.type} — not resolved")

        # Save to disk
        filepath = SCANS_DIR / f"{scan.id}.json"
        filepath.write_text(json.dumps(scan.model_dump(), indent=2, default=str))
        logger.info(f"Scan saved: {filepath}")

        self._current_scan = None
        return scan

    def load_scan_history(self, limit: int = 50) -> list[dict]:
        """Load recent scan reports from disk."""
        scans = []
        if not SCANS_DIR.exists():
            return scans

        files = sorted(SCANS_DIR.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
        for f in files[:limit]:
            try:
                scans.append(json.loads(f.read_text()))
            except Exception as e:
                logger.error(f"Failed to load {f}: {e}")

        return scans

    # ── Commands ─────────────────────────────────────────────

    async def dispatch(self, vendor: Vendor, target_rack: str):
        """Send dispatch command to the escort bot."""
        if not self._connected:
            logger.warning("Cannot dispatch — bot not connected")
            return False

        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.post(f"{self.base_url}/dispatch", json={
                    "vendor": vendor.model_dump(),
                    "target_rack": target_rack,
                })
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Dispatch failed: {e}")
            return False

    async def recall(self):
        """Recall the escort bot to charging bay."""
        if not self._connected:
            return False

        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.post(f"{self.base_url}/recall")
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Recall failed: {e}")
            return False

    async def stop(self):
        """Emergency stop."""
        if not self._connected:
            return False

        try:
            async with httpx.AsyncClient(timeout=2) as client:
                resp = await client.post(f"{self.base_url}/stop")
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Stop failed: {e}")
            return False

    async def handle_command(self, action: str, **kwargs):
        """Handle a command from the dashboard."""
        if action == "dispatch":
            vendor = Vendor(**kwargs["vendor"]) if "vendor" in kwargs else None
            rack = kwargs.get("target_rack", "")
            if vendor and rack:
                await self.dispatch(vendor, rack)
        elif action == "recall":
            await self.recall()
        elif action == "stop":
            await self.stop()
        elif action == "scan":
            vendor = Vendor(**kwargs["vendor"]) if "vendor" in kwargs else None
            rack = kwargs.get("target_rack", "")
            ru = kwargs.get("authorized_ru", "")
            if vendor:
                self.start_scan(vendor, rack, ru)
        else:
            logger.warning(f"Unknown escort command: {action}")


# Singleton
escort = EscortInterface()
