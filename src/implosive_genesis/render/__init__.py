"""Fraktale Frame-Rendering-Engine – rekursive Phi-skalierte Visualisierung.

Dieses Paket enthält die Rendering-Infrastruktur für das Implosive-Genesis-Framework:
  - FractalTesseract: Rekursive Phi-Skalierungs-Rendering-Engine
  - ASCII-Animation und SVG/PNG-Export
"""

from .fractal_tesseract import FractalFrame, FractalTesseract, RenderResult

__all__ = ["FractalFrame", "FractalTesseract", "RenderResult"]
