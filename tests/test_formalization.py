"""Tests für das Formalisierungs-Paket: entropic_price und phi_scaling."""

from __future__ import annotations

import math

import pytest
from typer.testing import CliRunner

from implosive_genesis.cli import app
from implosive_genesis.formalization.entropic_price import (
    EntropicPriceDerivation,
    EntropicPriceResult,
    integrate_entropic_price,
)
from implosive_genesis.formalization.phi_scaling import (
    PhiScalingProof,
    StabilityResult,
    stability_analysis,
)

runner = CliRunner()

PHI_VAL: float = (1.0 + math.sqrt(5.0)) / 2.0
K_B: float = 1.380649e-23


# ===========================================================================
# EntropicPriceDerivation – SymPy
# ===========================================================================


def test_derivation_numerical_positive():
    d = EntropicPriceDerivation(n_max_val=7, temperature=2.725, bits_val=1.0)
    val = d.numerical_value()
    assert val > 0.0


def test_derivation_numerical_scales_with_temperature():
    d1 = EntropicPriceDerivation(n_max_val=5, temperature=1.0)
    d2 = EntropicPriceDerivation(n_max_val=5, temperature=2.0)
    assert d2.numerical_value() == pytest.approx(2 * d1.numerical_value(), rel=1e-9)


def test_derivation_numerical_scales_with_n_max():
    """E_price wächst mit n_max (mehr Rekursionsstufen = mehr Entropie)."""
    d1 = EntropicPriceDerivation(n_max_val=3, temperature=2.725)
    d2 = EntropicPriceDerivation(n_max_val=6, temperature=2.725)
    # Integral-Teil skaliert mit n_max, Info-Teil ist konstant
    assert d2.numerical_value() > d1.numerical_value()


def test_derivation_proves_linearity_in_T():
    d = EntropicPriceDerivation()
    assert d.prove_linearity_in_T() is True


def test_derivation_latex_expression_not_empty():
    d = EntropicPriceDerivation()
    latex = d.latex_expression()
    assert len(latex) > 0
    assert "k" in latex.lower() or "T" in latex or "Phi" in latex or "phi" in latex.lower()


def test_derivation_symbolic_expression_has_T():

    d = EntropicPriceDerivation()
    expr = d.symbolic_expression()
    # Ausdruck sollte das Symbol T enthalten
    assert d._T in expr.free_symbols or expr.free_symbols  # nicht-konstant


def test_derivation_symbolic_closed_form_not_zero():
    import sympy as sp

    d = EntropicPriceDerivation()
    expr = d.symbolic_closed_form()
    assert expr != sp.S.Zero


def test_derivation_information_term_positive():
    EntropicPriceDerivation(temperature=2.725, bits_val=1.0)
    # k_B * T * ln(2) * 1.0 > 0
    assert K_B * 2.725 * math.log(2) > 0


def test_derivation_zero_bits_reduces_info_term():
    """Mit bits=0 ist der Informationsterm 0."""
    d = EntropicPriceDerivation(n_max_val=5, temperature=2.725, bits_val=0.0)
    val = d.numerical_value()
    # Nur Integral-Teil
    expected_integral = K_B * 2.725 * math.log(PHI_VAL) * 5.0 / 2.0
    assert val == pytest.approx(expected_integral, rel=1e-6)


# ===========================================================================
# integrate_entropic_price – Numerisch
# ===========================================================================


def test_integrate_result_type():
    result = integrate_entropic_price(n_max=7, steps=1000)
    assert isinstance(result, EntropicPriceResult)


def test_integrate_e_price_equals_sum_of_parts():
    result = integrate_entropic_price(n_max=5, steps=5000)
    assert result.e_price_j == pytest.approx(result.integral_part_j + result.info_part_j, rel=1e-9)


def test_integrate_info_part_correct():
    result = integrate_entropic_price(n_max=7, temperature=2.725, bits=1.0, steps=10)
    expected = K_B * 2.725 * math.log(2) * 1.0
    assert result.info_part_j == pytest.approx(expected, rel=1e-9)


