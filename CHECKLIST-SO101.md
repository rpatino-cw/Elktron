# SO-101 Robot Arm — Full Build Checklist

> Elktron Hackathon | CoreWeave March 2026
> Framework: LeRobot (HuggingFace) | Hardware: HiWonder SO-ARM101 kit

---

## Phase 1: Procurement & Inventory

### Parts Sourcing
- [ ] Order SO-101 kit from HiWonder (~$270) — https://www.hiwonder.com/products/lerobot-so-101
- [ ] Confirm kit includes: 2x arms (leader + follower), 12x Feetech STS3215 servos, 2x BusLinker V3.0 boards, USB-C cables, 3D-printed structural parts
- [ ] Order 12V 5A DC power supply (for follower arm) — if not included in kit
- [ ] Order 5V power supply (for leader arm) — if not included in kit
- [ ] Order USB webcam (Logitech C920 or similar, 1080p) — for wrist/overhead camera
- [ ] Order USB-C hub if laptop has limited ports (need 3 USB: 2 arms + 1 camera)
- [ ] Order table clamps or heavy base plate — arms need rigid mounting
- [ ] Optional: order optic transceiver tray (3D print from `optic-staging-tray.blend`)

### Inventory Check (before assembly day)
- [ ] 2 arms (leader = lighter, follower = heavier) present
- [ ] 12 servos (6 per arm) — all spin freely, none DOA
- [ ] 2 BusLinker V3.0 boards present
- [ ] 2 USB-C cables (data-capable, not charge-only)
- [ ] 12V 5A PSU present and tested
- [ ] 5V PSU present and tested
- [ ] Webcam present and working on laptop
- [ ] Small Phillips screwdriver set
- [ ] Velcro strips (for cable management demo)
- [ ] Optic transceivers (real or dummy) for seating demo

---

## Phase 2: Mechanical Assembly

### Leader Arm (teleoperation input)
- [ ] Unbox and lay out all leader arm parts
- [ ] Identify servo positions: base (S1), shoulder (S2), elbow (S3), wrist pitch (S4), wrist roll (S5), gripper (S6)
- [ ] Mount S1 (base) servo into base plate — ensure rotation axis is vertical
- [ ] Mount S2 (shoulder) servo — attach upper arm link
- [ ] Mount S3 (elbow) servo — attach forearm link
- [ ] Mount S4 (wrist pitch) servo
- [ ] Mount S5 (wrist roll) servo
- [ ] Mount S6 (gripper) servo — attach gripper fingers
- [ ] Route all servo cables cleanly down the arm — velcro strap at each joint
- [ ] Connect all 6 servo cables to BusLinker V3.0 board (daisy chain bus)
- [ ] Connect 5V PSU to leader BusLinker
- [ ] Connect USB-C from leader BusLinker to laptop
- [ ] Clamp leader arm to table — firm, no wobble

### Follower Arm (autonomous output)
- [ ] Repeat full assembly for follower arm (same steps as leader)
- [ ] Mount S1–S6 servos in identical positions to leader
- [ ] Route cables, velcro strap at joints
- [ ] Connect all 6 servo cables to follower BusLinker V3.0 board
- [ ] Connect 12V 5A PSU to follower BusLinker (higher voltage = more torque)
- [ ] Connect USB-C from follower BusLinker to laptop
- [ ] Clamp follower arm to table — ~30cm from leader arm
- [ ] Mount webcam overhead or on wrist bracket, pointing at follower workspace

### Mechanical Verification
- [ ] Manually move each leader arm joint — smooth, no binding, no grinding
- [ ] Manually move each follower arm joint — smooth, no binding
- [ ] Verify gripper opens and closes fully on both arms
- [ ] Confirm neither arm hits table/obstacles at full range of motion
- [ ] Check all screws are tight — loose screws = drift during training
- [ ] Verify cable routing doesn't snag during full arm sweep

---

## Phase 3: Electronics & Wiring

