"""Frameprinciple – OIPK (Orthogonal Impulse Photon Kernel) Definition.

Das Frame-Prinzip beschreibt, wie Bezugsrahmen (Frames) aus orthogonalen
Impuls-Photonen-Kernen (OIPK) emergieren. Jeder stabile Frame besitzt eine
charakteristische OIPK-Wellenlänge, aus der Frequenz, Energie und
Stabilitätskriterium abgeleitet werden.

Kern-Formeln:

    ω_F = 2π · c / λ_OIPK

    E_OIPK = ℏ · ω_F · α_Φ

    S_F = Φ² / α_Φ

    cos(θ_⊥) = −1 / Φ   (Orthogonalitätsbedingung)

    L_n = λ_OIPK · Φ^{n/3}   (Kohärenzlänge auf Rekursionsstufe n)

Verwendung::

    from implosive_genesis.theory.frameprinciple import OIPKernel, FramePrinciple
    kernel = OIPKernel(lambda_m=1e-9)
    fp = FramePrinciple(kernel=kernel)
    print(fp.coherence_length(3))
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from implosive_genesis.core.physics import PHI
from implosive_genesis.core.vrig import cosmic_alpha_phi

__all__ = [
    "HBAR",
    "C_LIGHT",
    "LAMBDA_OIPK_DEFAULT",
    "THETA_ORTHOGONAL",
    "OIPKernel",
    "FramePrinciple",
]

HBAR: float = 1.054571817e-34
"""Reduziertes Plancksches Wirkungsquantum ℏ in J·s."""

C_LIGHT: float = 299_792_458.0
"""Lichtgeschwindigkeit c in m/s."""

LAMBDA_OIPK_DEFAULT: float = C_LIGHT / (1352.0 * 1_000.0)
"""Standard-OIPK-Wellenlänge λ_OIPK = c / V_RIG [m], abgeleitet von V_RIG ≈ 1352 km/s."""

THETA_ORTHOGONAL: float = math.acos(-1.0 / PHI)
"""Orthogonalitätswinkel θ_⊥ = arccos(−1/Φ) ≈ 128.17° (in Radiant)."""


@dataclass
class OIPKernel:
    """Orthogonaler Impuls-Photonen-Kern (OIPK).

    Definiert die minimale photonische Struktur, die einen stabilen Frame
    in der Implosiven-Genesis-Theorie erzeugt. Die Kernparameter leiten
    Frequenz, Energie und Stabilitätskriterium des Frames ab.

    Attributes:
        lambda_m: OIPK-Wellenlänge λ_OIPK in Metern (Standard: LAMBDA_OIPK_DEFAULT).
        alpha_phi: Phi-skalierte Feinstrukturkonstante α_Φ (Standard: cosmic_alpha_phi()).

    Formeln (KaTeX):

    .. math::

        \\omega_F = \\frac{2\\pi c}{\\lambda_{OIPK}}

        E_{OIPK} = \\hbar \\cdot \\omega_F \\cdot \\alpha_{\\Phi}

        S_F = \\frac{\\Phi^2}{\\alpha_{\\Phi}}
    """

    lambda_m: float = field(default_factory=lambda: LAMBDA_OIPK_DEFAULT)
    alpha_phi: float = field(default_factory=cosmic_alpha_phi)

    def angular_frequency(self) -> float:
        """Winkelfrequenz des Frames: ω_F = 2π · c / λ_OIPK.

        Returns:
            Winkelfrequenz ω_F in rad/s.
        """
        return 2.0 * math.pi * C_LIGHT / self.lambda_m

    def energy(self) -> float:
        """OIPK-Energie: E_OIPK = ℏ · ω_F · α_Φ.

        Returns:
            Photonische Kernenergie E_OIPK in Joule.
        """
        return HBAR * self.angular_frequency() * self.alpha_phi

    def frame_stability(self) -> float:
        """Frame-Stabilitätskriterium: S_F = Φ² / α_Φ.

        Ein höherer Wert indiziert einen stabilereren Frame gegenüber
        Feldfluktuationen. S_F ist dimensionslos.

        Returns:
            Stabilitätskennzahl S_F (dimensionslos).
        """
        return PHI**2 / self.alpha_phi

    def orthogonality_angle_deg(self) -> float:
        """Orthogonalitätswinkel θ_⊥ in Grad: arccos(−1/Φ).

        Kernvektoren des OIPK spannen ein Gitter auf, dessen
        charakteristischer Winkel θ_⊥ ≈ 128.17° beträgt.

        Returns:
            θ_⊥ in Grad.
        """
        return math.degrees(THETA_ORTHOGONAL)


@dataclass
class FramePrinciple:
    """Frame-Prinzip: Rekursive Kohärenz- und Impulsenergieentfaltung.

    Leitet aus einem OIPKernel die rekursiven Eigenschaften eines Frames
    auf Stufe n ab. Die Phi-Skalierung sorgt für geometrisch optimale
    Raum-Zeit-Kohärenz.

    Attributes:
        kernel: Der zugrundeliegende OIPKernel.

    Formeln (KaTeX):

    .. math::

        L_n = \\lambda_{OIPK} \\cdot \\Phi^{n/3}

        I_n = E_{OIPK} \\cdot \\Phi^{n/3}

        \\cos(\\theta_\\perp) = -\\frac{1}{\\Phi}
    """

    kernel: OIPKernel = field(default_factory=OIPKernel)

    def coherence_length(self, n: int | float) -> float:
        """Kohärenzlänge auf Rekursionsstufe n: L_n = λ_OIPK · Φ^{n/3}.

        Args:
            n: Rekursionsstufe.

        Returns:
            Kohärenzlänge L_n in Metern.
        """
        return self.kernel.lambda_m * PHI ** (n / 3.0)

    def impulse_energy(self, n: int | float) -> float:
        """Impulsenergie auf Rekursionsstufe n: I_n = E_OIPK · Φ^{n/3}.

        Args:
            n: Rekursionsstufe.

        Returns:
            Impulsenergie I_n in Joule.
        """
        return self.kernel.energy() * PHI ** (n / 3.0)

    def coherence_series(self, n_max: int) -> list[float]:
        """Kohärenzlängen für n = 0, 1, …, n_max.

        Args:
            n_max: Maximale Rekursionsstufe (inklusiv).

        Returns:
            Liste mit n_max+1 Kohärenzlängen [L_0, L_1, …, L_{n_max}].
        """
        return [self.coherence_length(n) for n in range(n_max + 1)]

    def impulse_series(self, n_max: int) -> list[float]:
        """Impulsenergien für n = 0, 1, …, n_max.

        Args:
            n_max: Maximale Rekursionsstufe (inklusiv).

        Returns:
            Liste mit n_max+1 Impulsenergiewerten [I_0, I_1, …, I_{n_max}].
        """
        return [self.impulse_energy(n) for n in range(n_max + 1)]

    def stability_at(self, n: int | float) -> float:
        """Frame-Stabilität auf Rekursionsstufe n: S_F · Φ^{n/3}.

        Höhere Rekursionsstufen erhöhen die effektive Stabilität durch
        geometrische Akkumulation.

        Args:
            n: Rekursionsstufe.

        Returns:
            Effektive Stabilitätskennzahl auf Stufe n.
        """
        return self.kernel.frame_stability() * PHI ** (n / 3.0)
