"""Implosive-Genesis-Gesamtmodell – Zusammenführung aller Formeln.

Dieses Modul konsolidiert alle physikalischen Kernformeln des Implosive-
Genesis-Rahmens in einer einzigen, kohärenten Modellklasse. Alle Docstrings
sind KaTeX-kompatibel formuliert, um direkt in MkDocs-Dokumentation gerendert
werden zu können.

Enthaltene Teilmodelle:
    - Phi-Skalierung (PhiScaling, β_n)
    - V_RIG mit Monte-Carlo-Unsicherheit
    - OIPK / Frame-Prinzip (OIPKernel, FramePrinciple)
    - Tesseract-Zeitscheiben und CREP

Formeln (KaTeX):

.. math::

    \\beta_n = \\beta_0 \\cdot \\Phi^{n/3}

    V_{RIG} \\approx 1352 \\text{ km/s}

    \\omega_F = \\frac{2\\pi c}{\\lambda_{OIPK}}

    E_{OIPK} = \\hbar \\cdot \\omega_F \\cdot \\alpha_{\\Phi}

    S_F = \\frac{\\Phi^2}{\\alpha_{\\Phi}}

    T_n = t_0 \\cdot \\Phi^n

    V_{4D}(n) = T_n^4

    P_E(n, T) = n \\cdot k_B \\cdot T \\cdot \\ln(\\Phi)

    CREP = \\frac{S_{total} \\cdot V_{RIG}}{\\Phi \\cdot c^2}

Verwendung::

    from implosive_genesis.theory.models import ImplosiveGenesisModel
    model = ImplosiveGenesisModel()
    summary = model.full_summary(n=3, temperature=2.725)
    print(summary)
"""

from __future__ import annotations

from dataclasses import dataclass, field

from implosive_genesis.core.physics import PHI, PhiScaling
from implosive_genesis.core.vrig import (
    COSMIC_ALPHA,
    V_RIG_KMS,
    VRIGResult,
    compute_vrig,
    cosmic_alpha_phi,
)
from implosive_genesis.theory.frameprinciple import (
    LAMBDA_OIPK_DEFAULT,
    FramePrinciple,
    OIPKernel,
)
from implosive_genesis.theory.tesseract import CREP, T0_DEFAULT, Tesseract

__all__ = ["ImplosiveGenesisModel", "FullSummary"]


@dataclass(frozen=True)
class FullSummary:
    """Vollständige Zusammenfassung eines Implosive-Genesis-Zustands bei Stufe n.

    Attributes:
        n: Rekursionsstufe.
        beta_n: Phi-skalierter Kopplungsparameter β_n.
        v_rig_result: Monte-Carlo V_RIG-Ergebnis.
        coherence_length_m: Kohärenzlänge L_n in Metern.
        impulse_energy_j: Impulsenergie I_n in Joule.
        frame_stability: Dimensionslose Frame-Stabilität S_F · Φ^{n/3}.
        time_slice: Tesseract-Zeitscheibe T_n.
        volume_4d: 4D-Tesseraktvolumen V_4D(n).
        entropy_price_j: Entropischer Preis P_E(n, T) in Joule.
        crep: CREP-Wert für Gesamtentropie = 1.
        temperature_k: Temperatur T in Kelvin.

    Formeln (KaTeX):

    .. math::

        \\beta_n = \\beta_0 \\cdot \\Phi^{n/3}

        L_n = \\lambda_{OIPK} \\cdot \\Phi^{n/3}

        I_n = E_{OIPK} \\cdot \\Phi^{n/3}

        T_n = t_0 \\cdot \\Phi^n

        P_E = n \\cdot k_B \\cdot T \\cdot \\ln(\\Phi)
    """

    n: int | float
    beta_n: float
    v_rig_result: VRIGResult
    coherence_length_m: float
    impulse_energy_j: float
    frame_stability: float
    time_slice: float
    volume_4d: float
    entropy_price_j: float
    crep: float
    temperature_k: float

    def __str__(self) -> str:
        return (
            f"FullSummary(n={self.n})\n"
            f"  β_n            = {self.beta_n:.6f}\n"
            f"  V_RIG          = {self.v_rig_result.v_rig:.4f}"
            f" ± {self.v_rig_result.std_dev:.4f} km/s\n"
            f"  α_Φ            = {self.v_rig_result.alpha_phi:.8f}\n"
            f"  L_n            = {self.coherence_length_m:.6e} m\n"
            f"  I_n            = {self.impulse_energy_j:.6e} J\n"
            f"  S_F(n)         = {self.frame_stability:.6f}\n"
            f"  T_n            = {self.time_slice:.6f}\n"
            f"  V_4D(n)        = {self.volume_4d:.6e}\n"
            f"  P_E(n,T)       = {self.entropy_price_j:.6e} J  (T={self.temperature_k} K)\n"
            f"  CREP(S=1)      = {self.crep:.6e}\n"
        )


