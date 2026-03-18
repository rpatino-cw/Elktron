# Elktron — Project Overview

## What It Is

Elktron is a robotics platform for the data center floor. It automates repetitive physical work — escorting vendors, scanning racks, seating optics — so DCTs can spend their time on troubleshooting, rack turn-ups, and the problems that actually need a human.

The live proof point is the **Escort Bot**: an autonomous robot that detects a person, follows them through the data hall, and scans racks when they stop. The platform extends to a **robot arm** that learns optic seating by demonstration, and a **dashboard** that unifies both systems with live telemetry and control.

## The Problem

At a site like EVI01, technicians spend hours each shift on autopilot work:

- **Vendor escorts** — every visit requires a tech to physically shadow the vendor, 30 minutes to 2 hours each time
- **Optic seating** — inserting transceivers one by one, 5-10 minutes per module, hundreds of ports per rack turn-up
- **Rack inspections** — manual visual checks that could be captured and logged automatically

These tasks don't require engineering skill. They require presence. Elktron provides that presence.

## The Escort Bot

An autonomous 4WD robot that lives in the data hall. When a vendor enters, the bot detects them using real-time person detection (YOLOv8n on a Raspberry Pi 5), follows them through the aisles at a safe distance, and responds to their movement:

- **FOLLOW mode** — tracks the person, maintains target distance using dual PID controllers, steers using differential (tank-style) drive
- **SCAN mode** — when the person stops at a rack for ~3 seconds, the bot assumes work is happening and runs an automated camera sweep, capturing the state of every node from bottom to top
- **IDLE mode** — robot waits patiently until a person reappears

An ultrasonic sensor provides obstacle avoidance at 30cm, because a robot blindly following someone into a rack is how you create an incident report.

The tech checks in the vendor, assigns the bot, and goes back to real work.

**Stack:** Raspberry Pi 5, Arducam IMX708 wide-angle camera, LK-COKOINO 4WD chassis, L298N motor driver, HC-SR04 ultrasonic sensor, gpiozero + Python. No ROS. No cloud.

## The SO-101 Robot Arm

A robotic arm trained by demonstration to seat fiber optic transceivers into switch ports. A technician shows the arm the task — pick up a transceiver, align it, insert it — and the arm learns to repeat the motion autonomously. No manual programming. You teach by showing.

Built on the HiWonder SO-ARM101 (6-DOF, Feetech servos) using Hugging Face's LeRobot framework. After ~50 demonstrations recorded via leader-follower teleoperation, the system trains an ACT (Action Chunking Transformers) policy that generalizes the motion.

The arm represents where the platform goes next — every repetitive physical task on the DC floor is a candidate for this approach.

## The Dashboard

A unified control panel that ties the system together. Five panels: escort bot position and camera feed, arm task progress and joint angles, scan history with before/after images, training metrics, and system health.

Built on FastAPI with WebSocket for real-time telemetry. Designed with mock-data fallback so the dashboard demonstrates the full experience even when hardware isn't connected, then swaps to real data seamlessly when it is.

## Why It's Reproducible

Every component comes with interactive 3D documentation — step-by-step assembly instructions, GPIO wiring diagrams, and a full DC floor simulation. The system is packaged not just as a demo, but as something another CoreWeave site could understand and build.

Key resources:
- **3D Assembly Guide** — 15-step escort bot build with animated Three.js models
- **Interactive Wiring** — every connection between the Pi, motor driver, sensors, and power
- **DC Floor Simulation** — 10-rack data hall with autonomous bot AI
- **System Topology** — how all components connect

## The Stack

| Layer | Technology |
|-------|-----------|
| Compute | Raspberry Pi 5 (4GB, Bookworm 64-bit) |
| Vision | YOLOv8n (Ultralytics), Arducam IMX708 via libcamera |
| Motor control | gpiozero + L298N via GPIO |
| Steering | Custom dual PID (lateral centering + distance tracking) |
| Arm framework | LeRobot (Hugging Face) + ACT policy |
| Arm hardware | HiWonder SO-ARM101, Feetech STS3215 servos |
| Backend | FastAPI + WebSocket + Pydantic |
| Frontend | Vanilla JS — no frameworks |
| 3D documentation | Three.js (v0.162.0–v0.170.0) |
| Remote access | Tailscale |
| On-device dev | Claude Code running directly on the Pi |

## The Team

Six CoreWeave DCTs from Elk Grove:

| Name | Role |
|------|------|
| **Romeo Patino** | Lead — architecture, software, integration, daily comms |
| **Joshua Tapia** | SO-101 arm — assembly, calibration, ACT training |
| **Alex Murillo** | Escort bot hardware — chassis, wiring, field testing |
| **Parth Patel** | Dashboard backend — FastAPI, data integration |
| **Talha Shakil** | Media — demo video, pitch deck, logo |
| **Raphael Rodea** | Build crew — assembly, labels, logistics, demo day ops |

## The Pitch (One Paragraph)

Elktron is the data hall assistant. An autonomous escort bot follows vendors through the DC, scans racks when they stop, and feeds everything to a live dashboard. The platform extends to a robot arm that learns optic seating by demonstration — same dashboard, same telemetry, same unified control. Every component is documented with interactive 3D guides so another site can reproduce it. Built in 7 days by DCTs, for DCTs, with $430 in off-the-shelf parts. Elktron doesn't replace technicians. It gives them back their time.

## Budget

Total: **~$430** for both robots, all parts, off-the-shelf. No custom fabrication.

---

*CoreWeave "More. Better. Faster." Hackathon — March 23–25, 2026 · Demo Day: March 26*
*Track: Build with Velocity*
