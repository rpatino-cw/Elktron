# Elktron — Countdown to Demo Day

**Last updated:** 2026-03-21 (update every morning)

---

## Hard Rules

1. **Escort bot (RC) done by Monday 3/24.** No exceptions. This is the star of the demo.
2. **ARM GO/NO-GO: Monday 3/24 end of day.** If it's not assembled, calibrated, and running a basic teleop — cut it from the demo. One perfect robot > two broken robots.
3. **Feature freeze: Tuesday 3/25 noon.** After that, only bug fixes, video recording, and polish.
4. **Romeo does not push code while Josh/Parth are working onsite.** They own the repo during their sessions.

---

## Day-by-Day

### Friday 3/21 — Integration Sprint

| Task | Owner | Status |
|------|-------|--------|
| Pull latest repo on Pi | Josh | [x] Done |
| Dashboard running on Josh's laptop | Josh, Parth | [ ] |
| Set Pi IP in `escort.py` line 36, test connectivity | Josh | [ ] |
| Camera feed streaming Pi → dashboard | Josh | [ ] |
| Xbox controller teleoperation — bot drives | Josh | [ ] |
| YOLOv8n detection running on Pi camera | Josh, Parth | [ ] |
| Fix L298N 5V logic pin if not done | Josh, Parth | [ ] |
| Demo script review (remote) | Romeo | [ ] |
| Pitch deck polish (remote) | Romeo | [ ] |

**End-of-day check:** Can the bot drive via controller and stream camera to dashboard?

---

### Saturday 3/22 — Arm Print + Bot Tuning

| Task | Owner | Status |
|------|-------|--------|
| 3D print SO-101 arm parts (overnight print OK) | Josh | [ ] |
| PID tuning — smoother person following | Josh, Parth | [ ] |
| Ultrasonic sensor wired + tested | Josh, Parth | [ ] |
| PVC mast + camera elevation mounted | Onsite crew | [ ] |
| Wire cleanup — velcro, zip ties, clean routing | Onsite crew | [ ] |
| Dashboard polish — Drive & Detection panel | Romeo (remote) | [ ] |
| Repo README cleanup for judges | Romeo | [ ] |

**End-of-day check:** Bot follows a person smoothly. Arm parts printing.

---

### Sunday 3/23 — Hackathon Day 1: Bot Complete + Arm Assembly

| Task | Owner | Status |
|------|-------|--------|
| Escort bot end-to-end: follow + scan + dashboard | Josh, Parth | [ ] |
| Record phone video of bot following person | Anyone onsite | [ ] |
| Assemble SO-101 arm (3D-printed parts ready) | Josh | [ ] |
| Install LeRobot, calibrate servos | Josh | [ ] |
| First arm teleop test | Josh | [ ] |
| Coordinate with Talha on filming plan | Romeo | [ ] |

**End-of-day check:** Bot demo-ready. Arm assembled and servos responding.

---

### Monday 3/24 — Hackathon Day 2: ARM GO/NO-GO

| Task | Owner | Status |
|------|-------|--------|
| Arm basic teleop working? | Josh | [ ] |
| **GO/NO-GO DECISION (end of day):** | Team | [ ] |
| → GO: Record 50 optic seating demos, start ACT training | Josh | [ ] |
| → NO-GO: Cut arm from demo, double down on escort bot | Team | [ ] |
| Escort bot floor test — real DC aisle | Onsite crew | [ ] |
| Escort bot scan mode — camera sweeps rack | Onsite crew | [ ] |
| Dashboard with live data — ready for screen recording | Josh | [ ] |
| B-roll filming — bot on floor, wiring, Pi boot | Talha, Raphael | [ ] |

**End-of-day check:** Arm decision locked. Escort bot runs clean on DC floor.

---

### Tuesday 3/25 — Hackathon Day 3: FEATURE FREEZE + VIDEO

**NOON: FEATURE FREEZE. No new code after this.**

| Task | Owner | Status |
|------|-------|--------|
| Morning: final bug fixes only | Josh, Parth | [ ] |
| NOON: Feature freeze — lock it down | Team | [ ] |
| Record demo video (2:30 target) | Talha + team | [ ] |
| Screen-record dashboard walkthrough | Romeo or Josh | [ ] |
| Record voiceover (separate track) | Romeo | [ ] |
| Edit video — footage + VO + music | Talha | [ ] |
| If arm GO: record arm demo footage | Josh | [ ] |
| Slides/pitch deck finalized | Romeo, Talha | [ ] |
| GitHub repo — clean README, screenshots, links | Romeo | [ ] |
| Submit video + repo + slides | Talha | [ ] |

**End-of-day check:** Video submitted. Repo pushed. Slides done.

---

### Wednesday 3/26 — DEMO DAY (11am-2pm PT / 2pm-5pm ET)

| Task | Owner | Time |
|------|-------|------|
| Pack hardware — bot, arm (if GO), power banks, cables, laptop | Raphael | Morning |
| Set up demo table — bot on display, dashboard on screen | Team | 10:30am PT |
| Test live demo — bot drives, dashboard streams | Josh | 10:45am PT |
| Charge all batteries | Raphael | Night before |
| Presentations begin | Team | 11:00am PT |
| Raphael plays "vendor" during live demo | Raphael | During demo |

