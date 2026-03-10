"""Tests für das chronology-Modul – ChronologyValidator und verwandte Klassen."""

from __future__ import annotations

import math

import pytest

from implosive_genesis.chronology.integration import (
    C_LIGHT,
    CHRONOLOGY_PARTS,
    COSMIC_ALPHA,
    HBAR,
    PHI,
    V_RIG_KMS,
    ChronologyResult,
    ChronologyValidator,
)

# ---------------------------------------------------------------------------
# Konstanten-Tests
# ---------------------------------------------------------------------------


def test_phi_value():
    assert abs(PHI - (1.0 + math.sqrt(5.0)) / 2.0) < 1e-12


def test_v_rig_value():
    assert abs(V_RIG_KMS - 1352.0) < 1e-10


def test_c_light_value():
    assert abs(C_LIGHT - 299_792_458.0) < 1.0


def test_cosmic_alpha():
    assert abs(COSMIC_ALPHA - 1.0 / 137.035999084) < 1e-12


def test_hbar_positive():
    assert HBAR > 0.0


# ---------------------------------------------------------------------------
# CHRONOLOGY_PARTS – Struktur
# ---------------------------------------------------------------------------


def test_chronology_parts_count():
    assert len(CHRONOLOGY_PARTS) == 10


def test_chronology_parts_numbers():
    for i, part in enumerate(CHRONOLOGY_PARTS):
        assert part.number == i + 1


def test_chronology_parts_titles_nonempty():
    for part in CHRONOLOGY_PARTS:
        assert len(part.title) > 0


def test_chronology_parts_descriptions_nonempty():
    for part in CHRONOLOGY_PARTS:
        assert len(part.description) > 0


def test_chronology_parts_modules_nonempty():
    for part in CHRONOLOGY_PARTS:
        assert len(part.modules) >= 1


def test_chronology_parts_formulas_nonempty():
    for part in CHRONOLOGY_PARTS:
        assert len(part.key_formula) > 0


def test_chronology_parts_constants_positive():
    for part in CHRONOLOGY_PARTS:
        name, value = part.key_constant
        assert len(name) > 0
        assert math.isfinite(value)


def test_chronology_part_1_phi():
    part = CHRONOLOGY_PARTS[0]
    assert abs(part.key_constant[1] - PHI) < 1e-10


def test_chronology_part_2_vrig():
    part = CHRONOLOGY_PARTS[1]
    assert abs(part.key_constant[1] - V_RIG_KMS) < 1e-10


def test_chronology_part_frozen():
    """ChronologyPart ist ein frozen dataclass."""
    part = CHRONOLOGY_PARTS[0]
    with pytest.raises((AttributeError, TypeError)):
        part.number = 99  # type: ignore[misc]


# ---------------------------------------------------------------------------
# ChronologyValidator – Konstruktor
# ---------------------------------------------------------------------------


def test_validator_default():
    v = ChronologyValidator()
    assert v.tolerance == 1e-6


def test_validator_custom_tolerance():
    v = ChronologyValidator(tolerance=1e-9)
    assert v.tolerance == 1e-9


def test_validator_invalid_tolerance():
    with pytest.raises(ValueError, match="tolerance"):
        ChronologyValidator(tolerance=0.0)


def test_validator_invalid_tolerance_negative():
    with pytest.raises(ValueError, match="tolerance"):
        ChronologyValidator(tolerance=-1.0)


# ---------------------------------------------------------------------------
# ChronologyValidator – validate_part
# ---------------------------------------------------------------------------


def test_validate_part_invalid_number_0():
    v = ChronologyValidator()
    with pytest.raises(ValueError, match="Teilnummer"):
        v.validate_part(0)


def test_validate_part_invalid_number_11():
    v = ChronologyValidator()
    with pytest.raises(ValueError, match="Teilnummer"):
        v.validate_part(11)


@pytest.mark.parametrize("n", range(1, 11))
def test_validate_part_n_passes(n: int):
    v = ChronologyValidator()
    result = v.validate_part(n)
    assert result.passed, f"Teil {n} ({CHRONOLOGY_PARTS[n - 1].title}) failed: {result.checks}"


@pytest.mark.parametrize("n", range(1, 11))
def test_validate_part_n_returns_correct_part(n: int):
    v = ChronologyValidator()
    result = v.validate_part(n)
    assert result.part.number == n


@pytest.mark.parametrize("n", range(1, 11))
def test_validate_part_n_checks_nonempty(n: int):
    v = ChronologyValidator()
    result = v.validate_part(n)
    assert len(result.checks) > 0


