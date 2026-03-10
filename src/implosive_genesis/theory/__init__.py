"""Theorie-Core – OIPK, Frameprinciple, Tesseract, CREP, Gesamtmodell.

Dieses Paket stellt die theoretischen Kernmodule des Implosive-Genesis-
Rahmens bereit:

- ``frameprinciple``: OIPK-Definition und Frame-Prinzip
- ``tesseract``: Tesseract-Zeitscheiben, CREP und entropischer Preis
- ``models``: Vollständiges Gesamtmodell mit allen Formeln
"""

from implosive_genesis.theory.frameprinciple import (
    C_LIGHT,
    DIMENSION_AXIOM,
    HBAR,
    LAMBDA_OIPK_DEFAULT,
    THETA_ORTHOGONAL,
    EmergentDimensionEntry,
    FramePrinciple,
    OIPKernel,
)
from implosive_genesis.theory.models import FullSummary, ImplosiveGenesisModel
from implosive_genesis.theory.tesseract import (
    C_LIGHT_MS,
    CREP,
    K_BOLTZMANN,
    T0_DEFAULT,
    Tesseract,
)

__all__ = [
    # frameprinciple
    "HBAR",
    "C_LIGHT",
    "LAMBDA_OIPK_DEFAULT",
    "THETA_ORTHOGONAL",
    "DIMENSION_AXIOM",
    "OIPKernel",
    "FramePrinciple",
    "EmergentDimensionEntry",
    # tesseract
    "K_BOLTZMANN",
    "C_LIGHT_MS",
    "T0_DEFAULT",
    "Tesseract",
    "CREP",
    # models
    "FullSummary",
    "ImplosiveGenesisModel",
]
