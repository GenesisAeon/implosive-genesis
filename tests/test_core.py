"""Tests für den mathematischen Kern – Phase 2 (physics, vrig, type6, CLI)."""

from __future__ import annotations

import math

import pytest
from typer.testing import CliRunner

from implosive_genesis.cli import app
from implosive_genesis.core.physics import PHI, PhiScaling
from implosive_genesis.core.type6 import Type6Implosive, cubic_root_jump, inverted_sigmoid
from implosive_genesis.core.vrig import (
    COSMIC_ALPHA,
    V_RIG_KMS,
    VRIGResult,
    compute_vrig,
    cosmic_alpha_phi,
)

runner = CliRunner()


# ===========================================================================
# core/__init__.py – re-export smoke test
# ===========================================================================


def test_core_init_exports() -> None:
    """Alle öffentlichen Namen werden aus core/__init__.py re-exportiert."""
    from implosive_genesis import core

    for name in [
        "PHI",
        "PhiScaling",
        "COSMIC_ALPHA",
        "V_RIG_KMS",
        "VRIGResult",
        "compute_vrig",
        "cosmic_alpha_phi",
        "Type6Implosive",
        "cubic_root_jump",
        "inverted_sigmoid",
    ]:
        assert hasattr(core, name), f"core.{name} fehlt"


# ===========================================================================
# physics.py
# ===========================================================================


class TestPHI:
    def test_value(self) -> None:
        assert math.isclose(PHI, 1.6180339887498949, rel_tol=1e-12)

    def test_golden_ratio_property(self) -> None:
        """Φ² = Φ + 1 (Goldener Schnitt Identität)."""
        assert math.isclose(PHI**2, PHI + 1, rel_tol=1e-12)


class TestPhiScaling:
    def test_beta_n_zero(self) -> None:
        """β_0 = β₀ · Φ^0 = β₀."""
        ps = PhiScaling(beta_0=2.5)
        assert math.isclose(ps.beta_n(0), 2.5)

    def test_beta_n_three(self) -> None:
        """β_3 = β₀ · Φ^1 = β₀ · Φ."""
        ps = PhiScaling(beta_0=1.0)
        assert math.isclose(ps.beta_n(3), PHI, rel_tol=1e-12)

    def test_beta_n_six(self) -> None:
        """β_6 = β₀ · Φ²."""
        ps = PhiScaling(beta_0=1.0)
        assert math.isclose(ps.beta_n(6), PHI**2, rel_tol=1e-12)

    def test_beta_n_default_beta0(self) -> None:
        """Standard-β₀ ist 1.0."""
        ps = PhiScaling()
        assert math.isclose(ps.beta_n(0), 1.0)

    def test_beta_n_fractional(self) -> None:
        """β_n funktioniert mit nicht-ganzzahligem n."""
        ps = PhiScaling(beta_0=1.0)
        result = ps.beta_n(1.5)
        expected = PHI ** (1.5 / 3.0)
        assert math.isclose(result, expected, rel_tol=1e-12)

    def test_geometric_waste_zero(self) -> None:
        """W(0) = 0 – kein Verschnitt bei n=0."""
        ps = PhiScaling()
        assert math.isclose(ps.geometric_waste(0), 0.0)

    def test_geometric_waste_positive(self) -> None:
        """W(n) > 0 für n > 0."""
        ps = PhiScaling()
        assert ps.geometric_waste(1) > 0.0
        assert ps.geometric_waste(3) > 0.0

    def test_geometric_waste_less_than_one(self) -> None:
        """W(n) < 1 für alle endlichen n."""
        ps = PhiScaling()
        for n in range(1, 20):
            assert ps.geometric_waste(n) < 1.0

    def test_geometric_waste_monotonically_increasing(self) -> None:
        """W(n) ist streng monoton wachsend."""
        ps = PhiScaling()
        wastes = ps.waste_series(10)
        for i in range(len(wastes) - 1):
            assert wastes[i] < wastes[i + 1]

    def test_beta_series_length(self) -> None:
        """beta_series gibt n_max+1 Werte zurück."""
        ps = PhiScaling()
        series = ps.beta_series(5)
        assert len(series) == 6

    def test_beta_series_first_element(self) -> None:
        """Erstes Element ist β₀."""
        ps = PhiScaling(beta_0=3.0)
        assert math.isclose(ps.beta_series(3)[0], 3.0)

    def test_waste_series_length(self) -> None:
        """waste_series gibt n_max+1 Werte zurück."""
        ps = PhiScaling()
        series = ps.waste_series(7)
        assert len(series) == 8

    def test_min_waste_index_is_zero(self) -> None:
        """Geringster Verschnitt liegt immer bei n=0."""
        ps = PhiScaling()
        assert ps.min_waste_index(10) == 0

    def test_beta_n_scaling_with_beta0(self) -> None:
        """β_n skaliert linear mit β₀."""
        ps1 = PhiScaling(beta_0=1.0)
        ps2 = PhiScaling(beta_0=2.0)
        assert math.isclose(ps2.beta_n(6), 2.0 * ps1.beta_n(6), rel_tol=1e-12)


