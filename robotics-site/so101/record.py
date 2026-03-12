#!/usr/bin/env python3
"""
Elktron SO-101 — Record Demonstrations
Uses LeRobot teleoperation: physically move the leader arm,
follower mirrors it, camera + joint data recorded as a dataset.

Usage:
  python record.py --task optic_seating --episodes 50
"""

import argparse
import subprocess
import os

# ─── CONFIG ────────────────────────────────────────────────────────
HF_USER = os.environ.get("HF_USER", "rpatino")

TASKS = {
    "optic_seating": {
        "description": "Seat the optic into the transceiver port",
        "episodes": 50,
    },
    "rack_inspection": {
        "description": "Sweep camera across rack front to scan for faults",
        "episodes": 30,
    },
    "cable_management": {
        "description": "Route and dress a cable along the rack rail",
        "episodes": 100,
    },
}

ROBOT_CONFIG = {
    "follower_port": "/dev/ttyACM0",
    "leader_port": "/dev/ttyACM1",
    "camera_index": 0,
    "camera_width": 640,
    "camera_height": 480,
    "camera_fps": 30,
}


# ─── RECORD ────────────────────────────────────────────────────────

def record(task_name, num_episodes=None):
    if task_name not in TASKS:
        print(f"Unknown task: {task_name}")
        print(f"Available: {', '.join(TASKS.keys())}")
        return

    task = TASKS[task_name]
    episodes = num_episodes or task["episodes"]
    repo_id = f"{HF_USER}/elktron_{task_name}"

    cmd = [
        "lerobot-record",
        f"--robot.type=so101_follower",
        f"--robot.port={ROBOT_CONFIG['follower_port']}",
        f"--robot.id=elktron_follower",
        f"--robot.cameras={{ front: {{type: opencv, index_or_path: {ROBOT_CONFIG['camera_index']}, "
        f"width: {ROBOT_CONFIG['camera_width']}, height: {ROBOT_CONFIG['camera_height']}, "
        f"fps: {ROBOT_CONFIG['camera_fps']}}}}}",
        f"--teleop.type=so101_leader",
        f"--teleop.port={ROBOT_CONFIG['leader_port']}",
        f"--teleop.id=elktron_leader",
        f"--dataset.repo_id={repo_id}",
        f"--dataset.num_episodes={episodes}",
        f'--dataset.single_task="{task["description"]}"',
    ]

    print(f"[Elktron] Recording {episodes} episodes for: {task_name}")
    print(f"[Elktron] Dataset → {repo_id}")
    print(f"[Elktron] Task: {task['description']}")
    print()
    print("Move the LEADER arm. The follower will mirror.")
    print("Press Enter after each episode. Ctrl+C to stop early.")
    print()

    subprocess.run(" ".join(cmd), shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Record SO-101 demonstrations")
    parser.add_argument("--task", required=True, choices=TASKS.keys())
    parser.add_argument("--episodes", type=int, default=None)
    args = parser.parse_args()
    record(args.task, args.episodes)