### Connection Diagram
```
Laptop / Pi 5
  ├── USB-C → BusLinker V3.0 (Follower) → /dev/ttyACM0
  ├── USB-C → BusLinker V3.0 (Leader)   → /dev/ttyACM1
  └── USB-A → Webcam                     → camera_index=0

Power (separate from data):
  ├── 12V 5A PSU → Follower BusLinker (wall outlet)
  └── 5V PSU     → Leader BusLinker (wall outlet)
```

### Wiring Checks
- [ ] Follower BusLinker powered by 12V — LED on board lights up
- [ ] Leader BusLinker powered by 5V — LED on board lights up
- [ ] USB-C cables are data-capable (not charge-only) — test with `lsusb` or `ls /dev/ttyACM*`
- [ ] Follower detected as `/dev/ttyACM0` (or similar) — run `ls /dev/ttyACM*`
- [ ] Leader detected as `/dev/ttyACM1` (or similar)
- [ ] Webcam detected — run `ls /dev/video*` or `v4l2-ctl --list-devices`
- [ ] No USB bandwidth conflicts — if issues, use separate USB controllers (not same hub)

### Servo Configuration
- [ ] Each servo has unique ID (1–6 per arm) — factory default should be correct
- [ ] If IDs conflict, use Feetech servo configuration tool to reassign
- [ ] Test each servo responds to ping: `python -c "from lerobot.common.robot_devices.motors.feetech import FeetechMotorsBus; ..."`
- [ ] Verify servo direction — positive angle = expected direction for each joint
- [ ] Set servo speed limits if available (prevent damage during first tests)

---

## Phase 4: Software Environment Setup

### Compute Decision
- [ ] Decide primary compute: MacBook (M-series) / Linux laptop (NVIDIA GPU) / Pi 5
- [ ] For training: MacBook M1+ (`--device mps`) or Google Colab (free T4 GPU)
- [ ] For deployment: laptop or Pi 5 (Pi 5 can run inference, not training)

### Python Environment
- [ ] Install Python 3.10+ (3.11 recommended)
- [ ] Create virtual environment: `python3 -m venv ~/lerobot-env`
- [ ] Activate: `source ~/lerobot-env/bin/activate`
- [ ] Install LeRobot: `pip install lerobot` (or clone repo for latest)
- [ ] Install additional deps: `pip install torch torchvision opencv-python tensorboard`
- [ ] Verify torch backend: `python -c "import torch; print(torch.backends.mps.is_available())"` (Mac) or `torch.cuda.is_available()` (NVIDIA)
- [ ] Run `so101/install.sh` — verify no errors
- [ ] Verify `so101/requirements.txt` deps all installed

### LeRobot Configuration
- [ ] Create robot config YAML (or use default SO-101 config from LeRobot)
- [ ] Set correct serial ports: `leader_port: /dev/ttyACM1`, `follower_port: /dev/ttyACM0`
- [ ] Set camera config: `camera_index: 0`, resolution, FPS
- [ ] Set servo ID mapping for each joint (1–6)
- [ ] Test config loads without error: `python -c "from lerobot.common.robot_devices.robots.manipulator import ManipulatorRobot; ..."`

### Camera Setup
- [ ] Webcam streams live: `python -c "import cv2; cap=cv2.VideoCapture(0); ret,f=cap.read(); print(ret, f.shape)"`
- [ ] Resolution is adequate (at least 640x480, prefer 1280x720)
- [ ] Frame rate is stable (>15 FPS)
- [ ] Camera sees the full follower arm workspace
- [ ] Lighting is adequate — no deep shadows on workspace
- [ ] If using Pi Camera Module: test with `libcamera-hello --timeout 5000`

---

## Phase 5: Calibration

