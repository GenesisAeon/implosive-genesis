"""Tests für den Theorie-Core – Phase 3 (frameprinciple, tesseract, models)."""

from __future__ import annotations

import math

import pytest

from implosive_genesis.core.physics import PHI
from implosive_genesis.core.vrig import V_RIG_KMS, cosmic_alpha_phi
from implosive_genesis.theory.frameprinciple import (
    C_LIGHT,
    HBAR,
    LAMBDA_OIPK_DEFAULT,
    THETA_ORTHOGONAL,
    FramePrinciple,
    OIPKernel,
)
from implosive_genesis.theory.models import FullSummary, ImplosiveGenesisModel
from implosive_genesis.theory.tesseract import (
    C_LIGHT_MS,
    CREP,
    K_BOLTZMANN,
    T0_DEFAULT,
    Tesseract,
)


# ===========================================================================
# theory/__init__.py – re-export smoke test
# ===========================================================================


def test_theory_init_exports() -> None:
    """Alle öffentlichen Namen werden aus theory/__init__.py re-exportiert."""
    from implosive_genesis import theory

    expected = [
        "HBAR",
        "C_LIGHT",
        "LAMBDA_OIPK_DEFAULT",
        "THETA_ORTHOGONAL",
        "OIPKernel",
        "FramePrinciple",
        "K_BOLTZMANN",
        "C_LIGHT_MS",
        "T0_DEFAULT",
        "Tesseract",
        "CREP",
        "FullSummary",
        "ImplosiveGenesisModel",
    ]
    for name in expected:
        assert hasattr(theory, name), f"theory.{name} fehlt"


# ===========================================================================
# frameprinciple.py – Konstanten
# ===========================================================================


class TestFrameprincipleConstants:
    def test_hbar_value(self) -> None:
        """ℏ ≈ 1.054571817e-34 J·s."""
        assert math.isclose(HBAR, 1.054571817e-34, rel_tol=1e-10)

    def test_c_light_value(self) -> None:
        """c = 299 792 458 m/s (exakt)."""
        assert C_LIGHT == 299_792_458.0

    def test_lambda_oipk_default(self) -> None:
        """λ_OIPK = c / V_RIG_MS."""
        expected = C_LIGHT / (V_RIG_KMS * 1_000.0)
        assert math.isclose(LAMBDA_OIPK_DEFAULT, expected, rel_tol=1e-12)

    def test_theta_orthogonal_value(self) -> None:
        """θ_⊥ = arccos(−1/Φ) ≈ 2.2370 rad (≈ 128.17°)."""
        expected = math.acos(-1.0 / PHI)
        assert math.isclose(THETA_ORTHOGONAL, expected, rel_tol=1e-12)

    def test_theta_orthogonal_in_degrees(self) -> None:
        """θ_⊥ in Grad liegt zwischen 128° und 129°."""
        deg = math.degrees(THETA_ORTHOGONAL)
        assert 128.0 < deg < 129.0


# ===========================================================================
# OIPKernel
# ===========================================================================


