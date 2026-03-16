# PID Controller + Feed-Forward for Escort Bot Steering

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the P-only `compute_steering()` in `main.py` with a full PID controller for both lateral centering (steering) and longitudinal distance control (speed), plus a feed-forward term for smoother tracking when the person is moving.

**Architecture:** A standalone `PIDController` class in a new `pid.py` module. Two instances: one for lateral error (person left/right of center), one for distance error (person too close/far). The feed-forward term uses frame-to-frame bbox delta to predict where the person is heading. `compute_steering()` in `main.py` is replaced with a call that combines both PID outputs + feed-forward into final motor speeds.

**Tech Stack:** Python 3.11, gpiozero (existing), no new deps.

---

## Why PID over P-only

The current P-only controller (`KP * error`) has two problems on a real DC floor:

1. **Steady-state offset** — if the person walks slightly off-center, P-only reaches an equilibrium where the error is small but never zero. The bot drifts to one side. The **I** (integral) term accumulates error over time and drives it to zero.

2. **Overshoot and oscillation** — on smooth concrete floors, the bot's inertia carries it past the setpoint. The **D** (derivative) term detects rapid error changes and applies braking force. Without it, the bot wobble-follows.

3. **Latency on moving targets** — P reacts to where the person *is*. **Feed-forward** reacts to where the person is *going*, reducing the lag gap.

## PID Theory (for the implementer)

```
output = Kp * error + Ki * integral(error) + Kd * derivative(error) + Kff * feed_forward

Where:
  error         = setpoint - measurement  (e.g., frame_center - person_center)
  integral      = sum of error * dt over time (capped to prevent windup)
  derivative    = (error - prev_error) / dt
  feed_forward  = predicted change based on target velocity
```

**Anti-windup:** The integral term is clamped to `[-max_integral, +max_integral]` to prevent runaway accumulation when the bot is stuck or the person is out of frame.

**Derivative filtering:** Raw derivative is noisy from bbox jitter. A simple low-pass filter (exponential moving average with alpha=0.3) smooths it.

---

## File Structure

| File | Action | Responsibility |
|------|--------|---------------|
| `escort-bot/pid.py` | **Create** | `PIDController` class — generic, reusable, unit-testable |
| `escort-bot/main.py` | **Modify** | Replace `compute_steering()`, add PID instances, add feed-forward logic |
| `escort-bot/test_pid.py` | **Create** | Unit tests for PIDController — no hardware needed |

---

## Chunk 1: PID Controller Module

### Task 1: Create PIDController class with tests

**Files:**
- Create: `escort-bot/pid.py`
- Create: `escort-bot/test_pid.py`

- [ ] **Step 1: Write the failing tests**

Create `escort-bot/test_pid.py`:

