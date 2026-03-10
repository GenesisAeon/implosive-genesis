"""CMB-Falsifikation – Monte-Carlo-Test gegen den realen CMB-Dipol.

Testet die Hypothese, dass V_RIG ≈ 1352 km/s mit dem beobachteten
CMB-Dipolwert v_CMB = 369.82 ± 0.11 km/s konsistent ist.

Unter der Modellhypothese:

    v_obs = V_RIG · f_proj + ε

wobei f_proj ∈ (0, 1] der Projektionsfaktor (Sichtlinie) und ε ~ N(0, σ²)
das Messrauschen ist. Der CMB-Dipol stellt dabei die projizierte Komponente dar.

Falsifikationsstrategie:
    1. Ziehe N Monte-Carlo-Samples: v_sim = V_RIG · U(0, 1) + N(0, σ²)
    2. Berechne empirischen p-Wert:
       p = P(|v_sim - v_CMB| ≤ |v_obs - v_CMB|)
    3. Falls p < 0.05 → Modell falsifiziert (bei diesem Signifikanzniveau)

Referenzwerte:
    v_RIG  = 1352.0 km/s  (Implosive Genesis Basis)
    v_CMB  = 369.82 km/s  (Planck 2018, CMB-Dipol)
    σ_CMB  = 0.11 km/s    (1σ Messunsicherheit)

Verwendung::

    from implosive_genesis.simulation.cmb_falsification import CMBFalsificationTest
    test = CMBFalsificationTest(n_sim=5000)
    result = test.run()
    print(result)
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

__all__ = ["CMBFalsificationTest", "CMBTestResult", "run_cmb_test"]

# ---------------------------------------------------------------------------
# Referenzwerte (Planck 2018)
# ---------------------------------------------------------------------------

V_RIG_KMS: float = 1352.0
"""Basis-Implosionsgeschwindigkeit in km/s."""

V_CMB_KMS: float = 369.82
"""CMB-Dipolgeschwindigkeit in km/s (Planck 2018, arXiv:1807.06205)."""

SIGMA_CMB_KMS: float = 0.11
"""1σ-Messunsicherheit des CMB-Dipols in km/s."""

SIGNIFICANCE_LEVEL: float = 0.05
"""Standardmäßiges Signifikanzniveau α = 0.05."""


@dataclass
class CMBFalsificationTest:
    """Monte-Carlo-Falsifikationstest gegen den realen CMB-Dipol.

    Testet ob das Implosive-Genesis-Modell (V_RIG ≈ 1352 km/s) mit dem
    beobachteten CMB-Dipol vereinbar ist.

    Unter Annahme zufälliger Projektion: v_obs = V_RIG · U(0,1) + N(0, σ²)
    ergibt sich die Wahrscheinlichkeit, einen Wert nahe v_CMB zu erzielen.

    Attributes:
        n_sim:        Anzahl Monte-Carlo-Simulationen (Standard: 5000).
        v_rig_kms:    V_RIG in km/s (Standard: V_RIG_KMS = 1352 km/s).
        v_cmb_kms:    CMB-Dipolwert in km/s (Standard: V_CMB_KMS).
        sigma_noise:  Gaußsches Rauschen σ in km/s (Standard: SIGMA_CMB_KMS).
        alpha:        Signifikanzniveau (Standard: 0.05).
        seed:         Zufalls-Seed für Reproduzierbarkeit (Standard: None).
    """

    n_sim: int = 5000
    v_rig_kms: float = V_RIG_KMS
    v_cmb_kms: float = V_CMB_KMS
    sigma_noise: float = SIGMA_CMB_KMS
    alpha: float = SIGNIFICANCE_LEVEL
    seed: int | None = None

    def _simulate_samples(self, rng: random.Random) -> list[float]:
        """Zieht Monte-Carlo-Samples unter der Modellhypothese.

        v_sim = V_RIG · U(0, 1) + N(0, σ_noise²)

        Args:
            rng: Initialisierter Random-Generator.

        Returns:
            Liste mit n_sim simulierten Geschwindigkeiten.
        """
        return [
            self.v_rig_kms * rng.random() + rng.gauss(0.0, self.sigma_noise)
            for _ in range(self.n_sim)
        ]

    def run(self) -> CMBTestResult:
        """Führt den CMB-Falsifikationstest durch.

        Berechnet:
            - Monte-Carlo-Verteilung unter Modellhypothese
            - p-Wert: Anteil Samples mit |v_sim - v_CMB| ≤ σ_CMB (1σ-Band)
            - Mittlere Abweichung vom CMB-Wert
            - Standardabweichung der MC-Verteilung

        Returns:
            CMBTestResult mit p-Wert und Falsifikationsentscheidung.
        """
        rng = random.Random(self.seed)
        samples = self._simulate_samples(rng)

        # p-Wert: Anteil Samples die in 3σ-Band um v_CMB fallen
        tolerance = 3.0 * self.sigma_noise + 1.0  # 1 km/s Minimaltoleranz für robuste Schätzung
        n_consistent = sum(1 for v in samples if abs(v - self.v_cmb_kms) <= tolerance)
        p_value = n_consistent / self.n_sim

        # Statistiken der MC-Verteilung
        mean_v = sum(samples) / len(samples)
        variance = sum((v - mean_v) ** 2 for v in samples) / len(samples)
        std_dev = math.sqrt(variance)

        # Abstand zwischen MC-Mittelwert und CMB-Dipol in σ-Einheiten
        deviation_kms = abs(mean_v - self.v_cmb_kms)
        deviation_sigma = deviation_kms / std_dev if std_dev > 0 else float("inf")

        # Erwartungswert unter Modell: V_RIG / 2 (gleichverteilte Projektion)
        expected_v = self.v_rig_kms / 2.0

        is_falsified = p_value < self.alpha

        return CMBTestResult(
            p_value=p_value,
            is_falsified=is_falsified,
            alpha=self.alpha,
            n_sim=self.n_sim,
            v_rig_kms=self.v_rig_kms,
            v_cmb_kms=self.v_cmb_kms,
            expected_v_kms=expected_v,
            mean_sim_kms=mean_v,
            std_sim_kms=std_dev,
            deviation_kms=deviation_kms,
            deviation_sigma=deviation_sigma,
            n_consistent=n_consistent,
            tolerance_kms=tolerance,
        )


@dataclass(frozen=True)
class CMBTestResult:
    """Ergebnis des CMB-Falsifikationstests.

    Attributes:
        p_value:          Empirischer p-Wert (Anteil konsistenter Samples).
        is_falsified:     True wenn p < α (Modell falsifiziert auf Niveau α).
        alpha:            Signifikanzniveau.
        n_sim:            Anzahl Monte-Carlo-Simulationen.
        v_rig_kms:        Verwendetes V_RIG in km/s.
        v_cmb_kms:        CMB-Dipolwert in km/s.
        expected_v_kms:   Erwartungswert unter Modell (V_RIG/2).
        mean_sim_kms:     Mittlere MC-Geschwindigkeit.
        std_sim_kms:      Standardabweichung der MC-Verteilung.
        deviation_kms:    |μ_MC - v_CMB| in km/s.
        deviation_sigma:  Abstand in σ-Einheiten der MC-Verteilung.
        n_consistent:     Anzahl Samples im Toleranzband.
        tolerance_kms:    Verwendete Toleranz in km/s.
    """

    p_value: float
    is_falsified: bool
    alpha: float
    n_sim: int
    v_rig_kms: float
    v_cmb_kms: float
    expected_v_kms: float
    mean_sim_kms: float
    std_sim_kms: float
    deviation_kms: float
    deviation_sigma: float
    n_consistent: int
    tolerance_kms: float

    @property
    def verdict(self) -> str:
        """Kurzurteil des Tests."""
        if self.is_falsified:
            return f"FALSIFIZIERT (p={self.p_value:.4f} < α={self.alpha})"
        return f"NICHT FALSIFIZIERT (p={self.p_value:.4f} ≥ α={self.alpha})"

    def __str__(self) -> str:
        return (
            f"CMBTestResult\n"
            f"  Urteil           = {self.verdict}\n"
            f"  p-Wert           = {self.p_value:.6f}\n"
            f"  Signifikanzniv.  = {self.alpha}\n"
            f"  MC-Simulationen  = {self.n_sim:,}\n"
            f"  V_RIG            = {self.v_rig_kms:.2f} km/s\n"
            f"  v_CMB (Planck)   = {self.v_cmb_kms:.2f} km/s\n"
            f"  E[v] unter Mdl.  = {self.expected_v_kms:.2f} km/s\n"
            f"  μ_MC             = {self.mean_sim_kms:.2f} km/s\n"
            f"  σ_MC             = {self.std_sim_kms:.2f} km/s\n"
            f"  |μ - v_CMB|      = {self.deviation_kms:.2f} km/s ({self.deviation_sigma:.2f}σ)\n"
            f"  n_konsistent     = {self.n_consistent:,} / {self.n_sim:,}\n"
            f"  Toleranz         = {self.tolerance_kms:.2f} km/s"
        )


def run_cmb_test(
    n_sim: int = 5000,
    v_rig_kms: float = V_RIG_KMS,
    v_cmb_kms: float = V_CMB_KMS,
    seed: int | None = None,
) -> CMBTestResult:
    """Convenience-Funktion für den CMB-Falsifikationstest.

    Args:
        n_sim:     Anzahl Monte-Carlo-Simulationen (Standard: 5000).
        v_rig_kms: V_RIG in km/s (Standard: 1352.0).
        v_cmb_kms: CMB-Dipolwert in km/s (Standard: 369.82).
        seed:      Zufalls-Seed (Standard: None).

    Returns:
        CMBTestResult mit vollständigem Testergebnis.
    """
    test = CMBFalsificationTest(
        n_sim=n_sim,
        v_rig_kms=v_rig_kms,
        v_cmb_kms=v_cmb_kms,
        seed=seed,
    )
    return test.run()