# ===========================================================================
# vrig.py
# ===========================================================================


class TestConstants:
    def test_v_rig_kms(self) -> None:
        assert math.isclose(V_RIG_KMS, 1352.0)

    def test_cosmic_alpha(self) -> None:
        """α ≈ 1/137.036."""
        assert math.isclose(COSMIC_ALPHA, 1.0 / 137.035999084, rel_tol=1e-10)


class TestCosmicAlphaPhi:
    def test_default(self) -> None:
        result = cosmic_alpha_phi()
        assert math.isclose(result, COSMIC_ALPHA * PHI, rel_tol=1e-12)

    def test_custom_alpha(self) -> None:
        custom = 0.01
        result = cosmic_alpha_phi(alpha=custom)
        assert math.isclose(result, custom * PHI, rel_tol=1e-12)

    def test_value_range(self) -> None:
        """α_Φ liegt zwischen 0.011 und 0.012."""
        result = cosmic_alpha_phi()
        assert 0.011 < result < 0.012


class TestVRIGResult:
    def test_frozen(self) -> None:
        """VRIGResult ist immutable (frozen dataclass)."""
        r = VRIGResult(v_rig=1352.0, alpha_phi=0.011, std_dev=12.0, samples=100)
        with pytest.raises((AttributeError, TypeError)):
            r.v_rig = 0.0  # type: ignore[misc]

    def test_str_representation(self) -> None:
        r = VRIGResult(v_rig=1352.0, alpha_phi=0.01180, std_dev=11.9, samples=10000)
        s = str(r)
        assert "1352" in s
        assert "km/s" in s
        assert "α_Φ" in s

    def test_fields(self) -> None:
        r = VRIGResult(v_rig=1400.0, alpha_phi=0.012, std_dev=15.0, samples=5000)
        assert r.v_rig == 1400.0
        assert r.alpha_phi == 0.012
        assert r.std_dev == 15.0
        assert r.samples == 5000


class TestComputeVRIG:
    def test_returns_vrig_result(self) -> None:
        result = compute_vrig(seed=42)
        assert isinstance(result, VRIGResult)

    def test_base_case_n0_beta1(self) -> None:
        """n=0, β=1 → v ≈ V_RIG_KMS (Rauschen gemittelt weg)."""
        result = compute_vrig(beta_0=1.0, n=0, samples=100_000, noise_sigma=1.0, seed=0)
        assert math.isclose(result.v_rig, V_RIG_KMS, rel_tol=0.01)

    def test_n3_scales_by_phi(self) -> None:
        """n=3 → v ≈ V_RIG_KMS · Φ."""
        result = compute_vrig(beta_0=1.0, n=3, samples=100_000, noise_sigma=0.1, seed=0)
        expected = V_RIG_KMS * PHI
        assert math.isclose(result.v_rig, expected, rel_tol=0.01)

    def test_seed_reproducibility(self) -> None:
        """Gleicher Seed → gleiche Ergebnisse."""
        r1 = compute_vrig(seed=99)
        r2 = compute_vrig(seed=99)
        assert r1.v_rig == r2.v_rig
        assert r1.std_dev == r2.std_dev

    def test_different_seeds(self) -> None:
        """Unterschiedliche Seeds → unterschiedliche Ergebnisse (sehr wahrscheinlich)."""
        r1 = compute_vrig(seed=1)
        r2 = compute_vrig(seed=2)
        assert r1.v_rig != r2.v_rig

    def test_std_dev_near_noise_sigma(self) -> None:
        """Standardabweichung liegt nahe beim noise_sigma."""
        sigma = 10.0
        result = compute_vrig(samples=100_000, noise_sigma=sigma, seed=42)
        assert math.isclose(result.std_dev, sigma, rel_tol=0.05)

    def test_alpha_phi_value(self) -> None:
        result = compute_vrig(seed=0)
        assert math.isclose(result.alpha_phi, cosmic_alpha_phi(), rel_tol=1e-12)

    def test_samples_stored(self) -> None:
        result = compute_vrig(samples=500, seed=0)
        assert result.samples == 500

    def test_none_seed(self) -> None:
        """seed=None läuft ohne Fehler."""
        result = compute_vrig(seed=None, samples=100)
        assert result.v_rig > 0


