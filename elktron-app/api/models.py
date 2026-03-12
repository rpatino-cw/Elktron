"""
Elktron Dashboard — Data Models
Pydantic schemas for scan reports, training runs, arm state, escort state.
Used by server.py, arm.py, and escort.py.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ── Enums ────────────────────────────────────────────────────

class ArmPhase(str, Enum):
    idle = "idle"
    reaching = "reaching"
    gripping = "gripping"
    transiting = "transiting"
    inserting = "inserting"
    releasing = "releasing"
    retracting = "retracting"
    calibrating = "calibrating"
    error = "error"


class GripperState(str, Enum):
    open = "open"
    closing = "closing"
    closed = "closed"


class EscortPhase(str, Enum):
    idle = "idle"
    dispatched = "dispatched"
    escorting = "escorting"
    arrived = "arrived"
    scanning = "scanning"
    monitoring = "monitoring"
    verified = "verified"
    returning = "returning"
    error = "error"


class ScanResult(str, Enum):
    clean = "clean"
    flagged = "flagged"
    aborted = "aborted"


class TrainingStage(str, Enum):
    idle = "idle"
    recording = "recording"
    uploading = "uploading"
    training = "training"
    evaluating = "evaluating"
    complete = "complete"


# ── Arm Models ───────────────────────────────────────────────

class JointAngles(BaseModel):
    base: float = 0.0
    shoulder: float = 0.0
    elbow: float = 0.0
    wrist_pitch: float = 0.0
    wrist_roll: float = 0.0
    wrist_yaw: float = 0.0


class ArmState(BaseModel):
    type: str = "arm"
    phase: ArmPhase = ArmPhase.idle
    gripper: GripperState = GripperState.open
    holding_optic: bool = False
    joints: JointAngles = Field(default_factory=JointAngles)
    torque_avg: float = 0.0
    temp_c: float = 25.0
    cycle_count: int = 0
    accuracy_mm: float = 0.0
    connected: bool = False
    port: Optional[str] = None
    error: Optional[str] = None


# ── Escort Models ────────────────────────────────────────────

class Vendor(BaseModel):
    name: str
    ticket: str


class EscortAlert(BaseModel):
    ru: str
    type: str
    status: str


class EscortState(BaseModel):
    type: str = "escort"
    phase: EscortPhase = EscortPhase.idle
    location: str = "charging_bay"
    vendor: Optional[Vendor] = None
    target_rack: Optional[str] = None
    authorized_ru: Optional[str] = None
    scan_progress: int = 0
    alert: Optional[EscortAlert] = None
    battery_pct: int = 100
    nodes_scanned: int = 0
    connected: bool = False
    error: Optional[str] = None


# ── Scan Report ──────────────────────────────────────────────

class NodeBaseline(BaseModel):
    status: str = "healthy"
    optics: str = "ok"
    psu: str = "ok"


class ScanEvent(BaseModel):
    time: str
    ru: str
    type: str
    authorized: Optional[bool] = None
    resolved: Optional[bool] = None


class ScanReport(BaseModel):
    id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    vendor: str
    ticket: str
    rack: str
    authorized_ru: str
    baseline: dict[str, NodeBaseline] = Field(default_factory=dict)
    events: list[ScanEvent] = Field(default_factory=list)
    result: ScanResult = ScanResult.clean
    unauthorized_changes: int = 0
    nodes_scanned: int = 0
    flags: list[str] = Field(default_factory=list)
    duration_s: int = 0


# ── Training Models ──────────────────────────────────────────

class TrainingState(BaseModel):
    type: str = "training"
    stage: TrainingStage = TrainingStage.idle
    episodes_recorded: int = 0
    current_progress: float = 0.0
    model: str = "ACT-v1"
    policy: str = "act"
    last_loss: Optional[float] = None
    gpu: Optional[str] = None
    cost_so_far: float = 0.0


# ── Commands (frontend → backend) ────────────────────────────

class ArmCommand(BaseModel):
    action: str  # "calibrate", "start_task", "stop", "home"
    task: Optional[str] = None
    params: dict = Field(default_factory=dict)


class EscortCommand(BaseModel):
    action: str  # "dispatch", "recall", "stop", "scan"
    vendor: Optional[Vendor] = None
    target_rack: Optional[str] = None


class TrainingCommand(BaseModel):
    action: str  # "start_recording", "stop_recording", "start_training", "stop_training"
    task: Optional[str] = None
    episodes: Optional[int] = None
    device: Optional[str] = None  # "cuda", "mps", "cpu"
