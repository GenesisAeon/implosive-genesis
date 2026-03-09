"""Tesseract-Visualisierung – Zeitscheiben-Heatmap und CREP-Render.

Visualisiert die Tesseract-Zeitstruktur des Implosiven-Genesis-Rahmens:
    - Zeitscheiben T_n = t_0 · Φ^n als Heatmap
    - CREP-Werte (Collapse-Resonance-Entropy-Price) pro Stufe
    - Frame-Buffer-Darstellung der 4D-Volumina

Ausgabe:
    - matplotlib-Figure mit 3 Subplots:
        1. Zeitscheiben-Heatmap (n vs. Parameter)
        2. CREP-Balkendiagramm
        3. Log-Phi-Skalierungsübersicht

Verwendung::

    from implosive_genesis.simulation.tesseract_render import TesseractRenderer
    renderer = TesseractRenderer(n_max=7)
    fig = renderer.render()
    renderer.save("tesseract.png")
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from implosive_genesis.core.physics import PHI
from implosive_genesis.core.vrig import V_RIG_KMS
from implosive_genesis.theory.tesseract import CREP, K_BOLTZMANN, Tesseract

matplotlib.use("Agg")  # nicht-interaktives Backend für CLI

__all__ = ["TesseractRenderer", "TesseractFrameData", "render_tesseract"]

_LOG_PHI: float = math.log(PHI)


@dataclass(frozen=True)
class TesseractFrameData:
    """Datenstruktur für einen Tesseract-Frame.

    Attributes:
        n_values:      Array der Rekursionsstufen [0, …, n_max].
        time_slices:   T_n = t_0 · Φ^n für jedes n.
        crep_values:   CREP(P_E(n, T)) für jedes n.
        volumes_4d:    V_4D(n) = T_n^4 für jedes n.
        entropy_prices: P_E(n, T) = n · k_B · T · ln(Φ) für jedes n.
        phi:           Goldener Schnitt Φ.
        temperature_k: Temperatur T in Kelvin.
    """

    n_values: np.ndarray
    time_slices: np.ndarray
    crep_values: np.ndarray
    volumes_4d: np.ndarray
    entropy_prices: np.ndarray
    phi: float
    temperature_k: float


@dataclass
class TesseractRenderer:
    """Matplotlib-Renderer für Tesseract-Zeitscheiben und CREP-Heatmap.

    Erstellt eine 3-Panel-Figure:
        Panel 1: Heatmap der Zeitscheiben T_n (normiert, log-skaliert)
        Panel 2: CREP-Balkendiagramm pro Rekursionsstufe n
        Panel 3: Log-Phi-Skalierung (β_n = Φ^{n/3})

    Attributes:
        n_max:       Maximale Rekursionsstufe (Standard: 7).
        t_0:         Grundzeitscheibe (Standard: 1.0).
        temperature: Temperatur T in Kelvin (Standard: 2.725 K).
        v_rig_kms:   V_RIG in km/s (Standard: V_RIG_KMS).
        figsize:     Figurengröße (Standard: (14, 5)).
        dpi:         DPI für Speicherung (Standard: 150).
    """

    n_max: int = 7
    t_0: float = 1.0
    temperature: float = 2.725
    v_rig_kms: float = V_RIG_KMS
    figsize: tuple[int, int] = field(default_factory=lambda: (14, 5))
    dpi: int = 150

    def _compute_frame_data(self) -> TesseractFrameData:
        """Berechnet alle Frame-Daten für n = 0, …, n_max.

        Returns:
            TesseractFrameData mit allen Observablen.
        """
        tesseract = Tesseract(t_0=self.t_0)
        crep_model = CREP(v_rig_kms=self.v_rig_kms)

        n_arr = np.arange(self.n_max + 1, dtype=float)
        time_slices = np.array([tesseract.time_slice(int(n)) for n in n_arr])
        entropy_prices = np.array(
            [crep_model.entropy_price(int(n), self.temperature) for n in n_arr]
        )
        crep_vals = np.array([crep_model.crep_value(p) for p in entropy_prices])
        volumes = time_slices**4

        return TesseractFrameData(
            n_values=n_arr,
            time_slices=time_slices,
            crep_values=crep_vals,
            volumes_4d=volumes,
            entropy_prices=entropy_prices,
            phi=PHI,
            temperature_k=self.temperature,
        )

    def render(self) -> plt.Figure:
        """Erstellt die Tesseract-Visualisierung.

        Returns:
            matplotlib Figure mit 3 Subplots.
        """
        data = self._compute_frame_data()
        fig, axes = plt.subplots(1, 3, figsize=self.figsize)
        fig.patch.set_facecolor("#0d1117")

        ax_colors = {"bg": "#0d1117", "text": "#c9d1d9", "accent": "#58a6ff"}
        for ax in axes:
            ax.set_facecolor("#161b22")
            ax.tick_params(colors=ax_colors["text"])
            ax.xaxis.label.set_color(ax_colors["text"])
            ax.yaxis.label.set_color(ax_colors["text"])
            ax.title.set_color(ax_colors["text"])
            for spine in ax.spines.values():
                spine.set_edgecolor("#30363d")

        # --- Panel 1: Zeitscheiben-Heatmap ---
        ax1 = axes[0]
        # 2D-Matrix: Zeitscheiben vs. normierte Temperatur (0.5T, T, 2T)
        t_factors = np.array([0.5, 1.0, 2.0])
        heatmap = np.zeros((len(t_factors), self.n_max + 1))
        for i, tf in enumerate(t_factors):
            for j, n in enumerate(data.n_values):
                price = int(n) * K_BOLTZMANN * self.temperature * tf * _LOG_PHI
                heatmap[i, j] = price

        im = ax1.imshow(
            heatmap,
            aspect="auto",
            cmap="plasma",
            origin="lower",
            extent=[-0.5, self.n_max + 0.5, -0.5, 2.5],
        )
        ax1.set_yticks([0, 1, 2])
        ax1.set_yticklabels(["T/2", "T", "2T"], color=ax_colors["text"])
        ax1.set_xticks(range(self.n_max + 1))
        ax1.set_xlabel("Rekursionsstufe n", color=ax_colors["text"])
        ax1.set_title("CREP-Heatmap: P_E(n, T)", color=ax_colors["text"], fontsize=10)
        cbar = fig.colorbar(im, ax=ax1, pad=0.02)
        cbar.ax.yaxis.set_tick_params(color=ax_colors["text"])
        cbar.set_label("P_E [J]", color=ax_colors["text"])

        # --- Panel 2: CREP-Balken ---
        ax2 = axes[1]
        colors_bar = plt.cm.viridis(np.linspace(0.2, 0.9, self.n_max + 1))
        bars = ax2.bar(data.n_values, data.crep_values, color=colors_bar, edgecolor="#30363d")
        ax2.set_xlabel("Rekursionsstufe n", color=ax_colors["text"])
        ax2.set_ylabel("CREP(P_E)", color=ax_colors["text"])
        ax2.set_title("CREP-Werte pro Stufe", color=ax_colors["text"], fontsize=10)
        ax2.set_yscale("symlog", linthresh=1e-50)

        for bar, val in zip(bars, data.crep_values):
            if val > 0:
                ax2.text(
                    bar.get_x() + bar.get_width() / 2,
                    val * 1.1,
                    f"{val:.1e}",
                    ha="center",
                    va="bottom",
                    fontsize=6,
                    color=ax_colors["text"],
                )

        # --- Panel 3: Log-Phi-Skalierung der Zeitscheiben ---
        ax3 = axes[2]
        phi_n3 = PHI ** (data.n_values / 3.0)
        ax3.plot(
            data.n_values,
            np.log(data.time_slices + 1e-100),
            "o-",
            color="#58a6ff",
            label=r"$\ln(T_n)$",
            linewidth=2,
            markersize=6,
        )
        ax3.plot(
            data.n_values,
            np.log(phi_n3),
            "--",
            color="#3fb950",
            label=r"$\ln(\Phi^{n/3})$",
            linewidth=1.5,
            alpha=0.8,
        )
        ax3.set_xlabel("Rekursionsstufe n", color=ax_colors["text"])
        ax3.set_ylabel("ln(·)", color=ax_colors["text"])
        ax3.set_title(r"Log-$\Phi$-Skalierung $T_n$ vs. $\Phi^{n/3}$", color=ax_colors["text"], fontsize=10)
        legend = ax3.legend(facecolor="#161b22", edgecolor="#30363d", labelcolor=ax_colors["text"])

        fig.suptitle(
            f"Implosive Genesis – Tesseract-Visualisierung  "
            f"(n_max={self.n_max}, T={self.temperature} K, "
            f"V_RIG={self.v_rig_kms} km/s, Φ={PHI:.4f})",
            color=ax_colors["text"],
            fontsize=11,
            y=1.02,
        )
        fig.tight_layout()
        return fig

    def save(self, path: str | Path = "tesseract.png") -> Path:
        """Speichert die Visualisierung als Bilddatei.

        Args:
            path: Ausgabepfad (Standard: 'tesseract.png').

        Returns:
            Absoluter Pfad der gespeicherten Datei.
        """
        out = Path(path)
        fig = self.render()
        fig.savefig(out, dpi=self.dpi, bbox_inches="tight", facecolor="#0d1117")
        plt.close(fig)
        return out.resolve()

    def ascii_preview(self) -> str:
        """ASCII-Vorschau der Zeitscheiben-Werte für die CLI.

        Returns:
            Formatierter ASCII-String mit T_n und CREP-Werten.
        """
        data = self._compute_frame_data()
        lines = ["n  │  T_n          │  P_E [J]     │  CREP"]
        lines.append("───┼──────────────┼──────────────┼──────────────")
        for i, n in enumerate(data.n_values.astype(int)):
            lines.append(
                f"{n:2d} │ {data.time_slices[i]:12.4e} │ "
                f"{data.entropy_prices[i]:12.4e} │ "
                f"{data.crep_values[i]:12.4e}"
            )
        return "\n".join(lines)


def render_tesseract(
    n_max: int = 7,
    temperature: float = 2.725,
    save_path: str | Path | None = None,
) -> TesseractFrameData:
    """Convenience-Funktion: Rendert und speichert optional die Tesseract-Visualisierung.

    Args:
        n_max:      Maximale Rekursionsstufe.
        temperature: Temperatur T in Kelvin.
        save_path:  Pfad zum Speichern (None = nicht speichern).

    Returns:
        TesseractFrameData der berechneten Observablen.
    """
    renderer = TesseractRenderer(n_max=n_max, temperature=temperature)
    if save_path is not None:
        renderer.save(save_path)
    return renderer._compute_frame_data()