@pytest.mark.parametrize("n", range(1, 11))
def test_validate_part_n_finite_values(n: int):
    v = ChronologyValidator()
    result = v.validate_part(n)
    assert math.isfinite(result.computed_value)
    assert math.isfinite(result.expected_value)
    assert math.isfinite(result.relative_error)


# ---------------------------------------------------------------------------
# ChronologyValidator – validate (alle 10 Teile)
# ---------------------------------------------------------------------------


def test_validate_all_passes():
    v = ChronologyValidator()
    result = v.validate()
    assert result.passed, f"Chronologie fehlgeschlagen: {result.summary}"


def test_validate_n_total():
    v = ChronologyValidator()
    result = v.validate()
    assert result.n_total == 10


def test_validate_n_passed():
    v = ChronologyValidator()
    result = v.validate()
    assert result.n_passed == 10


def test_validate_pass_rate_100():
    v = ChronologyValidator()
    result = v.validate()
    assert abs(result.pass_rate - 100.0) < 1e-10


def test_validate_part_results_count():
    v = ChronologyValidator()
    result = v.validate()
    assert len(result.part_results) == 10


def test_validate_summary_nonempty():
    v = ChronologyValidator()
    result = v.validate()
    assert len(result.summary) > 0


def test_validate_summary_contains_alle_bestanden():
    v = ChronologyValidator()
    result = v.validate()
    assert "BESTANDEN" in result.summary or "bestanden" in result.summary.lower()


def test_validate_result_type():
    v = ChronologyValidator()
    result = v.validate()
    assert isinstance(result, ChronologyResult)


# ---------------------------------------------------------------------------
# Einzelne Teile – numerische Korrektheit
# ---------------------------------------------------------------------------


def test_part_1_beta_3_equals_phi():
    """β_3 = β_0 · Φ^{3/3} = Φ (mit β_0=1)."""
    beta_3 = PHI ** (3 / 3.0)
    assert abs(beta_3 - PHI) < 1e-12


def test_part_2_alpha_phi():
    """α_Φ = α · Φ."""
    alpha_phi = COSMIC_ALPHA * PHI
    assert 0.011 < alpha_phi < 0.013


def test_part_2_lambda_oipk():
    """λ_OIPK = c / V_RIG."""
    lambda_oipk = C_LIGHT / (V_RIG_KMS * 1000.0)
    assert 200.0 < lambda_oipk < 250.0


def test_part_3_sigmoid_at_zero():
    def inv_sigmoid(x, k=1.0):
        return 1.0 / (1.0 + math.exp(k * x))

    assert abs(inv_sigmoid(0.0) - 0.5) < 1e-12


def test_part_4_theta_orthogonal():
    """Θ = arccos(-1/Φ) ≈ 128.17°."""
    theta_deg = math.degrees(math.acos(-1.0 / PHI))
    assert 128.0 < theta_deg < 129.0


def test_part_5_log_phi():
    """log_Φ(Φ^3) = 3."""
    result = math.log(PHI**3) / math.log(PHI)
    assert abs(result - 3.0) < 1e-10


def test_part_6_time_slice_ratio():
    """T_{n+1} / T_n = Φ."""
    t0 = 1.0
    for n in range(5):
        tn = t0 * PHI**n
        tn1 = t0 * PHI ** (n + 1)
        assert abs(tn1 / tn - PHI) < 1e-10


def test_part_7_ln_phi_positive():
    assert math.log(PHI) > 0.0


def test_part_8_anesthesia_threshold():
    alpha_phi = COSMIC_ALPHA * PHI
    threshold = alpha_phi / PHI**2
    assert 0.004 < threshold < 0.005


def test_part_9_intensity_decreasing():
    intensities = [1.0 / PHI**n for n in range(8)]
    for i in range(len(intensities) - 1):
        assert intensities[i] > intensities[i + 1]


def test_part_10_golden_identity():
    """Φ² = Φ + 1."""
    assert abs(PHI**2 - (PHI + 1.0)) < 1e-10


def test_part_10_all_constants_finite():
    for c in [PHI, V_RIG_KMS, COSMIC_ALPHA, HBAR, C_LIGHT]:
        assert math.isfinite(c)
        assert c > 0.0


def test_part_2_alpha_phi_range():
    """α_Φ liegt im erwarteten Bereich."""
    alpha_phi = COSMIC_ALPHA * PHI
    assert 0.011 < alpha_phi < 0.013


