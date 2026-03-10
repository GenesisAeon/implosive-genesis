"""Tests für das Medium-Modulation-Modul (v0.3.0)."""

from __future__ import annotations

import math

import pytest

from implosive_genesis.medium.modulation import (
    ANESTHESIA_THRESHOLD,
    FRAME_BUFFER_SIZE,
    AnesthesiaEvent,
    AnesthesiaTestResult,
    FrameBuffer,
    MediumModulator,
    MediumState,
    run_anesthesia_test,
)

_PHI: float = (1.0 + math.sqrt(5.0)) / 2.0

# ===========================================================================
# Konstanten
# ===========================================================================


def test_anesthesia_threshold_positive() -> None:
    assert ANESTHESIA_THRESHOLD > 0


def test_anesthesia_threshold_less_than_one() -> None:
    assert ANESTHESIA_THRESHOLD < 1.0


def test_frame_buffer_size_positive() -> None:
    assert FRAME_BUFFER_SIZE > 0


def test_anesthesia_threshold_value() -> None:
    """Θ = α_Φ / Φ² ≈ 0.004504."""
    alpha_em = 7.2973525693e-3
    alpha_phi = alpha_em * _PHI
    expected = alpha_phi / _PHI**2
    assert abs(ANESTHESIA_THRESHOLD - expected) < 1e-12


# ===========================================================================
# FrameBuffer
# ===========================================================================


def test_framebuffer_empty_mean() -> None:
    buf = FrameBuffer()
    assert buf.mean() == 0.0


def test_framebuffer_single_push() -> None:
    buf = FrameBuffer()
    buf.push(0.5)
    assert buf.mean() == pytest.approx(0.5)


def test_framebuffer_two_pushes_mean() -> None:
    buf = FrameBuffer()
    buf.push(0.4)
    buf.push(0.6)
    assert buf.mean() == pytest.approx(0.5)


def test_framebuffer_respects_size() -> None:
    buf = FrameBuffer(size=3)
    for v in [0.1, 0.2, 0.3, 0.9]:
        buf.push(v)
    assert len(buf) == 3


def test_framebuffer_fifo_eviction() -> None:
    buf = FrameBuffer(size=2)
    buf.push(0.1)
    buf.push(0.2)
    buf.push(0.8)
    # oldest 0.1 evicted → mean of 0.2, 0.8
    assert buf.mean() == pytest.approx(0.5)


def test_framebuffer_is_conscious_high() -> None:
    buf = FrameBuffer()
    buf.push(1.0)
    assert buf.is_conscious() is True


def test_framebuffer_is_conscious_low() -> None:
    buf = FrameBuffer()
    buf.push(0.0)
    assert buf.is_conscious() is False


def test_framebuffer_is_conscious_empty_false() -> None:
    buf = FrameBuffer()
    assert buf.is_conscious() is False


def test_framebuffer_fill_level_empty() -> None:
    buf = FrameBuffer(size=10)
    assert buf.fill_level() == 0.0


def test_framebuffer_fill_level_full() -> None:
    buf = FrameBuffer(size=4)
    for _ in range(4):
        buf.push(0.5)
    assert buf.fill_level() == pytest.approx(1.0)


def test_framebuffer_fill_level_partial() -> None:
    buf = FrameBuffer(size=10)
    for _ in range(5):
        buf.push(0.5)
    assert buf.fill_level() == pytest.approx(0.5)


def test_framebuffer_reset() -> None:
    buf = FrameBuffer()
    buf.push(0.5)
    buf.reset()
    assert len(buf) == 0
    assert buf.mean() == 0.0


def test_framebuffer_len() -> None:
    buf = FrameBuffer()
    assert len(buf) == 0
    buf.push(0.5)
    assert len(buf) == 1


def test_framebuffer_custom_threshold() -> None:
    buf = FrameBuffer()
    buf.push(0.5)
    assert buf.is_conscious(threshold=0.3) is True
    assert buf.is_conscious(threshold=0.8) is False


# ===========================================================================
# MediumState
# ===========================================================================


def test_medium_state_str_conscious() -> None:
    s = MediumState(t=10.0, m_t=0.9, delta_m=0.1, normalized=0.9, conscious=True)
    assert "CONSCIOUS" in str(s)


def test_medium_state_str_anesthesia() -> None:
    s = MediumState(t=10.0, m_t=0.001, delta_m=0.999, normalized=0.001, conscious=False)
    assert "ANESTHESIA" in str(s)


