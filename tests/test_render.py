"""Tests für das render-Modul – FractalTesseract und verwandte Klassen."""

from __future__ import annotations

import math
import pytest

from implosive_genesis.render.fractal_tesseract import (
    FractalFrame,
    FractalTesseract,
    RenderResult,
    PHI,
    _ASCII_CHARS,
)

# ---------------------------------------------------------------------------
# Konstanten-Tests
# ---------------------------------------------------------------------------


def test_phi_value():
    assert abs(PHI - (1.0 + math.sqrt(5.0)) / 2.0) < 1e-12


def test_phi_golden_identity():
    """Φ² = Φ + 1 (goldene Identität)."""
    assert abs(PHI**2 - (PHI + 1.0)) < 1e-10


def test_ascii_chars_nonempty():
    assert len(_ASCII_CHARS) > 0


# ---------------------------------------------------------------------------
# FractalTesseract – Konstruktor
# ---------------------------------------------------------------------------


def test_fractal_tesseract_default():
    ft = FractalTesseract()
    assert ft.beta_0 == 1.0
    assert ft.branch_factor == 2
    assert ft.l0 > 0.0
    assert ft.t0 > 0.0


def test_fractal_tesseract_custom():
    ft = FractalTesseract(beta_0=2.5, l0=100.0, t0=1e-10, branch_factor=3)
    assert ft.beta_0 == 2.5
    assert ft.l0 == 100.0
    assert ft.t0 == 1e-10
    assert ft.branch_factor == 3


def test_fractal_tesseract_invalid_beta():
    with pytest.raises(ValueError, match="beta_0"):
        FractalTesseract(beta_0=0.0)


def test_fractal_tesseract_invalid_beta_negative():
    with pytest.raises(ValueError, match="beta_0"):
        FractalTesseract(beta_0=-1.0)


def test_fractal_tesseract_invalid_branch():
    with pytest.raises(ValueError, match="branch_factor"):
        FractalTesseract(branch_factor=0)


# ---------------------------------------------------------------------------
# FractalTesseract – phi_scale / coherence_length / time_slice / intensity
# ---------------------------------------------------------------------------


def test_phi_scale_n0():
    ft = FractalTesseract()
    assert abs(ft.phi_scale(0) - 1.0) < 1e-12


def test_phi_scale_n3():
    ft = FractalTesseract()
    assert abs(ft.phi_scale(3) - PHI) < 1e-12


def test_phi_scale_n6():
    ft = FractalTesseract()
    assert abs(ft.phi_scale(6) - PHI**2) < 1e-12


def test_coherence_length_n0():
    ft = FractalTesseract(l0=100.0)
    assert abs(ft.coherence_length(0) - 100.0) < 1e-12


def test_coherence_length_n3():
    ft = FractalTesseract(l0=100.0)
    assert abs(ft.coherence_length(3) - 100.0 * PHI) < 1e-10


def test_coherence_length_increases():
    ft = FractalTesseract()
    lengths = [ft.coherence_length(n) for n in range(6)]
    for i in range(len(lengths) - 1):
        assert lengths[i] < lengths[i + 1]


def test_time_slice_n0():
    ft = FractalTesseract(t0=1.0)
    assert abs(ft.time_slice(0) - 1.0) < 1e-12


def test_time_slice_n1():
    ft = FractalTesseract(t0=1.0)
    assert abs(ft.time_slice(1) - PHI) < 1e-12


def test_time_slice_n3():
    ft = FractalTesseract(t0=1.0)
    assert abs(ft.time_slice(3) - PHI**3) < 1e-10


def test_time_slice_increases():
    ft = FractalTesseract(t0=1.0)
    slices = [ft.time_slice(n) for n in range(6)]
    for i in range(len(slices) - 1):
        assert slices[i] < slices[i + 1]


def test_intensity_n0():
    ft = FractalTesseract()
    assert abs(ft.intensity(0) - 1.0) < 1e-12


def test_intensity_n1():
    ft = FractalTesseract()
    assert abs(ft.intensity(1) - 1.0 / PHI) < 1e-12


