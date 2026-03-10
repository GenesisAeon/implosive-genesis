"""Tests für das OIPK-Modul (v0.3.0) – Orthogonal Impulse Photon Kernel."""

from __future__ import annotations

import math

from implosive_genesis.oipk.kernel import (
    ALPHA_EM,
    C_LIGHT,
    HBAR,
    PHI,
    TAU_PERP_FACTOR,
    OIPKDimension,
    OIPKKernel,
    OIPKResult,
    compute_crep_oipk,
)

# ===========================================================================
# Konstanten
# ===========================================================================


def test_phi_value() -> None:
    assert abs(PHI - (1 + math.sqrt(5)) / 2) < 1e-12


def test_hbar_positive() -> None:
    assert HBAR > 0


def test_c_light_positive() -> None:
    assert C_LIGHT > 0


def test_alpha_em_value() -> None:
    assert abs(ALPHA_EM - 7.2973525693e-3) < 1e-15


def test_tau_perp_factor() -> None:
    assert abs(TAU_PERP_FACTOR - 1.0 / PHI) < 1e-12


# ===========================================================================
# OIPKKernel – Konstruktion
# ===========================================================================


def test_default_kernel_creates() -> None:
    k = OIPKKernel()
    assert k.lambda_m > 0
    assert k.alpha_phi > 0


def test_custom_lambda_kernel() -> None:
    k = OIPKKernel(lambda_m=1e-9)
    assert k.lambda_m == 1e-9


def test_custom_alpha_phi_kernel() -> None:
    k = OIPKKernel(alpha_phi=0.012)
    assert k.alpha_phi == 0.012


def test_default_lambda_derived_from_vrig() -> None:
    """λ_default = c / V_RIG ≈ 221.7 m."""
    k = OIPKKernel()
    expected = C_LIGHT / 1_352_000.0
    assert abs(k.lambda_m - expected) < 1e-6


def test_alpha_phi_default_is_alpha_times_phi() -> None:
    k = OIPKKernel()
    expected = ALPHA_EM * PHI
    assert abs(k.alpha_phi - expected) < 1e-15


# ===========================================================================
# OIPKKernel – tau_oipk und tau_perp
# ===========================================================================


def test_tau_oipk_equals_lambda_over_c() -> None:
    k = OIPKKernel(lambda_m=1e-6)
    assert abs(k.tau_oipk() - 1e-6 / C_LIGHT) < 1e-30


def test_tau_perp_equals_tau_over_phi() -> None:
    k = OIPKKernel(lambda_m=1e-6)
    assert abs(k.tau_perp() - k.tau_oipk() / PHI) < 1e-40


def test_tau_perp_less_than_tau_oipk() -> None:
    k = OIPKKernel()
    assert k.tau_perp() < k.tau_oipk()


def test_tau_perp_ratio_is_phi_inverse() -> None:
    k = OIPKKernel()
    ratio = k.tau_perp() / k.tau_oipk()
    assert abs(ratio - 1.0 / PHI) < 1e-12


# ===========================================================================
# OIPKKernel – angular_frequency
# ===========================================================================


def test_angular_frequency_formula() -> None:
    k = OIPKKernel(lambda_m=1e-6)
    expected = 2 * math.pi * C_LIGHT / 1e-6
    assert abs(k.angular_frequency() - expected) < 1.0


def test_angular_frequency_positive() -> None:
    assert OIPKKernel().angular_frequency() > 0


def test_angular_frequency_inversely_proportional_to_lambda() -> None:
    k1 = OIPKKernel(lambda_m=1e-9)
    k2 = OIPKKernel(lambda_m=2e-9)
    assert abs(k1.angular_frequency() / k2.angular_frequency() - 2.0) < 1e-10


# ===========================================================================
# OIPKKernel – energy
# ===========================================================================


def test_energy_formula() -> None:
    k = OIPKKernel(lambda_m=1e-6, alpha_phi=ALPHA_EM * PHI)
    expected = HBAR * k.angular_frequency() * k.alpha_phi
    assert abs(k.energy() - expected) < 1e-50


def test_energy_positive() -> None:
    assert OIPKKernel().energy() > 0


def test_energy_scales_with_lambda_inverse() -> None:
    k1 = OIPKKernel(lambda_m=1e-9)
    k2 = OIPKKernel(lambda_m=2e-9)
    ratio = k1.energy() / k2.energy()
    assert abs(ratio - 2.0) < 1e-10


# ===========================================================================
# OIPKKernel – frame_stability
# ===========================================================================


def test_frame_stability_formula() -> None:
    k = OIPKKernel()
    expected = PHI**2 / k.alpha_phi
    assert abs(k.frame_stability() - expected) < 1e-10


def test_frame_stability_large() -> None:
    """S_F ≫ 1 für realistische Parameter."""
    k = OIPKKernel()
    assert k.frame_stability() > 100


def test_frame_stability_dimensionless_positive() -> None:
    assert OIPKKernel().frame_stability() > 0


# ===========================================================================
# OIPKKernel – crep
# ===========================================================================


def test_crep_formula() -> None:
    k = OIPKKernel()
    expected = k.energy() * k.frame_stability() * PHI / C_LIGHT
    assert abs(k.crep() - expected) < 1e-50


def test_crep_positive() -> None:
    assert OIPKKernel().crep() > 0


def test_compute_crep_oipk_default() -> None:
    val = compute_crep_oipk()
    assert val > 0


def test_compute_crep_oipk_with_kernel() -> None:
    k = OIPKKernel(lambda_m=1e-9)
    val = compute_crep_oipk(k)
    assert abs(val - k.crep()) < 1e-50


