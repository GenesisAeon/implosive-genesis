"""Entropy Governance – Entropie-Steuerung im Tesseract-Physik-Rahmen.

Dieses Modul implementiert die Entropie-Governance-Schicht des
Implosiven-Genesis-Rahmens. Basierend auf den CREP-Formeln und der
Tesseract-Physik steuert es die Entropiezuteilung zwischen Rekursionsstufen
und erkennt Entropie-Überschüsse.

Kern-Formeln:

    P_E(n, T) = n · k_B · T · ln(Φ)           (Entropischer Preis auf Stufe n)

    Budget(n) = P_E(n,T) / Σ P_E(i,T)         (Relative Entropieallokation)

    CREP = S_total · V_RIG / (Φ · c²)         (Kollaps-Resonanz-Entropie-Preis)

    Overflow(n) = max(0, P_E(n,T) - ceiling_j) (Entropie-Überschuss)

Verwendung::

    from implosive_genesis.simulation.entropy_governance import EntropyGovernance
    gov = EntropyGovernance(n_max=5, temperature=2.725)
    report = gov.governance_report()
    print(report)
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from implosive_genesis.core.physics import PHI
from implosive_genesis.core.vrig import V_RIG_KMS
from implosive_genesis.theory.tesseract import CREP, K_BOLTZMANN

__all__ = ["EntropyBudget", "EntropyGovernance", "GovernanceReport"]

_LOG_PHI: float = math.log(PHI)


@dataclass(frozen=True)
class EntropyBudget:
    """Entropie-Budget für eine einzelne Rekursionsstufe.

    Attributes:
        n: Rekursionsstufe.
        entropy_price_j: Entropischer Preis P_E(n, T) in Joule.
        budget_fraction: Relativer Anteil am Gesamtbudget [0, 1].
        crep_contribution: CREP-Beitrag dieser Stufe.
        overflow_j: Entropie-Überschuss über die Decke (0 wenn kein Ceiling).
        temperature_k: Temperatur T in Kelvin.
    """

    n: int
    entropy_price_j: float
    budget_fraction: float
    crep_contribution: float
    overflow_j: float
    temperature_k: float

    @property
    def is_overflow(self) -> bool:
        """True wenn diese Stufe die Entropiedecke überschreitet."""
        return self.overflow_j > 0.0


@dataclass(frozen=True)
class GovernanceReport:
    """Vollständiger Governance-Bericht über alle Rekursionsstufen.

    Attributes:
        budgets: Liste der Entropie-Budgets pro Stufe.
        total_entropy_j: Gesamtentropischer Preis Σ P_E(n, T).
        total_crep: Kumulativer CREP-Wert.
        ceiling_j: Entropiedecke (None wenn keine definiert).
        n_overflow: Anzahl Stufen mit Entropie-Überschuss.
        phi: Goldener Schnitt Φ.
        v_rig_kms: V_RIG in km/s.
    """

    budgets: list[EntropyBudget]
    total_entropy_j: float
    total_crep: float
    ceiling_j: float | None
    n_overflow: int
    phi: float
    v_rig_kms: float

    def __str__(self) -> str:
        ceiling_str = f"{self.ceiling_j:.3e} J" if self.ceiling_j is not None else "—"
        return (
            f"GovernanceReport (n_max={len(self.budgets) - 1})\n"
            f"  Total Entropy  = {self.total_entropy_j:.6e} J\n"
            f"  Total CREP     = {self.total_crep:.6e}\n"
            f"  Ceiling        = {ceiling_str}\n"
            f"  Overflow count = {self.n_overflow}\n"
            f"  Φ              = {self.phi:.6f}\n"
            f"  V_RIG          = {self.v_rig_kms:.2f} km/s"
        )


@dataclass
class EntropyGovernance:
    """Entropie-Governance für das Tesseract-Physik-Modell.

    Verwaltet die Entropiezuteilung zwischen Rekursionsstufen und erkennt
    Entropie-Überschüsse (Overflow), die auf Instabilitäten hinweisen.

    Attributes:
        n_max: Maximale Rekursionsstufe (Standard: 7).
        temperature: Temperatur T in Kelvin (Standard: 2.725 K, CMB).
        v_rig_kms: V_RIG in km/s (Standard: V_RIG_KMS).
        ceiling_j: Optionale Entropiedecke in Joule. Überschüsse werden
            im GovernanceReport ausgewiesen.
    """

    n_max: int = 7
    temperature: float = 2.725
    v_rig_kms: float = V_RIG_KMS
    ceiling_j: float | None = None

    def entropy_price(self, n: int) -> float:
        """Entropischer Preis auf Stufe n: P_E(n, T) = n · k_B · T · ln(Φ).

        Args:
            n: Rekursionsstufe.

        Returns:
            P_E(n, T) in Joule.
        """
        return n * K_BOLTZMANN * self.temperature * _LOG_PHI

    def entropy_prices(self) -> list[float]:
        """Entropische Preise für n = 0, 1, …, n_max.

        Returns:
            Liste [P_E(0,T), …, P_E(n_max,T)].
        """
        return [self.entropy_price(n) for n in range(self.n_max + 1)]

    def total_entropy(self) -> float:
        """Gesamter entropischer Preis Σ P_E(n, T) für n = 0, …, n_max.

        Returns:
            Summe aller entropischen Preise in Joule.
        """
        return sum(self.entropy_prices())

    def budget_fractions(self) -> list[float]:
        """Relativer Entropie-Anteil jeder Stufe am Gesamtbudget.

        Budget(n) = P_E(n,T) / total_entropy.
        Bei total_entropy = 0 (n_max = 0) gibt Budget(0) = 0.0 zurück.

        Returns:
            Liste [Budget(0), …, Budget(n_max)] mit Σ = 1.0.
        """
        prices = self.entropy_prices()
        total = sum(prices)
        if total == 0.0:
            return [0.0] * len(prices)
        return [p / total for p in prices]

    def overflow(self, n: int) -> float:
        """Entropie-Überschuss auf Stufe n über die Decke.

        Returns 0.0 wenn keine Decke definiert oder kein Überschuss.

        Args:
            n: Rekursionsstufe.

        Returns:
            max(0, P_E(n,T) - ceiling_j) in Joule.
        """
        if self.ceiling_j is None:
            return 0.0
        return max(0.0, self.entropy_price(n) - self.ceiling_j)

    def crep_contributions(self) -> list[float]:
        """CREP-Beitrag jeder Rekursionsstufe: CREP(P_E(n,T)).

        Returns:
            Liste [CREP(P_E(0,T)), …, CREP(P_E(n_max,T))].
        """
        crep_model = CREP(v_rig_kms=self.v_rig_kms)
        return [crep_model.crep_value(p) for p in self.entropy_prices()]

    def governance_report(self) -> GovernanceReport:
        """Erstellt einen vollständigen Governance-Bericht.

        Returns:
            GovernanceReport mit Budgets, Gesamt-Entropie und CREP.
        """
        prices = self.entropy_prices()
        fractions = self.budget_fractions()
        crep_contrib = self.crep_contributions()
        total_e = sum(prices)
        total_crep = sum(crep_contrib)

        budgets = [
            EntropyBudget(
                n=n,
                entropy_price_j=prices[n],
                budget_fraction=fractions[n],
                crep_contribution=crep_contrib[n],
                overflow_j=self.overflow(n),
                temperature_k=self.temperature,
            )
            for n in range(self.n_max + 1)
        ]

        n_overflow = sum(1 for b in budgets if b.is_overflow)
        return GovernanceReport(
            budgets=budgets,
            total_entropy_j=total_e,
            total_crep=total_crep,
            ceiling_j=self.ceiling_j,
            n_overflow=n_overflow,
            phi=PHI,
            v_rig_kms=self.v_rig_kms,
        )

    def stable_levels(self) -> list[int]:
        """Rekursionsstufen ohne Entropie-Überschuss.

        Returns:
            Liste der Stufen n mit overflow(n) == 0.
        """
        return [n for n in range(self.n_max + 1) if self.overflow(n) == 0.0]

    def critical_level(self) -> int | None:
        """Erste Stufe mit Entropie-Überschuss.

        Returns:
            Kleinste Stufe n mit overflow(n) > 0, oder None wenn keine.
        """
        for n in range(self.n_max + 1):
            if self.overflow(n) > 0.0:
                return n
        return None
