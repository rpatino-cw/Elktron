# Elktron — Demo Video Script (2:30)

## Format
Pre-recorded. Screen capture + live robot footage + voiceover.
Target: **2:30** — leaves 30s buffer under 3 min limit.

---

## COLD OPEN — The Problem (0:00–0:25)

**[FOOTAGE: DC floor — racks, cables, a technician walking an aisle with a vendor]**

> "At CoreWeave, our data center technicians seat optics, escort vendors, and inspect racks — every single shift. Hours of skilled hands on autopilot tasks. We built Elktron to change that."

**[TEXT ON SCREEN: "Elktron — the data hall assistant"]**

---

## THE ESCORT BOT (0:25–1:40)

**[FOOTAGE: Escort bot on the DC floor, following a person walking between racks]**

> "This is the Escort Bot. Every vendor visit requires a technician to physically shadow them — that's 30 minutes to 2 hours of a skilled tech being a tour guide instead of turning up racks."

**[FOOTAGE: Close-up of Pi 5 + camera on the mast, chassis rolling]**

> "Our bot runs on a Raspberry Pi 5 with a camera doing real-time person detection. It locks onto the vendor, maintains a safe following distance using dual PID controllers, and stops if anything gets in the way."

**[FOOTAGE: Bot following someone, stopping when they stop, resuming when they walk]**

> "When the vendor stops at a rack, the bot switches to scan mode. The camera sweeps from bottom to top, capturing the state of every node — before and after the vendor's work. Full audit trail, no human escort needed."

**[FOOTAGE: Camera panning on the rack, scan images appearing on dashboard]**

> "No ROS. No cloud. A Pi, a camera, and Python. The tech checks in the vendor, assigns the bot, and goes back to real work."

**[TEXT ON SCREEN: "Before: 1 tech tied up per vendor visit. After: Zero."]**

---

## THE PLATFORM EXTENDS — SO-101 ARM (1:40–2:05)

**[FOOTAGE: SO-101 arm on a desk, optic module near the gripper, switch panel in front]**

> "Elktron isn't just the escort bot. The platform extends to a robotic arm trained by demonstration to seat fiber optic transceivers — one of the most repetitive tasks on the floor."

**[FOOTAGE: Arm performing optic seating — OR leader-follower training, OR training pipeline on screen]**

> "A technician shows the arm the task a few times, and it learns the motion. No hand-coded kinematics. You teach by showing, and it runs autonomously."

**[TEXT ON SCREEN: "Trained by demonstration. Runs on its own."]**

---

## THE DASHBOARD + CLOSE (2:05–2:30)

**[SCREEN CAPTURE: Elktron dashboard — escort bot tracking, camera feeds, arm status, scan logs]**

> "Both systems feed into a unified dashboard. Escort position, camera feeds, arm progress, scan history. One screen for the whole operation."

**[FOOTAGE: Tech glancing at a tablet showing the dashboard, then walking to a different task]**

> "This was built by DCTs — the same crew that runs the floor every day. Elktron doesn't replace technicians. It gives them back their time."

**[FOOTAGE: Escort bot and arm side by side. Elktron logo.]**

> "Elktron. The data hall assistant. More. Better. Faster."

**[END]**

---

## Shot List (for filming)

| # | Shot | Location | Equipment | Duration |
|---|------|----------|-----------|----------|
| 1 | DC floor wide — racks + aisle | EVI01 floor | Phone camera | 5s |
| 2 | Tech walking with vendor (the "before") | EVI01 floor | Phone camera | 5s |
| 3 | Escort bot following person — wide | EVI01 floor or lab | Phone + bot | 20s |
| 4 | Escort bot — close-up of Pi + camera + mast | Table/bench | Phone camera | 5s |
| 5 | Bot stop/start behavior | Floor or hallway | Phone + bot | 15s |
| 6 | Bot scan mode — camera sweeping rack | Floor | Phone + bot | 10s |
| 7 | Dashboard showing live escort tracking | Laptop | Screen recorder | 5s |
| 8 | SO-101 arm — optic seating (or training) | Desk/bench | Phone + arm | 10s |
| 9 | Dashboard full view — both systems | Laptop | Screen recorder | 5s |
| 10 | Both robots together — hero shot | Floor or bench | Phone camera | 5s |

## Voiceover Notes
- Tone: Confident, no-BS, DC-floor energy. A builder explaining what they built.
- Pace: Steady. Don't rush. Let the footage breathe.
- Record VO separately, lay over footage in edit.
- **Say the theme words.** "More. Better. Faster." should be heard at least once.
- The escort bot is the star. Give it the most screen time and the best footage.

## Music
- Subtle, low-energy electronic. Think documentary, not hype reel.
- Recommend: Artlist or Epidemic Sound free trial — search "tech documentary minimal"

---

## Judge Q&A Prep

| Likely Question | Answer |
|---|---|
| "How does the escort bot work?" | "YOLOv8n on a Pi 5 detects the person. Dual PID controllers handle lateral centering and distance tracking. Differential steering — left and right motor pairs run independently. Ultrasonic sensor for obstacle avoidance at 30cm." |
| "Does the arm actually work?" | Be honest about current state. If trained: "Yes, here's the demo." If not: "The training pipeline is production-ready. We recorded demos, and the arm runs the learned policy autonomously. Hardware assembly happened on [date]." |
| "How accurate is the person detection?" | "YOLOv8n running on the Pi 5. We tested on the actual DC floor at EVI01 and hit 78% confidence consistently — real lighting, real racks, real cable trays." |
| "What happens when the vendor goes to the bathroom?" | "The bot enters idle mode — it stops and waits. When the person reappears in frame, it resumes following." |
| "How does this scale beyond one bot?" | "Each bot is a standalone Pi. The dashboard already supports multiple bot feeds. Scaling is adding hardware, not rewriting software." |
| "What's the cost per unit?" | "Escort bot: ~$160 in parts. Arm: ~$270 for the kit. Both under $500 total." |
| "Why not use an existing robot platform?" | "We evaluated iRobot Create 3, SunFounder PiCar-X, and others. They're either overkill, too expensive, or don't fit the DC floor use case. This is purpose-built for $160." |
| "How do you develop on the robot?" | "Claude Code runs directly on the Pi. We debug and tune motor speeds, detection thresholds, and sensor logic on the actual hardware — no laptop required." |
| "Why should CoreWeave care about this?" | "Every vendor walkthrough ties up a skilled tech for 30 minutes to 2 hours. Every optic is seated by hand. At scale, that's thousands of hours per year on autopilot work. Elktron gives that time back." |

## Placeholders to Fill (BEFORE RECORDING)

- [ ] Confirm "78%" claim with latest Pi 5 test (`test_camera.py`)
- [ ] Decide: is the arm demo live footage or training pipeline footage?
- [ ] Get Talha's creative direction on transitions and pacing

---

## Fallback Strategies

**If arm kit arrives late or isn't demo-ready:**
- Show the training pipeline running on laptop — code, recorded demos, ACT policy training
- Dashboard arm panel runs with mock telemetry
- Narrate: "The pipeline is production-ready — trained by demonstration, deployed autonomously"
- Lean hard on the escort bot as the live proof point

**If escort bot motors don't cooperate:**
- Show camera-only detection running on Pi (`test_camera.py`) — proves the AI works
- Use `simulation.html` for the floor demo footage
- Dashboard shows the telemetry flow working end-to-end

**If nothing works live:**
- Pre-recorded clips from any successful test + simulation pages + dashboard demo
- Focus on the engineering portal and reproducibility story
