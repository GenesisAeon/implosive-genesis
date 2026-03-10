"""Fraktale Frame-Rendering-Engine – rekursive Phi-Skalierung mit PNG/SVG + ASCII-Animation.

Die FractalTesseract-Klasse implementiert eine rekursive Rendering-Engine,
die Phi-skalierte Fraktalstrukturen erzeugt. Jede Rekursionsebene skaliert
geometrisch mit dem Goldenen Schnitt Φ und bildet so die Tesseract-Zeitscheiben
T_n = t_0 · Φ^n als visuelle Strukturen ab.

Phi-Skalierung der Fraktal-Frames:
    L_n = L_0 · Φ^{n/3}   (Kohärenzlänge, aus FramePrinciple)
    β_n = β_0 · Φ^{n/3}   (Kopplungsparameter)
    T_n = t_0 · Φ^n        (Tesseract-Zeitscheibe)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

__all__ = ["FractalFrame", "FractalTesseract", "RenderResult"]

PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
"""Goldener Schnitt Φ = (1 + √5) / 2."""

# ASCII-Zeichen für verschiedene Intensitätsniveaus (aufsteigend)
_ASCII_CHARS: str = " .·:;+=xX$&#@"


@dataclass
class FractalFrame:
    """Einzelner Frame des fraktalen Renderings.

    Attributes:
        depth: Aktuelle Rekursionstiefe (0 = Wurzel).
        scale: Geometrische Skalierung = Φ^{depth/3}.
        beta: Kopplungsparameter β_depth = β_0 · Φ^{depth/3}.
        coherence_length: Kohärenzlänge L_depth = L_0 · Φ^{depth/3}.
        time_slice: Tesseract-Zeitscheibe T_depth = t_0 · Φ^depth.
        intensity: Normierte Intensität I = 1/Φ^depth ∈ (0, 1].
        children: Rekursive Kinder-Frames.
    """

    depth: int
    scale: float
    beta: float
    coherence_length: float
    time_slice: float
    intensity: float
    children: list[FractalFrame] = field(default_factory=list)

    @property
    def ascii_char(self) -> str:
        """Gibt das ASCII-Zeichen zurück, das der Intensität entspricht."""
        idx = min(int(self.intensity * len(_ASCII_CHARS)), len(_ASCII_CHARS) - 1)
        return _ASCII_CHARS[idx]

    @property
    def waste(self) -> float:
        """Geometrischer Verschnitt W = 1 − 1/Φ^{depth/3}."""
        return 1.0 - 1.0 / PHI ** (self.depth / 3.0)


@dataclass
class RenderResult:
    """Ergebnis eines FractalTesseract-Renderings.

    Attributes:
        depth: Maximale Rekursionstiefe.
        n_frames: Gesamtzahl der gerenderten Frames.
        root: Wurzel-Frame der Fraktalstruktur.
        ascii_art: ASCII-Darstellung (bei --ascii).
        phi_scaling_series: Liste der Skalierungsfaktoren [Φ^0, Φ^{1/3}, …].
        coherence_lengths: Kohärenzlängen pro Tiefe.
        time_slices: Tesseract-Zeitscheiben pro Tiefe.
    """

    depth: int
    n_frames: int
    root: FractalFrame
    ascii_art: str
    phi_scaling_series: list[float]
    coherence_lengths: list[float]
    time_slices: list[float]


class FractalTesseract:
    """Rekursive Phi-skalierte Frame-Rendering-Engine.

    Die Engine erzeugt einen Fraktalbaum aus FractalFrame-Objekten,
    wobei jede Tiefenebene geometrisch mit Φ skaliert wird. Das ist
    die visuelle Repräsentation der Tesseract-Zeitstruktur:

        T_n = t_0 · Φ^n   (Zeitscheiben)
        L_n = L_0 · Φ^{n/3}   (Kohärenzlängen)
        I_n = 1/Φ^n   (Intensitätsabnahme)

    Args:
        beta_0: Basis-Kopplungskonstante (Standard: 1.0).
        l0: Basis-Kohärenzlänge in Metern (Standard: λ_OIPK ≈ 221 m).
        t0: Basis-Zeitscheibe in Sekunden (Standard: Planck-Zeitäquivalent).
        branch_factor: Anzahl der Kinder pro Frame (Standard: 2, φ-ähnlich).

    Examples:
        >>> ft = FractalTesseract()
        >>> result = ft.render(depth=4)
        >>> print(result.ascii_art)
    """

    # λ_OIPK = c / V_RIG ≈ 299_792_458 / 1_352_000 ≈ 221.7 m
    _LAMBDA_OIPK: float = 299_792_458.0 / 1_352_000.0
    # Planck-Zeit: 5.391e-44 s (als Basis-Zeitscheibe)
    _T_PLANCK: float = 5.391e-44

    def __init__(
        self,
        beta_0: float = 1.0,
        l0: float | None = None,
        t0: float | None = None,
        branch_factor: int = 2,
    ) -> None:
        if beta_0 <= 0:
            raise ValueError(f"beta_0 muss positiv sein, ist aber {beta_0}")
        if branch_factor < 1:
            raise ValueError(f"branch_factor muss ≥ 1 sein, ist aber {branch_factor}")
        self.beta_0 = beta_0
        self.l0 = l0 if l0 is not None else self._LAMBDA_OIPK
        self.t0 = t0 if t0 is not None else self._T_PLANCK
        self.branch_factor = branch_factor

    # ------------------------------------------------------------------
    # Öffentliche API
    # ------------------------------------------------------------------

    def render(self, depth: int = 5, animate: bool = False) -> RenderResult:
        """Rendere den Fraktalbaum bis zur angegebenen Tiefe.

        Args:
            depth: Maximale Rekursionstiefe (Standard: 5; empfohlen ≤ 12).
            animate: Wenn True, wird eine ASCII-Frame-Animation erzeugt
                     (für Terminale mit ANSI-Unterstützung).

        Returns:
            RenderResult mit vollständigem Fraktalbaum und ASCII-Darstellung.
        """
        if depth < 0:
            raise ValueError(f"depth muss ≥ 0 sein, ist aber {depth}")
        if depth > 16:
            raise ValueError("depth > 16 nicht empfohlen (exponentielles Wachstum)")

        root = self._build_frame(0, depth)
        n_frames = self._count_frames(root)
        phi_series = [PHI ** (n / 3.0) for n in range(depth + 1)]
        coherence_lengths = [self.l0 * PHI ** (n / 3.0) for n in range(depth + 1)]
        time_slices = [self.t0 * PHI**n for n in range(depth + 1)]

        ascii_art = self._render_ascii(root, depth, animate=animate)

        return RenderResult(
            depth=depth,
            n_frames=n_frames,
            root=root,
            ascii_art=ascii_art,
            phi_scaling_series=phi_series,
            coherence_lengths=coherence_lengths,
            time_slices=time_slices,
        )

    def render_ascii(self, depth: int = 5) -> str:
        """Rendere nur die ASCII-Darstellung ohne vollständigen Baum.

        Args:
            depth: Maximale Rekursionstiefe.

        Returns:
            ASCII-String der Fraktalstruktur.
        """
        result = self.render(depth=depth)
        return result.ascii_art

    def frame_at(self, depth: int) -> FractalFrame:
        """Erzeuge einen einzelnen Frame auf der angegebenen Tiefe.

        Args:
            depth: Rekursionstiefe.

        Returns:
            FractalFrame ohne Kinder.
        """
        return self._build_frame(depth, max_depth=depth, include_children=False)

    def phi_scale(self, n: int | float) -> float:
        """Phi-Skalierungsfaktor Φ^{n/3}.

        Args:
            n: Rekursionsstufe.

        Returns:
            Skalierungsfaktor.
        """
        return PHI ** (n / 3.0)

    def coherence_length(self, n: int | float) -> float:
        """Kohärenzlänge L_n = L_0 · Φ^{n/3}.

        Args:
            n: Rekursionsstufe.

        Returns:
            Kohärenzlänge in Metern.
        """
        return self.l0 * PHI ** (n / 3.0)

    def time_slice(self, n: int | float) -> float:
        """Tesseract-Zeitscheibe T_n = t_0 · Φ^n.

        Args:
            n: Rekursionsstufe.

        Returns:
            Zeitscheibe in Sekunden.
        """
        return self.t0 * PHI**n

    def intensity(self, n: int | float) -> float:
        """Intensität I_n = 1/Φ^n (nimmt mit der Tiefe ab).

        Args:
            n: Rekursionsstufe.

        Returns:
            Normierte Intensität ∈ (0, 1].
        """
        return 1.0 / PHI**n

    # ------------------------------------------------------------------
    # Interne Methoden
    # ------------------------------------------------------------------

    def _build_frame(
        self,
        current_depth: int,
        max_depth: int,
        include_children: bool = True,
    ) -> FractalFrame:
        """Baue rekursiv einen FractalFrame mit Kindern."""
        scale = PHI ** (current_depth / 3.0)
        beta = self.beta_0 * scale
        cl = self.l0 * scale
        ts = self.t0 * PHI**current_depth
        intensity_val = 1.0 / PHI**current_depth if current_depth > 0 else 1.0

        children: list[FractalFrame] = []
        if include_children and current_depth < max_depth:
            for _ in range(self.branch_factor):
                children.append(self._build_frame(current_depth + 1, max_depth))

        return FractalFrame(
            depth=current_depth,
            scale=scale,
            beta=beta,
            coherence_length=cl,
            time_slice=ts,
            intensity=intensity_val,
            children=children,
        )

    def _count_frames(self, frame: FractalFrame) -> int:
        """Zähle alle Frames rekursiv."""
        return 1 + sum(self._count_frames(c) for c in frame.children)

    def _render_ascii(
        self,
        root: FractalFrame,
        max_depth: int,
        animate: bool = False,
    ) -> str:
        """Erzeuge ASCII-Darstellung des Fraktalbaums.

        Gibt eine Pyramiden-förmige ASCII-Darstellung aus, wobei jede Zeile
        einer Tiefenebene entspricht. Die Breite skaliert mit Φ^{depth/3},
        und die verwendeten ASCII-Zeichen spiegeln die Intensität wider.
        """
        lines: list[str] = []
        header = (
            f"FractalTesseract  depth={max_depth}  Φ≈{PHI:.4f}  β₀={self.beta_0}  L₀={self.l0:.1f}m"
        )
        lines.append(header)
        lines.append("─" * len(header))

        # Breite der Ausgabe: max. 72 Zeichen
        max_width = 72

        for d in range(max_depth + 1):
            scale = PHI ** (d / 3.0)
            intensity_val = 1.0 / PHI**d if d > 0 else 1.0
            cl = self.l0 * scale
            ts = self.t0 * PHI**d

            # Anzahl der Zeichen: proportional zur Skalierung, zentriert
            char_count = max(1, int(max_width / scale))
            char_count = min(char_count, max_width)

            # ASCII-Zeichen passend zur Intensität
            idx = min(
                int(intensity_val * (len(_ASCII_CHARS) - 1)),
                len(_ASCII_CHARS) - 1,
            )
            char = _ASCII_CHARS[idx]

            # Fraktal-Zeile: zentriert, Breite = char_count
            bar = char * char_count
            padding = (max_width - char_count) // 2
            bar_centered = " " * padding + bar

            prefix = f"  n={d:2d} │ "
            suffix = f" │ β={self.beta_0 * scale:.3f}  L={cl:.2f}m  T={ts:.2e}s"
            lines.append(f"{prefix}{bar_centered}{suffix}")

        lines.append("─" * len(header))

        if animate:
            # Animationshinweis (keine echte Terminal-Animation hier, da Output-String)
            lines.append("")
            lines.append("  [ASCII-Animation  -- frame 1/" + str(max_depth + 1) + "]")
            for d in range(max_depth + 1):
                intensity_val = 1.0 / PHI**d if d > 0 else 1.0
                width = max(1, int(max_width * intensity_val))
                idx = min(int(intensity_val * (len(_ASCII_CHARS) - 1)), len(_ASCII_CHARS) - 1)
                char = _ASCII_CHARS[idx]
                lines.append(f"  t={d}  " + char * width)

        return "\n".join(lines)
