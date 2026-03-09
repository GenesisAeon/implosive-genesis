"""Phi-skalierter Feldtheorie-Kern – geometrischer Verschnitt-Minimierung.

Formel: β_n ≈ β_0 · Φ^{n/3}

Die goldene Verhältniszahl Φ minimiert den geometrischen Verschnitt in
rekursiven Implosionsgittern (Phi-Lattice-Packing). Bei n-ter Rekursionsstufe
skaliert der Kopplungsparameter β_n gemäß der obigen Formel.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

__all__ = ["PHI", "PhiScaling"]

PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
"""Goldener Schnitt Φ = (1 + √5) / 2 ≈ 1.6180339887."""


@dataclass
class PhiScaling:
    """Phi-skalierter Kopplungsparameter mit minimiertem geometrischen Verschnitt.

    Attributes:
        beta_0: Basis-Kopplungskonstante bei n=0 (Standard: 1.0).
    """

    beta_0: float = 1.0

    def beta_n(self, n: int | float) -> float:
        """Berechne β_n ≈ β_0 · Φ^{n/3}.

        Args:
            n: Rekursionsstufe (kann auch nicht-ganzzahlig sein).

        Returns:
            Skalierter Kopplungsparameter β_n.
        """
        return self.beta_0 * PHI ** (n / 3.0)

    def geometric_waste(self, n: int | float) -> float:
        """Geringster geometrischer Verschnitt bei Rekursionsstufe n.

        W(n) = 1 − 1/Φ^{n/3} repräsentiert die geometrische Ineffizienz
        (Verschnitt) auf Stufe n. Gegen ∞ strebt W(n) → 1; bei n=0 ist W=0.

        Args:
            n: Rekursionsstufe.

        Returns:
            Verschnittanteil W(n) ∈ [0, 1).
        """
        return 1.0 - 1.0 / PHI ** (n / 3.0)

    def beta_series(self, n_max: int) -> list[float]:
        """Berechne β_n für n = 0, 1, …, n_max.

        Args:
            n_max: Maximale Rekursionsstufe (inklusiv).

        Returns:
            Liste mit n_max+1 Werten [β_0, β_1, …, β_{n_max}].
        """
        return [self.beta_n(n) for n in range(n_max + 1)]

    def waste_series(self, n_max: int) -> list[float]:
        """Berechne W(n) für n = 0, 1, …, n_max.

        Args:
            n_max: Maximale Rekursionsstufe (inklusiv).

        Returns:
            Liste mit n_max+1 Verschnittwerten.
        """
        return [self.geometric_waste(n) for n in range(n_max + 1)]

    def min_waste_index(self, n_max: int) -> int:
        """Gibt das n mit geringstem Verschnitt zurück (immer 0).

        Bei n=0 ist W=0 – der absolute Minimalwert. Diese Methode ist für
        symmetrische Auswertungszwecke vorgesehen.

        Args:
            n_max: Suchbereich [0, n_max].

        Returns:
            Index n mit minimalem W(n) innerhalb [0, n_max].
        """
        wastes = self.waste_series(n_max)
        return int(min(range(len(wastes)), key=lambda i: wastes[i]))
