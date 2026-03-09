"""Entropischer Preis – SymPy-Formalisierung und numerische Integration.

Leitet symbolisch den entropischen Preis des Implosiven-Genesis-Rahmens ab:

    E_price = ∫(S_V - S_A) dV  +  k_B · T · ln2 · bits

Wobei:
    S_V   = Volumen-Entropiedichte (SymPy-Symbol)
    S_A   = Areal-Entropiedichte  (SymPy-Symbol, Holographisch)
    k_B   = Boltzmann-Konstante (1.380649e-23 J/K)
    T     = Temperatur in Kelvin
    bits  = Informationsgehalt in Bits

Im Phi-skalierten Rahmen wird S_V - S_A durch den rekursiven Gradienten
approximiert:

    ΔS(n) = k_B · T · ln(Φ^n) = n · k_B · T · ln(Φ)

Die numerische Integration über V ∈ [0, 1] (normiert) ergibt:

    E_price = ∫₀¹ ΔS(n(V)) dV  +  k_B · T · ln2 · bits

Verwendung::

    from implosive_genesis.formalization.entropic_price import (
        EntropicPriceDerivation,
        integrate_entropic_price,
    )
    deriv = EntropicPriceDerivation()
    expr = deriv.symbolic_expression()
    result = integrate_entropic_price(steps=10000)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import sympy as sp

__all__ = ["EntropicPriceDerivation", "EntropicPriceResult", "integrate_entropic_price"]

# ---------------------------------------------------------------------------
# Physikalische Konstanten
# ---------------------------------------------------------------------------

K_B: float = 1.380649e-23
"""Boltzmann-Konstante k_B in J/K."""

PHI_VAL: float = (1.0 + math.sqrt(5.0)) / 2.0
"""Goldener Schnitt Φ ≈ 1.6180339887."""

LN2: float = math.log(2.0)
"""Natürlicher Logarithmus von 2."""


# ---------------------------------------------------------------------------
# SymPy-Symbole
# ---------------------------------------------------------------------------

V, T_sym, n_sym, k_B_sym, Phi_sym, bits_sym = sp.symbols(
    "V T n k_B Phi bits", real=True, positive=True
)


@dataclass
class EntropicPriceDerivation:
    """SymPy-Ableitung des entropischen Preises im Implosiven-Genesis-Rahmen.

    Formalisiert die Gleichung:

        E_price = ∫(S_V - S_A) dV  +  k_B · T · ln2 · bits

    Im Phi-skalierten Rahmen (kontinuierliche Annäherung, n → V auf [0,1]):

        ΔS(V) = k_B · T · ln(Φ) · (n_max · V)

    Attributes:
        n_max_val:    Maximale Rekursionsstufe (für numerische Auswertung).
        temperature:  Temperatur T in Kelvin (Standard: 2.725 K, CMB).
        bits_val:     Informationsgehalt in Bits (Standard: 1.0).
    """

    n_max_val: int = 7
    temperature: float = 2.725
    bits_val: float = 1.0

    # SymPy-Symbole als class-level Attribute
    _phi: sp.Symbol = field(default_factory=lambda: sp.Symbol("Phi", positive=True))
    _k_b: sp.Symbol = field(default_factory=lambda: sp.Symbol("k_B", positive=True))
    _T: sp.Symbol = field(default_factory=lambda: sp.Symbol("T", positive=True))
    _n: sp.Symbol = field(default_factory=lambda: sp.Symbol("n", positive=True))
    _V: sp.Symbol = field(default_factory=lambda: sp.Symbol("V", positive=True))
    _bits: sp.Symbol = field(default_factory=lambda: sp.Symbol("bits", positive=True))

    def delta_s_symbolic(self) -> sp.Expr:
        """Symbolischer Entropiegradient ΔS(V) = k_B · T · ln(Φ) · (n_max · V).

        Approximation für kontinuierliches n(V) = n_max · V auf [0, 1].

        Returns:
            SymPy-Ausdruck für ΔS(V).
        """
        n_max_sym = sp.Symbol("n_max", positive=True)
        return self._k_b * self._T * sp.log(self._phi) * (n_max_sym * self._V)

    def information_term_symbolic(self) -> sp.Expr:
        """Symbolischer Informationsterm: k_B · T · ln(2) · bits.

        Returns:
            SymPy-Ausdruck für den Informationsterm.
        """
        return self._k_b * self._T * sp.log(2) * self._bits

    def symbolic_expression(self) -> sp.Expr:
        """Vollständiger symbolischer Ausdruck für E_price.

        E_price = ∫₀¹ k_B · T · ln(Φ) · (n_max · V) dV  +  k_B · T · ln2 · bits
                = k_B · T · ln(Φ) · n_max / 2  +  k_B · T · ln2 · bits

        Returns:
            SymPy-Ausdruck (symbolisch, nicht ausgewertet).
        """
        n_max_sym = sp.Symbol("n_max", positive=True)
        integrand = self._k_b * self._T * sp.log(self._phi) * n_max_sym * self._V
        integral = sp.integrate(integrand, (self._V, 0, 1))
        info_term = self.information_term_symbolic()
        return sp.simplify(integral + info_term)

    def symbolic_closed_form(self) -> sp.Expr:
        """Geschlossene Form: k_B · T · (ln(Φ) · n_max/2 + ln2 · bits).

        Returns:
            Vereinfachter SymPy-Ausdruck.
        """
        n_max_sym = sp.Symbol("n_max", positive=True)
        return (
            self._k_b
            * self._T
            * (sp.log(self._phi) * n_max_sym / 2 + sp.log(2) * self._bits)
        )

    def numerical_value(self) -> float:
        """Numerisch ausgewerteter entropischer Preis E_price.

        Substituiert: k_B → K_B, T → temperature, Φ → PHI_VAL,
                      n_max → n_max_val, bits → bits_val.

        Returns:
            E_price in Joule.
        """
        n_max_sym = sp.Symbol("n_max", positive=True)
        expr = self.symbolic_closed_form()
        subs = {
            self._k_b: K_B,
            self._T: self.temperature,
            self._phi: PHI_VAL,
            n_max_sym: self.n_max_val,
            self._bits: self.bits_val,
        }
        return float(expr.subs(subs).evalf())

    def latex_expression(self) -> str:
        """LaTeX-Darstellung des symbolischen Ausdrucks.

        Returns:
            LaTeX-String für E_price.
        """
        return sp.latex(self.symbolic_closed_form())

    def prove_linearity_in_T(self) -> bool:
        """Beweis: E_price ist linear in T (symbolisch).

        Prüft, ob d(E_price)/dT = E_price/T (lineare Abhängigkeit).

        Returns:
            True wenn E_price linear in T ist.
        """
        n_max_sym = sp.Symbol("n_max", positive=True)
        expr = self.symbolic_closed_form()
        deriv = sp.diff(expr, self._T)
        # E_price linear in T ↔ deriv = expr/T
        ratio = sp.simplify(deriv - expr / self._T)
        return ratio == sp.S.Zero


@dataclass(frozen=True)
class EntropicPriceResult:
    """Ergebnis der numerischen Integration des entropischen Preises.

    Attributes:
        e_price_j:        Gesamter entropischer Preis E_price in Joule.
        integral_part_j:  ∫(S_V - S_A)dV in Joule.
        info_part_j:      k_B · T · ln2 · bits in Joule.
        steps:            Anzahl der Integrations-Schritte.
        temperature_k:    Temperatur in Kelvin.
        n_max:            Maximale Rekursionsstufe.
        bits:             Informationsgehalt in Bits.
        phi:              Verwendeter Wert des Goldenen Schnitts Φ.
    """

    e_price_j: float
    integral_part_j: float
    info_part_j: float
    steps: int
    temperature_k: float
    n_max: int
    bits: float
    phi: float

    def __str__(self) -> str:
        return (
            f"EntropicPriceResult\n"
            f"  E_price        = {self.e_price_j:.6e} J\n"
            f"  ∫(ΔS)dV        = {self.integral_part_j:.6e} J\n"
            f"  k_B·T·ln2·bits = {self.info_part_j:.6e} J\n"
            f"  Steps          = {self.steps:,}\n"
            f"  T              = {self.temperature_k} K\n"
            f"  n_max          = {self.n_max}\n"
            f"  Φ              = {self.phi:.10f}"
        )


def integrate_entropic_price(
    n_max: int = 7,
    temperature: float = 2.725,
    bits: float = 1.0,
    steps: int = 10_000,
) -> EntropicPriceResult:
    """Numerische Integration des entropischen Preises via Riemann-Summe.

    Berechnet:

        ∫₀¹ k_B · T · ln(Φ) · (n_max · V) dV  +  k_B · T · ln2 · bits

    Analytisch: k_B · T · ln(Φ) · n_max / 2  +  k_B · T · ln2 · bits

    Args:
        n_max:       Maximale Rekursionsstufe (Standard: 7).
        temperature: Temperatur T in Kelvin (Standard: 2.725 K).
        bits:        Informationsgehalt in Bits (Standard: 1.0).
        steps:       Anzahl Riemann-Summations-Schritte (Standard: 10 000).

    Returns:
        EntropicPriceResult mit allen Teilbeiträgen.
    """
    dv = 1.0 / steps
    ln_phi = math.log(PHI_VAL)

    # Riemann-Summe: Mittelpunktmethode für ∫₀¹ k_B · T · ln(Φ) · n_max · V dV
    integral_sum = 0.0
    for i in range(steps):
        v_mid = (i + 0.5) * dv
        delta_s = K_B * temperature * ln_phi * (n_max * v_mid)
        integral_sum += delta_s * dv

    # Informationsterm
    info_term = K_B * temperature * LN2 * bits

    total = integral_sum + info_term

    return EntropicPriceResult(
        e_price_j=total,
        integral_part_j=integral_sum,
        info_part_j=info_term,
        steps=steps,
        temperature_k=temperature,
        n_max=n_max,
        bits=bits,
        phi=PHI_VAL,
    )