def test_part_2_alpha_ratio_equals_phi():
    """α_Φ / α = Φ (exakte Relation)."""
    alpha_phi = COSMIC_ALPHA * PHI
    assert abs(alpha_phi / COSMIC_ALPHA - PHI) < 1e-10


def test_part_10_lambda_oipk_identity():
    """λ_OIPK · V_RIG / c = 1 (Definitionsidentität)."""
    v_rig_ms = V_RIG_KMS * 1000.0
    lambda_oipk = C_LIGHT / v_rig_ms
    assert abs(lambda_oipk * v_rig_ms / C_LIGHT - 1.0) < 1e-10


# ---------------------------------------------------------------------------
# ChronologyResult – pass_rate
# ---------------------------------------------------------------------------


def test_pass_rate_calculation():
    v = ChronologyValidator()
    result = v.validate()
    expected = 100.0 * result.n_passed / result.n_total
    assert abs(result.pass_rate - expected) < 1e-10


def test_pass_rate_empty_would_be_zero():
    """pass_rate = 0 wenn n_total = 0 (Grenzfall)."""
    dummy_result = ChronologyResult(
        passed=True,
        n_passed=0,
        n_total=0,
        part_results=[],
        summary="",
    )
    assert dummy_result.pass_rate == 0.0


# ---------------------------------------------------------------------------
# Tests für core/integration (ImplosiveGenesis)
# ---------------------------------------------------------------------------


def test_implosive_genesis_import():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis()
    assert ig is not None


def test_implosive_genesis_phi():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis()
    assert abs(ig.phi - PHI) < 1e-12


def test_implosive_genesis_v_rig():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis()
    assert abs(ig.v_rig_kms - V_RIG_KMS) < 1e-10


def test_implosive_genesis_alpha_phi():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis()
    assert abs(ig.alpha_phi - COSMIC_ALPHA * PHI) < 1e-12


def test_implosive_genesis_lambda_oipk():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis()
    expected = C_LIGHT / (V_RIG_KMS * 1000.0)
    assert abs(ig.lambda_oipk - expected) < 0.001


def test_implosive_genesis_beta_n_0():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis(beta_0=1.0)
    assert abs(ig.beta_n(0) - 1.0) < 1e-12


def test_implosive_genesis_beta_n_3():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis(beta_0=1.0)
    assert abs(ig.beta_n(3) - PHI) < 1e-10


def test_implosive_genesis_coherence_length():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis()
    expected = ig.lambda_oipk * PHI ** (3 / 3.0)
    assert abs(ig.coherence_length(3) - expected) < 1e-8


def test_implosive_genesis_time_slice():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis(t0=1.0)
    assert abs(ig.time_slice(3) - PHI**3) < 1e-10


def test_implosive_genesis_fractal_intensity():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis()
    assert abs(ig.fractal_intensity(0) - 1.0) < 1e-12
    assert abs(ig.fractal_intensity(1) - 1.0 / PHI) < 1e-12


def test_implosive_genesis_geometric_waste():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis()
    assert abs(ig.geometric_waste(0) - 0.0) < 1e-12
    assert 0.0 < ig.geometric_waste(3) < 1.0


def test_implosive_genesis_invalid_beta():
    from implosive_genesis.core.integration import ImplosiveGenesis

    with pytest.raises(ValueError, match="beta_0"):
        ImplosiveGenesis(beta_0=-1.0)


def test_implosive_genesis_render_fractal_ascii():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis()
    art = ig.render_fractal_ascii(depth=3)
    assert isinstance(art, str)
    assert "FractalTesseract" in art


def test_implosive_genesis_render_fractal_result():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis()
    result = ig.render_fractal(depth=3)
    assert result.depth == 3


def test_implosive_genesis_validate_chronology():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis()
    result = ig.validate_chronology()
    assert result.passed
    assert result.n_passed == 10


def test_implosive_genesis_full_summary():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis()
    summary = ig.full_summary(n=5)
    assert summary.n == 5
    assert summary.chronology_passed
    assert summary.n_chronology_passed == 10
    assert summary.consistency_check
    assert summary.golden_identity
    assert abs(summary.phi - PHI) < 1e-12


def test_implosive_genesis_full_summary_no_chronology():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis()
    summary = ig.full_summary(n=3, validate_chronology=False)
    assert summary.n == 3
    assert not summary.chronology_passed
    assert summary.n_chronology_passed == 0


def test_implosive_genesis_repr():
    from implosive_genesis.core.integration import ImplosiveGenesis

    ig = ImplosiveGenesis()
    r = repr(ig)
    assert "ImplosiveGenesis" in r
    assert "V_RIG" in r
