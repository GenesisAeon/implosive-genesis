"""Tests für neue Simulations-Module (v0.2.0): tesseract_render und cmb_falsification."""

from __future__ import annotations

import math
from pathlib import Path

import pytest
from typer.testing import CliRunner

from implosive_genesis.cli import app
from implosive_genesis.core.physics import PHI
from implosive_genesis.simulation.cmb_falsification import (
    CMBFalsificationTest,
    CMBTestResult,
    run_cmb_test,
    V_CMB_KMS,
    V_RIG_KMS,
)
from implosive_genesis.simulation.tesseract_render import (
    TesseractFrameData,
    TesseractRenderer,
    render_tesseract,
)

runner = CliRunner()


# ===========================================================================
# TesseractFrameData
# ===========================================================================


def test_frame_data_fields():
    import numpy as np

    data = TesseractFrameData(
        n_values=np.array([0, 1, 2]),
        time_slices=np.array([1.0, PHI, PHI**2]),
        crep_values=np.array([0.0, 1e-20, 2e-20]),
        volumes_4d=np.array([1.0, PHI**4, PHI**8]),
        entropy_prices=np.array([0.0, 1e-23, 2e-23]),
        phi=PHI,
        temperature_k=2.725,
    )
    assert data.phi == pytest.approx(PHI, rel=1e-9)
    assert len(data.n_values) == 3


# ===========================================================================
# TesseractRenderer
# ===========================================================================


def test_renderer_default_creates():
    renderer = TesseractRenderer(n_max=5)
    assert renderer.n_max == 5
    assert renderer.temperature == 2.725


def test_renderer_compute_frame_data():
    renderer = TesseractRenderer(n_max=4)
    data = renderer._compute_frame_data()
    assert len(data.n_values) == 5  # n = 0..4


def test_renderer_time_slices_phi_scaling():
    renderer = TesseractRenderer(n_max=4, t_0=1.0)
    data = renderer._compute_frame_data()
    for i, n in enumerate(data.n_values.astype(int)):
        assert data.time_slices[i] == pytest.approx(PHI**n, rel=1e-9)


def test_renderer_volumes_are_fourth_power():
    renderer = TesseractRenderer(n_max=3, t_0=1.0)
    data = renderer._compute_frame_data()
    for i in range(len(data.n_values)):
        assert data.volumes_4d[i] == pytest.approx(data.time_slices[i] ** 4, rel=1e-9)


def test_renderer_entropy_price_n0_is_zero():
    renderer = TesseractRenderer(n_max=5)
    data = renderer._compute_frame_data()
    assert data.entropy_prices[0] == pytest.approx(0.0, abs=1e-40)


def test_renderer_crep_n0_is_zero():
    renderer = TesseractRenderer(n_max=5)
    data = renderer._compute_frame_data()
    assert data.crep_values[0] == pytest.approx(0.0, abs=1e-40)


def test_renderer_crep_monotone_increasing():
    renderer = TesseractRenderer(n_max=5)
    data = renderer._compute_frame_data()
    crep = data.crep_values
    assert all(crep[i] <= crep[i + 1] for i in range(len(crep) - 1))


def test_renderer_ascii_preview_not_empty():
    renderer = TesseractRenderer(n_max=3)
    preview = renderer.ascii_preview()
    assert len(preview) > 0
    assert "T_n" in preview
    assert "CREP" in preview


def test_renderer_ascii_preview_contains_all_n():
    renderer = TesseractRenderer(n_max=4)
    preview = renderer.ascii_preview()
    for n in range(5):
        assert str(n) in preview


def test_renderer_render_returns_figure():
    import matplotlib.pyplot as plt

    renderer = TesseractRenderer(n_max=4)
    fig = renderer.render()
    assert fig is not None
    # 3 Haupt-Subplots + 1 Colorbar-Axes
    assert len(fig.axes) >= 3
    plt.close(fig)


def test_renderer_save_creates_file(tmp_path):
    renderer = TesseractRenderer(n_max=3)
    out = tmp_path / "test_tess.png"
    saved = renderer.save(out)
    assert saved.exists()
    assert saved.suffix == ".png"