class TestOIPKernel:
    def test_default_lambda(self) -> None:
        """Standard-λ_OIPK entspricht LAMBDA_OIPK_DEFAULT."""
        kernel = OIPKernel()
        assert math.isclose(kernel.lambda_m, LAMBDA_OIPK_DEFAULT, rel_tol=1e-12)

    def test_angular_frequency_formula(self) -> None:
        """ω_F = 2π · c / λ."""
        kernel = OIPKernel(lambda_m=1.0)
        expected = 2.0 * math.pi * C_LIGHT
        assert math.isclose(kernel.angular_frequency(), expected, rel_tol=1e-12)

    def test_angular_frequency_positive(self) -> None:
        """ω_F > 0 für alle λ > 0."""
        kernel = OIPKernel(lambda_m=1e-10)
        assert kernel.angular_frequency() > 0.0

    def test_energy_positive(self) -> None:
        """E_OIPK > 0."""
        kernel = OIPKernel()
        assert kernel.energy() > 0.0

    def test_energy_formula(self) -> None:
        """E_OIPK = ℏ · ω_F · α_Φ."""
        kernel = OIPKernel()
        expected = HBAR * kernel.angular_frequency() * kernel.alpha_phi
        assert math.isclose(kernel.energy(), expected, rel_tol=1e-12)

    def test_frame_stability_positive(self) -> None:
        """S_F > 0."""
        kernel = OIPKernel()
        assert kernel.frame_stability() > 0.0

    def test_frame_stability_formula(self) -> None:
        """S_F = Φ² / α_Φ."""
        kernel = OIPKernel()
        expected = PHI**2 / kernel.alpha_phi
        assert math.isclose(kernel.frame_stability(), expected, rel_tol=1e-12)

    def test_frame_stability_large(self) -> None:
        """S_F >> 1 (makroskopische Stabilität)."""
        kernel = OIPKernel()
        assert kernel.frame_stability() > 100.0

    def test_orthogonality_angle_deg(self) -> None:
        """θ_⊥ in Grad ≈ 128.17°."""
        kernel = OIPKernel()
        deg = kernel.orthogonality_angle_deg()
        assert 128.0 < deg < 129.0

    def test_custom_lambda_scales_frequency(self) -> None:
        """Doppelte Wellenlänge → halbe Frequenz."""
        k1 = OIPKernel(lambda_m=1.0)
        k2 = OIPKernel(lambda_m=2.0)
        assert math.isclose(k1.angular_frequency(), 2.0 * k2.angular_frequency(), rel_tol=1e-12)

    def test_custom_alpha_phi(self) -> None:
        """Benutzerdefiniertes α_Φ wird korrekt gesetzt."""
        kernel = OIPKernel(alpha_phi=0.01)
        assert math.isclose(kernel.alpha_phi, 0.01)

    def test_default_alpha_phi(self) -> None:
        """Standard-α_Φ stimmt mit cosmic_alpha_phi() überein."""
        kernel = OIPKernel()
        assert math.isclose(kernel.alpha_phi, cosmic_alpha_phi(), rel_tol=1e-12)


# ===========================================================================
# FramePrinciple
# ===========================================================================


class TestFramePrinciple:
    def test_default_kernel(self) -> None:
        """Standard-FramePrinciple hat einen OIPKernel."""
        fp = FramePrinciple()
        assert isinstance(fp.kernel, OIPKernel)

    def test_coherence_length_n0(self) -> None:
        """L_0 = λ_OIPK (bei n=0 kein Skalierungsfaktor)."""
        kernel = OIPKernel(lambda_m=1.0)
        fp = FramePrinciple(kernel=kernel)
        assert math.isclose(fp.coherence_length(0), 1.0)

    def test_coherence_length_n3(self) -> None:
        """L_3 = λ_OIPK · Φ."""
        kernel = OIPKernel(lambda_m=1.0)
        fp = FramePrinciple(kernel=kernel)
        assert math.isclose(fp.coherence_length(3), PHI, rel_tol=1e-12)

    def test_coherence_length_monotone(self) -> None:
        """L_n streng monoton wachsend für n > 0."""
        fp = FramePrinciple()
        lengths = fp.coherence_series(8)
        for i in range(len(lengths) - 1):
            assert lengths[i] < lengths[i + 1]

    def test_impulse_energy_n0(self) -> None:
        """I_0 = E_OIPK."""
        fp = FramePrinciple()
        assert math.isclose(fp.impulse_energy(0), fp.kernel.energy(), rel_tol=1e-12)

    def test_impulse_energy_n3(self) -> None:
        """I_3 = E_OIPK · Φ."""
        fp = FramePrinciple()
        expected = fp.kernel.energy() * PHI
        assert math.isclose(fp.impulse_energy(3), expected, rel_tol=1e-12)

    def test_coherence_series_length(self) -> None:
        """coherence_series(n_max) liefert n_max+1 Werte."""
        fp = FramePrinciple()
        series = fp.coherence_series(4)
        assert len(series) == 5

    def test_impulse_series_length(self) -> None:
        """impulse_series(n_max) liefert n_max+1 Werte."""
        fp = FramePrinciple()
        series = fp.impulse_series(6)
        assert len(series) == 7

    def test_stability_at_n0(self) -> None:
        """S_F(0) = S_F des Kernels."""
        fp = FramePrinciple()
        assert math.isclose(fp.stability_at(0), fp.kernel.frame_stability(), rel_tol=1e-12)

    def test_stability_increases_with_n(self) -> None:
        """Stabilität wächst mit n."""
        fp = FramePrinciple()
        assert fp.stability_at(3) > fp.stability_at(0)
        assert fp.stability_at(6) > fp.stability_at(3)

    def test_coherence_length_fractional_n(self) -> None:
        """coherence_length funktioniert mit nicht-ganzzahligem n."""
        fp = FramePrinciple(kernel=OIPKernel(lambda_m=1.0))
        result = fp.coherence_length(1.5)
        expected = PHI ** (1.5 / 3.0)
        assert math.isclose(result, expected, rel_tol=1e-12)