# ===========================================================================
# MediumModulator – modulate
# ===========================================================================


def test_modulate_t0_equals_m0() -> None:
    mod = MediumModulator(m0=1.0, tau_m=60.0)
    s = mod.modulate(0.0)
    assert s.m_t == pytest.approx(1.0)


def test_modulate_delta_m_t0_is_zero() -> None:
    mod = MediumModulator(m0=1.0, tau_m=60.0)
    s = mod.modulate(0.0)
    assert s.delta_m == pytest.approx(0.0)


def test_modulate_normalized_t0_is_one() -> None:
    mod = MediumModulator(m0=1.0, tau_m=60.0)
    s = mod.modulate(0.0)
    assert s.normalized == pytest.approx(1.0)


def test_modulate_conscious_at_t0() -> None:
    mod = MediumModulator(m0=1.0, tau_m=60.0)
    assert mod.modulate(0.0).conscious is True


def test_modulate_decays_over_time() -> None:
    mod = MediumModulator(m0=1.0, tau_m=60.0)
    s1 = mod.modulate(30.0)
    s2 = mod.modulate(60.0)
    assert s1.m_t > s2.m_t


def test_modulate_formula_exp() -> None:
    mod = MediumModulator(m0=1.0, tau_m=100.0)
    t = 50.0
    expected = math.exp(-t / 100.0)
    assert mod.modulate(t).normalized == pytest.approx(expected, rel=1e-9)


def test_modulate_delta_m_plus_mt_equals_m0() -> None:
    mod = MediumModulator(m0=1.0, tau_m=60.0)
    s = mod.modulate(45.0)
    assert s.m_t + s.delta_m == pytest.approx(mod.m0, rel=1e-9)


def test_modulate_negative_t_clamped() -> None:
    mod = MediumModulator(m0=1.0, tau_m=60.0)
    s = mod.modulate(-10.0)
    assert s.t == 0.0


def test_modulate_very_large_t_near_zero() -> None:
    mod = MediumModulator(m0=1.0, tau_m=10.0)
    s = mod.modulate(1000.0)
    assert s.normalized < 1e-10


def test_modulate_conscious_false_eventually() -> None:
    mod = MediumModulator(m0=1.0, tau_m=1.0)
    s = mod.modulate(100.0)
    assert s.conscious is False


# ===========================================================================
# MediumModulator – modulation_series
# ===========================================================================


def test_modulation_series_length() -> None:
    mod = MediumModulator()
    series = mod.modulation_series(t_max=100.0, n_steps=10)
    assert len(series) == 11


def test_modulation_series_t0_first() -> None:
    mod = MediumModulator()
    series = mod.modulation_series(t_max=100.0, n_steps=10)
    assert series[0].t == pytest.approx(0.0)


def test_modulation_series_last_t_is_t_max() -> None:
    mod = MediumModulator()
    series = mod.modulation_series(t_max=100.0, n_steps=10)
    assert series[-1].t == pytest.approx(100.0)


def test_modulation_series_monotone_decreasing_amplitude() -> None:
    mod = MediumModulator(m0=1.0, tau_m=60.0)
    series = mod.modulation_series(t_max=300.0, n_steps=20)
    for i in range(len(series) - 1):
        assert series[i].m_t >= series[i + 1].m_t


# ===========================================================================
# MediumModulator – frame_loss
# ===========================================================================


def test_frame_loss_t0_is_zero() -> None:
    mod = MediumModulator(tau_m=60.0)
    assert mod.frame_loss(0.0) == pytest.approx(0.0)


def test_frame_loss_large_t_approaches_one() -> None:
    mod = MediumModulator(tau_m=1.0)
    assert mod.frame_loss(1000.0) > 0.999


def test_frame_loss_formula() -> None:
    mod = MediumModulator(tau_m=60.0)
    t = 60.0
    expected = 1.0 - math.exp(-t / 60.0)
    assert mod.frame_loss(t) == pytest.approx(expected, rel=1e-9)


def test_frame_loss_monotone() -> None:
    mod = MediumModulator(tau_m=60.0)
    vals = [mod.frame_loss(t) for t in [0, 30, 60, 120, 300]]
    assert all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1))


# ===========================================================================
# MediumModulator – recovery_rate
# ===========================================================================


def test_recovery_rate_t0_is_one() -> None:
    mod = MediumModulator(tau_m=60.0)
    assert mod.recovery_rate(0.0) == pytest.approx(1.0)


