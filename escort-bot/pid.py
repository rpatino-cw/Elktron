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