### Servo Calibration
- [ ] Run LeRobot calibration routine: `python lerobot/scripts/control_robot.py calibrate --robot-path <config>`
- [ ] Move each joint to physical limits when prompted
- [ ] Record min/max angles for all 6 joints on both arms
- [ ] Verify leader and follower have matching calibration ranges
- [ ] Save calibration file — do NOT lose this
- [ ] Test: move leader joint 1 to 90 degrees — follower joint 1 should match exactly
- [ ] Test: move leader joint 2 to 45 degrees — follower joint 2 matches
- [ ] Repeat for all 6 joints — each should mirror within ~2 degrees

### Workspace Calibration
- [ ] Define "home" position for follower arm (all joints at neutral)
- [ ] Mark home position with tape on table
- [ ] Define optic tray position — mark with tape
- [ ] Define switch port position — mark with tape
- [ ] Verify follower can reach: home → tray → switch port → home
- [ ] Measure and note distances between positions (for debugging)

---

## Phase 6: Teleoperation (Data Collection)

### Leader-Follower Teleoperation
- [ ] Launch teleoperation: `python lerobot/scripts/control_robot.py teleoperate --robot-path <config>`
- [ ] Verify: moving leader arm causes follower to mirror in real-time
- [ ] Test responsiveness — latency should be <100ms
- [ ] Practice the optic seating task manually (leader) 5+ times before recording
- [ ] Practice smoothly: grab optic → lift → move to port → seat → release → retract

### Keyboard Teleoperation (backup, no leader arm needed)
- [ ] Install keyboard teleop branch: `pip install git+https://github.com/seanxu112/lerobot.git@teleop`
- [ ] Launch: `python lerobot/scripts/control_robot.py teleoperate --robot-path <config> --teleop-type keyboard`
- [ ] Map keys to joints — practice moving arm with keyboard
- [ ] This is slower but works as backup if leader arm has issues

### Recording Episodes
- [ ] Create dataset directory: `mkdir -p data/optic_seating`
- [ ] Start recording: `python so101/record.py` (or LeRobot record command)
- [ ] Record episode 1: home → pick optic → seat in port → retract → home
- [ ] Review episode 1 video — is the motion clean? Camera captures full action?
- [ ] Record episodes 2–10 — vary starting position slightly each time
- [ ] Record episodes 11–30 — aim for consistent, smooth motions
- [ ] Record episodes 31–50 — add minor variations (optic angle, approach path)
- [ ] Target: 50 episodes minimum, 100+ is better for robust policy
- [ ] Each episode should be 10–30 seconds
- [ ] Verify dataset: check video files exist, joint angle CSVs look correct
- [ ] Backup dataset to external drive or cloud (DO NOT lose training data)

### Recording Quality Checks
- [ ] No dropped frames in video recordings
- [ ] Joint angles recorded at consistent frequency (50Hz typical)
- [ ] Camera angle didn't shift between episodes
- [ ] Lighting didn't change significantly between episodes
- [ ] No table bumps or arm mount shifts during recording
- [ ] Episodes where the arm collided or dropped the optic — DELETE those

---

## Phase 7: Training (Policy Learning)

### Pre-Training
- [ ] Decide training compute: Mac MPS (2–4 hrs), NVIDIA GPU (1–2 hrs), Colab (3–5 hrs)
- [ ] If Colab: upload dataset zip, set up notebook, verify GPU runtime
- [ ] Choose policy: ACT (Action Chunking with Transformers) recommended for manipulation
- [ ] Review training config: batch size, learning rate, epochs, chunk size

### Training Run
- [ ] Start training: `python so101/train.py` (or LeRobot train command)
- [ ] Monitor loss curve via TensorBoard: `tensorboard --logdir outputs/`
- [ ] Loss should decrease steadily for first 50–100 epochs
- [ ] Watch for overfitting: if validation loss increases while train loss decreases, stop
- [ ] Training typically converges in 500–2000 epochs depending on data quality
- [ ] Expected training time: 2–4 hours on Mac M-series, 1–2 hours on RTX 3060+
- [ ] Save best checkpoint (lowest validation loss)
- [ ] Backup trained model to cloud or external drive