---

## Talha's Deliverables — Media & Presentation Timeline

| Deadline | Deliverable | Notes |
|----------|-------------|-------|
| **Sun 3/23** | Filming plan finalized | Coordinate with Romeo on shot list (`docs/DEMO-SCRIPT.md`) |
| **Mon 3/24** | B-roll filmed | Bot on DC floor, wiring close-ups, Pi boot, terminal output, team working |
| **Mon 3/24 EOD** | Logo + team signage ready | Printed for demo table |
| **Tue 3/25 morning** | All live robot footage filmed | Bot following person, scan mode, arm demo (if GO) |
| **Tue 3/25 noon** | Screen recordings done | Dashboard walkthrough, training pipeline (if arm GO) |
| **Tue 3/25 afternoon** | Voiceover recorded | Romeo records VO, Talha receives audio track |
| **Tue 3/25 evening** | Video edited + exported | 2:30 target, footage + VO + music layered |
| **Tue 3/25 night** | Slides finalized | With Romeo — 5-7 slides max |
| **Tue 3/25 EOD** | **SUBMIT: video + repo + slides** | Final deliverable — non-negotiable deadline |

**Talha needs from the team:**
- Shot list approval by Sunday (Romeo)
- Working robot on DC floor by Monday (Josh)
- Dashboard running live by Monday (Josh)
- Voiceover audio by Tuesday noon (Romeo)
- Arm GO/NO-GO by Monday EOD (determines what to film Tuesday)

---

## Giving Talha Filmable Moments

Talha can't edit what doesn't exist. The team's #1 job Monday is creating footage, not writing code.

**What Talha needs filmed (and who makes it happen):**

| Footage | Who Sets It Up | When | Notes |
|---------|---------------|------|-------|
| Bot following a person through DC aisle (wide shot) | Josh drives bot, Raphael walks as "vendor" | Mon 3/24 | THE hero shot. Get 3-4 takes minimum. |
| Bot stop/start behavior — vendor stops, bot stops | Same setup | Mon 3/24 | Shows intelligence, not just driving |
| Bot scan mode — camera sweeps rack | Josh triggers scan | Mon 3/24 | Slow, dramatic tilt. Talha films from side. |
| Close-up: Pi 5 + camera on mast, chassis rolling | Anyone | Mon 3/24 | B-roll. Show the hardware. |
| Dashboard with live data on laptop screen | Josh has dashboard running | Mon 3/24 | Screen-record AND film the laptop from over-shoulder |
| Arm optic seating (if GO) | Josh demos arm | Tue 3/25 morning | Even 1 successful grab is enough |
| Arm training — leader-follower teleop | Josh | Tue 3/25 morning | Shows "teach by demonstration" |
| Team working — wiring, terminal, debugging | Anyone | Mon 3/24 | Candid B-roll. Shows builder energy. |
| DC environment — racks, aisles, cables | Anyone with phone | Mon 3/24 | Sets the scene. 5-10 seconds is enough. |
| Pi boot sequence — terminal scrolling | Anyone | Anytime | Cool visual for transitions |

**How to make this happen:**
1. **Sunday:** Romeo coordinates with Talha on shot list above. Talha confirms he has a phone/camera ready.
2. **Monday morning:** Josh gets bot driving + dashboard live. This is Talha's filming window.
3. **Monday midday:** Talha films all bot footage (30-45 min dedicated filming session). Josh and Raphael support.
4. **Monday afternoon:** Talha films B-roll (team working, DC environment, hardware close-ups).
5. **Tuesday morning:** If arm is GO, Talha films arm footage. If NO-GO, skip — Talha starts editing.
6. **Tuesday noon:** Romeo records voiceover. Sends audio to Talha.
7. **Tuesday afternoon-evening:** Talha edits. Team reviews. Final export.

**Rule:** Monday is filming day, not coding day. If something isn't working by Monday morning, don't spend all day debugging — film what IS working and move on.

---

## Fallback: Single-Robot Demo (if arm is cut)

The demo becomes 100% escort bot:
- **More screen time** for bot following + scanning
- **Dashboard** shows escort tracking, camera feeds, scan logs (arm panel shows "Coming Soon" or mock data)
- **Narration** mentions the arm as "next phase" — pipeline is built, just needs hardware time
- **Demo script adjustment:** expand bot section from 1:15 to 1:45, shrink arm section to a 15s "what's next" teaser
- Reference `docs/DEMO-SCRIPT.md` → Fallback Strategies section

---

## Demo Day Packing Checklist

- [ ] Escort bot (fully assembled, clean wiring)
- [ ] SO-101 arm (if GO)
- [ ] Raspberry Pi 5 + power bank + USB-C cable
- [ ] Laptop (dashboard ready to run)
- [ ] Xbox controller
- [ ] Phone for backup filming
- [ ] Extension cord / power strip
- [ ] Spare 18650 batteries (charged)
- [ ] Spare USB-C power bank
- [ ] Printed team name card / signage