# ===========================================================================
# type6.py
# ===========================================================================


class TestInvertedSigmoid:
    def test_at_zero(self) -> None:
        """f(0) = 0.5 für jede Steilheit."""
        assert math.isclose(inverted_sigmoid(0.0), 0.5)

    def test_negative_infinity(self) -> None:
        """f(−∞) → 1."""
        assert math.isclose(inverted_sigmoid(-1000.0), 1.0, abs_tol=1e-9)

    def test_positive_infinity(self) -> None:
        """f(+∞) → 0."""
        assert math.isclose(inverted_sigmoid(1000.0), 0.0, abs_tol=1e-9)

    def test_monotonically_decreasing(self) -> None:
        xs = [-3.0, -1.0, 0.0, 1.0, 3.0]
        vals = [inverted_sigmoid(x) for x in xs]
        for i in range(len(vals) - 1):
            assert vals[i] > vals[i + 1]

    def test_output_in_zero_one(self) -> None:
        for x in [-10.0, -1.0, 0.0, 1.0, 10.0]:
            v = inverted_sigmoid(x)
            assert 0.0 < v < 1.0 or math.isclose(v, 0.0) or math.isclose(v, 1.0)

    def test_steepness_effect(self) -> None:
        """Höhere Steilheit → steilerer Abfall."""
        v_low = inverted_sigmoid(1.0, steepness=0.5)
        v_high = inverted_sigmoid(1.0, steepness=2.0)
        assert v_low > v_high

    def test_extreme_positive_clamp(self) -> None:
        """Für sehr großes x·k: kein OverflowError, Rückgabe ≈ 0."""
        result = inverted_sigmoid(1000.0, steepness=1000.0)
        assert result == 0.0

    def test_extreme_negative_clamp(self) -> None:
        """Für sehr kleines x·k: kein OverflowError, Rückgabe = 1."""
        result = inverted_sigmoid(-1000.0, steepness=1000.0)
        assert result == 1.0


class TestCubicRootJump:
    def test_at_threshold(self) -> None:
        """f(threshold) = 0."""
        assert cubic_root_jump(0.0) == 0.0
        assert cubic_root_jump(2.0, threshold=2.0) == 0.0

    def test_positive_side(self) -> None:
        """f(1; t=0, A=1) = 1^{1/3} = 1."""
        assert math.isclose(cubic_root_jump(1.0), 1.0)

    def test_negative_side(self) -> None:
        """f(-8; t=0, A=1) = -2."""
        assert math.isclose(cubic_root_jump(-8.0), -2.0)

    def test_amplitude_scaling(self) -> None:
        """Amplitude skaliert das Ergebnis."""
        v1 = cubic_root_jump(8.0, amplitude=1.0)
        v2 = cubic_root_jump(8.0, amplitude=3.0)
        assert math.isclose(v2, 3.0 * v1)

    def test_antisymmetry(self) -> None:
        """f(-x; t=0) = -f(x; t=0)."""
        for x in [1.0, 2.0, 5.0]:
            assert math.isclose(cubic_root_jump(-x), -cubic_root_jump(x))

    def test_custom_threshold(self) -> None:
        """Mit threshold=2: f(10; t=2) = (10-2)^{1/3} = 8^{1/3} = 2."""
        assert math.isclose(cubic_root_jump(10.0, threshold=2.0), 2.0)