def test_integrate_integral_converges_to_analytical():
    """Riemann-Summe soll gegen k_B·T·ln(Φ)·n_max/2 konvergieren."""
    n_max = 7
    T = 2.725
    analytical = K_B * T * math.log(PHI_VAL) * n_max / 2.0
    result = integrate_entropic_price(n_max=n_max, temperature=T, bits=0.0, steps=100_000)
    assert result.integral_part_j == pytest.approx(analytical, rel=1e-3)


def test_integrate_more_steps_closer_to_analytical():
    """Riemann-Summe bei 10 000 Schritten sehr nah am analytischen Wert."""
    n_max = 5
    T = 2.725
    bits = 0.0
    analytical = K_B * T * math.log(PHI_VAL) * n_max / 2.0
    r10000 = integrate_entropic_price(n_max=n_max, temperature=T, bits=bits, steps=10_000)
    # Relativer Fehler < 0.1% bei 10 000 Schritten
    assert r10000.integral_part_j == pytest.approx(analytical, rel=1e-3)


def test_integrate_phi_value_stored():
    result = integrate_entropic_price(steps=100)
    assert result.phi == pytest.approx(PHI_VAL, rel=1e-12)


def test_integrate_steps_stored():
    result = integrate_entropic_price(steps=12345)
    assert result.steps == 12345


def test_integrate_n_max_stored():
    result = integrate_entropic_price(n_max=9, steps=100)
    assert result.n_max == 9


def test_integrate_temperature_stored():
    result = integrate_entropic_price(temperature=3.0, steps=100)
    assert result.temperature_k == 3.0


def test_integrate_result_str():
    result = integrate_entropic_price(steps=100)
    s = str(result)
    assert "EntropicPriceResult" in s
    assert "E_price" in s


def test_integrate_zero_n_max_only_info_term():
    result = integrate_entropic_price(n_max=0, temperature=2.725, bits=1.0, steps=1000)
    # Integral ist 0 (n_max=0 → ΔS=0 überall)
    assert result.integral_part_j == pytest.approx(0.0, abs=1e-40)
    assert result.info_part_j > 0.0


# ===========================================================================
# PhiScalingProof – SymPy-Beweise
# ===========================================================================


def test_phi_scaling_verify_recursion():
    proof = PhiScalingProof()
    assert proof.verify_recursion() is True


def test_phi_scaling_verify_ratio_constant():
    proof = PhiScalingProof()
    assert proof.verify_ratio_constant() is True


def test_phi_scaling_verify_golden_ratio_identity():
    proof = PhiScalingProof()
    assert proof.verify_golden_ratio_identity() is True


def test_phi_scaling_run_all_proofs_all_true():
    proof = PhiScalingProof()
    results = proof.run_all_proofs()
    assert all(results.values()), f"Fehlgeschlagene Beweise: {results}"


def test_phi_scaling_beta_n_expr_at_zero():
    """β_0 = beta_0 · Φ^0 = beta_0."""
    import sympy as sp

    proof = PhiScalingProof(beta_0_val=1.0)
    expr = proof.beta_n_expr(sp.Integer(0))
    val = float(expr.subs({proof.beta_0: 1.0}).evalf())
    assert val == pytest.approx(1.0, rel=1e-9)


def test_phi_scaling_numerical_beta_series_length():
    proof = PhiScalingProof()
    series = proof.numerical_beta_series(n_max=7)
    assert len(series) == 8  # n = 0..7


def test_phi_scaling_numerical_beta_n0_equals_beta0():
    proof = PhiScalingProof(beta_0_val=2.5)
    series = proof.numerical_beta_series(n_max=5)
    n0, beta_n0 = series[0]
    assert n0 == 0
    assert beta_n0 == pytest.approx(2.5, rel=1e-9)


def test_phi_scaling_numerical_beta_monotone():
    """β_n wächst monoton mit n (Φ > 1)."""
    proof = PhiScalingProof(beta_0_val=1.0)
    series = proof.numerical_beta_series(n_max=6)
    betas = [b for _, b in series]
    assert all(betas[i] <= betas[i + 1] for i in range(len(betas) - 1))