# ===========================================================================
# tesseract.py – Konstanten
# ===========================================================================


class TestTesseractConstants:
    def test_k_boltzmann(self) -> None:
        """k_B = 1.380649e-23 J/K."""
        assert math.isclose(K_BOLTZMANN, 1.380649e-23, rel_tol=1e-10)

    def test_c_light_ms(self) -> None:
        """c = 299 792 458 m/s."""
        assert C_LIGHT_MS == 299_792_458.0

    def test_t0_default(self) -> None:
        """T0_DEFAULT = 1.0."""
        assert T0_DEFAULT == 1.0


# ===========================================================================
# Tesseract
# ===========================================================================


class TestTesseract:
    def test_time_slice_n0(self) -> None:
        """T_0 = t_0."""
        ts = Tesseract(t_0=2.0)
        assert math.isclose(ts.time_slice(0), 2.0)

    def test_time_slice_n1(self) -> None:
        """T_1 = t_0 · Φ."""
        ts = Tesseract(t_0=1.0)
        assert math.isclose(ts.time_slice(1), PHI, rel_tol=1e-12)

    def test_time_slice_n3(self) -> None:
        """T_3 = t_0 · Φ³."""
        ts = Tesseract(t_0=1.0)
        assert math.isclose(ts.time_slice(3), PHI**3, rel_tol=1e-12)

    def test_time_slice_monotone(self) -> None:
        """T_n streng monoton wachsend."""
        ts = Tesseract()
        slices = ts.slice_series(6)
        for i in range(len(slices) - 1):
            assert slices[i] < slices[i + 1]

    def test_volume_4d_n0(self) -> None:
        """V_4D(0) = t_0^4."""
        ts = Tesseract(t_0=2.0)
        assert math.isclose(ts.volume_4d(0), 16.0)

    def test_volume_4d_formula(self) -> None:
        """V_4D(n) = (t_0 · Φ^n)^4."""
        ts = Tesseract(t_0=1.0)
        for n in [0, 1, 2, 3]:
            expected = (PHI**n) ** 4
            assert math.isclose(ts.volume_4d(n), expected, rel_tol=1e-12)

    def test_slice_series_length(self) -> None:
        """slice_series(n_max) liefert n_max+1 Elemente."""
        ts = Tesseract()
        assert len(ts.slice_series(5)) == 6

    def test_volume_series_length(self) -> None:
        """volume_series(n_max) liefert n_max+1 Elemente."""
        ts = Tesseract()
        assert len(ts.volume_series(4)) == 5

    def test_resonance_frequency_positive(self) -> None:
        """f_R(n) > 0."""
        ts = Tesseract(t_0=1.0)
        assert ts.resonance_frequency(0) > 0.0
        assert ts.resonance_frequency(3) > 0.0

    def test_resonance_frequency_decreases_with_n(self) -> None:
        """Höheres n → niedrigere Resonanzfrequenz (T_n wächst)."""
        ts = Tesseract(t_0=1.0)
        assert ts.resonance_frequency(3) < ts.resonance_frequency(0)

    def test_resonance_frequency_formula(self) -> None:
        """f_R(n) = V_RIG_MS / T_n."""
        ts = Tesseract(t_0=1.0)
        v_rig_ms = V_RIG_KMS * 1_000.0
        for n in [0, 1, 2]:
            expected = v_rig_ms / ts.time_slice(n)
            assert math.isclose(ts.resonance_frequency(n), expected, rel_tol=1e-12)

    def test_expansion_ratio_formula(self) -> None:
        """Expansionsverhältnis = Φ^n."""
        ts = Tesseract()
        for n in [0, 1, 2, 3]:
            assert math.isclose(ts.expansion_ratio(n), PHI**n, rel_tol=1e-12)

    def test_default_t0(self) -> None:
        """Standard-t_0 ist T0_DEFAULT = 1.0."""
        ts = Tesseract()
        assert ts.t_0 == T0_DEFAULT