### Training Troubleshooting
- [ ] If loss plateaus high: need more/better training data
- [ ] If loss oscillates wildly: reduce learning rate
- [ ] If OOM (out of memory): reduce batch size
- [ ] If training is too slow on Mac: switch to Colab
- [ ] If MPS errors on Mac: try `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0` env var

---

## Phase 8: Deployment (Autonomous Execution)

### Pre-Deployment
- [ ] Load best checkpoint into `so101/deploy.py`
- [ ] Verify model file exists and loads without error
- [ ] Set up identical workspace as training (same positions, lighting, camera angle)
- [ ] Place optic in tray at expected position
- [ ] Place switch/port at expected position
- [ ] Arm at home position

### First Autonomous Run
- [ ] Run: `python so101/deploy.py`
- [ ] WATCH CAREFULLY — be ready to hit emergency stop (Ctrl+C) if arm moves erratically
- [ ] Does arm move toward optic tray? (basic directional test)
- [ ] Does arm attempt to grasp optic?
- [ ] Does arm lift and move toward port?
- [ ] Does arm seat optic successfully?
- [ ] Does arm retract to home?
- [ ] SUCCESS CRITERIA: 3 out of 5 attempts complete the full task

### Tuning
- [ ] If arm overshoots: check servo calibration, possibly retrain with slower demos
- [ ] If arm doesn't reach far enough: workspace positions may differ from training
- [ ] If gripper misses optic: ensure optic position matches training data exactly
- [ ] If good but not great: record 20 more episodes and retrain (fine-tune)
- [ ] Run 10 consecutive autonomous attempts — log success/failure rate
- [ ] Target: >60% success rate for demo (80%+ ideal)

---

## Phase 9: Demo Preparation

### Demo Setup
- [ ] Clean workspace — table, arms, tray, port all visible and presentable
- [ ] Good lighting — no shadows on workspace, camera can see clearly
- [ ] Laptop screen visible showing dashboard with arm status panel
- [ ] Camera angle captures: arm, tray, port, and laptop screen in one shot
- [ ] Backup plan: if autonomous fails, switch to teleoperation (leader arm on standby)

### Demo Script (60 seconds)
- [ ] 0:00–0:10 — Show arm at home position, dashboard showing "READY"
- [ ] 0:10–0:15 — Narrate: "SO-101 arm trained via imitation learning to seat optics"
- [ ] 0:15–0:20 — Trigger autonomous run
- [ ] 0:20–0:45 — Arm picks optic, moves to port, seats it
- [ ] 0:45–0:55 — Dashboard updates: task complete, joint angles return to home
- [ ] 0:55–1:00 — "Trained from 50 demonstrations using LeRobot ACT policy"

### Video Recording
- [ ] Record 5+ full demo takes (pick best one for submission)
- [ ] Audio: clear narration, minimal background noise
- [ ] Video: 1080p minimum, well-lit, steady camera
- [ ] Include close-up of optic being seated (the money shot)
- [ ] Include dashboard screen showing live joint angles updating
- [ ] Total arm segment: 60 seconds max for the 3-minute final video

### Failsafe Plan
- [ ] If autonomous fails on camera: switch to teleoperation demo (still impressive)
- [ ] If hardware breaks: show training videos + Colab notebook + explain approach
- [ ] If time runs out on training: show teleoperation + "policy trains in 2 hours"
- [ ] Keep leader arm connected and ready throughout demo day

---

## Phase 10: Integration with Elktron Dashboard

- [ ] FastAPI server (`elktron-app/api/server.py`) receives arm telemetry via WebSocket
- [ ] Dashboard shows: current joint angles (6 values), gripper state, current task name
- [ ] Dashboard shows: task status (IDLE → RUNNING → COMPLETE)
- [ ] Camera feed from wrist/overhead cam streams to dashboard (WebSocket binary frames)
- [ ] Training controls: start/stop recording, episode count, training status
- [ ] If no live hardware: use mock data (JSON replay of recorded episode) for dashboard demo