```python
#!/usr/bin/env python3
"""Unit tests for PIDController — no hardware required."""

import time
from pid import PIDController


def test_p_only():
    """With Ki=0, Kd=0, output should be Kp * error."""
    pid = PIDController(kp=1.0, ki=0.0, kd=0.0)
    output = pid.update(error=0.5, dt=0.05)
    assert abs(output - 0.5) < 1e-6, f"Expected 0.5, got {output}"


def test_integral_accumulates():
    """Integral term should accumulate error over time."""
    pid = PIDController(kp=0.0, ki=1.0, kd=0.0)
    pid.update(error=1.0, dt=0.1)  # integral = 1.0 * 0.1 = 0.1
    output = pid.update(error=1.0, dt=0.1)  # integral = 0.1 + 0.1 = 0.2
    assert abs(output - 0.2) < 1e-6, f"Expected 0.2, got {output}"


def test_integral_windup_clamp():
    """Integral should be clamped to max_integral."""
    pid = PIDController(kp=0.0, ki=1.0, kd=0.0, max_integral=0.5)
    for _ in range(100):
        output = pid.update(error=1.0, dt=0.1)
    assert abs(output - 0.5) < 1e-6, f"Expected clamped at 0.5, got {output}"


def test_derivative_responds_to_change():
    """Derivative should be non-zero when error changes."""
    pid = PIDController(kp=0.0, ki=0.0, kd=1.0, d_filter_alpha=1.0)  # No filter
    pid.update(error=0.0, dt=0.05)
    output = pid.update(error=0.5, dt=0.05)
    # derivative = (0.5 - 0.0) / 0.05 = 10.0
    assert abs(output - 10.0) < 1e-6, f"Expected 10.0, got {output}"


def test_derivative_filter_smooths():
    """With filter alpha < 1.0, derivative should be smoothed."""
    pid = PIDController(kp=0.0, ki=0.0, kd=1.0, d_filter_alpha=0.3)
    pid.update(error=0.0, dt=0.05)
    output = pid.update(error=0.5, dt=0.05)
    # raw_d = 10.0, filtered = 0.3 * 10.0 + 0.7 * 0.0 = 3.0
    assert abs(output - 3.0) < 1e-6, f"Expected 3.0, got {output}"


def test_output_clamp():
    """Output should be clamped to [-max_output, +max_output]."""
    pid = PIDController(kp=10.0, ki=0.0, kd=0.0, max_output=1.0)
    output = pid.update(error=5.0, dt=0.05)
    assert abs(output - 1.0) < 1e-6, f"Expected clamped at 1.0, got {output}"
    output = pid.update(error=-5.0, dt=0.05)
    assert abs(output - (-1.0)) < 1e-6, f"Expected clamped at -1.0, got {output}"


def test_reset():
    """Reset should clear integral and derivative state."""
    pid = PIDController(kp=0.0, ki=1.0, kd=0.0)
    pid.update(error=1.0, dt=0.1)
    pid.update(error=1.0, dt=0.1)
    pid.reset()
    output = pid.update(error=1.0, dt=0.1)
    assert abs(output - 0.1) < 1e-6, f"Expected 0.1 after reset, got {output}"


def test_zero_dt_safe():
    """dt=0 should not cause division by zero."""
    pid = PIDController(kp=1.0, ki=1.0, kd=1.0)
    output = pid.update(error=1.0, dt=0.0)
    # Should return Kp * error only (no integral/derivative contribution)
    assert abs(output - 1.0) < 1e-6, f"Expected 1.0, got {output}"


if __name__ == "__main__":
    tests = [
        test_p_only,
        test_integral_accumulates,
        test_integral_windup_clamp,
        test_derivative_responds_to_change,
        test_derivative_filter_smooths,
        test_output_clamp,
        test_reset,
        test_zero_dt_safe,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS: {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL: {t.__name__} — {e}")
        except Exception as e:
            print(f"  ERROR: {t.__name__} — {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/rpatino/hackathon/escort-bot && python3 test_pid.py`
Expected: ImportError — `pid` module doesn't exist yet.

- [ ] **Step 3: Implement PIDController**

Create `escort-bot/pid.py`:

```python
#!/usr/bin/env python3
"""
PID Controller — generic, reusable, no hardware dependencies.

Used by the escort bot for:
  1. Lateral PID  — keeps person centered in frame (steering)
  2. Distance PID — keeps person at target follow distance (speed)

Theory:
  output = Kp * error + Ki * integral(error) + Kd * d(error)/dt

  Anti-windup: integral clamped to [-max_integral, +max_integral]
  Derivative filter: exponential moving average (alpha) to reduce bbox jitter
  Output clamp: final value clamped to [-max_output, +max_output]
"""


class PIDController:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0,
                 max_integral=1.0, max_output=1.0,
                 d_filter_alpha=0.3):
        """
        Args:
            kp: Proportional gain — immediate response to error
            ki: Integral gain — eliminates steady-state offset
            kd: Derivative gain — dampens overshoot
            max_integral: Anti-windup clamp for integral accumulator
            max_output: Clamp for final output
            d_filter_alpha: Low-pass filter for derivative (0-1, lower = smoother)
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max_integral = max_integral
        self.max_output = max_output
        self.d_filter_alpha = d_filter_alpha

        # State
        self._integral = 0.0
        self._prev_error = 0.0
        self._filtered_derivative = 0.0
        self._first_update = True

    def update(self, error, dt):
        """
        Compute PID output for the given error and timestep.

        Args:
            error: setpoint - measurement (positive = need to move right/forward)
            dt: time since last update in seconds

        Returns:
            Clamped PID output in [-max_output, +max_output]
        """
        # ── Proportional ──
        p_term = self.kp * error

        # ── Integral (with anti-windup) ──
        if dt > 0:
            self._integral += error * dt
            self._integral = max(-self.max_integral,
                                 min(self.max_integral, self._integral))
        i_term = self.ki * self._integral

        # ── Derivative (with low-pass filter) ──
        if dt > 0 and not self._first_update:
            raw_derivative = (error - self._prev_error) / dt
            self._filtered_derivative = (
                self.d_filter_alpha * raw_derivative +
                (1.0 - self.d_filter_alpha) * self._filtered_derivative
            )
        d_term = self.kd * self._filtered_derivative

        self._prev_error = error
        self._first_update = False

        # ── Sum and clamp ──
        output = p_term + i_term + d_term
        return max(-self.max_output, min(self.max_output, output))

    def reset(self):
        """Clear all accumulated state."""
        self._integral = 0.0
        self._prev_error = 0.0
        self._filtered_derivative = 0.0
        self._first_update = True
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/rpatino/hackathon/escort-bot && python3 test_pid.py`
Expected: `8/8 tests passed`

- [ ] **Step 5: Commit**

```bash
cd /Users/rpatino/hackathon
git add escort-bot/pid.py escort-bot/test_pid.py
git commit -m "feat(escort): add PID controller module with unit tests

Generic PIDController class with anti-windup, derivative filtering,
and output clamping. 8 unit tests covering all edge cases."
```

---

## Chunk 2: Integrate PID + Feed-Forward into main.py

### Task 2: Replace P-only steering with PID + feed-forward

**Files:**
- Modify: `escort-bot/main.py:25-50` (CONFIG section — add PID gains + feed-forward constant)
- Modify: `escort-bot/main.py:125-149` (replace `compute_steering()`)
- Modify: `escort-bot/main.py:230-240` (add PID instances to `main()` setup)
- Modify: `escort-bot/main.py:286-292` (update follow mode to pass dt + prev_bbox for feed-forward)

- [ ] **Step 1: Add PID config constants to CONFIG section**

In `main.py`, after line 50 (`LOST_TIMEOUT = 1.5`), add:

```python
# PID — Lateral (steering: keeps person centered in frame)
KP_LATERAL = 1.0            # Proportional — immediate turn response
KI_LATERAL = 0.1            # Integral — eliminates steady drift
KD_LATERAL = 0.3            # Derivative — dampens oscillation
MAX_INTEGRAL_LATERAL = 0.5  # Anti-windup clamp

# PID — Distance (speed: keeps person at target follow distance)
KP_DISTANCE = 1.2           # Proportional — speed up/slow down
KI_DISTANCE = 0.05          # Integral — eliminates steady-state gap
KD_DISTANCE = 0.2           # Derivative — smooth braking
MAX_INTEGRAL_DISTANCE = 0.3 # Anti-windup clamp

# Feed-forward
KFF = 0.15                  # Feed-forward gain — predict target motion
```

- [ ] **Step 2: Replace `compute_steering()` with PID version**

Replace the entire `compute_steering()` function (lines 127-149) with:

