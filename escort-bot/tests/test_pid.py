#!/usr/bin/env python3
"""Unit tests for PIDController — no hardware required."""

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
    pid = PIDController(kp=0.0, ki=0.0, kd=1.0, d_filter_alpha=1.0, max_output=100.0)
    pid.update(error=0.0, dt=0.05)
    output = pid.update(error=0.5, dt=0.05)
    # derivative = (0.5 - 0.0) / 0.05 = 10.0
    assert abs(output - 10.0) < 1e-6, f"Expected 10.0, got {output}"


def test_derivative_filter_smooths():
    """With filter alpha < 1.0, derivative should be smoothed."""
    pid = PIDController(kp=0.0, ki=0.0, kd=1.0, d_filter_alpha=0.3, max_output=100.0)
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
