"""V_RIG – Rekursive Implosionsgeschwindigkeit (≈ 1352 km/s).

Kombiniert kosmische Alpha-Phi-Skalierung (cosmic_alpha_phi) mit
Monte-Carlo-Unsicherheitsschätzung für die charakteristische
Implosionsgeschwindigkeit des Feldtheorie-Rahmens.

Referenz: v_RIG ≈ 1352 km/s (empirisch aus Feld-Kollaps-Gleichgewicht).
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

from .physics import PHI

__all__ = [
    "COSMIC_ALPHA",
    "V_RIG_KMS",
    "VRIGResult",
    "cosmic_alpha_phi",
    "compute_vrig",
]

V_RIG_KMS: float = 1352.0
"""Basis-Implosionsgeschwindigkeit in km/s."""

COSMIC_ALPHA: float = 1.0 / 137.035999084
"""Kosmische Feinstrukturkonstante α ≈ 1/137."""


def cosmic_alpha_phi(alpha: float = COSMIC_ALPHA) -> float:
    """Kosmische Feinstrukturkonstante skaliert mit dem Goldenen Schnitt.

    α_Φ = α · Φ

    Args:
        alpha: Feinstrukturkonstante (Standard: COSMIC_ALPHA ≈ 1/137).

    Returns:
        Phi-skalierte Feinstrukturkonstante α_Φ.
    """
    return alpha * PHI


@dataclass(frozen=True)
class VRIGResult:
    """Ergebnis einer V_RIG-Berechnung mit Monte-Carlo-Statistik.

    Attributes:
        v_rig: Mittlere Implosionsgeschwindigkeit [km/s].
        alpha_phi: Phi-skalierte Feinstrukturkonstante α_Φ.
        std_dev: Standardabweichung aus Monte-Carlo-Simulation [km/s].
        samples: Anzahl der Monte-Carlo-Samples.
    """

    v_rig: float
    alpha_phi: float
    std_dev: float
    samples: int

    def __str__(self) -> str:
        return (
            f"V_RIG = {self.v_rig:.4f} ± {self.std_dev:.4f} km/s  "
            f"(α_Φ = {self.alpha_phi:.8f}, n={self.samples})"
        )


def compute_vrig(
    beta_0: float = 1.0,
    n: int = 3,
    samples: int = 10_000,
    noise_sigma: float = 12.0,
    seed: int | None = None,
) -> VRIGResult:
    """Berechne V_RIG mit Phi-Skalierung und Monte-Carlo-Unsicherheit.

    Die Basisgeschwindigkeit wird über den Phi-skalierten Kopplungsparameter
    β_n moduliert:

        v = V_RIG_KMS · β_n

    Dann wird durch Monte-Carlo mit Gaußschem Rauschen (σ = noise_sigma)
    eine statistische Unsicherheitsschätzung durchgeführt.

    Args:
        beta_0: Basis-Kopplungskonstante (Standard: 1.0).
        n: Phi-Skalierungsstufe für β_n (Standard: 3).
        samples: Anzahl Monte-Carlo-Samples (Standard: 10 000).
        noise_sigma: Standardabweichung des Gaußrauschens [km/s] (Standard: 12.0).
        seed: Zufalls-Seed für Reproduzierbarkeit (Standard: None).

    Returns:
        VRIGResult mit v_rig, alpha_phi, std_dev und samples.
    """
    from .physics import PhiScaling

    scaler = PhiScaling(beta_0=beta_0)
    beta = scaler.beta_n(n)
    v_base = V_RIG_KMS * beta

    rng = random.Random(seed)
    mc_samples = [v_base + rng.gauss(0.0, noise_sigma) for _ in range(samples)]

    mean_v = sum(mc_samples) / len(mc_samples)
    variance = sum((x - mean_v) ** 2 for x in mc_samples) / len(mc_samples)
    std_dev = math.sqrt(variance)

    return VRIGResult(
        v_rig=mean_v,
        alpha_phi=cosmic_alpha_phi(),
        std_dev=std_dev,
        samples=samples,
    )