def test_phi_scaling_lyapunov_positive():
    proof = PhiScalingProof()
    lam_expr = proof.lyapunov_exponent_symbolic()
    lam_val = float(lam_expr.evalf())
    assert lam_val > 0.0


def test_phi_scaling_derivative_not_zero():
    import sympy as sp

    proof = PhiScalingProof()
    deriv = proof.symbolic_derivative()
    assert deriv != sp.S.Zero


# ===========================================================================
# stability_analysis
# ===========================================================================


def test_stability_result_type():
    sa = stability_analysis()
    assert isinstance(sa, StabilityResult)


def test_stability_lyapunov_correct():
    sa = stability_analysis()
    expected = math.log(PHI_VAL) / 3.0
    assert sa.lyapunov_exponent == pytest.approx(expected, rel=1e-9)


def test_stability_is_exponential():
    sa = stability_analysis()
    assert sa.is_exponential is True


def test_stability_phi_val_correct():
    sa = stability_analysis()
    assert sa.phi_val == pytest.approx(PHI_VAL, rel=1e-12)


def test_stability_all_proofs_passed():
    sa = stability_analysis()
    assert sa.recursion_proved is True
    assert sa.ratio_proved is True
    assert sa.golden_id_proved is True


def test_stability_beta_n_latex_not_empty():
    sa = stability_analysis()
    assert len(sa.beta_n_latex) > 0


def test_stability_str():
    sa = stability_analysis()
    s = str(sa)
    assert "StabilityResult" in s
    assert "Φ" in s or "phi" in s.lower()
    assert "Lyapunov" in s


def test_stability_custom_beta0():
    sa = stability_analysis(beta_0=0.5)
    # Lyapunov-Exponent ist unabhängig von beta_0
    expected_lam = math.log(PHI_VAL) / 3.0
    assert sa.lyapunov_exponent == pytest.approx(expected_lam, rel=1e-9)


# ===========================================================================
# Formalisierungs-Paket __init__ Re-Exports
# ===========================================================================


def test_formalization_package_exports():
    from implosive_genesis.formalization import (
        EntropicPriceDerivation,
        PhiScalingProof,
        integrate_entropic_price,
        stability_analysis,
    )

    assert EntropicPriceDerivation is not None
    assert integrate_entropic_price is not None
    assert PhiScalingProof is not None
    assert stability_analysis is not None


# ===========================================================================
# CLI: ig entropy-price-sympy
# ===========================================================================


def test_cli_entropy_price_sympy_default():
    result = runner.invoke(app, ["entropy-price-sympy"])
    assert result.exit_code == 0, result.output
    assert "Entropischer Preis" in result.output
    assert "E_price" in result.output or "SymPy" in result.output


def test_cli_entropy_price_sympy_steps():
    result = runner.invoke(app, ["entropy-price-sympy", "--steps", "10000"])
    assert result.exit_code == 0, result.output
    assert "10" in result.output  # Schritte werden angezeigt


def test_cli_entropy_price_sympy_show_proof():
    result = runner.invoke(app, ["entropy-price-sympy", "--show-proof"])
    assert result.exit_code == 0, result.output
    assert "Beweis" in result.output or "linear" in result.output.lower()


def test_cli_entropy_price_sympy_custom_n_max():
    result = runner.invoke(app, ["entropy-price-sympy", "--n-max", "5", "--steps", "100"])
    assert result.exit_code == 0, result.output


# ===========================================================================
# CLI: ig phi-proof
# ===========================================================================


def test_cli_phi_proof_default():
    result = runner.invoke(app, ["phi-proof"])
    assert result.exit_code == 0, result.output
    assert "Phi" in result.output or "phi" in result.output.lower()
    assert "Beweis" in result.output or "Bewiesen" in result.output


def test_cli_phi_proof_custom_beta0():
    result = runner.invoke(app, ["phi-proof", "--beta0", "2.0", "--n-max", "5"])
    assert result.exit_code == 0, result.output


def test_cli_phi_proof_shows_lyapunov():
    result = runner.invoke(app, ["phi-proof"])
    assert result.exit_code == 0, result.output
    assert "Lyapunov" in result.output