# ===========================================================================
# CREP
# ===========================================================================


class TestCREP:
    def test_crep_value_positive(self) -> None:
        """CREP(S_total > 0) > 0."""
        crep = CREP()
        assert crep.crep_value(1.0) > 0.0

    def test_crep_value_zero(self) -> None:
        """CREP(0) = 0."""
        crep = CREP()
        assert crep.crep_value(0.0) == 0.0

    def test_crep_value_linear(self) -> None:
        """CREP ist linear in S_total."""
        crep = CREP()
        assert math.isclose(crep.crep_value(2.0), 2.0 * crep.crep_value(1.0), rel_tol=1e-12)

    def test_crep_value_formula(self) -> None:
        """CREP = S · V_RIG_MS / (Φ · c²)."""
        crep = CREP()
        v_ms = V_RIG_KMS * 1_000.0
        s = 1.5
        expected = s * v_ms / (PHI * C_LIGHT_MS**2)
        assert math.isclose(crep.crep_value(s), expected, rel_tol=1e-12)

    def test_entropy_price_n0(self) -> None:
        """P_E(0, T) = 0 (keine Entropie bei n=0)."""
        crep = CREP()
        assert crep.entropy_price(0, 300.0) == 0.0

    def test_entropy_price_positive(self) -> None:
        """P_E(n > 0, T > 0) > 0."""
        crep = CREP()
        assert crep.entropy_price(1, 300.0) > 0.0

    def test_entropy_price_formula(self) -> None:
        """P_E(n, T) = n · k_B · T · ln(Φ)."""
        crep = CREP()
        n, T = 3, 100.0
        expected = n * K_BOLTZMANN * T * math.log(PHI)
        assert math.isclose(crep.entropy_price(n, T), expected, rel_tol=1e-12)

    def test_entropy_price_linear_in_n(self) -> None:
        """P_E linear in n."""
        crep = CREP()
        p1 = crep.entropy_price(1, 300.0)
        p3 = crep.entropy_price(3, 300.0)
        assert math.isclose(p3, 3.0 * p1, rel_tol=1e-12)

    def test_entropy_price_linear_in_temperature(self) -> None:
        """P_E linear in T."""
        crep = CREP()
        p100 = crep.entropy_price(2, 100.0)
        p200 = crep.entropy_price(2, 200.0)
        assert math.isclose(p200, 2.0 * p100, rel_tol=1e-12)

    def test_entropy_price_negative_temp_raises(self) -> None:
        """Negative Temperatur löst ValueError aus."""
        crep = CREP()
        with pytest.raises(ValueError, match="Temperatur"):
            crep.entropy_price(1, -1.0)

    def test_entropy_price_series_length(self) -> None:
        """entropy_price_series liefert n_max+1 Werte."""
        crep = CREP()
        series = crep.entropy_price_series(4, 300.0)
        assert len(series) == 5

    def test_entropy_price_series_first_zero(self) -> None:
        """Erster Wert der Serie ist 0 (n=0)."""
        crep = CREP()
        series = crep.entropy_price_series(4, 300.0)
        assert series[0] == 0.0

    def test_cumulative_crep(self) -> None:
        """Kumulativer CREP = Summe der Einzel-CREPs."""
        crep = CREP()
        values = [0.5, 1.0, 1.5]
        expected = sum(crep.crep_value(v) for v in values)
        assert math.isclose(crep.cumulative_crep(values), expected, rel_tol=1e-12)

    def test_crep_ratio_dimensionless(self) -> None:
        """crep_ratio ist kleiner als 1 für physikalische Entropiewerte."""
        crep = CREP()
        # CREP/c ist extrem klein für S_total=1 → ratio ≈ CREP·c/V_RIG_MS ≪ 1
        ratio = crep.crep_ratio(1.0)
        assert abs(ratio) < 1.0

    def test_custom_v_rig(self) -> None:
        """Benutzerdefiniertes v_rig_kms wird korrekt verwendet."""
        crep1 = CREP(v_rig_kms=1352.0)
        crep2 = CREP(v_rig_kms=2704.0)
        assert math.isclose(crep2.crep_value(1.0), 2.0 * crep1.crep_value(1.0), rel_tol=1e-12)