class TestType6Implosive:
    def test_default_steepness_is_phi(self) -> None:
        model = Type6Implosive()
        assert math.isclose(model.steepness, PHI)

    def test_response_is_sum(self) -> None:
        """R(x) = sigmoid(x) + jump(x)."""
        model = Type6Implosive(steepness=1.0, threshold=0.0, amplitude=1.0)
        x = 2.0
        expected = inverted_sigmoid(x, 1.0) + cubic_root_jump(x, 0.0, 1.0)
        assert math.isclose(model.response(x), expected)

    def test_simulate_length(self) -> None:
        model = Type6Implosive()
        pts = model.simulate((-2.0, 2.0), steps=10)
        assert len(pts) == 10

    def test_simulate_single_step(self) -> None:
        model = Type6Implosive()
        pts = model.simulate((-1.0, 1.0), steps=1)
        assert len(pts) == 1
        assert math.isclose(pts[0][0], -1.0)

    def test_simulate_x_range(self) -> None:
        model = Type6Implosive()
        pts = model.simulate((-3.0, 3.0), steps=7)
        assert math.isclose(pts[0][0], -3.0)
        assert math.isclose(pts[-1][0], 3.0)

    def test_simulate_invalid_steps(self) -> None:
        model = Type6Implosive()
        with pytest.raises(ValueError, match="steps"):
            model.simulate((-1.0, 1.0), steps=0)

    def test_critical_point(self) -> None:
        model = Type6Implosive(threshold=1.5)
        assert math.isclose(model.critical_point(), 1.5)

    def test_sigmoid_only(self) -> None:
        model = Type6Implosive(steepness=2.0)
        x = 1.0
        assert math.isclose(model.sigmoid_only(x), inverted_sigmoid(x, 2.0))

    def test_jump_only(self) -> None:
        model = Type6Implosive(threshold=1.0, amplitude=2.0)
        x = 9.0
        expected = cubic_root_jump(9.0, threshold=1.0, amplitude=2.0)
        assert math.isclose(model.jump_only(x), expected)

    def test_response_components_sum(self) -> None:
        """response = sigmoid_only + jump_only."""
        model = Type6Implosive(steepness=0.8, threshold=0.5, amplitude=1.5)
        for x in [-2.0, 0.0, 1.0, 3.0]:
            assert math.isclose(model.response(x), model.sigmoid_only(x) + model.jump_only(x))


# ===========================================================================
# CLI: ig vrig-calc
# ===========================================================================


class TestCLIVrigCalc:
    def test_default_run(self) -> None:
        result = runner.invoke(app, ["vrig-calc"])
        assert result.exit_code == 0
        assert "V_RIG" in result.output
        assert "km/s" in result.output

    def test_output_contains_alpha_phi(self) -> None:
        result = runner.invoke(app, ["vrig-calc", "--seed", "42"])
        assert result.exit_code == 0
        assert "α_Φ" in result.output or "alpha" in result.output.lower()

    def test_with_custom_params(self) -> None:
        result = runner.invoke(
            app, ["vrig-calc", "--beta0", "0.5", "--n", "6", "--samples", "100", "--seed", "7"]
        )
        assert result.exit_code == 0
        assert "V_RIG" in result.output

    def test_seed_reproducibility_via_cli(self) -> None:
        r1 = runner.invoke(app, ["vrig-calc", "--seed", "123", "--samples", "500"])
        r2 = runner.invoke(app, ["vrig-calc", "--seed", "123", "--samples", "500"])
        assert r1.output == r2.output

    def test_sigma_option(self) -> None:
        result = runner.invoke(app, ["vrig-calc", "--sigma", "5.0", "--seed", "0"])
        assert result.exit_code == 0

    def test_base_v_rig_displayed(self) -> None:
        result = runner.invoke(app, ["vrig-calc"])
        assert "1352" in result.output


# ===========================================================================
# CLI: ig type6-sim
# ===========================================================================


class TestCLIType6Sim:
    def test_default_run(self) -> None:
        result = runner.invoke(app, ["type6-sim"])
        assert result.exit_code == 0
        assert "Type-6" in result.output or "R(x)" in result.output

    def test_table_has_rows(self) -> None:
        result = runner.invoke(app, ["type6-sim", "--steps", "5"])
        assert result.exit_code == 0
        # 5 data rows → output contains 5 x-values
        assert result.output.count("+") > 0 or result.output.count("-") > 0

    def test_custom_range(self) -> None:
        result = runner.invoke(app, ["type6-sim", "--xmin", "-1", "--xmax", "1", "--steps", "3"])
        assert result.exit_code == 0

    def test_invalid_xmin_ge_xmax(self) -> None:
        result = runner.invoke(app, ["type6-sim", "--xmin", "2", "--xmax", "1"])
        assert result.exit_code != 0

    def test_invalid_steps_less_than_2(self) -> None:
        result = runner.invoke(app, ["type6-sim", "--steps", "1"])
        assert result.exit_code != 0

    def test_critical_point_displayed(self) -> None:
        result = runner.invoke(app, ["type6-sim", "--threshold", "1.5"])
        assert result.exit_code == 0
        assert "1.5" in result.output

    def test_custom_steepness_amplitude(self) -> None:
        result = runner.invoke(
            app,
            ["type6-sim", "--steepness", "2.0", "--amplitude", "0.5", "--steps", "4"],
        )
        assert result.exit_code == 0

    def test_phi_steepness_in_output(self) -> None:
        result = runner.invoke(app, ["type6-sim"])
        assert result.exit_code == 0
        # Default steepness = PHI ≈ 1.618
        assert "1.618" in result.output
