"""Implosive Genesis – Simulation-Paket.

Enthält Simulationsmodule für kosmische Momente, Entropie-Governance,
Tesseract-Visualisierung und CMB-Falsifikation.

Enthaltene Module:
    - cosmic_moments:     Phi-skalierte Zeitevolution der Implosiven Genesis
    - entropy_governance: Entropie-Steuerung im Tesseract-Physik-Rahmen
    - tesseract_render:   Matplotlib-Visualisierung von Tesseract-Zeitscheiben (v0.2.0)
    - cmb_falsification:  Monte-Carlo-Falsifikationstest gegen CMB-Dipol (v0.2.0)
"""

from __future__ import annotations

from .cmb_falsification import CMBFalsificationTest, CMBTestResult, run_cmb_test
from .cosmic_moments import CosmicMoment, CosmicMomentsSimulator
from .entropy_governance import EntropyBudget, EntropyGovernance, GovernanceReport
from .tesseract_render import TesseractFrameData, TesseractRenderer, render_tesseract

__all__ = [
    "CMBFalsificationTest",
    "CMBTestResult",
    "CosmicMoment",
    "CosmicMomentsSimulator",
    "EntropyBudget",
    "EntropyGovernance",
    "GovernanceReport",
    "TesseractFrameData",
    "TesseractRenderer",
    "render_tesseract",
    "run_cmb_test",
]
