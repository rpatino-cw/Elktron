# Elktron — Demo Video Script (2–3 min)

## Format
Pre-recorded. Screen capture + live robot footage + voiceover.
Target: **2:30** — leaves 30s buffer under 3 min limit.

---

## COLD OPEN — The Problem (0:00–0:25)

**[FOOTAGE: DC floor — racks, cables, a technician walking an aisle with a vendor]**

> "At CoreWeave, we run some of the densest GPU data centers in the world. Our DCTs — data center technicians — handle everything from seating optics to escorting vendors across the floor. These tasks are manual, repetitive, and take skilled hands away from higher-value work."

**[TEXT ON SCREEN: "2 tasks. 2 robots. 1 crew."]**

> "We built Elktron — two robots that handle the physical grunt work so our techs can focus on what matters."

---

## ROBOT 1 — Escort Bot (0:25–1:10)

**[FOOTAGE: Escort bot on the DC floor, following a person walking between racks]**

> "First — the Escort Bot. Every time a vendor comes on-site, a technician has to physically walk with them the entire time. That's 30 minutes to 2 hours of a skilled tech being a tour guide."

**[FOOTAGE: Close-up of Pi 5 + camera on the Freenove chassis]**

> "Our escort bot uses a Raspberry Pi 5 with a camera running MobileNet SSD — real-time person detection at 20 frames per second. It locks onto the vendor, maintains a safe following distance, and stops if anything gets in the way."

**[FOOTAGE: Bot following someone, stopping when they stop, resuming when they walk]**

> "No ROS. No cloud. Just a Pi, a camera, and 150 lines of Python. The tech checks in the vendor, assigns the bot, and goes back to real work."

**[TEXT ON SCREEN: "Before: 1 tech tied up per vendor visit. After: Zero."]**

---

## ROBOT 2 — SO-101 Arm (1:10–1:55)

**[FOOTAGE: SO-101 arm on a desk, optic module in the gripper, switch panel in front]**

> "Second — the SO-101 arm. Seating optics into switch ports is one of the most common tasks on the floor. It takes a steady hand and costs a tech 5–10 minutes per module. Multiply that by hundreds of ports per rack turn-up."

**[FOOTAGE: Arm performing optic seating — picking up a transceiver, aligning, inserting into port]**

> "We trained the arm using imitation learning. A tech demonstrates the task 50 times using a leader-follower setup. The arm watches, records, and learns the motion through Hugging Face's LeRobot framework."

**[FOOTAGE: Side-by-side — human demo on leader arm vs. autonomous execution on follower arm]**

> "After training, it runs autonomously. Same motion. Same precision. No fatigue. And every new task — cable routing, rack inspection — is just 50 more demos away."

**[TEXT ON SCREEN: "Before: 10 min/optic, human hands. After: Autonomous."]**

---

## THE SYSTEM — Dashboard (1:55–2:15)

**[SCREEN CAPTURE: Elktron dashboard — arm status, escort bot tracking, camera feeds]**

> "Both robots feed into a single dashboard. Arm task status, escort bot location, live camera feeds, training logs. One screen to manage the whole crew."

**[FOOTAGE: Tech glancing at a tablet showing the dashboard, then walking to a different task]**

> "Elktron doesn't replace technicians. It gives them back their time."

---

## CLOSE — The Pitch (2:15–2:30)

**[FOOTAGE: Both robots side by side on the DC floor. Elktron logo.]**

> "Two robots. Built in 48 hours. Real hardware, real AI, real DC tasks. No wrappers, no dashboards pretending to be products. Just machines doing the work."

**[TEXT ON SCREEN: "Elktron — Build with Velocity"]**

> "Elktron. More hands on the floor."

**[END]**

---

## Shot List (for filming)

| # | Shot | Location | Equipment | Duration |
|---|------|----------|-----------|----------|
| 1 | DC floor wide — racks + aisle | EVI01 floor | Phone camera | 5s |
| 2 | Tech walking with vendor (the "before") | EVI01 floor | Phone camera | 5s |
| 3 | Escort bot following person — wide | EVI01 floor or lab | Phone + bot | 15s |
| 4 | Escort bot — close-up of Pi + camera | Table/bench | Phone camera | 5s |
| 5 | Bot stop/start behavior | Floor or hallway | Phone + bot | 10s |
| 6 | SO-101 arm — optic seating full task | Desk/bench | Phone + arm | 15s |
| 7 | Leader-follower side-by-side | Desk with both arms | Phone camera | 10s |
| 8 | Dashboard screen capture | Laptop | Screen recorder | 10s |
| 9 | Tech with tablet, walking away | Floor | Phone camera | 5s |
| 10 | Both robots together — hero shot | Floor or bench | Phone camera | 5s |

## Voiceover Notes
- Tone: Confident, no-BS, DC-floor energy. Not a sales pitch — a builder explaining what they built.
- Pace: Steady. Don't rush. Let the footage breathe.
- Record VO separately, lay over footage in edit.

## Music
- Subtle, low-energy electronic. Think documentary, not hype reel.
- Recommend: Artlist or Epidemic Sound free trial — search "tech documentary minimal"