def test_renderer_save_pdf(tmp_path):
    renderer = TesseractRenderer(n_max=3)
    out = tmp_path / "test_tess.pdf"
    saved = renderer.save(out)
    assert saved.exists()


# ===========================================================================
# render_tesseract (Convenience-Funktion)
# ===========================================================================


def test_render_tesseract_returns_frame_data():
    data = render_tesseract(n_max=4)
    assert isinstance(data, TesseractFrameData)
    assert len(data.n_values) == 5


def test_render_tesseract_save(tmp_path):
    out = tmp_path / "tesseract_test.png"
    data = render_tesseract(n_max=3, save_path=out)
    assert out.exists()
    assert isinstance(data, TesseractFrameData)


# ===========================================================================
# CMBFalsificationTest
# ===========================================================================


def test_cmb_test_default_creates():
    test = CMBFalsificationTest(n_sim=100)
    assert test.n_sim == 100
    assert test.v_rig_kms == V_RIG_KMS
    assert test.v_cmb_kms == V_CMB_KMS


def test_cmb_test_run_returns_result():
    test = CMBFalsificationTest(n_sim=500, seed=42)
    result = test.run()
    assert isinstance(result, CMBTestResult)


def test_cmb_test_p_value_in_range():
    test = CMBFalsificationTest(n_sim=1000, seed=42)
    result = test.run()
    assert 0.0 <= result.p_value <= 1.0


def test_cmb_test_n_consistent_leq_n_sim():
    test = CMBFalsificationTest(n_sim=500, seed=42)
    result = test.run()
    assert 0 <= result.n_consistent <= result.n_sim


def test_cmb_test_p_value_equals_n_consistent_ratio():
    test = CMBFalsificationTest(n_sim=200, seed=7)
    result = test.run()
    assert result.p_value == pytest.approx(result.n_consistent / result.n_sim, rel=1e-9)


def test_cmb_test_expected_v_is_vrig_half():
    test = CMBFalsificationTest(v_rig_kms=1352.0)
    result = test.run()
    assert result.expected_v_kms == pytest.approx(676.0, rel=1e-9)


def test_cmb_test_mean_near_vrig_half():
    """MC-Mittelwert sollte nahe bei V_RIG/2 liegen (für viele Samples)."""
    test = CMBFalsificationTest(n_sim=50_000, seed=123)
    result = test.run()
    # Bei 50k Samples: Mittelwert ≈ V_RIG/2 = 676 km/s ± einige km/s
    assert abs(result.mean_sim_kms - result.expected_v_kms) < 20.0


def test_cmb_test_std_near_vrig_over_sqrt12():
    """Std-Abweichung von U(0, V_RIG) ≈ V_RIG / sqrt(12)."""
    test = CMBFalsificationTest(n_sim=50_000, seed=99, sigma_noise=0.0)
    result = test.run()
    expected_std = V_RIG_KMS / math.sqrt(12.0)
    assert abs(result.std_sim_kms - expected_std) < 50.0  # tolerant wegen Noise


def test_cmb_test_reproducible_with_seed():
    t1 = CMBFalsificationTest(n_sim=500, seed=42)
    t2 = CMBFalsificationTest(n_sim=500, seed=42)
    r1 = t1.run()
    r2 = t2.run()
    assert r1.p_value == r2.p_value
    assert r1.mean_sim_kms == r2.mean_sim_kms


def test_cmb_test_different_seeds_differ():
    t1 = CMBFalsificationTest(n_sim=500, seed=1)
    t2 = CMBFalsificationTest(n_sim=500, seed=2)
    r1 = t1.run()
    r2 = t2.run()
    assert r1.mean_sim_kms != r2.mean_sim_kms


def test_cmb_test_v_rig_stored():
    test = CMBFalsificationTest(n_sim=100, v_rig_kms=1000.0)
    result = test.run()
    assert result.v_rig_kms == 1000.0


