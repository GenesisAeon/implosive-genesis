"""OIPK – Orthogonal Impulse Photon Kernel (eigenständiges Modul).

Definiert den **Orthogonalen Impuls-Photonen-Kern** als abgeschlossenes System mit
der τ ⊥ t Bedingung (orthogonale Prozesszeit τ gegenüber Raumzeit-Zeit t) sowie
der vollständigen CREP-Berechnung.

Kern-Gleichungen (geschlossen):

    τ_OIPK = λ_OIPK / c                         (OIPK-Prozesszeit)

    τ ⊥ t  ⟺  ⟨τ, t⟩ = 0                      (Orthogonalitätsbedingung)

    ω_OIPK = 2π / τ_OIPK = 2π·c / λ_OIPK       (Kreisfrequenz)

    E_OIPK = ℏ·ω_OIPK·α_Φ                      (Kernenergie)

    S_F    = Φ² / α_Φ                           (Frame-Stabilität)

    CREP   = E_OIPK · S_F · Φ / c              (Kollaps-Resonanz-Entropie-Preis)

    D_n    = ⌈log_Φ(I_n / E_OIPK)⌉              (Emergente Dimension auf Stufe n)

„A dimension emerges when information would otherwise collapse."

Verwendung::

    from implosive_genesis.oipk.kernel import OIPKKernel, compute_crep_oipk

    kernel = OIPKKernel()
    result = kernel.compute()
    print(result)

    crep = compute_crep_oipk(kernel)
    print(f"CREP = {crep:.4e} kg·m/s")
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

__all__ = [
    "HBAR",
    "C_LIGHT",
    "PHI",
    "ALPHA_EM",
    "TAU_PERP_FACTOR",
    "OIPKKernel",
    "OIPKResult",
    "OIPKDimension",
    "compute_crep_oipk",
]

# ---------------------------------------------------------------------------
# Physikalische Konstanten
# ---------------------------------------------------------------------------

HBAR: float = 1.054571817e-34
"""Reduziertes Plancksches Wirkungsquantum ℏ (J·s)."""

C_LIGHT: float = 299_792_458.0
"""Lichtgeschwindigkeit c (m/s)."""

PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
"""Goldener Schnitt Φ ≈ 1.6180339887."""

ALPHA_EM: float = 7.2973525693e-3
"""Elektromagnetische Feinstrukturkonstante α ≈ 1/137."""

TAU_PERP_FACTOR: float = 1.0 / PHI
"""Skalierungsfaktor für die orthogonale Prozesszeit τ: τ_⊥ = τ_OIPK / Φ."""

# Standard-Implosionsgeschwindigkeit
_V_RIG_MS: float = 1_352_000.0  # 1352 km/s in m/s
_LAMBDA_DEFAULT: float = C_LIGHT / _V_RIG_MS


def _default_alpha_phi() -> float:
    """Phi-skalierte Feinstrukturkonstante α_Φ = α · Φ."""
    return ALPHA_EM * PHI


# ---------------------------------------------------------------------------
# Datenklassen
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OIPKResult:
    """Vollständiges Ergebnis einer OIPK-Berechnung.

    Attributes:
        lambda_m:        OIPK-Wellenlänge λ_OIPK [m]
        tau_oipk:        OIPK-Prozesszeit τ = λ/c [s]
        tau_perp:        Orthogonale Prozesszeit τ_⊥ = τ/Φ [s]
        omega:           Kreisfrequenz ω = 2π/τ [rad/s]
        energy_j:        Kernenergie E_OIPK = ℏ·ω·α_Φ [J]
        frame_stability: Frame-Stabilitätskriterium S_F = Φ²/α_Φ
        crep:            CREP-Wert E_OIPK·S_F·Φ/c [kg·m/s]
        alpha_phi:       Phi-skalierte Feinstrukturkonstante α_Φ
        is_orthogonal:   τ ⊥ t Bedingung (immer True per Konstruktion)
    """

    lambda_m: float
    tau_oipk: float
    tau_perp: float
    omega: float
    energy_j: float
    frame_stability: float
    crep: float
    alpha_phi: float
    is_orthogonal: bool = True

    def __str__(self) -> str:
        return (
            f"OIPKResult(\n"
            f"  λ_OIPK     = {self.lambda_m:.4e} m\n"
            f"  τ_OIPK     = {self.tau_oipk:.4e} s\n"
            f"  τ_⊥        = {self.tau_perp:.4e} s  (τ ⊥ t: {self.is_orthogonal})\n"
            f"  ω          = {self.omega:.4e} rad/s\n"
            f"  E_OIPK     = {self.energy_j:.4e} J\n"
            f"  S_F        = {self.frame_stability:.4f}\n"
            f"  CREP       = {self.crep:.4e} kg·m/s\n"
            f"  α_Φ        = {self.alpha_phi:.6f}\n"
            f")"
        )


@dataclass(frozen=True)
class OIPKDimension:
    """Emergente Dimension auf Rekursionsstufe n.

    „A dimension emerges when information would otherwise collapse."
    Wenn die akkumulierte Impulsenergie I_n die Kernenergie E_OIPK
    um einen Phi-Faktor übersteigt, emergiert eine neue Dimension.

    Attributes:
        n:           Rekursionsstufe
        impulse_j:   Impulsenergie I_n = E_OIPK · Φ^(n/3) [J]
        dimension:   Emergierte Dimension D_n = ⌈log_Φ(I_n/E_OIPK)⌉
        collapsed:   True wenn I_n < E_OIPK (Kollaps-Regime)
    """

    n: int
    impulse_j: float
    dimension: int
    collapsed: bool


# ---------------------------------------------------------------------------
# Hauptklasse
# ---------------------------------------------------------------------------


@dataclass
class OIPKKernel:
    """Orthogonaler Impuls-Photonen-Kern – vollständige geschlossene Formulierung.

    Implementiert die τ ⊥ t Bedingung: Die Prozesszeit τ des OIPK ist
    orthogonal zur Raumzeit-Zeit t, d.h. ⟨τ, t⟩ = 0. Diese Orthogonalität
    ist geometrisch durch die Phi-Skalierung garantiert.

    Attributes:
        lambda_m:   OIPK-Wellenlänge [m]. Standard: c / V_RIG.
        alpha_phi:  Phi-skalierte Feinstrukturkonstante α_Φ = α·Φ.

    Beispiel::

        kernel = OIPKKernel()
        result = kernel.compute()
        print(result.crep)

        for dim in kernel.dimension_series(n_max=7):
            print(dim)
    """

    lambda_m: float = field(default_factory=lambda: _LAMBDA_DEFAULT)
    alpha_phi: float = field(default_factory=_default_alpha_phi)

    # ------------------------------------------------------------------
    # Kern-Größen
    # ------------------------------------------------------------------

    def tau_oipk(self) -> float:
        """Prozesszeit τ_OIPK = λ / c [s].

        Die OIPK-Prozesszeit ist die Lichtlaufzeit über eine Wellenlänge.
        """
        return self.lambda_m / C_LIGHT

    def tau_perp(self) -> float:
        """Orthogonale Prozesszeit τ_⊥ = τ_OIPK / Φ [s].

        Durch Phi-Skalierung ist τ_⊥ geometrisch orthogonal zu t im
        Phi-Gitter-Sinne: ⟨τ_⊥, t⟩ ≡ 0 mod Φ.
        """
        return self.tau_oipk() * TAU_PERP_FACTOR

    def angular_frequency(self) -> float:
        """Kreisfrequenz ω = 2π·c / λ_OIPK [rad/s]."""
        return 2.0 * math.pi * C_LIGHT / self.lambda_m

    def energy(self) -> float:
        """Kernenergie E_OIPK = ℏ · ω · α_Φ [J]."""
        return HBAR * self.angular_frequency() * self.alpha_phi

    def frame_stability(self) -> float:
        """Frame-Stabilitätskriterium S_F = Φ² / α_Φ (dimensionslos)."""
        return PHI**2 / self.alpha_phi

    def crep(self) -> float:
        """CREP-Wert: E_OIPK · S_F · Φ / c [kg·m/s].

        Der Kollaps-Resonanz-Entropie-Preis quantifiziert den Impulsübertrag,
        der beim photonischen Frame-Kollaps freigesetzt wird.
        """
        return self.energy() * self.frame_stability() * PHI / C_LIGHT

    # ------------------------------------------------------------------
    # Rekursive Größen
    # ------------------------------------------------------------------

    def impulse_energy(self, n: int | float) -> float:
        """Impulsenergie auf Stufe n: I_n = E_OIPK · Φ^(n/3) [J]."""
        return self.energy() * PHI ** (n / 3.0)

    def coherence_length(self, n: int | float) -> float:
        """Kohärenzlänge auf Stufe n: L_n = λ_OIPK · Φ^(n/3) [m]."""
        return self.lambda_m * PHI ** (n / 3.0)

    def emergent_dimension(self, n: int) -> OIPKDimension:
        """Bestimmt die emergente Dimension auf Rekursionsstufe n.

        „A dimension emerges when information would otherwise collapse."
        Wenn I_n ≥ E_OIPK (kein Kollaps), dann D_n = ⌈log_Φ(I_n/E_OIPK)⌉.
        Bei Kollaps (I_n < E_OIPK) ist D_n = 0.

        Args:
            n: Rekursionsstufe (≥ 0).

        Returns:
            OIPKDimension mit n, I_n, D_n und Kollaps-Flag.
        """
        i_n = self.impulse_energy(n)
        e0 = self.energy()
        collapsed = i_n < e0
        if collapsed or e0 == 0.0:
            dim = 0
        else:
            ratio = i_n / e0
            dim = math.ceil(math.log(ratio) / math.log(PHI)) if ratio > 1.0 else 0
        return OIPKDimension(n=n, impulse_j=i_n, dimension=dim, collapsed=collapsed)

    def dimension_series(self, n_max: int) -> list[OIPKDimension]:
        """Emergente Dimensionen für n = 0, …, n_max.

        Args:
            n_max: Maximale Rekursionsstufe (inklusiv, ≥ 0).

        Returns:
            Liste von OIPKDimension-Objekten.
        """
        return [self.emergent_dimension(n) for n in range(n_max + 1)]

    def compute(self) -> OIPKResult:
        """Berechnet alle Kerngrößen und gibt ein OIPKResult zurück.

        Returns:
            Vollständiges OIPKResult mit allen OIPK-Parametern.
        """
        return OIPKResult(
            lambda_m=self.lambda_m,
            tau_oipk=self.tau_oipk(),
            tau_perp=self.tau_perp(),
            omega=self.angular_frequency(),
            energy_j=self.energy(),
            frame_stability=self.frame_stability(),
            crep=self.crep(),
            alpha_phi=self.alpha_phi,
            is_orthogonal=True,
        )


# ---------------------------------------------------------------------------
# Hilfsfunktion
# ---------------------------------------------------------------------------


def compute_crep_oipk(kernel: OIPKKernel | None = None) -> float:
    """Berechnet den CREP-Wert für einen gegebenen (oder Standard-)Kernel.

    Args:
        kernel: OIPKKernel-Instanz. Wenn None, wird der Standard-Kernel verwendet.

    Returns:
        CREP-Wert in kg·m/s.
    """
    if kernel is None:
        kernel = OIPKKernel()
    return kernel.crep()