def test_recovery_rate_decreases() -> None:
    mod = MediumModulator(tau_m=60.0)
    r1 = mod.recovery_rate(60.0)
    r2 = mod.recovery_rate(120.0)
    assert r1 > r2


def test_recovery_rate_formula() -> None:
    mod = MediumModulator(tau_m=60.0)
    t = 60.0
    expected = math.exp(-t / (60.0 * _PHI))
    assert mod.recovery_rate(t) == pytest.approx(expected, rel=1e-9)


def test_recovery_rate_in_range() -> None:
    mod = MediumModulator(tau_m=60.0)
    for t in [0, 30, 60, 120, 300]:
        r = mod.recovery_rate(t)
        assert 0.0 <= r <= 1.0


# ===========================================================================
# AnesthesiaTestResult
# ===========================================================================


def test_run_anesthesia_test_returns_result() -> None:
    result = run_anesthesia_test(duration=60.0, tau_m=10.0, dt=1.0)
    assert isinstance(result, AnesthesiaTestResult)


def test_anesthesia_test_duration_stored() -> None:
    result = run_anesthesia_test(duration=60.0)
    assert result.duration == 60.0


def test_anesthesia_test_tau_m_stored() -> None:
    result = run_anesthesia_test(tau_m=90.0)
    assert result.tau_m == 90.0


def test_anesthesia_test_times_nonempty() -> None:
    result = run_anesthesia_test(duration=10.0, dt=1.0)
    assert len(result.times) > 0


def test_anesthesia_test_frame_means_same_length_as_times() -> None:
    result = run_anesthesia_test(duration=10.0, dt=1.0)
    assert len(result.frame_means) == len(result.times)


def test_anesthesia_test_loss_rate_in_range() -> None:
    result = run_anesthesia_test(duration=60.0, tau_m=60.0)
    assert 0.0 <= result.loss_rate <= 1.0


def test_anesthesia_test_recovery_rate_in_range() -> None:
    result = run_anesthesia_test(duration=60.0, tau_m=60.0)
    assert 0.0 < result.recovery_rate <= 1.0


def test_anesthesia_test_short_tau_has_events() -> None:
    """Mit kleiner τ_M (1s) muss bei Dauer 300s Anesthesia eintreten."""
    result = run_anesthesia_test(duration=300.0, tau_m=1.0, dt=1.0)
    assert result.n_events() > 0


def test_anesthesia_test_long_tau_conscious() -> None:
    """Mit sehr langer τ_M bleibt das System während kurzer Tests bewusst."""
    result = run_anesthesia_test(duration=10.0, tau_m=100000.0, dt=1.0)
    assert result.consciousness_fraction() > 0.99


def test_anesthesia_test_n_events_nonneg() -> None:
    result = run_anesthesia_test(duration=60.0)
    assert result.n_events() >= 0


def test_anesthesia_test_total_anesthesia_time_nonneg() -> None:
    result = run_anesthesia_test(duration=60.0)
    assert result.total_anesthesia_time() >= 0.0


def test_anesthesia_test_consciousness_fraction_in_range() -> None:
    result = run_anesthesia_test(duration=60.0)
    assert 0.0 <= result.consciousness_fraction() <= 1.0


def test_anesthesia_test_summary_string() -> None:
    result = run_anesthesia_test(duration=30.0, dt=1.0)
    s = result.summary()
    assert "AnesthesiaTestResult" in s
    assert "R_loss" in s


def test_anesthesia_event_duration() -> None:
    ev = AnesthesiaEvent(t_start=10.0, t_end=30.0, depth=0.5, recovery=0.8)
    assert ev.duration == pytest.approx(20.0)


def test_anesthesia_event_duration_none_if_open() -> None:
    ev = AnesthesiaEvent(t_start=10.0, t_end=None, depth=0.5, recovery=0.8)
    assert ev.duration is None


def test_anesthesia_test_default_300s() -> None:
    result = run_anesthesia_test()
    assert result.duration == 300.0


# ===========================================================================
# medium __init__ re-exports
# ===========================================================================


def test_medium_init_exports() -> None:
    from implosive_genesis import medium

    for name in [
        "ANESTHESIA_THRESHOLD",
        "FRAME_BUFFER_SIZE",
        "MediumState",
        "FrameBuffer",
        "AnesthesiaEvent",
        "AnesthesiaTestResult",
        "MediumModulator",
        "run_anesthesia_test",
    ]:
        assert hasattr(medium, name), f"Missing export: {name}"
