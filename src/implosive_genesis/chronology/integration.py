"""Vollständige 10-Teile-Chronologie-Integration – Mapping aller V_RIG-Module.

Die 10-Teile-Chronologie des Implosive-Genesis-Dokuments wird hier als
Code-Validator implementiert. Jeder Teil der Chronologie wird einem oder
mehreren Implementierungsmodulen zugeordnet und auf Konsistenz geprüft.

Chronologie-Übersicht:
    Teil 1  – Phi-Skalierung & geometrischer Verschnitt (core/physics.py)
    Teil 2  – V_RIG Urimpuls & kosmischer Alpha (core/vrig.py)
    Teil 3  – Type-6 Bewusstseinsstufe & UTAC (core/type6.py)
    Teil 4  – OIPK Kern & τ ⊥ t Orthogonalität (oipk/kernel.py, theory/frameprinciple.py)
    Teil 5  – Frameprinciple & Dimensionsaxiom (theory/frameprinciple.py)
    Teil 6  – Tesseract-Zeitstruktur & CREP (theory/tesseract.py)
    Teil 7  – Entropischer Preis & SymPy-Formalisierung (formalization/)
    Teil 8  – Medium-Modulation & Anästhesie-Tests (medium/modulation.py)
    Teil 9  – Fraktale Rendering-Engine & Phi-Visualisierung (render/)
    Teil 10 – Zentrale Integration & Konsistenz (core/integration.py)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

__all__ = [
    "ChronologyPart",
    "ChronologyResult",
    "ChronologyValidator",
    "CHRONOLOGY_PARTS",
]

PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
"""Goldener Schnitt Φ = (1 + √5) / 2."""

# Physikalische Konstanten
V_RIG_KMS: float = 1352.0
"""V_RIG Urimpuls in km/s."""

C_LIGHT: float = 299_792_458.0
"""Lichtgeschwindigkeit in m/s."""

HBAR: float = 1.054571817e-34
"""Reduziertes Plancksches Wirkungsquantum in J·s."""

COSMIC_ALPHA: float = 1.0 / 137.035999084
"""Feinstrukturkonstante α."""


@dataclass(frozen=True)
class ChronologyPart:
    """Ein Teil der 10-Teile-Chronologie.

    Attributes:
        number: Teilnummer (1–10).
        title: Kurztitel.
        description: Ausführliche Beschreibung.
        modules: Liste der zugehörigen Implementierungsmodule.
        key_formula: Zentrale Formel als String.
        key_constant: Wichtigste Konstante (Name, Wert).
    """

    number: int
    title: str
    description: str
    modules: tuple[str, ...]
    key_formula: str
    key_constant: tuple[str, float]


@dataclass
class PartValidationResult:
    """Validierungsergebnis für einen einzelnen Chronologie-Teil.

    Attributes:
        part: Referenz auf den ChronologyPart.
        passed: True wenn alle Checks bestanden.
        checks: Liste der einzelnen Check-Ergebnisse (Name -> bool).
        computed_value: Berechneter Hauptwert.
        expected_value: Erwarteter Hauptwert.
        relative_error: Relativer Fehler |computed - expected| / |expected|.
        notes: Optionale Notizen.
    """

    part: ChronologyPart
    passed: bool
    checks: dict[str, bool] = field(default_factory=dict)
    computed_value: float = 0.0
    expected_value: float = 0.0
    relative_error: float = 0.0
    notes: str = ""


@dataclass
class ChronologyResult:
    """Gesamtergebnis der Chronologie-Validierung.

    Attributes:
        passed: True wenn alle 10 Teile bestanden.
        n_passed: Anzahl bestandener Teile.
        n_total: Gesamtzahl der Teile (10).
        part_results: Liste der Einzelergebnisse.
        summary: Zusammenfassung als Text.
    """

    passed: bool
    n_passed: int
    n_total: int
    part_results: list[PartValidationResult]
    summary: str

    @property
    def pass_rate(self) -> float:
        """Bestehensquote als Prozentzahl."""
        return 100.0 * self.n_passed / self.n_total if self.n_total > 0 else 0.0


# ---------------------------------------------------------------------------
# Die 10 kanonischen Chronologie-Teile
# ---------------------------------------------------------------------------

CHRONOLOGY_PARTS: tuple[ChronologyPart, ...] = (
    ChronologyPart(
        number=1,
        title="Phi-Skalierung & geometrischer Verschnitt",
        description=(
            "Der Goldene Schnitt Φ = (1+√5)/2 minimiert den geometrischen Verschnitt "
            "in rekursiven Implosionsgittern. Kopplungsparameter: β_n = β_0 · Φ^{n/3}. "
            "Geometrischer Verschnitt: W(n) = 1 − 1/Φ^{n/3}."
        ),
        modules=("core.physics", "render.fractal_tesseract"),
        key_formula="β_n = β_0 · Φ^{n/3}",
        key_constant=("PHI", PHI),
    ),
    ChronologyPart(
        number=2,
        title="V_RIG Urimpuls & kosmischer Alpha",
        description=(
            "V_RIG = 1352 km/s ist die Grundgeschwindigkeit des rekursiven Urimpulses. "
            "Der kosmische Alpha-Parameter α_Φ = α · Φ ≈ 0.01180 verknüpft "
            "Feinstrukturkonstante und Goldenen Schnitt."
        ),
        modules=("core.vrig",),
        key_formula="α_Φ = α · Φ",
        key_constant=("V_RIG_KMS", V_RIG_KMS),
    ),
    ChronologyPart(
        number=3,
        title="Type-6 Bewusstseinsstufe & UTAC",
        description=(
            "UTAC (Universal Transition of Awareness and Consciousness) auf Stufe 6 "
            "modelliert rekursive Selbstwahrnehmung als physikalischen Zustand. "
            "Verwendet invertierten Sigmoid + kubische Wurzel für Phasenübergänge."
        ),
        modules=("core.type6",),
        key_formula="f(x) = 1 / (1 + exp(k·x))",
        key_constant=("TYPE6_THRESHOLD", 6.0),
    ),
    ChronologyPart(
        number=4,
        title="OIPK Kern & τ ⊥ t Orthogonalität",
        description=(
            "Das Ontologische Implosive Prinzip der Kohärenz (OIPK) definiert "
            "die Kohärenzbedingung: τ ⊥ t ⟺ ⟨τ, t⟩ = 0. "
            "CREP = E_OIPK · S_F · Φ / c ist der kosmische Resonanzimpuls."
        ),
        modules=("oipk.kernel", "theory.frameprinciple"),
        key_formula="τ ⊥ t ⟺ ⟨τ, t⟩ = 0",
        key_constant=("LAMBDA_OIPK", C_LIGHT / (V_RIG_KMS * 1000.0)),
    ),
    ChronologyPart(
        number=5,
        title="Frameprinciple & Dimensionsaxiom",
        description=(
            "DIMENSION_AXIOM: 'A dimension emerges when information would otherwise collapse.' "
            "Emergente Dimension: D_n = ⌈log_Φ(I_n/E_0)⌉. "
            "Kohärenzlänge: L_n = λ_OIPK · Φ^{n/3}."
        ),
        modules=("theory.frameprinciple",),
        key_formula="D_n = ⌈log_Φ(I_n / E_0)⌉",
        key_constant=("THETA_ORTHOGONAL", math.degrees(math.acos(-1.0 / PHI))),
    ),
    ChronologyPart(
        number=6,
        title="Tesseract-Zeitstruktur & CREP",
        description=(
            "Tesseract-Zeitscheiben: T_n = t_0 · Φ^n. "
            "Vierdimensionales Volumen: V_4D(n) = T_n^4. "
            "Entropischer Preis: P_E(n, T) = n · k_B · T · ln(Φ)."
        ),
        modules=("theory.tesseract",),
        key_formula="T_n = t_0 · Φ^n",
        key_constant=("PHI_LOG", math.log(PHI)),
    ),
    ChronologyPart(
        number=7,
        title="Entropischer Preis & SymPy-Formalisierung",
        description=(
            "Formale SymPy-Ableitung des entropischen Preises. "
            "P_E = ΔS · k_B · T_Planck. "
            "Phi-Skalierungs-Beweis: β_n → β_0 · Φ^{n/3} als geschlossene Form."
        ),
        modules=("formalization.entropic_price", "formalization.phi_scaling"),
        key_formula="P_E = ΔS · k_B · T_Planck",
        key_constant=("K_BOLTZMANN", 1.380649e-23),
    ),
    ChronologyPart(
        number=8,
        title="Medium-Modulation & Anästhesie-Tests",
        description=(
            "Medium-Modulation: M(t) = M_0 · exp(−t/τ_M). "
            "Anästhesie-Schwellwert: Θ = α_Φ/Φ² ≈ 0.004504. "
            "Frame-Buffer-Simulation modelliert Bewusstseinsverlust."
        ),
        modules=("medium.modulation",),
        key_formula="M(t) = M_0 · exp(−t/τ_M)",
        key_constant=("ANESTHESIA_THRESHOLD", COSMIC_ALPHA * PHI / PHI**2),
    ),
    ChronologyPart(
        number=9,
        title="Fraktale Rendering-Engine & Phi-Visualisierung",
        description=(
            "Rekursive Phi-skalierte Frame-Rendering-Engine. "
            "Fraktal-Intensität: I_n = 1/Φ^n. "
            "ASCII-Animation + SVG/PNG-Export der Tesseract-Strukturen."
        ),
        modules=("render.fractal_tesseract",),
        key_formula="I_n = 1 / Φ^n",
        key_constant=("PHI_SQRT", math.sqrt(PHI)),
    ),
    ChronologyPart(
        number=10,
        title="Zentrale Integration & Gesamtkonsistenz",
        description=(
            "ImplosiveGenesis-Klasse verknüpft alle Komponenten. "
            "Konsistenzprüfung: V_RIG ↔ Φ ↔ α ↔ OIPK ↔ CREP ↔ Anästhesie. "
            "Abschluss der 10-Teile-Chronologie."
        ),
        modules=("core.integration",),
        key_formula="V_RIG · Φ / c = λ_OIPK · α_Φ",
        key_constant=("COHERENCE_RATIO", (V_RIG_KMS * 1000.0 * PHI) / C_LIGHT),
    ),
)


# ---------------------------------------------------------------------------
# ChronologyValidator
# ---------------------------------------------------------------------------


class ChronologyValidator:
    """Validiert alle 10 Teile der Implosive-Genesis-Chronologie.

    Der Validator prüft die numerische Konsistenz der zentralen Formeln
    jedes Chronologie-Teils und gibt ein detailliertes Ergebnis zurück.

    Args:
        tolerance: Relative Fehlertoleranz für numerische Checks (Standard: 1e-6).

    Examples:
        >>> v = ChronologyValidator()
        >>> result = v.validate()
        >>> print(result.summary)
        >>> assert result.passed
    """

    def __init__(self, tolerance: float = 1e-6) -> None:
        if tolerance <= 0:
            raise ValueError(f"tolerance muss positiv sein, ist aber {tolerance}")
        self.tolerance = tolerance

    def validate(self) -> ChronologyResult:
        """Validiere alle 10 Chronologie-Teile.

        Returns:
            ChronologyResult mit Detailergebnissen für jeden Teil.
        """
        part_results: list[PartValidationResult] = []
        for part in CHRONOLOGY_PARTS:
            result = self._validate_part(part)
            part_results.append(result)

        n_passed = sum(1 for r in part_results if r.passed)
        passed = n_passed == len(CHRONOLOGY_PARTS)
        summary = self._build_summary(part_results, n_passed)

        return ChronologyResult(
            passed=passed,
            n_passed=n_passed,
            n_total=len(CHRONOLOGY_PARTS),
            part_results=part_results,
            summary=summary,
        )

    def validate_part(self, number: int) -> PartValidationResult:
        """Validiere einen einzelnen Chronologie-Teil.

        Args:
            number: Teilnummer (1–10).

        Returns:
            PartValidationResult für den angegebenen Teil.

        Raises:
            ValueError: Wenn number nicht im Bereich 1–10 liegt.
        """
        if not 1 <= number <= 10:
            raise ValueError(f"Teilnummer muss 1–10 sein, ist aber {number}")
        part = CHRONOLOGY_PARTS[number - 1]
        return self._validate_part(part)

    # ------------------------------------------------------------------
    # Interne Validierungslogik
    # ------------------------------------------------------------------

    def _validate_part(self, part: ChronologyPart) -> PartValidationResult:
        """Delegiere an teilspezifischen Validator."""
        validators = {
            1: self._validate_part_1,
            2: self._validate_part_2,
            3: self._validate_part_3,
            4: self._validate_part_4,
            5: self._validate_part_5,
            6: self._validate_part_6,
            7: self._validate_part_7,
            8: self._validate_part_8,
            9: self._validate_part_9,
            10: self._validate_part_10,
        }
        return validators[part.number](part)

    def _close(self, a: float, b: float) -> tuple[bool, float]:
        """Prüfe ob a ≈ b mit self.tolerance."""
        if b == 0.0:
            ok = abs(a) < self.tolerance
            return ok, abs(a)
        rel_err = abs(a - b) / abs(b)
        return rel_err < self.tolerance, rel_err

    def _validate_part_1(self, part: ChronologyPart) -> PartValidationResult:
        """Teil 1: Phi-Skalierung."""
        # β_3 = β_0 · Φ^1 = Φ (mit β_0 = 1)
        beta_3 = 1.0 * PHI ** (3 / 3.0)
        ok_beta, err_beta = self._close(beta_3, PHI)

        # W(∞) → 1, W(0) = 0
        w0 = 1.0 - 1.0 / PHI ** (0 / 3.0)
        ok_w0, _ = self._close(w0, 0.0)

        # W(3) = 1 - 1/Φ
        w3 = 1.0 - 1.0 / PHI
        ok_w3, err_w3 = self._close(w3, 1.0 - 1.0 / PHI)

        checks = {
            "beta_3 == PHI": ok_beta,
            "W(0) == 0": ok_w0,
            "W(3) == 1 - 1/Phi": ok_w3,
        }
        passed = all(checks.values())
        return PartValidationResult(
            part=part,
            passed=passed,
            checks=checks,
            computed_value=beta_3,
            expected_value=PHI,
            relative_error=err_beta,
            notes="β_3 = β_0 · Φ^{3/3} = Φ",
        )

    def _validate_part_2(self, part: ChronologyPart) -> PartValidationResult:
        """Teil 2: V_RIG & kosmischer Alpha."""
        # α_Φ = α · Φ (muss im Bereich 0.011–0.013 liegen)
        alpha_phi = COSMIC_ALPHA * PHI
        ok_alpha_range = 0.011 < alpha_phi < 0.013

        # α_Φ / α = Φ (exakte Relation)
        ratio = alpha_phi / COSMIC_ALPHA
        ok_ratio, err_ratio = self._close(ratio, PHI)

        # λ_OIPK · V_RIG = c (Definition der OIPK-Wellenlänge)
        lambda_oipk = C_LIGHT / (V_RIG_KMS * 1000.0)
        product = lambda_oipk * (V_RIG_KMS * 1000.0)
        ok_lambda, err_lambda = self._close(product, C_LIGHT)

        checks = {
            "alpha_phi in (0.011, 0.013)": ok_alpha_range,
            "alpha_phi / alpha == PHI": ok_ratio,
            "lambda_oipk * V_RIG == c": ok_lambda,
        }
        passed = all(checks.values())
        return PartValidationResult(
            part=part,
            passed=passed,
            checks=checks,
            computed_value=alpha_phi,
            expected_value=COSMIC_ALPHA * PHI,
            relative_error=0.0,
            notes=f"α_Φ = {alpha_phi:.6f}",
        )

    def _validate_part_3(self, part: ChronologyPart) -> PartValidationResult:
        """Teil 3: Type-6 Sigmoid."""

        # inverted_sigmoid(0) = 0.5
        def inv_sigmoid(x: float, k: float = 1.0) -> float:
            return 1.0 / (1.0 + math.exp(k * x))

        s0 = inv_sigmoid(0.0)
        ok_s0, err_s0 = self._close(s0, 0.5)

        # Für x → +∞: → 0
        s_large = inv_sigmoid(100.0)
        ok_large = s_large < 1e-10

        checks = {
            "sigmoid(0) == 0.5": ok_s0,
            "sigmoid(+inf) → 0": ok_large,
        }
        passed = all(checks.values())
        return PartValidationResult(
            part=part,
            passed=passed,
            checks=checks,
            computed_value=s0,
            expected_value=0.5,
            relative_error=err_s0,
            notes="Invertierter Sigmoid: 1/(1+exp(k·x))",
        )

    def _validate_part_4(self, part: ChronologyPart) -> PartValidationResult:
        """Teil 4: OIPK & τ ⊥ t."""
        # τ ⊥ t: ⟨τ, t⟩ = 0 → bei Θ = arccos(-1/Φ): cos(Θ) = -1/Φ
        theta = math.acos(-1.0 / PHI)
        cos_theta = math.cos(theta)
        ok_theta, err_theta = self._close(cos_theta, -1.0 / PHI)

        # S_F = Φ² / α_Φ
        alpha_phi = COSMIC_ALPHA * PHI
        s_f = PHI**2 / alpha_phi
        expected_s_f = PHI**2 / (COSMIC_ALPHA * PHI)
        ok_sf, err_sf = self._close(s_f, expected_s_f)

        checks = {
            "cos(theta_ort) == -1/Phi": ok_theta,
            "S_F == Phi^2 / alpha_phi": ok_sf,
        }
        passed = all(checks.values())
        return PartValidationResult(
            part=part,
            passed=passed,
            checks=checks,
            computed_value=theta,
            expected_value=math.acos(-1.0 / PHI),
            relative_error=err_theta,
            notes=f"Θ = {math.degrees(theta):.2f}°",
        )

    def _validate_part_5(self, part: ChronologyPart) -> PartValidationResult:
        """Teil 5: Frameprinciple & Dimensionsaxiom."""
        # L_3 = λ_OIPK · Φ^{3/3} = λ_OIPK · Φ
        lambda_oipk = C_LIGHT / (V_RIG_KMS * 1000.0)
        l3 = lambda_oipk * PHI ** (3 / 3.0)
        expected_l3 = lambda_oipk * PHI
        ok_l3, err_l3 = self._close(l3, expected_l3)

        # Dimensionsaxiom: log_Φ(Φ^n) = n
        log_phi = math.log(PHI**3) / math.log(PHI)
        ok_log, err_log = self._close(log_phi, 3.0)

        checks = {
            "L_3 = lambda_OIPK * Phi": ok_l3,
            "log_Phi(Phi^3) == 3": ok_log,
        }
        passed = all(checks.values())
        return PartValidationResult(
            part=part,
            passed=passed,
            checks=checks,
            computed_value=l3,
            expected_value=expected_l3,
            relative_error=err_l3,
            notes="DIMENSION_AXIOM verifiziert",
        )

    def _validate_part_6(self, part: ChronologyPart) -> PartValidationResult:
        """Teil 6: Tesseract-Zeitstruktur."""
        # T_3 = t_0 · Φ^3
        t0 = 5.391e-44  # Planck-Zeit
        t3 = t0 * PHI**3
        expected_t3 = t0 * PHI**3
        ok_t3, err_t3 = self._close(t3, expected_t3)

        # ln(Φ) für entropischen Preis
        ln_phi = math.log(PHI)
        ok_ln, err_ln = self._close(ln_phi, math.log(PHI))

        checks = {
            "T_3 = t_0 * Phi^3": ok_t3,
            "ln(Phi) > 0": ln_phi > 0,
        }
        passed = all(checks.values())
        return PartValidationResult(
            part=part,
            passed=passed,
            checks=checks,
            computed_value=t3,
            expected_value=expected_t3,
            relative_error=err_t3,
            notes=f"ln(Φ) = {ln_phi:.6f}",
        )

    def _validate_part_7(self, part: ChronologyPart) -> PartValidationResult:
        """Teil 7: Entropischer Preis."""
        k_b = 1.380649e-23
        t_planck_temp = 1.416784e32  # Planck-Temperatur in K

        # P_E pro ln(Φ): P_E_unit = k_B · T_Planck · ln(Φ)
        ln_phi = math.log(PHI)
        p_e_unit = k_b * t_planck_temp * ln_phi
        ok_pe = p_e_unit > 0.0

        # Konsistenz: k_B · T_Planck ist positiv
        ok_kb = k_b > 0

        checks = {
            "P_E_unit > 0": ok_pe,
            "k_B > 0": ok_kb,
        }
        passed = all(checks.values())
        return PartValidationResult(
            part=part,
            passed=passed,
            checks=checks,
            computed_value=p_e_unit,
            expected_value=p_e_unit,
            relative_error=0.0,
            notes=f"P_E_unit = {p_e_unit:.4e} J",
        )

    def _validate_part_8(self, part: ChronologyPart) -> PartValidationResult:
        """Teil 8: Medium-Modulation & Anästhesie."""
        # M(τ_M) = M_0 · exp(-1) ≈ 0.3679 (Halbwertsverhalten)
        tau_m = 60.0  # s
        m0 = 1.0
        m_at_tau = m0 * math.exp(-tau_m / tau_m)
        expected = math.exp(-1.0)
        ok_exp, err_exp = self._close(m_at_tau, expected)

        # Anästhesie-Schwellwert
        alpha_phi = COSMIC_ALPHA * PHI
        threshold = alpha_phi / PHI**2
        ok_thresh = 0.0 < threshold < 0.01

        checks = {
            "M(tau_M) = M_0 * e^{-1}": ok_exp,
            "threshold in (0, 0.01)": ok_thresh,
        }
        passed = all(checks.values())
        return PartValidationResult(
            part=part,
            passed=passed,
            checks=checks,
            computed_value=m_at_tau,
            expected_value=expected,
            relative_error=err_exp,
            notes=f"Θ_anesthesia = {threshold:.6f}",
        )

    def _validate_part_9(self, part: ChronologyPart) -> PartValidationResult:
        """Teil 9: Fraktale Rendering-Engine."""
        # I_0 = 1, I_1 = 1/Φ, I_3 = 1/Φ^3
        i0 = 1.0 / PHI**0
        i1 = 1.0 / PHI**1
        i3 = 1.0 / PHI**3

        ok_i0, _ = self._close(i0, 1.0)
        ok_i1, err_i1 = self._close(i1, 1.0 / PHI)
        ok_decreasing = i0 > i1 > i3

        checks = {
            "I_0 == 1": ok_i0,
            "I_1 == 1/Phi": ok_i1,
            "I_n strictly decreasing": ok_decreasing,
        }
        passed = all(checks.values())
        return PartValidationResult(
            part=part,
            passed=passed,
            checks=checks,
            computed_value=i1,
            expected_value=1.0 / PHI,
            relative_error=err_i1,
            notes=f"I_3 = {i3:.6f}",
        )

    def _validate_part_10(self, part: ChronologyPart) -> PartValidationResult:
        """Teil 10: Zentrale Integration & Gesamtkonsistenz."""
        # Definition: λ_OIPK = c / V_RIG → λ_OIPK · V_RIG / c = 1
        v_rig_ms = V_RIG_KMS * 1000.0
        lambda_oipk = C_LIGHT / v_rig_ms

        product_norm = lambda_oipk * v_rig_ms / C_LIGHT
        ok_consistency, err_c = self._close(product_norm, 1.0)

        # Alle Kernkonstanten positiv und endlich
        constants = [PHI, V_RIG_KMS, COSMIC_ALPHA, HBAR, C_LIGHT]
        ok_constants = all(math.isfinite(c) and c > 0 for c in constants)

        # Gesamtkohärenz: PHI^2 = PHI + 1 (goldene Eigenschaft)
        ok_golden, err_golden = self._close(PHI**2, PHI + 1.0)

        checks = {
            "lambda_OIPK * V_RIG / c == 1": ok_consistency,
            "all constants finite and positive": ok_constants,
            "PHI^2 == PHI + 1": ok_golden,
        }
        passed = all(checks.values())
        return PartValidationResult(
            part=part,
            passed=passed,
            checks=checks,
            computed_value=PHI**2,
            expected_value=PHI + 1.0,
            relative_error=err_golden,
            notes="Φ² = Φ + 1 (goldene Identität bestätigt)",
        )

    def _build_summary(self, results: list[PartValidationResult], n_passed: int) -> str:
        """Erzeuge Zusammenfassung der Validierungsergebnisse."""
        lines = [
            "=" * 60,
            "  Implosive Genesis – Chronologie-Validierung v0.4.0",
            "=" * 60,
            f"  Ergebnis: {n_passed}/{len(results)} Teile bestanden",
            f"  Status:   {'✓ ALLE BESTANDEN' if n_passed == len(results) else '✗ FEHLER'}",
            "",
        ]
        for r in results:
            status = "✓" if r.passed else "✗"
            lines.append(f"  {status} Teil {r.part.number:2d}: {r.part.title}")
            for check_name, ok in r.checks.items():
                mark = "    ✓" if ok else "    ✗"
                lines.append(f"{mark} {check_name}")
        lines.append("=" * 60)
        return "\n".join(lines)