```python
def compute_steering(bbox, lateral_pid, distance_pid, dt, prev_bbox=None):
    """
    PID-based steering with feed-forward.

    Two PID loops:
      1. Lateral — error = how far person is from frame center (steering)
      2. Distance — error = target area ratio - actual area ratio (speed)

    Feed-forward: uses frame-to-frame bbox center delta to predict
    where the person is heading, reducing tracking lag.

    Returns (left_speed, right_speed) each in range [-1, 1].
    """
    x, y, w, h = bbox
    person_center_x = x + w / 2
    frame_center_x = FRAME_WIDTH / 2

    # ── Lateral PID (steering) ──
    lateral_error = (person_center_x - frame_center_x) / FRAME_WIDTH
    steering = lateral_pid.update(lateral_error, dt)

    # ── Distance PID (speed) ──
    area_ratio = (w * h) / (FRAME_WIDTH * FRAME_HEIGHT)
    distance_error = TARGET_AREA_RATIO - area_ratio  # positive = too far, go forward
    speed = distance_pid.update(distance_error, dt)

    # Clamp speed to [0, BASE_SPEED] — no reversing toward person
    speed = max(0.0, min(BASE_SPEED, speed))

    # ── Feed-forward (predict target motion) ──
    ff = 0.0
    if prev_bbox is not None:
        px, py, pw, ph = prev_bbox
        prev_center_x = px + pw / 2
        delta_x = (person_center_x - prev_center_x) / FRAME_WIDTH
        ff = KFF * delta_x  # positive = person moving right

    # ── Combine into differential drive ──
    turn = steering + ff
    left_speed = max(-1.0, min(1.0, speed + turn))
    right_speed = max(-1.0, min(1.0, speed - turn))

    return left_speed, right_speed
```

- [ ] **Step 3: Add PID imports and instances in `main()`**

At top of `main.py`, add import:

```python
from pid import PIDController
```

In `main()`, after line 221 (`os.makedirs(SCAN_OUTPUT_DIR, exist_ok=True)`), add:

```python
    # PID controllers
    lateral_pid = PIDController(
        kp=KP_LATERAL, ki=KI_LATERAL, kd=KD_LATERAL,
        max_integral=MAX_INTEGRAL_LATERAL, max_output=1.0
    )
    distance_pid = PIDController(
        kp=KP_DISTANCE, ki=KI_DISTANCE, kd=KD_DISTANCE,
        max_integral=MAX_INTEGRAL_DISTANCE, max_output=BASE_SPEED
    )
```

- [ ] **Step 4: Add `dt` tracking and update follow mode call**

In `main()`, after `scan_count = 0` (line 236), add:

```python
    last_time = time.time()
```

At the top of the while loop, after `frame = camera.capture_array()`, add:

```python
            now = time.time()
            dt = now - last_time
            last_time = now
```

Replace the follow mode block (lines 286-292):

```python
                # Normal follow mode
                mode = MODE_FOLLOW
                left, right = compute_steering(bbox, lateral_pid, distance_pid, dt, prev_bbox)
                drive(robot, left, right)
                x, y, w, h = bbox
                print(f"[FOLLOW] person@({x},{y}) size={w}x{h} → L={left:.2f} R={right:.2f}")
```

- [ ] **Step 5: Reset PIDs on mode transitions**

After `mode = MODE_IDLE` (line 305), add:

```python
                        lateral_pid.reset()
                        distance_pid.reset()
```

After `mode = MODE_FOLLOW` in the SCAN→FOLLOW transition (line 279), add:

```python
                        lateral_pid.reset()
                        distance_pid.reset()
```

- [ ] **Step 6: Remove old KP constant**

Delete line 45: `KP = 1.0                    # Proportional gain — tune on the floor`

(The old `KP` is replaced by the PID gain constants.)

- [ ] **Step 7: Verify no syntax errors**

Run: `cd /Users/rpatino/hackathon/escort-bot && python3 -c "import main; print('OK')"`
Expected: May fail due to hardware imports (picamera2, gpiozero) — that's fine on Mac.

