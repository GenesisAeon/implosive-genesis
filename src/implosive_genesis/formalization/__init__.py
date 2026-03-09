"""Implosive Genesis – Formalisierungs-Paket (v0.2.0).

Enthält SymPy-basierte Formalisierungen der Kerntheoreme:
    - entropic_price: Symbolische Ableitung und numerische Integration des entropischen Preises
    - phi_scaling:    Exakter Beweis für β_n = β_0 · Φ^{n/3} + Stabilitätsanalyse
"""

from __future__ import annotations

from .entropic_price import EntropicPriceDerivation, integrate_entropic_price
from .phi_scaling import PhiScalingProof, stability_analysis

__all__ = [
    "EntropicPriceDerivation",
    "integrate_entropic_price",
    "PhiScalingProof",
    "stability_analysis",
]