def test_intensity_decreases():
    ft = FractalTesseract()
    vals = [ft.intensity(n) for n in range(6)]
    for i in range(len(vals) - 1):
        assert vals[i] > vals[i + 1]


def test_intensity_positive():
    ft = FractalTesseract()
    for n in range(10):
        assert ft.intensity(n) > 0.0


# ---------------------------------------------------------------------------
# FractalTesseract – frame_at
# ---------------------------------------------------------------------------


def test_frame_at_depth_0():
    ft = FractalTesseract()
    frame = ft.frame_at(0)
    assert frame.depth == 0
    assert abs(frame.scale - 1.0) < 1e-12
    assert abs(frame.intensity - 1.0) < 1e-12
    assert frame.children == []


def test_frame_at_depth_3():
    ft = FractalTesseract(beta_0=1.0, l0=100.0)
    frame = ft.frame_at(3)
    assert frame.depth == 3
    assert abs(frame.scale - PHI) < 1e-10
    assert abs(frame.beta - PHI) < 1e-10
    assert abs(frame.coherence_length - 100.0 * PHI) < 1e-10


def test_frame_at_no_children():
    ft = FractalTesseract()
    frame = ft.frame_at(5)
    assert frame.children == []


# ---------------------------------------------------------------------------
# FractalTesseract – render
# ---------------------------------------------------------------------------


def test_render_depth_0():
    ft = FractalTesseract()
    result = ft.render(depth=0)
    assert result.depth == 0
    assert result.n_frames == 1
    assert isinstance(result.ascii_art, str)
    assert len(result.ascii_art) > 0


def test_render_depth_3():
    ft = FractalTesseract()
    result = ft.render(depth=3)
    assert result.depth == 3
    # 2-branch: 1 + 2 + 4 + 8 = 15 frames
    assert result.n_frames == 15


def test_render_depth_4():
    ft = FractalTesseract()
    result = ft.render(depth=4)
    # 2-branch: sum(2^n for n in 0..4) = 31
    assert result.n_frames == 31


def test_render_branch_factor_1():
    ft = FractalTesseract(branch_factor=1)
    result = ft.render(depth=5)
    assert result.n_frames == 6  # 1 per depth level


def test_render_branch_factor_3():
    ft = FractalTesseract(branch_factor=3)
    result = ft.render(depth=3)
    # sum(3^n for n in 0..3) = 1 + 3 + 9 + 27 = 40
    assert result.n_frames == 40


def test_render_phi_series_length():
    ft = FractalTesseract()
    result = ft.render(depth=5)
    assert len(result.phi_scaling_series) == 6  # 0..5 inclusive


def test_render_phi_series_values():
    ft = FractalTesseract()
    result = ft.render(depth=3)
    for n, val in enumerate(result.phi_scaling_series):
        assert abs(val - PHI ** (n / 3.0)) < 1e-10


def test_render_coherence_lengths_length():
    ft = FractalTesseract()
    result = ft.render(depth=4)
    assert len(result.coherence_lengths) == 5


def test_render_coherence_lengths_values():
    ft = FractalTesseract(l0=200.0)
    result = ft.render(depth=3)
    for n, val in enumerate(result.coherence_lengths):
        assert abs(val - 200.0 * PHI ** (n / 3.0)) < 1e-8


def test_render_time_slices_length():
    ft = FractalTesseract(t0=1.0)
    result = ft.render(depth=5)
    assert len(result.time_slices) == 6


def test_render_time_slices_values():
    ft = FractalTesseract(t0=1.0)
    result = ft.render(depth=3)
    for n, val in enumerate(result.time_slices):
        assert abs(val - PHI**n) < 1e-10


def test_render_ascii_contains_header():
    ft = FractalTesseract()
    result = ft.render(depth=3)
    assert "FractalTesseract" in result.ascii_art


def test_render_ascii_contains_depth_info():
    ft = FractalTesseract()
    result = ft.render(depth=4)
    assert "depth=4" in result.ascii_art


def test_render_animate():
    ft = FractalTesseract()
    result = ft.render(depth=3, animate=True)
    assert "ASCII-Animation" in result.ascii_art


