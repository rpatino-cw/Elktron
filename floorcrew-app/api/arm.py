"""
FloorCrew Dashboard — SO-ARM101 Interface
Wraps LeRobot's Feetech motor bus for reading joint state and sending commands.
Falls back to mock data when hardware is not connected.
"""

import logging
import time
from typing import Optional

from models import ArmPhase, ArmState, GripperState, JointAngles

logger = logging.getLogger("floorcrew.arm")

# Servo IDs on the Feetech bus (STS3215, daisy-chained via BusLinker V3.0)
SERVO_IDS = {
    "base": 1,
    "shoulder": 2,
    "elbow": 3,
    "wrist_pitch": 4,
    "wrist_roll": 5,
    "wrist_yaw": 6,
}

# Home position (degrees) — arm straight up, gripper open
HOME_POSITION = {name: 0.0 for name in SERVO_IDS}

# Serial config
DEFAULT_PORT = "/dev/ttyACM0"
BAUDRATE = 1_000_000  # Feetech STS3215 default


class ArmInterface:
    """Interface to SO-ARM101 via LeRobot's Feetech motor bus."""

    def __init__(self, port: str = DEFAULT_PORT):
        self.port = port
        self._bus = None
        self._connected = False
        self._phase = ArmPhase.idle
        self._gripper = GripperState.open
        self._holding_optic = False
        self._cycle_count = 0
        self._error: Optional[str] = None

    @property
    def connected(self) -> bool:
        return self._connected

    def connect(self) -> bool:
        """Connect to the arm via USB serial. Returns True on success."""
        try:
            from lerobot.common.robot_devices.motors.feetech import FeetechMotorsBus

            self._bus = FeetechMotorsBus(
                port=self.port,
                motors={name: (sid, "sts3215") for name, sid in SERVO_IDS.items()},
            )
            self._bus.connect()
            self._connected = True
            self._error = None
            logger.info(f"SO-ARM101 connected on {self.port}")
            return True
        except ImportError:
            self._error = "lerobot not installed — run: pip install lerobot"
            logger.warning(self._error)
            return False
        except Exception as e:
            self._error = f"Connection failed: {e}"
            logger.warning(self._error)
            self._connected = False
            return False

    def disconnect(self):
        """Disconnect from the arm."""
        if self._bus is not None:
            try:
                self._bus.disconnect()
            except Exception:
                pass
        self._bus = None
        self._connected = False
        logger.info("SO-ARM101 disconnected")

    def read_joints(self) -> JointAngles:
        """Read current joint positions from all 6 servos."""
        if not self._connected or self._bus is None:
            return JointAngles()

        try:
            positions = self._bus.read("Present_Position")
            names = list(SERVO_IDS.keys())
            angles = {}
            for i, name in enumerate(names):
                # Convert raw servo ticks to degrees
                # STS3215: 0-4095 ticks = 0-360 degrees, center at 2048
                raw = positions[i] if i < len(positions) else 2048
                angles[name] = round((raw - 2048) * (360.0 / 4096.0), 1)
            return JointAngles(**angles)
        except Exception as e:
            logger.error(f"Failed to read joints: {e}")
            return JointAngles()

    def read_temperature(self) -> float:
        """Read average servo temperature (Celsius)."""
        if not self._connected or self._bus is None:
            return 25.0

        try:
            temps = self._bus.read("Present_Temperature")
            return round(sum(temps) / len(temps), 1)
        except Exception:
            return 25.0

    def read_load(self) -> float:
        """Read average servo torque load."""
        if not self._connected or self._bus is None:
            return 0.0

        try:
            loads = self._bus.read("Present_Load")
            return round(sum(abs(l) for l in loads) / len(loads), 1)
        except Exception:
            return 0.0

    def go_home(self):
        """Move all joints to home position."""
        if not self._connected or self._bus is None:
            return

        try:
            positions = [2048] * len(SERVO_IDS)  # Center position for all servos
            self._bus.write("Goal_Position", positions)
            self._phase = ArmPhase.retracting
            logger.info("Arm moving to home position")
        except Exception as e:
            logger.error(f"Failed to go home: {e}")

    def set_gripper(self, state: GripperState):
        """Open or close the gripper (wrist_yaw servo)."""
        if not self._connected or self._bus is None:
            return

        try:
            grip_id = SERVO_IDS["wrist_yaw"]
            if state == GripperState.open:
                target = 2048 + 512  # Open position
            else:
                target = 2048 - 512  # Closed position
            self._bus.write("Goal_Position", [target], motor_names=["wrist_yaw"])
            self._gripper = state
        except Exception as e:
            logger.error(f"Failed to set gripper: {e}")

    def get_state(self) -> ArmState:
        """Get complete arm state for dashboard broadcast."""
        joints = self.read_joints()
        temp = self.read_temperature()
        torque = self.read_load()

        return ArmState(
            phase=self._phase,
            gripper=self._gripper,
            holding_optic=self._holding_optic,
            joints=joints,
            torque_avg=torque,
            temp_c=temp,
            cycle_count=self._cycle_count,
            accuracy_mm=0.8,  # Placeholder — updated after calibration
            connected=self._connected,
            port=self.port if self._connected else None,
            error=self._error,
        )

    def handle_command(self, action: str, **kwargs):
        """Handle a command from the dashboard."""
        if action == "home":
            self.go_home()
        elif action == "calibrate":
            self._phase = ArmPhase.calibrating
            self.go_home()
            time.sleep(2)
            self._phase = ArmPhase.idle
        elif action == "stop":
            if self._bus and self._connected:
                try:
                    self._bus.write("Torque_Enable", [0] * len(SERVO_IDS))
                except Exception:
                    pass
            self._phase = ArmPhase.idle
        elif action == "start_task":
            task = kwargs.get("task", "optic_seating")
            self._phase = ArmPhase.reaching
            logger.info(f"Starting task: {task}")
        else:
            logger.warning(f"Unknown arm command: {action}")


# Singleton — import and use directly
arm = ArmInterface()
