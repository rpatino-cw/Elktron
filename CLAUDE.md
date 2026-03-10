# FloorCrew — Hackathon Project Config

## Key Info
- **Event:** March 23–25, 2026
- **Demo Day:** March 26 (2–5pm ET)
- **Sign-up deadline:** March 12, 2026 — channel: `#more-better-faster-2026`
- **Deliverable:** 2–3 min pre-recorded demo + optional slides + GitHub repo
- **Track:** Build with Velocity

## Focus Check (run at session start — one line only)

> `Session: Hackathon | Status: LOCKED — FloorCrew (two robots) | Sign-up: March 12`

---

## Project: FloorCrew

Two robots for the DC floor. One project, three components:

| Component | Path | What It Does |
|-----------|------|-------------|
| **SO-101 Arm** | `robotics-site/so101/` | Imitation learning for DC tasks — optic seating, rack inspection. LeRobot + ACT policy. |
| **Escort Bot** | `escort-bot/` | Person-following vendor escort. Pi 5 + TFLite MobileNet SSD + Freenove 4WD. |
| **Dashboard** | `floorcrew-app/` | Unified control panel — arm status, escort tracking, camera feeds, scan logs. FastAPI + vanilla JS. |

## Key Docs

| Doc | What |
|-----|------|
| `CHECKLIST-SO101.md` | Full arm build checklist (10 phases) |
| `CHECKLIST-ESCORT-BOT.md` | Full bot build checklist (11 phases) |
| `PROGRESS.md` | What's done, what's next, hardware status |
| `PARTS-LIST.md` | Hardware shopping list + costs |
| `VELOCITY.md` | Engineering philosophy |
| `WORKFLOW.md` | Day-of timeline |

## Judging Tracks
1. **Build with Velocity** — AI to accelerate dev or DC construction (OUR TRACK)
2. Productivity at Scale — 10x faster workflows
3. Win the Customer — speed to production

## Bonus Categories
- People's Choice
- Cross Functional Team
- Most Company OKRs

## Winning Formula
- Specificity beats generality
- Closed loop > visualization
- Physical world beats software toys
- Measurable delta beats vibes
- Authenticity > flash
