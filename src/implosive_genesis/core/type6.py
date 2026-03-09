"""UTAC Type-6 Implosive Singularität – invertiertes Sigmoid + Kubikwurzel-Sprung.

Das Type-6-Modell beschreibt den kritischen Übergang in der implosiven
Feldtheorie: Ein invertiertes Sigmoid (weicher Zerfall) überlagert sich mit
einem Kubikwurzel-Sprung (harter Phasenübergang), sodass die kombinierte
Response nicht-linear und symmetriebrechend ist.

Verwendung:
    from implosive_genesis.core.type6 import Type6Implosive
    model = Type6Implosive()
    points = model.simulate((-3.0, 3.0), steps=50)
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .physics import PHI

__all__ = [
    "inverted_sigmoid",
    "cubic_root_jump",
    "Type6Implosive",
]


def inverted_sigmoid(x: float, steepness: float = 1.0) -> float:
    """Invertiertes Sigmoid: f(x) = 1 / (1 + exp(k·x)).

    Für k > 0 fällt die Funktion monoton von 1 (x → −∞) nach 0 (x → +∞).
    Die Steilheit k skaliert die Übergangsbreite.

    Args:
        x: Eingabewert.
        steepness: Steilheitsfaktor k (Standard: 1.0).

    Returns:
        Wert im Intervall (0, 1).
    """
    # Clip to avoid overflow for extreme x values
    exp_arg = steepness * x
    if exp_arg > 709.0:
        return 0.0
    if exp_arg < -709.0:
        return 1.0
    return 1.0 / (1.0 + math.exp(exp_arg))


def cubic_root_jump(x: float, threshold: float = 0.0, amplitude: float = 1.0) -> float:
    """Kubikwurzel-Sprung: sgn(δ) · |δ|^{1/3} · amplitude, mit δ = x − threshold.

    Erzeugt einen kontinuierlichen, aber nicht-differenzierbaren Übergang am
    threshold-Punkt. Der Vorzeichenwechsel um threshold herum erzeugt den
    charakteristischen „Sprung"-Charakter des Type-6-Übergangs.

    Args:
        x: Eingabewert.
        threshold: Sprungpunkt (Standard: 0.0).
        amplitude: Skalierungsfaktor der Amplitude (Standard: 1.0).

    Returns:
        Kubikwurzel-Sprung-Wert (kann negativ sein).
    """
    delta = x - threshold
    if delta == 0.0:
        return 0.0
    return math.copysign(abs(delta) ** (1.0 / 3.0), delta) * amplitude


@dataclass
class Type6Implosive:
    """UTAC Type-6 Implosive Feldantwort.

    Kombiniert invertiertes Sigmoid und Kubikwurzel-Sprung zur Modellierung
    des kritischen Phasenübergangs in implosiven Feldtheorien.

    Attributes:
        steepness: Steilheit des invertierten Sigmoids (Standard: Φ ≈ 1.618).
        threshold: Sprungpunkt des Kubikwurzel-Sprungs (Standard: 0.0).
        amplitude: Amplitude des Kubikwurzel-Sprungs (Standard: 1.0).
    """

    steepness: float = PHI
    threshold: float = 0.0
    amplitude: float = 1.0

    def response(self, x: float) -> float:
        """Kombinierte Type-6-Antwort an Punkt x.

        R(x) = invertiertes_Sigmoid(x; k) + Kubikwurzel_Sprung(x; t, A)

        Args:
            x: Eingabewert.

        Returns:
            Kombinierter Feldwert R(x).
        """
        return inverted_sigmoid(x, self.steepness) + cubic_root_jump(
            x, self.threshold, self.amplitude
        )

    def simulate(
        self, x_range: tuple[float, float], steps: int = 100
    ) -> list[tuple[float, float]]:
        """Simuliere Type-6-Antwort über ein x-Intervall.

        Args:
            x_range: (x_start, x_end) Simulationsintervall.
            steps: Anzahl der Stützpunkte (Standard: 100).

        Returns:
            Liste von (x, R(x))-Tupeln, gleichmäßig über x_range verteilt.

        Raises:
            ValueError: Wenn steps < 1.
        """
        if steps < 1:
            raise ValueError(f"steps muss ≥ 1 sein, erhalten: {steps}")

        x_start, x_end = x_range
        if steps == 1:
            return [(x_start, self.response(x_start))]

        step_size = (x_end - x_start) / (steps - 1)
        return [(x_start + i * step_size, self.response(x_start + i * step_size)) for i in range(steps)]

    def critical_point(self) -> float:
        """Gib den kritischen Punkt (threshold) zurück, an dem der Sprung auftritt.

        Returns:
            threshold-Wert des Modells.
        """
        return self.threshold

    def sigmoid_only(self, x: float) -> float:
        """Reine Sigmoid-Komponente ohne Kubikwurzel-Sprung.

        Args:
            x: Eingabewert.

        Returns:
            Invertiertes Sigmoid f(x; k).
        """
        return inverted_sigmoid(x, self.steepness)

    def jump_only(self, x: float) -> float:
        """Reine Kubikwurzel-Sprung-Komponente ohne Sigmoid.

        Args:
            x: Eingabewert.

        Returns:
            Kubikwurzel-Sprung bei threshold mit Amplitude.
        """
        return cubic_root_jump(x, self.threshold, self.amplitude)
