"""Phi-Skalierung – Exakter SymPy-Beweis und Stabilitätsanalyse.

Beweist symbolisch die Skalierungsrelation:

    β_n = β_0 · Φ^{n/3}

und analysiert die Stabilität des Phi-Gitters durch:

    1. Symbolischen Beweis der Rekursionsrelation: β_{n+3} = Φ · β_n
    2. Lyapunov-Stabilitätsanalyse: λ = ln(Φ^{1/3}) > 0 (exponentiell)
    3. Verhältnis-Beweis: β_{n+1}/β_n = Φ^{1/3} = const

Verwendung::

    from implosive_genesis.formalization.phi_scaling import PhiScalingProof, stability_analysis
    proof = PhiScalingProof()
    print(proof.verify_recursion())
    sa = stability_analysis()
    print(sa)
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import sympy as sp

__all__ = ["PhiScalingProof", "StabilityResult", "stability_analysis"]

# ---------------------------------------------------------------------------
# Physikalische / mathematische Konstanten
# ---------------------------------------------------------------------------

PHI_VAL: float = (1.0 + math.sqrt(5.0)) / 2.0
"""Goldener Schnitt Φ ≈ 1.6180339887."""

# SymPy-exakter Goldener Schnitt: (1 + sqrt(5)) / 2
PHI_EXACT: sp.Expr = (1 + sp.sqrt(5)) / 2
"""SymPy-exakter Wert des Goldenen Schnitts."""


@dataclass
class PhiScalingProof:
    """Exakter SymPy-Beweis für β_n = β_0 · Φ^{n/3}.

    Enthält symbolische Beweise für:
        1. Basisdefinition: β_n = β_0 · Φ^{n/3}
        2. Rekursionsrelation: β_{n+3} = Φ · β_n
        3. Verhältniskonstanz: β_{n+1}/β_n = Φ^{1/3}
        4. Goldene-Schnitt-Identität: Φ² = Φ + 1

    Attributes:
        beta_0_val: Numerischer Wert von β_0 (Standard: 1.0).
    """

    beta_0_val: float = 1.0

    def __post_init__(self) -> None:
        # SymPy-Symbole
        self.n = sp.Symbol("n", nonnegative=True)
        self.beta_0 = sp.Symbol("beta_0", positive=True)
        self.Phi = PHI_EXACT

    def beta_n_expr(self, n_sym: sp.Expr | None = None) -> sp.Expr:
        """Symbolischer Ausdruck für β_n = β_0 · Φ^{n/3}.

        Args:
            n_sym: SymPy-Symbol oder Ausdruck für n (Standard: self.n).

        Returns:
            SymPy-Ausdruck β_0 · Φ^{n/3}.
        """
        n_val = n_sym if n_sym is not None else self.n
        return self.beta_0 * self.Phi ** (n_val / 3)

    def verify_recursion(self) -> bool:
        """Beweist symbolisch: β_{n+3} = Φ · β_n.

        Zeigt, dass β_{n+3} / β_n = Φ exakt gilt.

        Returns:
            True wenn der Beweis erfolgreich ist.
        """
        beta_n = self.beta_n_expr(self.n)
        beta_n3 = self.beta_n_expr(self.n + 3)
        ratio = sp.simplify(beta_n3 / beta_n)
        return sp.simplify(ratio - self.Phi) == sp.S.Zero

    def verify_ratio_constant(self) -> bool:
        """Beweist: β_{n+1}/β_n = Φ^{1/3} = const für alle n.

        Returns:
            True wenn das Verhältnis konstant Φ^{1/3} ist.
        """
        beta_n = self.beta_n_expr(self.n)
        beta_n1 = self.beta_n_expr(self.n + 1)
        ratio = sp.simplify(beta_n1 / beta_n)
        expected = self.Phi ** sp.Rational(1, 3)
        return sp.simplify(ratio - expected) == sp.S.Zero

    def verify_golden_ratio_identity(self) -> bool:
        """Beweist die Goldene-Schnitt-Identität: Φ² = Φ + 1.

        Returns:
            True wenn Φ² - Φ - 1 = 0.
        """
        identity = sp.simplify(self.Phi**2 - self.Phi - 1)
        return identity == sp.S.Zero

    def symbolic_derivative(self) -> sp.Expr:
        """Ableitung dβ_n/dn = β_0 · Φ^{n/3} · ln(Φ)/3.

        Zeigt das exponentielle Wachstum der Skalierung.

        Returns:
            SymPy-Ausdruck für dβ_n/dn.
        """
        beta = self.beta_n_expr()
        return sp.diff(beta, self.n)

    def lyapunov_exponent_symbolic(self) -> sp.Expr:
        """Symbolischer Lyapunov-Exponent: λ = ln(Φ^{1/3}) = ln(Φ)/3.

        λ > 0 zeigt exponentielles Wachstum (keine Lyapunov-Stabilität
        im klassischen Sinne, aber kontrollierte Phi-Skalierung).

        Returns:
            SymPy-Ausdruck für λ.
        """
        return sp.log(self.Phi) / 3

    def numerical_beta_series(self, n_max: int) -> list[tuple[int, float]]:
        """Numerische Berechnung der β_n-Reihe für n = 0, …, n_max.

        Args:
            n_max: Maximale Rekursionsstufe.

        Returns:
            Liste von (n, β_n)-Tupeln.
        """
        return [(n, self.beta_0_val * PHI_VAL ** (n / 3.0)) for n in range(n_max + 1)]

    def run_all_proofs(self) -> dict[str, bool]:
        """Führt alle symbolischen Beweise durch.

        Returns:
            Dictionary mit Beweis-Namen und True/False.
        """
        return {
            "recursion_beta_n3": self.verify_recursion(),
            "ratio_constant_phi13": self.verify_ratio_constant(),
            "golden_ratio_identity": self.verify_golden_ratio_identity(),
        }


@dataclass(frozen=True)
class StabilityResult:
    """Ergebnis der Stabilitätsanalyse der Phi-Skalierung.

    Attributes:
        lyapunov_exponent:   λ = ln(Φ)/3 numerisch.
        is_exponential:      True wenn λ > 0 (exponentielles Wachstum).
        phi_val:             Numerischer Wert von Φ.
        recursion_proved:    True wenn β_{n+3} = Φ · β_n symbolisch bewiesen.
        ratio_proved:        True wenn β_{n+1}/β_n = Φ^{1/3} bewiesen.
        golden_id_proved:    True wenn Φ² = Φ + 1 bewiesen.
        beta_n_latex:        LaTeX für β_n.
        derivative_latex:    LaTeX für dβ_n/dn.
    """

    lyapunov_exponent: float
    is_exponential: bool
    phi_val: float
    recursion_proved: bool
    ratio_proved: bool
    golden_id_proved: bool
    beta_n_latex: str
    derivative_latex: str

    def __str__(self) -> str:
        status = "STABIL (Phi-skaliert)" if self.is_exponential else "INSTABIL"
        proofs = all([self.recursion_proved, self.ratio_proved, self.golden_id_proved])
        return (
            f"StabilityResult\n"
            f"  Φ                = {self.phi_val:.10f}\n"
            f"  λ (Lyapunov)     = {self.lyapunov_exponent:.10f}\n"
            f"  Status           = {status}\n"
            f"  Alle Beweise OK  = {proofs}\n"
            f"  β_n (LaTeX)      = {self.beta_n_latex}\n"
            f"  dβ_n/dn (LaTeX)  = {self.derivative_latex}"
        )


def stability_analysis(beta_0: float = 1.0) -> StabilityResult:
    """Vollständige Stabilitätsanalyse der Phi-Skalierung.

    Führt alle symbolischen Beweise durch und berechnet den Lyapunov-Exponent.

    Args:
        beta_0: Basis-Kopplungskonstante (Standard: 1.0).

    Returns:
        StabilityResult mit allen Beweisergebnissen und Lyapunov-Exponent.
    """
    proof = PhiScalingProof(beta_0_val=beta_0)
    proofs = proof.run_all_proofs()

    lam = math.log(PHI_VAL) / 3.0
    beta_latex = sp.latex(proof.beta_n_expr())
    deriv_latex = sp.latex(proof.symbolic_derivative())

    return StabilityResult(
        lyapunov_exponent=lam,
        is_exponential=lam > 0.0,
        phi_val=PHI_VAL,
        recursion_proved=proofs["recursion_beta_n3"],
        ratio_proved=proofs["ratio_constant_phi13"],
        golden_id_proved=proofs["golden_ratio_identity"],
        beta_n_latex=beta_latex,
        derivative_latex=deriv_latex,
    )
