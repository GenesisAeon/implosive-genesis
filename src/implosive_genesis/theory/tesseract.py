"""Tesseract-Zeitscheiben, CREP und entropischer Preis.

Das Tesseract-Modell beschreibt die 4-dimensionale Zeitstruktur des
Implosiven-Genesis-Rahmens. Zeitscheiben T_n skalieren mit dem Goldenen
Schnitt Φ, während CREP (Collapse-Resonance-Entropy-Price) die thermodynamischen
Kosten des Kollapses quantifiziert.

Kern-Formeln:

    T_n = t_0 · Φ^n                       (Zeitscheibe auf Stufe n)

    V_4D(n) = T_n^4 = t_0^4 · Φ^{4n}    (4D-Tesseraktvolumen)

    P_E(n, T) = k_B · T · ln(Φ^n)        (Entropischer Preis)

    CREP = S_total · V_RIG / (Φ · c²)    (Kollaps-Resonanz-Entropie-Preis)

    f_R(n) = V_RIG / (t_0 · Φ^n)         (Resonanzfrequenz auf Stufe n)

Verwendung::

    from implosive_genesis.theory.tesseract import Tesseract, CREP
    ts = Tesseract(t_0=1e-15)
    print(ts.time_slice(3))
    crep = CREP(v_rig_kms=1352.0)
    print(crep.crep_value(s_total=1.0))
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from implosive_genesis.core.physics import PHI
from implosive_genesis.core.vrig import V_RIG_KMS

__all__ = [
    "K_BOLTZMANN",
    "C_LIGHT_MS",
    "T0_DEFAULT",
    "Tesseract",
    "CREP",
]

K_BOLTZMANN: float = 1.380649e-23
"""Boltzmann-Konstante k_B in J/K."""

C_LIGHT_MS: float = 299_792_458.0
"""Lichtgeschwindigkeit c in m/s."""

T0_DEFAULT: float = 1.0
"""Standard-Grundzeitscheibe t_0 (normiert, dimensionslos 1.0)."""


@dataclass
class Tesseract:
    """4-dimensionales Zeitscheiben-Modell (Tesseract).

    Der Tesseract beschreibt die Entfaltung von Zeitscheiben T_n in der
    implosiven Feldtheorie. Mit wachsender Rekursionsstufe n skaliert die
    Zeitscheibe exponentiell mit dem Goldenen Schnitt.

    Attributes:
        t_0: Fundamentale Grundzeitscheibe (Standard: T0_DEFAULT = 1.0).

    Formeln (KaTeX):

    .. math::

        T_n = t_0 \\cdot \\Phi^n

        V_{4D}(n) = T_n^4 = t_0^4 \\cdot \\Phi^{4n}

        f_R(n) = \\frac{V_{RIG}}{t_0 \\cdot \\Phi^n}
    """

    t_0: float = T0_DEFAULT

    def time_slice(self, n: int | float) -> float:
        """Zeitscheibe auf Stufe n: T_n = t_0 · Φ^n.

        Args:
            n: Rekursionsstufe.

        Returns:
            Zeitscheibe T_n in den Einheiten von t_0.
        """
        return self.t_0 * PHI**n

    def volume_4d(self, n: int | float) -> float:
        """4D-Tesseraktvolumen: V_4D(n) = T_n^4 = t_0^4 · Φ^{4n}.

        Das 4D-Volumen wächst mit der vierten Potenz der Zeitscheibe,
        was der hyperbolischen Struktur des Tesserakts entspricht.

        Args:
            n: Rekursionsstufe.

        Returns:
            4D-Volumen V_4D(n) in den Einheiten von t_0^4.
        """
        return self.time_slice(n) ** 4

    def slice_series(self, n_max: int) -> list[float]:
        """Zeitscheiben für n = 0, 1, …, n_max.

        Args:
            n_max: Maximale Rekursionsstufe (inklusiv).

        Returns:
            Liste [T_0, T_1, …, T_{n_max}] der Zeitscheiben.
        """
        return [self.time_slice(n) for n in range(n_max + 1)]

    def volume_series(self, n_max: int) -> list[float]:
        """4D-Volumina für n = 0, 1, …, n_max.

        Args:
            n_max: Maximale Rekursionsstufe (inklusiv).

        Returns:
            Liste [V_4D(0), …, V_4D(n_max)] der Tesseraktvolumina.
        """
        return [self.volume_4d(n) for n in range(n_max + 1)]

    def resonance_frequency(self, n: int | float, v_rig_kms: float = V_RIG_KMS) -> float:
        """Resonanzfrequenz auf Stufe n: f_R(n) = V_RIG_MS / T_n.

        Args:
            n: Rekursionsstufe.
            v_rig_kms: Implosionsgeschwindigkeit in km/s (Standard: V_RIG_KMS).

        Returns:
            Resonanzfrequenz f_R(n) in Hz (wenn t_0 in Sekunden).

        Raises:
            ZeroDivisionError: Wenn t_0 = 0.
        """
        v_rig_ms = v_rig_kms * 1_000.0
        return v_rig_ms / self.time_slice(n)

    def expansion_ratio(self, n: int | float) -> float:
        """Expansionsverhältnis: T_n / T_0 = Φ^n.

        Args:
            n: Rekursionsstufe.

        Returns:
            Dimensionsloses Wachstumsverhältnis Φ^n.
        """
        return PHI**n


@dataclass
class CREP:
    """Collapse-Resonance-Entropy-Price (CREP).

    CREP quantifiziert den thermodynamischen Preis des implosiven Kollapses,
    d.h. die Energie, die beim Übergang zwischen Rekursionsstufen entropisiert
    wird. Der Wert ist Grundlage für die Entropiebilanz des Genesis-Rahmens.

    Attributes:
        v_rig_kms: Implosionsgeschwindigkeit in km/s (Standard: V_RIG_KMS).
        c_ms: Lichtgeschwindigkeit in m/s (Standard: C_LIGHT_MS).

    Formeln (KaTeX):

    .. math::

        CREP = \\frac{S_{total} \\cdot V_{RIG}}{\\Phi \\cdot c^2}

        P_E(n, T) = k_B \\cdot T \\cdot \\ln(\\Phi^n)

        P_E(n, T) = n \\cdot k_B \\cdot T \\cdot \\ln(\\Phi)
    """

    v_rig_kms: float = field(default=V_RIG_KMS)
    c_ms: float = field(default=C_LIGHT_MS)

    def crep_value(self, s_total: float) -> float:
        """CREP-Wert: CREP = S_total · V_RIG_MS / (Φ · c²).

        Der entropische Preis des Gesamt-Kollapses, normiert auf die
        relativistische Energieskala Φ · c².

        Args:
            s_total: Gesamte Entropie S_total (in Joule/Kelvin oder normiert).

        Returns:
            CREP-Wert (gleiche Einheit wie s_total · m/s / (m/s)²  = s_total / (m/s)).
        """
        v_rig_ms = self.v_rig_kms * 1_000.0
        return s_total * v_rig_ms / (PHI * self.c_ms**2)

    def entropy_price(self, n: int | float, temperature: float) -> float:
        """Entropischer Preis auf Stufe n: P_E(n, T) = n · k_B · T · ln(Φ).

        Quantifiziert den thermodynamischen Preis für das Erreichen der
        Rekursionsstufe n bei Temperatur T. Ist equivalent zu k_B · T · ln(Φ^n).

        Args:
            n: Rekursionsstufe.
            temperature: Temperatur T in Kelvin.

        Returns:
            Entropischer Preis P_E in Joule.

        Raises:
            ValueError: Wenn temperature < 0.
        """
        if temperature < 0.0:
            raise ValueError(f"Temperatur muss ≥ 0 K sein, erhalten: {temperature}")
        return n * K_BOLTZMANN * temperature * math.log(PHI)

    def entropy_price_series(self, n_max: int, temperature: float) -> list[float]:
        """Entropische Preise für n = 0, 1, …, n_max bei Temperatur T.

        Args:
            n_max: Maximale Rekursionsstufe (inklusiv).
            temperature: Temperatur T in Kelvin.

        Returns:
            Liste [P_E(0,T), P_E(1,T), …, P_E(n_max,T)].
        """
        return [self.entropy_price(n, temperature) for n in range(n_max + 1)]

    def cumulative_crep(self, s_values: list[float]) -> float:
        """Kumulativer CREP über eine Liste von Entropiewerten.

        CREP_total = Σ CREP(s_i) für alle s_i in s_values.

        Args:
            s_values: Liste von Entropiewerten S_i.

        Returns:
            Summierter CREP-Gesamtwert.
        """
        return sum(self.crep_value(s) for s in s_values)

    def crep_ratio(self, s_total: float) -> float:
        """CREP-Verhältnis normiert auf V_RIG²/c²: CREP · c / V_RIG_MS.

        Dimensionsloser Vergleichswert, der CREP auf die Skala V_RIG/c
        normiert.

        Args:
            s_total: Gesamtentropie S_total.

        Returns:
            Normierter CREP-Wert (dimensionslos wenn s_total dimensionslos).
        """
        v_rig_ms = self.v_rig_kms * 1_000.0
        return self.crep_value(s_total) * self.c_ms / v_rig_ms