def test_crep_matches_compute_helper() -> None:
    k = OIPKKernel()
    assert abs(k.crep() - compute_crep_oipk(k)) < 1e-50


# ===========================================================================
# OIPKKernel – impulse_energy
# ===========================================================================


def test_impulse_energy_n0_equals_kernel_energy() -> None:
    k = OIPKKernel()
    assert abs(k.impulse_energy(0) - k.energy()) < 1e-50


def test_impulse_energy_scales_with_phi() -> None:
    k = OIPKKernel()
    ratio = k.impulse_energy(3) / k.impulse_energy(0)
    assert abs(ratio - PHI) < 1e-10


def test_impulse_energy_positive_all_n() -> None:
    k = OIPKKernel()
    for n in range(10):
        assert k.impulse_energy(n) > 0


def test_impulse_energy_monotone_increasing() -> None:
    k = OIPKKernel()
    vals = [k.impulse_energy(n) for n in range(8)]
    assert all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))


# ===========================================================================
# OIPKKernel – coherence_length
# ===========================================================================


def test_coherence_length_n0_equals_lambda() -> None:
    k = OIPKKernel(lambda_m=1e-6)
    assert abs(k.coherence_length(0) - 1e-6) < 1e-20


def test_coherence_length_n3_scales_phi() -> None:
    k = OIPKKernel()
    assert abs(k.coherence_length(3) / k.coherence_length(0) - PHI) < 1e-10


def test_coherence_length_positive() -> None:
    k = OIPKKernel()
    for n in range(6):
        assert k.coherence_length(n) > 0


# ===========================================================================
# OIPKKernel – emergent_dimension
# ===========================================================================


def test_emergent_dimension_n0_not_collapsed() -> None:
    k = OIPKKernel()
    d = k.emergent_dimension(0)
    # n=0: I_0 = E_0, ratio=1 → D=0, not collapsed
    assert not d.collapsed
    assert isinstance(d.dimension, int)


def test_emergent_dimension_large_n_positive_dim() -> None:
    k = OIPKKernel()
    d = k.emergent_dimension(15)
    assert d.dimension >= 1
    assert not d.collapsed


def test_emergent_dimension_returns_oipk_dimension() -> None:
    k = OIPKKernel()
    d = k.emergent_dimension(5)
    assert isinstance(d, OIPKDimension)


def test_emergent_dimension_n_stored() -> None:
    k = OIPKKernel()
    d = k.emergent_dimension(7)
    assert d.n == 7


def test_emergent_dimension_axiom_no_collapse_for_n_gte_0() -> None:
    """Für n≥0 bleibt die Dimensionszahl ≥ 0."""
    k = OIPKKernel()
    for n in range(10):
        d = k.emergent_dimension(n)
        assert d.dimension >= 0


# ===========================================================================
# OIPKKernel – dimension_series
# ===========================================================================


def test_dimension_series_length() -> None:
    k = OIPKKernel()
    series = k.dimension_series(n_max=5)
    assert len(series) == 6


def test_dimension_series_n_values() -> None:
    k = OIPKKernel()
    series = k.dimension_series(n_max=4)
    for i, d in enumerate(series):
        assert d.n == i


def test_dimension_series_dimensions_nonneg() -> None:
    k = OIPKKernel()
    for d in k.dimension_series(n_max=9):
        assert d.dimension >= 0


# ===========================================================================
# OIPKKernel – compute (OIPKResult)
# ===========================================================================


def test_compute_returns_oipk_result() -> None:
    k = OIPKKernel()
    r = k.compute()
    assert isinstance(r, OIPKResult)


def test_compute_is_orthogonal_true() -> None:
    r = OIPKKernel().compute()
    assert r.is_orthogonal is True


def test_compute_lambda_consistent() -> None:
    k = OIPKKernel(lambda_m=1e-9)
    r = k.compute()
    assert r.lambda_m == 1e-9


def test_compute_tau_oipk_consistent() -> None:
    k = OIPKKernel(lambda_m=1e-9)
    r = k.compute()
    assert abs(r.tau_oipk - k.tau_oipk()) < 1e-40


def test_compute_tau_perp_consistent() -> None:
    k = OIPKKernel(lambda_m=1e-9)
    r = k.compute()
    assert abs(r.tau_perp - k.tau_perp()) < 1e-40


def test_compute_energy_consistent() -> None:
    k = OIPKKernel()
    r = k.compute()
    assert abs(r.energy_j - k.energy()) < 1e-50


def test_compute_crep_consistent() -> None:
    k = OIPKKernel()
    r = k.compute()
    assert abs(r.crep - k.crep()) < 1e-50


def test_compute_str_contains_lambda() -> None:
    r = OIPKKernel().compute()
    assert "λ_OIPK" in str(r)


def test_compute_str_contains_crep() -> None:
    r = OIPKKernel().compute()
    assert "CREP" in str(r)


def test_compute_str_contains_tau_perp() -> None:
    r = OIPKKernel().compute()
    assert "τ_⊥" in str(r)


# ===========================================================================
# oipk __init__ re-exports
# ===========================================================================


def test_oipk_init_exports() -> None:
    from implosive_genesis import oipk

    for name in ["OIPKKernel", "OIPKResult", "OIPKDimension", "compute_crep_oipk"]:
        assert hasattr(oipk, name), f"Missing export: {name}"


def test_oipk_init_constants_exported() -> None:
    from implosive_genesis import oipk

    assert hasattr(oipk, "HBAR")
    assert hasattr(oipk, "C_LIGHT")
    assert hasattr(oipk, "PHI")
    assert hasattr(oipk, "TAU_PERP_FACTOR")