Run: `cd /Users/rpatino/hackathon/escort-bot && python3 -c "from pid import PIDController; print('PID import OK')"`
Expected: `PID import OK`

- [ ] **Step 8: Commit**

```bash
cd /Users/rpatino/hackathon
git add escort-bot/main.py
git commit -m "feat(escort): integrate PID steering + feed-forward into main loop

Replace P-only compute_steering with dual PID (lateral + distance) and
feed-forward term. Lateral PID eliminates drift, distance PID smooths
braking, feed-forward predicts target motion for reduced tracking lag.
PID state resets on mode transitions (IDLE, SCAN→FOLLOW)."
```

---

## Chunk 3: Update documentation

### Task 3: Update CLAUDE.md and WIRING.md with PID tuning info

**Files:**
- Modify: `escort-bot/CLAUDE.md` (update tuning parameters table)

- [ ] **Step 1: Update tuning parameters table in escort-bot/CLAUDE.md**

Replace the existing tuning parameters table with:

```markdown
## Key Tuning Parameters (in main.py)

| Parameter | Default | What It Controls |
|-----------|---------|-----------------|
| `KP_LATERAL` | 1.0 | Lateral PID proportional — immediate turn response |
| `KI_LATERAL` | 0.1 | Lateral PID integral — eliminates steady drift |
| `KD_LATERAL` | 0.3 | Lateral PID derivative — dampens turn oscillation |
| `KP_DISTANCE` | 1.2 | Distance PID proportional — speed up/slow down |
| `KI_DISTANCE` | 0.05 | Distance PID integral — eliminates steady-state gap |
| `KD_DISTANCE` | 0.2 | Distance PID derivative — smooth braking |
| `KFF` | 0.15 | Feed-forward gain — predict target motion |
| `BASE_SPEED` | 0.5 | Max forward speed (0.0-1.0) — start low on real floor |
| `STOP_DISTANCE` | 0.30m | Ultrasonic cutoff — stop if obstacle closer than this |
| `TARGET_AREA_RATIO` | 0.15 | How close to follow — higher = closer following distance |
| `CONFIDENCE_THRESHOLD` | 0.5 | Min detection confidence score to consider a person |
| `SCAN_IDLE_TIME` | 3.0s | How long person must be still before triggering scan |
| `LOST_TIMEOUT` | 1.5s | How long with no detection before switching to IDLE |

### PID Tuning Guide (on the floor)

1. Start with **P-only**: set Ki=0, Kd=0 for both. Increase Kp until the bot tracks but oscillates.
2. Add **D**: increase Kd until oscillation stops. Too much D = sluggish response.
3. Add **I**: increase Ki slowly until steady-state drift disappears. Too much I = slow windup oscillation.
4. Tune **feed-forward (KFF)**: increase until the bot anticipates direction changes. Too much = overcorrection.
```

- [ ] **Step 2: Commit**

```bash
cd /Users/rpatino/hackathon
git add escort-bot/CLAUDE.md
git commit -m "docs(escort): update tuning params table with PID gains + tuning guide"
```

---

## Tuning Starting Points

These defaults are conservative — designed to be stable out of the box on a smooth DC floor:

| Gain | Value | Reasoning |
|------|-------|-----------|
| KP_LATERAL = 1.0 | Same as old KP — proven baseline |
| KI_LATERAL = 0.1 | Low — just enough to correct drift over 2-3 seconds |
| KD_LATERAL = 0.3 | Moderate — dampens bbox jitter without sluggishness |
| KP_DISTANCE = 1.2 | Slightly aggressive — approach target distance quickly |
| KI_DISTANCE = 0.05 | Very low — distance control tolerates small errors |
| KD_DISTANCE = 0.2 | Moderate — smooth braking when approaching person |
| KFF = 0.15 | Conservative — small predictive boost without overcorrection |

**On the Pi:** Tune by editing the constants at the top of `main.py`. No rebuild needed — just restart the script. Claude Code on the Pi makes this instant.