def test_cmb_test_v_cmb_stored():
    test = CMBFalsificationTest(n_sim=100, v_cmb_kms=370.0)
    result = test.run()
    assert result.v_cmb_kms == 370.0


def test_cmb_test_alpha_stored():
    test = CMBFalsificationTest(n_sim=100, alpha=0.01)
    result = test.run()
    assert result.alpha == 0.01


def test_cmb_test_is_falsified_consistent_with_p():
    test = CMBFalsificationTest(n_sim=500, seed=42, alpha=0.05)
    result = test.run()
    assert result.is_falsified == (result.p_value < result.alpha)


def test_cmb_test_verdict_not_empty():
    test = CMBFalsificationTest(n_sim=100, seed=42)
    result = test.run()
    assert len(result.verdict) > 0
    assert "FALSIFIZIERT" in result.verdict


def test_cmb_test_str_representation():
    test = CMBFalsificationTest(n_sim=100, seed=42)
    result = test.run()
    s = str(result)
    assert "CMBTestResult" in s
    assert "p-Wert" in s
    assert "V_RIG" in s


# ===========================================================================
# run_cmb_test (Convenience-Funktion)
# ===========================================================================


def test_run_cmb_test_returns_result():
    result = run_cmb_test(n_sim=100, seed=42)
    assert isinstance(result, CMBTestResult)


def test_run_cmb_test_custom_v_rig():
    result = run_cmb_test(n_sim=100, v_rig_kms=2000.0, seed=1)
    assert result.v_rig_kms == 2000.0


def test_run_cmb_test_custom_v_cmb():
    result = run_cmb_test(n_sim=100, v_cmb_kms=400.0, seed=1)
    assert result.v_cmb_kms == 400.0


# ===========================================================================
# CLI: ig tesseract-render
# ===========================================================================


def test_cli_tesseract_render_ascii():
    result = runner.invoke(app, ["tesseract-render", "--ascii"])
    assert result.exit_code == 0, result.output
    assert "T_n" in result.output
    assert "CREP" in result.output


def test_cli_tesseract_render_ascii_n_max():
    result = runner.invoke(app, ["tesseract-render", "--ascii", "--n-max", "4"])
    assert result.exit_code == 0, result.output
    # Alle n von 0 bis 4 sollen sichtbar sein
    for n in range(5):
        assert str(n) in result.output


def test_cli_tesseract_render_default(tmp_path):
    # Ohne --save: nur ASCII + Tipp
    result = runner.invoke(app, ["tesseract-render"])
    assert result.exit_code == 0, result.output
    assert "Tesseract" in result.output


def test_cli_tesseract_render_save_png(tmp_path):
    out = str(tmp_path / "test_render.png")
    result = runner.invoke(app, ["tesseract-render", "--save", out, "--n-max", "3"])
    assert result.exit_code == 0, result.output
    assert Path(out).exists()


# ===========================================================================
# CLI: ig cmb-test
# ===========================================================================


def test_cli_cmb_test_default():
    result = runner.invoke(app, ["cmb-test"])
    assert result.exit_code == 0, result.output
    assert "CMB" in result.output
    assert "p-Wert" in result.output or "Urteil" in result.output


def test_cli_cmb_test_n_sim():
    result = runner.invoke(app, ["cmb-test", "--n-sim", "500"])
    assert result.exit_code == 0, result.output
    assert "500" in result.output


def test_cli_cmb_test_seed():
    result = runner.invoke(app, ["cmb-test", "--n-sim", "500", "--seed", "42"])
    assert result.exit_code == 0, result.output


def test_cli_cmb_test_custom_v_rig():
    result = runner.invoke(app, ["cmb-test", "--v-rig", "1352.0", "--n-sim", "200"])
    assert result.exit_code == 0, result.output
    assert "1352" in result.output


def test_cli_cmb_test_shows_verdict():
    result = runner.invoke(app, ["cmb-test", "--n-sim", "200", "--seed", "0"])
    assert result.exit_code == 0, result.output
    assert "FALSIFIZIERT" in result.output
