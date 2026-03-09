"""Tests für die Simulations-Module: cosmic_moments und entropy_governance."""

from __future__ import annotations

import pytest
from typer.testing import CliRunner

from implosive_genesis.cli import app
from implosive_genesis.core.physics import PHI
from implosive_genesis.simulation.cosmic_moments import CosmicMoment, CosmicMomentsSimulator
from implosive_genesis.simulation.entropy_governance import (
    EntropyBudget,
    EntropyGovernance,
    GovernanceReport,
)

runner = CliRunner()

# ---------------------------------------------------------------------------
# CosmicMoment
# ---------------------------------------------------------------------------


def test_cosmic_moment_fields():
    m = CosmicMoment(
        n=3,
        time_slice=4.236,
        resonance_freq=1.0e9,
        entropy_price_j=1.5e-23,
        impulse_energy_j=2.0e-35,
        crep_value=3.0e-15,
        expansion_ratio=PHI**3,
        temperature_k=2.725,
    )
    assert m.n == 3
    assert m.expansion_ratio == pytest.approx(PHI**3, rel=1e-9)
    assert m.temperature_k == 2.725


def test_cosmic_moment_str():
    m = CosmicMoment(
        n=2,
        time_slice=2.618,
        resonance_freq=5.0e8,
        entropy_price_j=1.0e-23,
        impulse_energy_j=1.0e-35,
        crep_value=1.0e-15,
        expansion_ratio=PHI**2,
        temperature_k=2.725,
    )
    s = str(m)
    assert "CosmicMoment(n=2)" in s
    assert "T_n" in s
    assert "f_R" in s


# ---------------------------------------------------------------------------
# CosmicMomentsSimulator
# ---------------------------------------------------------------------------


def test_simulator_run_length():
    sim = CosmicMomentsSimulator(n_max=5)
    moments = sim.run()
    assert len(moments) == 6  # n = 0..5


def test_simulator_run_n_values():
    sim = CosmicMomentsSimulator(n_max=4)
    moments = sim.run()
    assert [m.n for m in moments] == [0, 1, 2, 3, 4]


def test_simulator_time_slice_phi_scaling():
    sim = CosmicMomentsSimulator(n_max=3, t_0=1.0)
    moments = sim.run()
    for m in moments:
        assert m.time_slice == pytest.approx(PHI**m.n, rel=1e-9)


def test_simulator_expansion_ratio():
    sim = CosmicMomentsSimulator(n_max=4)
    moments = sim.run()
    for m in moments:
        assert m.expansion_ratio == pytest.approx(PHI**m.n, rel=1e-9)


def test_simulator_entropy_price_n0():
    """n=0 gibt P_E = 0."""
    sim = CosmicMomentsSimulator(n_max=3, temperature=2.725)
    moments = sim.run()
    assert moments[0].entropy_price_j == pytest.approx(0.0, abs=1e-40)


def test_simulator_resonance_decreases_with_n():
    """Resonanzfrequenz nimmt mit n ab (T_n wächst)."""
    sim = CosmicMomentsSimulator(n_max=5)
    moments = sim.run()
    freqs = [m.resonance_freq for m in moments]
    assert all(freqs[i] > freqs[i + 1] for i in range(len(freqs) - 1))


def test_simulator_peak_moment_is_n0():
    """Peak-Resonanz ist bei n=0 (höchste Frequenz)."""
    sim = CosmicMomentsSimulator(n_max=5)
    peak = sim.peak_moment()
    assert peak.n == 0


def test_simulator_total_entropy_price_positive():
    sim = CosmicMomentsSimulator(n_max=5, temperature=2.725)
    total = sim.total_entropy_price()
    assert total > 0.0


def test_simulator_total_entropy_price_sum():
    sim = CosmicMomentsSimulator(n_max=4, temperature=2.725)
    moments = sim.run()
    expected = sum(m.entropy_price_j for m in moments)
    assert sim.total_entropy_price() == pytest.approx(expected, rel=1e-9)


