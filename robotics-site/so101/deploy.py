#!/usr/bin/env python3
"""
Elktron SO-101 — Deploy Trained Policy
Runs the trained ACT model on the follower arm autonomously.

Usage:
  python deploy.py --task optic_seating
  python deploy.py --task optic_seating --checkpoint last
"""

import argparse
import subprocess
import os

HF_USER = os.environ.get("HF_USER", "rpatino")

OUTPUT_DIR = "outputs/train"

ROBOT_CONFIG = {
    "follower_port": "/dev/ttyACM0",
    "camera_index": 0,
    "camera_width": 640,
    "camera_height": 480,
    "camera_fps": 30,
}


def deploy(task_name, checkpoint="last", eval_episodes=10):
    job_name = f"act_{task_name}"
    model_path = os.path.join(OUTPUT_DIR, job_name, "checkpoints", checkpoint, "pretrained_model")
    eval_repo = f"{HF_USER}/eval_elktron_{task_name}"

    if not os.path.exists(model_path):
        print(f"[ERROR] Model not found at: {model_path}")
        print(f"Train first: python train.py --task {task_name}")
        return

    cmd = [
        "lerobot-record",
        f"--robot.type=so101_follower",
        f"--robot.port={ROBOT_CONFIG['follower_port']}",
        f"--robot.id=elktron_follower",
        f"--robot.cameras={{ front: {{type: opencv, index_or_path: {ROBOT_CONFIG['camera_index']}, "
        f"width: {ROBOT_CONFIG['camera_width']}, height: {ROBOT_CONFIG['camera_height']}, "
        f"fps: {ROBOT_CONFIG['camera_fps']}}}}}",
        f"--control.policy.path={model_path}",
        f"--dataset.repo_id={eval_repo}",
        f'--dataset.single_task="Seat the optic into the transceiver port"',
        f"--dataset.num_episodes={eval_episodes}",
    ]

    print(f"[Elktron] Deploying trained policy: {task_name}")
    print(f"[Elktron] Model: {model_path}")
    print(f"[Elktron] Eval dataset: {eval_repo}")
    print()
    print("The arm will move AUTONOMOUSLY. Keep hands clear!")
    print("Press Ctrl+C to stop at any time.")
    print()

    subprocess.run(" ".join(cmd), shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy SO-101 trained policy")
    parser.add_argument("--task", required=True)
    parser.add_argument("--checkpoint", default="last")
    parser.add_argument("--episodes", type=int, default=10)
    args = parser.parse_args()
    deploy(args.task, args.checkpoint, args.episodes)