# ===========================================================================
# models.py – ImplosiveGenesisModel
# ===========================================================================


class TestImplosiveGenesisModel:
    def test_phi(self) -> None:
        """phi() gibt Goldenen Schnitt zurück."""
        model = ImplosiveGenesisModel()
        assert math.isclose(model.phi(), PHI, rel_tol=1e-12)

    def test_alpha_phi(self) -> None:
        """alpha_phi() stimmt mit cosmic_alpha_phi() überein."""
        model = ImplosiveGenesisModel()
        assert math.isclose(model.alpha_phi(), cosmic_alpha_phi(), rel_tol=1e-12)

    def test_beta_n_n0(self) -> None:
        """β_0 = β_0 (Basiskopplungskonstante)."""
        model = ImplosiveGenesisModel(beta_0=2.0)
        assert math.isclose(model.beta_n(0), 2.0)

    def test_beta_n_n3(self) -> None:
        """β_3 = β_0 · Φ."""
        model = ImplosiveGenesisModel(beta_0=1.0)
        assert math.isclose(model.beta_n(3), PHI, rel_tol=1e-12)

    def test_vrig_returns_vrig_result(self) -> None:
        """vrig() gibt VRIGResult zurück."""
        from implosive_genesis.core.vrig import VRIGResult

        model = ImplosiveGenesisModel()
        result = model.vrig(samples=100, seed=42)
        assert isinstance(result, VRIGResult)

    def test_coherence_length_n0(self) -> None:
        """coherence_length(0) = λ_OIPK."""
        model = ImplosiveGenesisModel()
        assert math.isclose(model.coherence_length(0), model.lambda_m, rel_tol=1e-12)

    def test_frame_stability_increases_with_n(self) -> None:
        """Frame-Stabilität wächst mit n."""
        model = ImplosiveGenesisModel()
        assert model.frame_stability(3) > model.frame_stability(0)

    def test_time_slice_n0(self) -> None:
        """time_slice(0) = t_0."""
        model = ImplosiveGenesisModel(t_0=2.5)
        assert math.isclose(model.time_slice(0), 2.5)

    def test_volume_4d_n0(self) -> None:
        """volume_4d(0) = t_0^4."""
        model = ImplosiveGenesisModel(t_0=2.0)
        assert math.isclose(model.volume_4d(0), 16.0)

    def test_entropy_price_n0(self) -> None:
        """entropy_price(0, T) = 0."""
        model = ImplosiveGenesisModel()
        assert model.entropy_price(0, 300.0) == 0.0

    def test_crep_positive(self) -> None:
        """crep() > 0."""
        model = ImplosiveGenesisModel()
        assert model.crep(s_total=1.0) > 0.0

    def test_constants_keys(self) -> None:
        """constants() enthält alle erwarteten Schlüssel."""
        model = ImplosiveGenesisModel()
        consts = model.constants()
        for key in ["PHI", "COSMIC_ALPHA", "alpha_phi", "V_RIG_KMS", "beta_0", "lambda_m", "t_0"]:
            assert key in consts, f"Schlüssel '{key}' fehlt in constants()"

    def test_constants_phi_value(self) -> None:
        """constants()['PHI'] ist der goldene Schnitt."""
        model = ImplosiveGenesisModel()
        assert math.isclose(model.constants()["PHI"], PHI, rel_tol=1e-12)