def test_render_invalid_depth_negative():
    ft = FractalTesseract()
    with pytest.raises(ValueError, match="depth"):
        ft.render(depth=-1)


def test_render_invalid_depth_too_large():
    ft = FractalTesseract()
    with pytest.raises(ValueError, match="depth"):
        ft.render(depth=17)


def test_render_ascii_only():
    ft = FractalTesseract()
    art = ft.render_ascii(depth=3)
    assert isinstance(art, str)
    assert "FractalTesseract" in art


# ---------------------------------------------------------------------------
# FractalFrame – Eigenschaften
# ---------------------------------------------------------------------------


def test_fractal_frame_ascii_char_full_intensity():
    frame = FractalFrame(
        depth=0,
        scale=1.0,
        beta=1.0,
        coherence_length=100.0,
        time_slice=1e-44,
        intensity=1.0,
    )
    # Intensität 1.0 → letztes Zeichen
    assert frame.ascii_char == _ASCII_CHARS[-1]


def test_fractal_frame_ascii_char_low_intensity():
    frame = FractalFrame(
        depth=10,
        scale=PHI ** (10 / 3.0),
        beta=1.0 * PHI ** (10 / 3.0),
        coherence_length=221.0,
        time_slice=1e-44,
        intensity=0.001,
    )
    # Niedrige Intensität → frühes Zeichen
    assert frame.ascii_char in _ASCII_CHARS[:3]


def test_fractal_frame_waste_n0():
    frame = FractalFrame(0, 1.0, 1.0, 100.0, 1e-44, 1.0)
    assert abs(frame.waste - 0.0) < 1e-12


def test_fractal_frame_waste_n3():
    frame = FractalFrame(3, PHI, PHI, 100.0 * PHI, 1e-44, 1.0 / PHI**3)
    expected_waste = 1.0 - 1.0 / PHI
    assert abs(frame.waste - expected_waste) < 1e-10


def test_fractal_frame_children_default():
    frame = FractalFrame(0, 1.0, 1.0, 100.0, 1e-44, 1.0)
    assert frame.children == []


# ---------------------------------------------------------------------------
# RenderResult – Struktur
# ---------------------------------------------------------------------------


def test_render_result_type():
    ft = FractalTesseract()
    result = ft.render(depth=2)
    assert isinstance(result, RenderResult)


def test_render_result_root_depth():
    ft = FractalTesseract()
    result = ft.render(depth=3)
    assert result.root.depth == 0


def test_render_result_root_children():
    ft = FractalTesseract(branch_factor=2)
    result = ft.render(depth=2)
    assert len(result.root.children) == 2


def test_render_result_root_grandchildren():
    ft = FractalTesseract(branch_factor=2)
    result = ft.render(depth=2)
    for child in result.root.children:
        assert len(child.children) == 2


# ---------------------------------------------------------------------------
# Render-Konsistenz-Tests
# ---------------------------------------------------------------------------


def test_beta_series_consistent():
    ft = FractalTesseract(beta_0=2.0, l0=50.0)
    result = ft.render(depth=5)
    for n, l in enumerate(result.coherence_lengths):
        expected = 50.0 * PHI ** (n / 3.0)
        assert abs(l - expected) < 1e-8


def test_render_root_scale_1():
    ft = FractalTesseract()
    result = ft.render(depth=4)
    assert abs(result.root.scale - 1.0) < 1e-12


def test_render_child_depth():
    ft = FractalTesseract(branch_factor=2)
    result = ft.render(depth=3)
    for child in result.root.children:
        assert child.depth == 1
        for grandchild in child.children:
            assert grandchild.depth == 2


def test_lambda_oipk_value():
    ft = FractalTesseract()
    # λ_OIPK ≈ c / V_RIG = 299_792_458 / 1_352_000
    expected = 299_792_458.0 / 1_352_000.0
    assert abs(ft._LAMBDA_OIPK - expected) < 0.01


def test_default_l0_equals_lambda_oipk():
    ft = FractalTesseract()
    assert abs(ft.l0 - ft._LAMBDA_OIPK) < 1e-10