@dataclass
class ImplosiveGenesisModel:
    """Vollständiges Implosive-Genesis-Modell.

    Kombiniert Phi-Skalierung, V_RIG (Monte-Carlo), OIPK-Frameprinciple
    und Tesseract-Zeitscheiben zu einem einheitlichen Rahmen.

    Attributes:
        beta_0: Basis-Kopplungskonstante β_0 (Standard: 1.0).
        lambda_m: OIPK-Wellenlänge λ_OIPK in Metern.
        t_0: Grundzeitscheibe t_0 (Standard: T0_DEFAULT = 1.0).
        v_rig_kms: Implosionsgeschwindigkeit in km/s (Standard: V_RIG_KMS).

    Alle Untermodelle werden bei der ersten Verwendung aus diesen
    Grundparametern instanziiert.

    Formeln (KaTeX):

    .. math::

        \\beta_n = \\beta_0 \\cdot \\Phi^{n/3}

        \\omega_F = \\frac{2\\pi c}{\\lambda_{OIPK}}

        E_{OIPK} = \\hbar \\cdot \\omega_F \\cdot \\alpha_{\\Phi}

        S_F = \\frac{\\Phi^2}{\\alpha_{\\Phi}}

        T_n = t_0 \\cdot \\Phi^n

        V_{4D}(n) = T_n^4

        P_E(n, T) = n \\cdot k_B \\cdot T \\cdot \\ln(\\Phi)

        CREP = \\frac{S_{total} \\cdot V_{RIG}}{\\Phi \\cdot c^2}
    """

    beta_0: float = 1.0
    lambda_m: float = field(default_factory=lambda: LAMBDA_OIPK_DEFAULT)
    t_0: float = T0_DEFAULT
    v_rig_kms: float = V_RIG_KMS

    # --- Teilmodelle (lazy) -------------------------------------------------

    def _phi_scaling(self) -> PhiScaling:
        return PhiScaling(beta_0=self.beta_0)

    def _kernel(self) -> OIPKernel:
        return OIPKernel(lambda_m=self.lambda_m, alpha_phi=cosmic_alpha_phi())

    def _frame(self) -> FramePrinciple:
        return FramePrinciple(kernel=self._kernel())

    def _tesseract(self) -> Tesseract:
        return Tesseract(t_0=self.t_0)

    def _crep(self) -> CREP:
        return CREP(v_rig_kms=self.v_rig_kms)

    # --- Schnell-Zugriff auf Teilformeln ------------------------------------

    def phi(self) -> float:
        """Goldener Schnitt Φ.

        .. math:: \\Phi = \\frac{1 + \\sqrt{5}}{2} \\approx 1.618

        Returns:
            Φ ≈ 1.6180339887.
        """
        return PHI

    def alpha_phi(self) -> float:
        """Phi-skalierte Feinstrukturkonstante α_Φ = α · Φ.

        .. math:: \\alpha_\\Phi = \\alpha \\cdot \\Phi

        Returns:
            α_Φ ≈ 0.01180.
        """
        return cosmic_alpha_phi()

    def beta_n(self, n: int | float) -> float:
        """Phi-skalierter Kopplungsparameter β_n.

        .. math:: \\beta_n = \\beta_0 \\cdot \\Phi^{n/3}

        Args:
            n: Rekursionsstufe.

        Returns:
            β_n-Wert.
        """
        return self._phi_scaling().beta_n(n)

    def vrig(self, samples: int = 10_000, seed: int | None = None) -> VRIGResult:
        """Monte-Carlo V_RIG-Berechnung.

        .. math:: V_{RIG} = V_{base} \\cdot \\beta_n \\pm \\sigma_{MC}

        Args:
            samples: Anzahl Monte-Carlo-Samples.
            seed: Zufalls-Seed für Reproduzierbarkeit.

        Returns:
            VRIGResult mit Mittelwert und Standardabweichung.
        """
        return compute_vrig(beta_0=self.beta_0, samples=samples, seed=seed)

    def coherence_length(self, n: int | float) -> float:
        """Kohärenzlänge L_n = λ_OIPK · Φ^{n/3}.

        .. math:: L_n = \\lambda_{OIPK} \\cdot \\Phi^{n/3}

        Args:
            n: Rekursionsstufe.

        Returns:
            Kohärenzlänge in Metern.
        """
        return self._frame().coherence_length(n)

    def frame_stability(self, n: int | float) -> float:
        """Frame-Stabilität auf Stufe n: S_F · Φ^{n/3}.

        .. math:: S_F(n) = \\frac{\\Phi^2}{\\alpha_\\Phi} \\cdot \\Phi^{n/3}

        Args:
            n: Rekursionsstufe.

        Returns:
            Effektive Stabilitätskennzahl (dimensionslos).
        """
        return self._frame().stability_at(n)

    def time_slice(self, n: int | float) -> float:
        """Tesseract-Zeitscheibe T_n = t_0 · Φ^n.

        .. math:: T_n = t_0 \\cdot \\Phi^n

        Args:
            n: Rekursionsstufe.

        Returns:
            Zeitscheibe in den Einheiten von t_0.
        """
        return self._tesseract().time_slice(n)

    def volume_4d(self, n: int | float) -> float:
        """4D-Tesseraktvolumen V_4D(n) = T_n^4.

        .. math:: V_{4D}(n) = T_n^4 = t_0^4 \\cdot \\Phi^{4n}

        Args:
            n: Rekursionsstufe.

        Returns:
            4D-Volumen in Einheiten von t_0^4.
        """
        return self._tesseract().volume_4d(n)

    def entropy_price(self, n: int | float, temperature: float) -> float:
        """Entropischer Preis P_E(n, T) = n · k_B · T · ln(Φ).

        .. math:: P_E(n, T) = n \\cdot k_B \\cdot T \\cdot \\ln(\\Phi)

        Args:
            n: Rekursionsstufe.
            temperature: Temperatur in Kelvin.

        Returns:
            Entropischer Preis in Joule.
        """
        return self._crep().entropy_price(n, temperature)

    def crep(self, s_total: float = 1.0) -> float:
        """CREP-Wert: CREP = S_total · V_RIG / (Φ · c²).

        .. math:: CREP = \\frac{S_{total} \\cdot V_{RIG}}{\\Phi \\cdot c^2}

        Args:
            s_total: Gesamtentropie S_total (Standard: 1.0).

        Returns:
            CREP-Wert.
        """
        return self._crep().crep_value(s_total)

    def full_summary(
        self,
        n: int | float = 3,
        temperature: float = 2.725,
        samples: int = 1_000,
        seed: int | None = 0,
    ) -> FullSummary:
        """Vollständige Zustandszusammenfassung für Rekursionsstufe n.

        Berechnet alle Kerngrößen des Implosive-Genesis-Modells auf einmal
        und gibt sie als immutables FullSummary-Objekt zurück.

        Args:
            n: Rekursionsstufe (Standard: 3).
            temperature: Temperatur für entropischen Preis in Kelvin (Standard: 2.725 K,
                kosmische Hintergrundstrahlung).
            samples: Monte-Carlo-Samples für V_RIG (Standard: 1 000).
            seed: Zufalls-Seed für V_RIG-Reproduzierbarkeit (Standard: 0).

        Returns:
            FullSummary mit allen berechneten Größen.
        """
        vrig_result = self.vrig(samples=samples, seed=seed)
        return FullSummary(
            n=n,
            beta_n=self.beta_n(n),
            v_rig_result=vrig_result,
            coherence_length_m=self.coherence_length(n),
            impulse_energy_j=self._frame().impulse_energy(n),
            frame_stability=self.frame_stability(n),
            time_slice=self.time_slice(n),
            volume_4d=self.volume_4d(n),
            entropy_price_j=self.entropy_price(n, temperature),
            crep=self.crep(s_total=1.0),
            temperature_k=temperature,
        )

    def constants(self) -> dict[str, float]:
        """Alle Modellkonstanten als Dictionary.

        Returns:
            Dict mit Konstantennamen und -werten:
            PHI, COSMIC_ALPHA, alpha_phi, V_RIG_KMS, beta_0, lambda_m, t_0.
        """
        return {
            "PHI": PHI,
            "COSMIC_ALPHA": COSMIC_ALPHA,
            "alpha_phi": self.alpha_phi(),
            "V_RIG_KMS": self.v_rig_kms,
            "beta_0": self.beta_0,
            "lambda_m": self.lambda_m,
            "t_0": self.t_0,
        }