def test_simulator_entropy_weighted_crep_positive():
    sim = CosmicMomentsSimulator(n_max=5)
    ewc = sim.entropy_weighted_crep()
    assert ewc >= 0.0


def test_simulator_crep_value_constant():
    """CREP(S=1) ist für alle Momente identisch."""
    sim = CosmicMomentsSimulator(n_max=3)
    moments = sim.run()
    crep_vals = [m.crep_value for m in moments]
    assert all(v == pytest.approx(crep_vals[0], rel=1e-9) for v in crep_vals)


def test_simulator_custom_vrig():
    sim = CosmicMomentsSimulator(n_max=2, v_rig_kms=1000.0)
    moments = sim.run()
    assert len(moments) == 3


# ---------------------------------------------------------------------------
# EntropyBudget
# ---------------------------------------------------------------------------


def test_entropy_budget_not_overflow_by_default():
    b = EntropyBudget(
        n=2,
        entropy_price_j=1e-23,
        budget_fraction=0.2,
        crep_contribution=1e-15,
        overflow_j=0.0,
        temperature_k=2.725,
    )
    assert not b.is_overflow


def test_entropy_budget_is_overflow():
    b = EntropyBudget(
        n=5,
        entropy_price_j=5e-23,
        budget_fraction=0.5,
        crep_contribution=5e-15,
        overflow_j=1e-24,
        temperature_k=2.725,
    )
    assert b.is_overflow


# ---------------------------------------------------------------------------
# EntropyGovernance
# ---------------------------------------------------------------------------


def test_governance_entropy_price_n0():
    gov = EntropyGovernance(n_max=5, temperature=2.725)
    assert gov.entropy_price(0) == pytest.approx(0.0, abs=1e-40)


def test_governance_entropy_price_scales_linearly():
    gov = EntropyGovernance(n_max=5, temperature=2.725)
    p1 = gov.entropy_price(1)
    p3 = gov.entropy_price(3)
    assert p3 == pytest.approx(3 * p1, rel=1e-9)


def test_governance_entropy_prices_length():
    gov = EntropyGovernance(n_max=6)
    prices = gov.entropy_prices()
    assert len(prices) == 7  # n = 0..6


def test_governance_total_entropy():
    gov = EntropyGovernance(n_max=4, temperature=2.725)
    prices = gov.entropy_prices()
    assert gov.total_entropy() == pytest.approx(sum(prices), rel=1e-9)


def test_governance_budget_fractions_sum_to_one():
    gov = EntropyGovernance(n_max=5, temperature=2.725)
    fracs = gov.budget_fractions()
    assert sum(fracs) == pytest.approx(1.0, rel=1e-9)


def test_governance_budget_fractions_n_max_0():
    """n_max=0 → P_E=0, alle Fraktionen 0."""
    gov = EntropyGovernance(n_max=0)
    fracs = gov.budget_fractions()
    assert fracs == [0.0]


def test_governance_overflow_none_ceiling():
    gov = EntropyGovernance(n_max=5, ceiling_j=None)
    assert gov.overflow(5) == 0.0


def test_governance_overflow_with_ceiling():
    gov = EntropyGovernance(n_max=5, temperature=2.725, ceiling_j=1e-25)
    p5 = gov.entropy_price(5)
    expected = max(0.0, p5 - 1e-25)
    assert gov.overflow(5) == pytest.approx(expected, rel=1e-9)


def test_governance_stable_levels_no_ceiling():
    gov = EntropyGovernance(n_max=5)
    stable = gov.stable_levels()
    assert stable == list(range(6))


def test_governance_critical_level_none():
    gov = EntropyGovernance(n_max=5, ceiling_j=None)
    assert gov.critical_level() is None


def test_governance_critical_level_very_low_ceiling():
    gov = EntropyGovernance(n_max=7, temperature=2.725, ceiling_j=1e-30)
    crit = gov.critical_level()
    # n=0 hat P_E=0, also kein Overflow; n=1 sollte P_E > 1e-30 haben
    assert crit is not None
    assert crit >= 1


