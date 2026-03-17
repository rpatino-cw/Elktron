# Elktron — Demo Video Script (2–3 min)

## Format
Pre-recorded. Screen capture + live robot footage + voiceover.
Target: **2:30** — leaves 30s buffer under 3 min limit.

---

## COLD OPEN — The Problem (0:00–0:25)

**[FOOTAGE: DC floor — racks, cables, a technician walking an aisle with a vendor]**

> "At CoreWeave, our data center technicians seat optics, escort vendors, and inspect racks — every single shift. At a site like EVI01, that's [X] optics seated and [X] vendor escorts per week. Hours of skilled hands on autopilot tasks."

**[TEXT ON SCREEN: "2 tasks. 2 robots. 1 crew."]**

> "We built Elktron — two robots that handle the physical grunt work so our techs can focus on what actually moves the needle."

---

## ROBOT 1 — Escort Bot (0:25–1:10)

**[FOOTAGE: Escort bot on the DC floor, following a person walking between racks]**

> "First — the Escort Bot. Every vendor visit requires a technician to physically shadow them the entire time. That's 30 minutes to 2 hours of a skilled tech being a tour guide instead of turning up racks."

**[FOOTAGE: Close-up of Pi 5 + camera on the mast, chassis rolling]**

> "Our escort bot runs on a Raspberry Pi 5 with a camera doing real-time person detection. It locks onto the vendor, maintains a safe following distance, and stops if anything gets in the way."

**[FOOTAGE: Bot following someone, stopping when they stop, resuming when they walk]**

> "No ROS. No cloud. A Pi, a camera, and Python. The tech checks in the vendor, assigns the bot, and goes back to real work."

**[TEXT ON SCREEN: "Before: 1 tech tied up per vendor visit. After: Zero."]**

---

## ROBOT 2 — SO-101 Arm (1:10–1:55)

**[FOOTAGE: SO-101 arm on a desk, optic module near the gripper, switch panel in front]**

> "Second — the SO-101 arm. Seating optics into switch ports is one of the most repetitive tasks on the floor. It takes a steady hand and costs a tech 5–10 minutes per module. Multiply that across hundreds of ports per rack turn-up."

**[FOOTAGE: Arm performing optic seating — picking up a transceiver, aligning, inserting into port]**
**[FALLBACK: If no live arm footage — show leader-follower training animation, training pipeline diagram, or simulation clip from the dashboard]**

> "We trained the arm using imitation learning — a tech demonstrates the task a few hours, and the arm learns the motion through Hugging Face's LeRobot framework. No hand-coded kinematics. It learns by watching."

**[FOOTAGE: Side-by-side — human demo on leader arm vs. autonomous execution on follower arm]**
**[FALLBACK: Show the training pipeline diagram + code running on screen]**

> "After training, it runs autonomously. Same motion. Same precision. No fatigue. And every new task is just a few more hours of teaching away."

**[TEXT ON SCREEN: "Before: 10 min/optic, human hands. After: Autonomous."]**

---

## THE SYSTEM — Dashboard + Team (1:55–2:20)

**[SCREEN CAPTURE: Elktron dashboard — arm status, escort bot tracking, camera feeds, scan logs]**

> "Both robots feed into a unified dashboard. Arm task progress, escort bot position, live camera feeds, scan history. A tech sees at a glance what's running, what's done, and what needs attention — without walking the floor."

**[FOOTAGE: Tech glancing at a tablet showing the dashboard, then walking to a different task]**

> "This was built by a cross-functional team — DC ops, software engineers, hardware builders, and media — the same kind of crew that runs the floor every day. Elktron doesn't replace technicians. It gives them back their time."

---

## CLOSE — The Pitch (2:20–2:30)

**[FOOTAGE: Both robots side by side on the DC floor. Elktron logo.]**

> "Two robots. Real hardware, real AI, real DC tasks. Physical machines doing physical work on the data center floor."

**[TEXT ON SCREEN: "More floor coverage. Better accuracy. Faster deployments."]**

> "Elktron. More. Better. Faster."

**[END]**

---

## Shot List (for filming)

