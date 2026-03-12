#!/usr/bin/env python3
"""
Elktron SO-101 — Train Policy
Trains an ACT (Action Chunking with Transformers) policy on recorded demos.

Usage:
  python train.py --task optic_seating
  python train.py --task optic_seating --device mps   # Mac
  python train.py --task optic_seating --device cuda   # NVIDIA GPU
"""

import argparse
import subprocess
import os

HF_USER = os.environ.get("HF_USER", "rpatino")

OUTPUT_DIR = "outputs/train"


def train(task_name, device="cuda"):
    repo_id = f"{HF_USER}/elktron_{task_name}"
    job_name = f"act_{task_name}"
    output = os.path.join(OUTPUT_DIR, job_name)

    cmd = [
        "lerobot-train",
        f"--dataset.repo_id={repo_id}",
        f"--policy.type=act",
        f"--output_dir={output}",
        f"--job_name={job_name}",
        f"--policy.device={device}",
    ]

    print(f"[Elktron] Training ACT policy for: {task_name}")
    print(f"[Elktron] Dataset: {repo_id}")
    print(f"[Elktron] Device: {device}")
    print(f"[Elktron] Output: {output}")
    print()
    print("This will take a while. Monitor with tensorboard:")
    print(f"  tensorboard --logdir {output}")
    print()

    subprocess.run(" ".join(cmd), shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train SO-101 policy")
    parser.add_argument("--task", required=True)
    parser.add_argument("--device", default="cuda", choices=["cuda", "mps", "cpu"])
    args = parser.parse_args()
    train(args.task, args.device)