# ===========================================================================
# FullSummary
# ===========================================================================


class TestFullSummary:
    def _make_summary(self) -> FullSummary:
        model = ImplosiveGenesisModel()
        return model.full_summary(n=3, temperature=2.725, samples=100, seed=0)

    def test_returns_full_summary(self) -> None:
        """full_summary() gibt FullSummary zurück."""
        summary = self._make_summary()
        assert isinstance(summary, FullSummary)

    def test_n_stored(self) -> None:
        """n wird korrekt gespeichert."""
        summary = self._make_summary()
        assert summary.n == 3

    def test_temperature_stored(self) -> None:
        """Temperatur wird korrekt gespeichert."""
        summary = self._make_summary()
        assert math.isclose(summary.temperature_k, 2.725)

    def test_beta_n_positive(self) -> None:
        """β_n > 0."""
        summary = self._make_summary()
        assert summary.beta_n > 0.0

    def test_v_rig_positive(self) -> None:
        """V_RIG > 0."""
        summary = self._make_summary()
        assert summary.v_rig_result.v_rig > 0.0

    def test_coherence_length_positive(self) -> None:
        """L_n > 0."""
        summary = self._make_summary()
        assert summary.coherence_length_m > 0.0

    def test_impulse_energy_positive(self) -> None:
        """I_n > 0."""
        summary = self._make_summary()
        assert summary.impulse_energy_j > 0.0

    def test_frame_stability_positive(self) -> None:
        """S_F(n) > 0."""
        summary = self._make_summary()
        assert summary.frame_stability > 0.0

    def test_time_slice_positive(self) -> None:
        """T_n > 0."""
        summary = self._make_summary()
        assert summary.time_slice > 0.0

    def test_volume_4d_positive(self) -> None:
        """V_4D(n) > 0."""
        summary = self._make_summary()
        assert summary.volume_4d > 0.0

    def test_entropy_price_positive(self) -> None:
        """P_E > 0 für n > 0 und T > 0."""
        summary = self._make_summary()
        assert summary.entropy_price_j > 0.0

    def test_crep_positive(self) -> None:
        """CREP > 0."""
        summary = self._make_summary()
        assert summary.crep > 0.0

    def test_frozen(self) -> None:
        """FullSummary ist immutable (frozen dataclass)."""
        summary = self._make_summary()
        with pytest.raises((AttributeError, TypeError)):
            summary.n = 99  # type: ignore[misc]

    def test_str_representation(self) -> None:
        """__str__ enthält Schlüsselgrößen."""
        summary = self._make_summary()
        s = str(summary)
        assert "β_n" in s
        assert "V_RIG" in s
        assert "T_n" in s
        assert "CREP" in s

    def test_reproducible_with_seed(self) -> None:
        """Gleicher Seed → gleiche V_RIG-Ergebnisse."""
        model = ImplosiveGenesisModel()
        s1 = model.full_summary(n=2, temperature=300.0, samples=100, seed=7)
        s2 = model.full_summary(n=2, temperature=300.0, samples=100, seed=7)
        assert s1.v_rig_result.v_rig == s2.v_rig_result.v_rig