| # | Shot | Location | Equipment | Duration | Fallback |
|---|------|----------|-----------|----------|----------|
| 1 | DC floor wide — racks + aisle | EVI01 floor | Phone camera | 5s | Stock DC footage |
| 2 | Tech walking with vendor (the "before") | EVI01 floor | Phone camera | 5s | Two people walking any hallway |
| 3 | Escort bot following person — wide | EVI01 floor or lab | Phone + bot | 15s | Simulation clip from `simulation.html` |
| 4 | Escort bot — close-up of Pi + camera + mast | Table/bench | Phone camera | 5s | Photo still with labels |
| 5 | Bot stop/start behavior | Floor or hallway | Phone + bot | 10s | Simulation clip |
| 6 | SO-101 arm — optic seating full task | Desk/bench | Phone + arm | 15s | Training pipeline diagram + code on screen |
| 7 | Leader-follower side-by-side | Desk with both arms | Phone camera | 10s | Animation or LeRobot demo video |
| 8 | Dashboard screen capture | Laptop | Screen recorder | 10s | — |
| 9 | Tech with tablet, walking away | Floor | Phone camera | 5s | — |
| 10 | Both robots together — hero shot | Floor or bench | Phone camera | 5s | Side-by-side renders from Blender |

## Fallback Strategy

**If arm kit arrives late (ETA 3/18, demo 3/23):**
- **Plan A:** Full live demo — arm + bot running on the floor
- **Plan B (no arm hardware):** Show the training pipeline, code, and LeRobot framework running on laptop. Use dashboard arm panel with mock telemetry. Narrate: "The software is production-ready — waiting on hardware to ship."
- **Plan C (nothing works live):** Pre-recorded clips from any successful test + simulation pages + dashboard demo. Lean hard on the escort bot (hardware arrives earlier).

**If escort bot motors don't cooperate:**
- Show camera-only detection running on Pi (`test_camera.py` with `--display`) — proves the AI works even if wheels don't spin
- Use `simulation.html` for the floor demo footage

## Voiceover Notes
- Tone: Confident, no-BS, DC-floor energy. A builder explaining what they built.
- Pace: Steady. Don't rush. Let the footage breathe.
- Record VO separately, lay over footage in edit.
- **Say the theme words.** "More. Better. Faster." should be heard at least once.

## Music
- Subtle, low-energy electronic. Think documentary, not hype reel.
- Recommend: Artlist or Epidemic Sound free trial — search "tech documentary minimal"

## Judge Q&A Prep

| Likely Question | Answer |
|---|---|
| "Does the arm actually work?" | Be honest about current state. If trained: "Yes, here's the demo." If not: "Software is production-ready. Hardware arrived [date]. Phase 1 is the pipeline, phase 2 is full autonomy." |
| "How accurate is the person detection?" | "MobileNet SSD v2 via OpenCV DNN runs at ~20 FPS on a Pi 5. Accuracy is strong for single-person tracking in a controlled aisle environment." |
| "What happens when the vendor goes to the bathroom?" | "The bot enters idle mode — it stops and waits. When the person reappears in frame, it resumes following." |
| "How does this scale beyond one bot?" | "Each bot is a standalone Pi. The dashboard already supports multiple bot feeds. Scaling is adding hardware, not rewriting software." |
| "What's the cost per unit?" | "Escort bot: ~$100 in parts plus a Pi you already own. Arm: ~$300 for the kit. Both under $500 total." |
| "Why not just use an existing robot platform?" | "We evaluated iRobot Create 3, SunFounder PiCar-X, and others. They're either overkill, too expensive, or don't fit the DC floor use case. This is purpose-built." |
| "How do you develop on the robot?" | "Claude Code runs directly on the Pi. We debug and tune motor speeds, detection thresholds, and sensor logic on the actual hardware — no laptop required. On demo day, if something needs a tweak, we fix it on the spot." |

## Placeholders to Fill (BEFORE RECORDING)

- [ ] **[X] optics seated per week** — get real number from Romeo / EVI01 floor data
- [ ] **[X] vendor escorts per week** — get real number from Romeo / EVI01 floor data
- [ ] Confirm "20 FPS" claim with actual Pi 5 test (`test_camera.py`)
- [ ] Decide: is the arm demo live footage or fallback?
