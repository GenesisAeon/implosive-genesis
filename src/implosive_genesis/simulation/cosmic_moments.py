"""Kosmische Momente – Phi-skalierte Zeitevolution der Implosiven Genesis.

Dieses Modul simuliert kosmische Schlüsselmomente entlang der rekursiven
Zeitachse des Tesseract-Modells. Jeder Moment kodiert Zeitscheibe,
Resonanzfrequenz, CREP-Beitrag und Phi-Skalierungsparameter.

Kern-Formeln:

    T_n = t_0 · Φ^n                       (Zeitscheibe auf Stufe n)

    f_R(n) = V_RIG_MS / T_n               (Resonanzfrequenz)

    P_E(n, T) = n · k_B · T · ln(Φ)      (Entropischer Preis)

    I_n = E_OIPK · Φ^{n/3}               (Impulsenergie)

    CREP = S_total · V_RIG / (Φ · c²)    (Kollaps-Resonanz-Entropie-Preis)

Verwendung::

    from implosive_genesis.simulation.cosmic_moments import CosmicMomentsSimulator
    sim = CosmicMomentsSimulator(n_max=7, temperature=2.725)
    moments = sim.run()
    print(moments[3])
"""

from __future__ import annotations

from dataclasses import dataclass

from implosive_genesis.core.physics import PHI
from implosive_genesis.core.vrig import V_RIG_KMS
from implosive_genesis.theory.frameprinciple import FramePrinciple, OIPKernel
from implosive_genesis.theory.tesseract import CREP, Tesseract

__all__ = ["CosmicMoment", "CosmicMomentsSimulator"]


@dataclass(frozen=True)
class CosmicMoment:
    """Ein Augenblick in der kosmischen Zeitentfaltung.

    Attributes:
        n: Rekursionsstufe.
        time_slice: Zeitscheibe T_n = t_0 · Φ^n.
        resonance_freq: Resonanzfrequenz f_R(n) = V_RIG_MS / T_n.
        entropy_price_j: Entropischer Preis P_E(n, T) in Joule.
        impulse_energy_j: Impulsenergie I_n = E_OIPK · Φ^{n/3} in Joule.
        crep_value: CREP-Beitrag bei S_total = 1.
        expansion_ratio: Expansionsverhältnis Φ^n.
        temperature_k: Temperatur T in Kelvin.
    """

    n: int
    time_slice: float
    resonance_freq: float
    entropy_price_j: float
    impulse_energy_j: float
    crep_value: float
    expansion_ratio: float
    temperature_k: float

    def __str__(self) -> str:
        return (
            f"CosmicMoment(n={self.n})\n"
            f"  T_n            = {self.time_slice:.6e}\n"
            f"  f_R(n)         = {self.resonance_freq:.6e} Hz\n"
            f"  P_E(n,T)       = {self.entropy_price_j:.6e} J"
            f"  (T={self.temperature_k} K)\n"
            f"  I_n            = {self.impulse_energy_j:.6e} J\n"
            f"  CREP(S=1)      = {self.crep_value:.6e}\n"
            f"  Φ^n            = {self.expansion_ratio:.6f}\n"
        )


@dataclass
class CosmicMomentsSimulator:
    """Simulator für kosmische Momente entlang der Phi-Zeitachse.

    Berechnet für jede Rekursionsstufe n von 0 bis n_max einen vollständigen
    kosmischen Moment mit allen relevanten Observablen.

    Attributes:
        n_max: Maximale Rekursionsstufe (inklusiv, Standard: 7).
        temperature: Temperatur T in Kelvin (Standard: 2.725 K, CMB).
        t_0: Grundzeitscheibe (Standard: 1.0).
        v_rig_kms: V_RIG in km/s (Standard: V_RIG_KMS = 1352 km/s).
    """

    n_max: int = 7
    temperature: float = 2.725
    t_0: float = 1.0
    v_rig_kms: float = V_RIG_KMS

    def run(self) -> list[CosmicMoment]:
        """Führt die Simulation aus und gibt alle kosmischen Momente zurück.

        Returns:
            Liste von CosmicMoment-Objekten für n = 0, 1, …, n_max.
        """
        tesseract = Tesseract(t_0=self.t_0)
        crep_model = CREP(v_rig_kms=self.v_rig_kms)
        kernel = OIPKernel()
        frame = FramePrinciple(kernel=kernel)
        crep_val = crep_model.crep_value(1.0)

        moments = []
        for n in range(self.n_max + 1):
            ts = tesseract.time_slice(n)
            freq = tesseract.resonance_frequency(n, v_rig_kms=self.v_rig_kms)
            price = crep_model.entropy_price(n, self.temperature)
            energy = frame.impulse_energy(n)
            ratio = PHI**n
            moments.append(
                CosmicMoment(
                    n=n,
                    time_slice=ts,
                    resonance_freq=freq,
                    entropy_price_j=price,
                    impulse_energy_j=energy,
                    crep_value=crep_val,
                    expansion_ratio=ratio,
                    temperature_k=self.temperature,
                )
            )
        return moments

    def peak_moment(self) -> CosmicMoment:
        """Gibt den kosmischen Moment mit maximaler Resonanzfrequenz zurück.

        Da f_R(n) = V_RIG / T_n mit T_n = t_0 · Φ^n ist die Resonanzfrequenz
        bei n=0 maximal (kleinste Zeitscheibe).

        Returns:
            CosmicMoment mit maximaler Resonanzfrequenz (n=0).
        """
        moments = self.run()
        return max(moments, key=lambda m: m.resonance_freq)

    def total_entropy_price(self) -> float:
        """Gesamter entropischer Preis über alle Stufen.

        Returns:
            Summe aller P_E(n, T) für n = 0, …, n_max in Joule.
        """
        moments = self.run()
        return sum(m.entropy_price_j for m in moments)

    def entropy_weighted_crep(self) -> float:
        """Entropiegewichteter CREP-Gesamtbeitrag.

        CREP_weighted = Σ CREP(P_E(n,T)) für n = 0, …, n_max

        Returns:
            Summe der CREP-Werte gewichtet mit dem entropischen Preis.
        """
        crep_model = CREP(v_rig_kms=self.v_rig_kms)
        moments = self.run()
        return sum(crep_model.crep_value(m.entropy_price_j) for m in moments)
