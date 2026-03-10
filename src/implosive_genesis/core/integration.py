"""Zentrale ImplosiveGenesis-Integrationsklasse – verbindet alle Komponenten.

Diese Klasse ist der zentrale Einstiegspunkt für das gesamte
Implosive-Genesis-Framework (v0.4.0). Sie verknüpft alle Teilmodule:

- core: Phi-Skalierung, V_RIG, Type-6
- theory: FramePrinciple, Tesseract, CREP, Models
- oipk: OIPK-Kern und τ ⊥ t Orthogonalität
- medium: Medium-Modulation und Anästhesie-Tests
- formalization: Entropischer Preis und Phi-Beweis
- render: Fraktale Rendering-Engine
- chronology: 10-Teile-Chronologie-Validator

Teil 10 der Chronologie – Gesamtintegration.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

__all__ = ["ImplosiveGenesis", "IntegrationSummary"]

PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
V_RIG_KMS: float = 1352.0
C_LIGHT: float = 299_792_458.0
COSMIC_ALPHA: float = 1.0 / 137.035999084
HBAR: float = 1.054571817e-34


@dataclass
class IntegrationSummary:
    """Zusammenfassung einer vollständigen ImplosiveGenesis-Berechnung.

    Attributes:
        phi: Goldener Schnitt.
        v_rig_kms: V_RIG in km/s.
        alpha_phi: Kosmischer Alpha-Parameter α_Φ = α · Φ.
        lambda_oipk: OIPK-Wellenlänge in Metern.
        beta_n: Kopplungsparameter bei Stufe n.
        coherence_length_n: Kohärenzlänge bei Stufe n.
        time_slice_n: Tesseract-Zeitscheibe bei Stufe n.
        fractal_intensity_n: Fraktale Intensität bei Stufe n.
        chronology_passed: True wenn alle 10 Chronologie-Teile bestanden.
        n_chronology_passed: Anzahl bestandener Chronologie-Teile.
        consistency_check: True wenn V_RIG-Phi-Alpha-Konsistenz erfüllt.
        golden_identity: Φ² ≈ Φ + 1 (Wahrheitswert).
        n: Verwendete Rekursionsstufe.
    """

    phi: float
    v_rig_kms: float
    alpha_phi: float
    lambda_oipk: float
    beta_n: float
    coherence_length_n: float
    time_slice_n: float
    fractal_intensity_n: float
    chronology_passed: bool
    n_chronology_passed: int
    consistency_check: bool
    golden_identity: bool
    n: int


class ImplosiveGenesis:
    """Zentrale Integrationsklasse – verbindet alle V_RIG-Komponenten.

    ImplosiveGenesis ist der Haupt-Einstiegspunkt für das gesamte Framework.
    Sie instantiiert alle Teilmodule und bietet eine einheitliche API für
    Berechnungen, Validierungen und Renderings.

    Args:
        beta_0: Basis-Kopplungskonstante (Standard: 1.0).
        t0: Basis-Zeitscheibe in Sekunden (Standard: Planck-Zeit).

    Examples:
        >>> ig = ImplosiveGenesis()
        >>> summary = ig.full_summary(n=5)
        >>> print(f"β_5 = {summary.beta_n:.4f}")
        >>> print(f"Chronologie: {summary.n_chronology_passed}/10 bestanden")

        >>> # Fraktales Rendering
        >>> ascii_art = ig.render_fractal_ascii(depth=6)
        >>> print(ascii_art)

        >>> # Chronologie validieren
        >>> chron_result = ig.validate_chronology()
        >>> assert chron_result.passed
    """

    def __init__(
        self,
        beta_0: float = 1.0,
        t0: float = 5.391e-44,
    ) -> None:
        if beta_0 <= 0:
            raise ValueError(f"beta_0 muss positiv sein, ist aber {beta_0}")
        self.beta_0 = beta_0
        self.t0 = t0
        self._lambda_oipk = C_LIGHT / (V_RIG_KMS * 1000.0)
        self._alpha_phi = COSMIC_ALPHA * PHI

    # ------------------------------------------------------------------
    # Kern-Berechnungen
    # ------------------------------------------------------------------

    @property
    def phi(self) -> float:
        """Goldener Schnitt Φ."""
        return PHI

    @property
    def v_rig_kms(self) -> float:
        """V_RIG in km/s."""
        return V_RIG_KMS

    @property
    def alpha_phi(self) -> float:
        """Kosmischer Alpha-Parameter α_Φ = α · Φ."""
        return self._alpha_phi

    @property
    def lambda_oipk(self) -> float:
        """OIPK-Wellenlänge λ_OIPK = c / V_RIG in Metern."""
        return self._lambda_oipk

    def beta_n(self, n: int | float) -> float:
        """Kopplungsparameter β_n = β_0 · Φ^{n/3}.

        Args:
            n: Rekursionsstufe.

        Returns:
            Kopplungsparameter bei Stufe n.
        """
        return self.beta_0 * PHI ** (n / 3.0)

    def coherence_length(self, n: int | float) -> float:
        """Kohärenzlänge L_n = λ_OIPK · Φ^{n/3}.

        Args:
            n: Rekursionsstufe.

        Returns:
            Kohärenzlänge in Metern.
        """
        return self._lambda_oipk * PHI ** (n / 3.0)

    def time_slice(self, n: int | float) -> float:
        """Tesseract-Zeitscheibe T_n = t_0 · Φ^n.

        Args:
            n: Rekursionsstufe.

        Returns:
            Zeitscheibe in Sekunden.
        """
        return self.t0 * PHI**n

    def fractal_intensity(self, n: int | float) -> float:
        """Fraktale Intensität I_n = 1/Φ^n.

        Args:
            n: Rekursionsstufe.

        Returns:
            Normierte Intensität ∈ (0, 1].
        """
        return 1.0 / PHI**n

    def geometric_waste(self, n: int | float) -> float:
        """Geometrischer Verschnitt W(n) = 1 − 1/Φ^{n/3}.

        Args:
            n: Rekursionsstufe.

        Returns:
            Verschnittanteil W(n) ∈ [0, 1).
        """
        return 1.0 - 1.0 / PHI ** (n / 3.0)

    # ------------------------------------------------------------------
    # Render-Integration
    # ------------------------------------------------------------------

    def render_fractal_ascii(self, depth: int = 5, animate: bool = False) -> str:
        """Rendere den fraktalen Tesseract als ASCII-Art.

        Args:
            depth: Maximale Rekursionstiefe (Standard: 5).
            animate: Wenn True, zusätzliche Animations-Frames ausgeben.

        Returns:
            ASCII-String der Fraktalstruktur.
        """
        from ..render.fractal_tesseract import FractalTesseract

        ft = FractalTesseract(beta_0=self.beta_0, t0=self.t0)
        result = ft.render(depth=depth, animate=animate)
        return result.ascii_art

    def render_fractal(self, depth: int = 5, animate: bool = False):
        """Rendere den fraktalen Tesseract vollständig.

        Args:
            depth: Maximale Rekursionstiefe.
            animate: Wenn True, Animations-Frames einschließen.

        Returns:
            RenderResult mit Fraktalbaum und ASCII-Darstellung.
        """
        from ..render.fractal_tesseract import FractalTesseract

        ft = FractalTesseract(beta_0=self.beta_0, t0=self.t0)
        return ft.render(depth=depth, animate=animate)

    # ------------------------------------------------------------------
    # Chronologie-Integration
    # ------------------------------------------------------------------

    def validate_chronology(self, tolerance: float = 1e-6):
        """Validiere die vollständige 10-Teile-Chronologie.

        Args:
            tolerance: Relative Fehlertoleranz für numerische Checks.

        Returns:
            ChronologyResult mit Detailergebnissen.
        """
        from ..chronology.integration import ChronologyValidator

        validator = ChronologyValidator(tolerance=tolerance)
        return validator.validate()

    # ------------------------------------------------------------------
    # Gesamtzusammenfassung
    # ------------------------------------------------------------------

    def full_summary(self, n: int = 5, validate_chronology: bool = True) -> IntegrationSummary:
        """Erzeuge eine vollständige Integrations-Zusammenfassung.

        Berechnet alle Kerngrößen auf Rekursionsstufe n und führt
        optional die Chronologie-Validierung durch.

        Args:
            n: Rekursionsstufe (Standard: 5).
            validate_chronology: Wenn True, Chronologie-Validierung einschließen.

        Returns:
            IntegrationSummary mit allen berechneten Größen.
        """
        # Konsistenz: λ_OIPK · V_RIG = c (Definition der OIPK-Wellenlänge)
        v_rig_ms = V_RIG_KMS * 1000.0
        product_norm = self._lambda_oipk * v_rig_ms / C_LIGHT
        consistency = abs(product_norm - 1.0) < 1e-10

        # Goldene Identität: Φ² = Φ + 1
        golden = abs(PHI**2 - (PHI + 1.0)) < 1e-10

        chronology_passed = False
        n_chron_passed = 0
        if validate_chronology:
            chron = self.validate_chronology()
            chronology_passed = chron.passed
            n_chron_passed = chron.n_passed

        return IntegrationSummary(
            phi=PHI,
            v_rig_kms=V_RIG_KMS,
            alpha_phi=self._alpha_phi,
            lambda_oipk=self._lambda_oipk,
            beta_n=self.beta_n(n),
            coherence_length_n=self.coherence_length(n),
            time_slice_n=self.time_slice(n),
            fractal_intensity_n=self.fractal_intensity(n),
            chronology_passed=chronology_passed,
            n_chronology_passed=n_chron_passed,
            consistency_check=consistency,
            golden_identity=golden,
            n=n,
        )

    def __repr__(self) -> str:
        return (
            f"ImplosiveGenesis(beta_0={self.beta_0}, "
            f"Φ={PHI:.6f}, V_RIG={V_RIG_KMS} km/s, "
            f"λ_OIPK={self._lambda_oipk:.2f} m)"
        )
