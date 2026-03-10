# Fraktale Rendering-Engine

**Modul**: `implosive_genesis.render.fractal_tesseract`
**Version**: v0.4.0

---

## Überblick

Die **FractalTesseract**-Klasse implementiert eine rekursive Phi-skalierte Frame-Rendering-Engine.
Jede Tiefenebene skaliert geometrisch mit dem Goldenen Schnitt Φ und bildet so die
Tesseract-Zeitscheiben als visuelle Strukturen ab.

$$\beta_n = \beta_0 \cdot \Phi^{n/3}$$

$$L_n = \lambda_{OIPK} \cdot \Phi^{n/3}$$

$$T_n = t_0 \cdot \Phi^n$$

$$I_n = \frac{1}{\Phi^n}$$

---

## Schnellstart

```python
from implosive_genesis.render.fractal_tesseract import FractalTesseract

ft = FractalTesseract()
result = ft.render(depth=6)
print(result.ascii_art)
```

CLI:

```bash
ig fractal-render --depth 8 --animate
ig fractal-render --depth 6 --ascii
```

---

## API

### `FractalTesseract`

```python
FractalTesseract(
    beta_0: float = 1.0,
    l0: float | None = None,       # Standard: λ_OIPK ≈ 221.7 m
    t0: float | None = None,       # Standard: t_Planck ≈ 5.39e-44 s
    branch_factor: int = 2,
)
```

**Methoden**:

| Methode | Beschreibung |
|---------|-------------|
| `render(depth, animate)` | Vollständiges Rendering → `RenderResult` |
| `render_ascii(depth)` | Nur ASCII-String |
| `frame_at(depth)` | Einzelner `FractalFrame` ohne Kinder |
| `phi_scale(n)` | Φ^{n/3} |
| `coherence_length(n)` | L_n = L_0 · Φ^{n/3} |
| `time_slice(n)` | T_n = t_0 · Φ^n |
| `intensity(n)` | I_n = 1/Φ^n |

### `FractalFrame`

```python
@dataclass
class FractalFrame:
    depth: int
    scale: float
    beta: float
    coherence_length: float
    time_slice: float
    intensity: float
    children: list[FractalFrame]

    @property
    def ascii_char(self) -> str: ...

    @property
    def waste(self) -> float: ...
```

### `RenderResult`

```python
@dataclass
class RenderResult:
    depth: int
    n_frames: int
    root: FractalFrame
    ascii_art: str
    phi_scaling_series: list[float]
    coherence_lengths: list[float]
    time_slices: list[float]
```

---

## Beispiel-ASCII-Ausgabe (`ig fractal-render --depth 5 --ascii`)

```
FractalTesseract  depth=5  Φ≈1.6180  β₀=1.0  L₀=221.7m
────────────────────────────────────────────────────────
  n= 0 │ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ │ β=1.000  L=221.74m  T=5.39e-44s
  n= 1 │ ####################################### │ β=1.173  L=260.18m  T=8.73e-44s
  n= 2 │ ################################ │ β=1.376  L=305.03m  T=1.41e-43s
  n= 3 │ ###################### │ β=1.618  L=358.32m  T=2.29e-43s
  n= 4 │ ############### │ β=1.899  L=420.61m  T=3.70e-43s
  n= 5 │ ########## │ β=2.230  L=493.60m  T=5.99e-43s
────────────────────────────────────────────────────────
```

---

## Phi-Skalierungs-Tabelle

| Tiefe n | Φ^{n/3} | β_n | L_n [m] | I_n |
|---------|---------|-----|---------|-----|
| 0 | 1.0000 | 1.0000 | 221.74 | 1.0000 |
| 1 | 1.1736 | 1.1736 | 260.19 | 0.6180 |
| 2 | 1.3764 | 1.3764 | 305.03 | 0.3820 |
| 3 | 1.6180 | 1.6180 | 358.32 | 0.2361 |
| 4 | 1.8993 | 1.8993 | 420.62 | 0.1459 |
| 5 | 2.2297 | 2.2297 | 494.35 | 0.0902 |
| 6 | 2.6180 | 2.6180 | 580.33 | 0.0557 |
| 7 | 3.0723 | 3.0723 | 681.36 | 0.0344 |
| 8 | 3.6067 | 3.6067 | 799.73 | 0.0213 |

---

## Verbindung zu anderen Modulen

- **`core.physics`**: PHI-Konstante, β_n-Formel
- **`theory.frameprinciple`**: Kohärenzlänge L_n, λ_OIPK
- **`theory.tesseract`**: Zeitscheiben T_n
- **`core.integration`**: ImplosiveGenesis-Klasse (zentraler Zugriff)
- **`chronology.integration`**: Teil 9 der Chronologie
