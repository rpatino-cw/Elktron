# Elktron SO-101 — Hardware Guide

## What to Buy

### Option A: HiWonder Kit (easiest)
| Item | Price | Link |
|------|-------|------|
| SO-ARM101 DIY Kit (both arms, all servos, boards, power, clamps) | $270 | [hiwonder.com/products/lerobot-so-101](https://www.hiwonder.com/products/lerobot-so-101) |
| USB webcam (1080p) | $20-30 | Any OpenCV-compatible |
| **Total** | **~$300** | |

### Option B: Seeed Studio + 3D Print (cheaper)
| Item | Price |
|------|-------|
| Servo motor kit (12x STS3215 servos + boards) | $220 |
| 3D-printed parts (order from JLCPCB/PCBWay or self-print) | $35 |
| USB webcam | $20-30 |
| **Total** | **~$275** | |

### Already Have
- Raspberry Pi 5 (or laptop for training)
- USB-C cables (2x, included in kit)

## Kit Contents (HiWonder DIY)
- 1x Follower arm: 6x HX-30HM bus servos (STS3215, 30kg.cm torque)
- 1x Leader arm: 6x HX-10HM bus servos (STS3215, lighter gearing)
- 2x BusLinker V3.0 servo controller boards
- 1x 12V 5A power supply (follower)
- 1x 5V power supply (leader)
- 4x table clamps
- All 3D-printed structural parts
- Screws, cables, assembly tools

## Assembly Notes
- DIY kit: ~2-3 hours to assemble both arms
- Follow HiWonder's assembly video or [TheRobotStudio GitHub](https://github.com/TheRobotStudio/SO-ARM100) for STLs and build guide
- Clamp both arms to the same table, ~30cm apart
- Camera mounts above or to the side of the follower workspace

## Connections

```
Laptop/Pi 5
  ├── USB-C → BusLinker (Leader arm)
  ├── USB-C → BusLinker (Follower arm)
  └── USB   → Webcam

12V 5A PSU → Follower arm power
5V PSU     → Leader arm power
```

## Compute Options for Training

| Machine | Device flag | Training time (50 episodes) |
|---------|------------|----------------------------|
| Mac M1/M2/M3 | `--device mps` | ~2-4 hours |
| NVIDIA GPU (RTX 3060+) | `--device cuda` | ~1-2 hours |
| Google Colab (free T4) | `--device cuda` | ~3-5 hours |
| Raspberry Pi 5 (CPU) | `--device cpu` | Not recommended for training |

**Hackathon strategy:** Record on Pi/laptop → train on Mac or Colab → deploy on Pi.

## Demo Day Setup

For the March 23 demo, you need:
1. Follower arm clamped to table
2. Optic + transceiver cage in workspace
3. Pi 5 or laptop running `deploy.py`
4. Camera showing the arm's view on a monitor (impressive for audience)

Keep the leader arm connected but out of the way — useful for live teleoperation fallback if the trained policy struggles.