def test_governance_crep_contributions_length():
    gov = EntropyGovernance(n_max=4)
    contribs = gov.crep_contributions()
    assert len(contribs) == 5


def test_governance_report_type():
    gov = EntropyGovernance(n_max=3)
    report = gov.governance_report()
    assert isinstance(report, GovernanceReport)
    assert len(report.budgets) == 4


def test_governance_report_total_entropy():
    gov = EntropyGovernance(n_max=4, temperature=2.725)
    report = gov.governance_report()
    assert report.total_entropy_j == pytest.approx(gov.total_entropy(), rel=1e-9)


def test_governance_report_str():
    gov = EntropyGovernance(n_max=3)
    report = gov.governance_report()
    s = str(report)
    assert "GovernanceReport" in s
    assert "Φ" in s


def test_governance_report_n_overflow_zero_no_ceiling():
    gov = EntropyGovernance(n_max=5)
    report = gov.governance_report()
    assert report.n_overflow == 0


def test_governance_report_ceiling_stored():
    gov = EntropyGovernance(n_max=3, ceiling_j=5e-24)
    report = gov.governance_report()
    assert report.ceiling_j == 5e-24


# ---------------------------------------------------------------------------
# CLI: ig simulate
# ---------------------------------------------------------------------------


def test_cli_simulate_default():
    result = runner.invoke(app, ["simulate"])
    assert result.exit_code == 0, result.output
    assert "Simulation" in result.output
    assert "T_n" in result.output


def test_cli_simulate_n_max():
    result = runner.invoke(app, ["simulate", "--n-max", "3"])
    assert result.exit_code == 0, result.output
    # Check rows 0-3 are present
    for n in range(4):
        assert str(n) in result.output


def test_cli_simulate_custom_temperature():
    result = runner.invoke(app, ["simulate", "--temperature", "3.0", "--n-max", "3"])
    assert result.exit_code == 0, result.output


# ---------------------------------------------------------------------------
# CLI: ig entropy-price
# ---------------------------------------------------------------------------


def test_cli_entropy_price_default():
    result = runner.invoke(app, ["entropy-price"])
    assert result.exit_code == 0, result.output
    assert "Entropy" in result.output
    assert "P_E" in result.output


def test_cli_entropy_price_with_ceiling():
    result = runner.invoke(app, ["entropy-price", "--n-max", "5", "--ceiling", "1e-23"])
    assert result.exit_code == 0, result.output
    assert "ceiling" in result.output.lower() or "Ceiling" in result.output


def test_cli_entropy_price_n_max():
    result = runner.invoke(app, ["entropy-price", "--n-max", "4"])
    assert result.exit_code == 0, result.output


# ---------------------------------------------------------------------------
# CLI: ig frame-render
# ---------------------------------------------------------------------------


def test_cli_frame_render_default():
    result = runner.invoke(app, ["frame-render"])
    assert result.exit_code == 0, result.output
    assert "Frame" in result.output
    assert "L_n" in result.output


def test_cli_frame_render_n_max():
    result = runner.invoke(app, ["frame-render", "--n-max", "4"])
    assert result.exit_code == 0, result.output
    for n in range(5):
        assert str(n) in result.output


def test_cli_frame_render_custom_lambda():
    result = runner.invoke(app, ["frame-render", "--lambda", "1e-3", "--n-max", "3"])
    assert result.exit_code == 0, result.output


# ---------------------------------------------------------------------------
# Simulation __init__ re-exports
# ---------------------------------------------------------------------------


def test_simulation_package_exports():
    from implosive_genesis.simulation import (
        CosmicMoment,
        CosmicMomentsSimulator,
        EntropyBudget,
        EntropyGovernance,
        GovernanceReport,
    )

    assert CosmicMoment is not None
    assert CosmicMomentsSimulator is not None
    assert EntropyBudget is not None
    assert EntropyGovernance is not None
    assert GovernanceReport is not None
