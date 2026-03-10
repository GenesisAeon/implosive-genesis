# Tesseract-Visualisierung (v0.2.0)

Die **Tesseract-Visualisierung** rendert die 4-dimensionale Zeitstruktur des
Implosiven-Genesis-Rahmens als interaktive matplotlib-Figure mit drei Panels:

1. **CREP-Heatmap**: $P_E(n, T)$ über Rekursionsstufen $n$ und Temperaturfaktoren
2. **CREP-Balkendiagramm**: CREP-Werte pro Stufe (log-skaliert)
3. **Log-Phi-Skalierung**: $\ln(T_n)$ vs. $\ln(\Phi^{n/3})$

## Kern-Formeln

$$
T_n = t_0 \cdot \Phi^n \qquad \text{(Zeitscheibe)}
$$

$$
V_{4D}(n) = T_n^4 = t_0^4 \cdot \Phi^{4n} \qquad \text{(4D-Volumen)}
$$

$$
\text{CREP}(n) = \frac{P_E(n,T) \cdot V_{\text{RIG}}}{\Phi \cdot c^2}
$$

$$
P_E(n, T) = n \cdot k_B \cdot T \cdot \ln(\Phi) \qquad \text{(entropischer Preis)}
$$

## Tesseract-Zeitscheiben

| $n$ | $T_n = \Phi^n$ | $V_{4D}(n) = \Phi^{4n}$ |
|-----|----------------|--------------------------|
| 0 | 1.0000 | 1.0000 |
| 1 | 1.6180 | 6.8541 |
| 2 | 2.6180 | 46.979 |
| 3 | 4.2361 | 321.99 |
| 4 | 6.8541 | 2207.0 |
| 5 | 11.090 | 15127 |
| 6 | 17.944 | 103682 |
| 7 | 29.034 | 710647 |

## Frame-Buffer-Konzept

Jede Zeitscheibe $T_n$ entspricht einem **Frame-Buffer** in der Tesseract-Struktur.
Die CREP-Heatmap zeigt, wie der entropische Preis über verschiedene
Temperaturskalen (T/2, T, 2T) skaliert.

## Python-API

```python
from implosive_genesis.simulation.tesseract_render import TesseractRenderer, render_tesseract

# Renderer konfigurieren
renderer = TesseractRenderer(n_max=7, temperature=2.725)

# ASCII-Vorschau (kein matplotlib nötig)
print(renderer.ascii_preview())

# Figure rendern
fig = renderer.render()

# Als PNG speichern (300 DPI)
renderer.dpi = 300
saved = renderer.save("tesseract_output.png")
print(f"Gespeichert: {saved}")

# Convenience-Funktion
data = render_tesseract(n_max=7, save_path="tesseract.png")
print(data.time_slices)
```

## CLI-Nutzung

```bash
# ASCII-Vorschau (schnell, kein matplotlib)
ig tesseract-render --ascii

# PNG speichern
ig tesseract-render --save png

# PDF speichern mit angepasstem n_max
ig tesseract-render --save tesseract.pdf --n-max 10

# Spezifischen Dateipfad angeben
ig tesseract-render --save /tmp/my_tesseract.png
```

### Beispiel-Ausgabe (`--ascii`)

```
╭─────────────────────────────────────────────────────────────────╮
│ Tesseract-Visualisierung  (n_max=7, T=2.725 K, Φ=1.618034)    │
╰─────────────────────────────────────────────────────────────────╯

 n  │  T_n          │  P_E [J]     │  CREP
───┼──────────────┼──────────────┼──────────────
 0 │   1.0000e+00 │   0.0000e+00 │   0.0000e+00
 1 │   1.6180e+00 │   3.5534e-24 │   2.1408e-39
 2 │   2.6180e+00 │   7.1068e-24 │   4.2816e-39
 3 │   4.2361e+00 │   1.0660e-23 │   6.4224e-39
 4 │   6.8541e+00 │   1.4214e-23 │   8.5632e-39
 5 │   1.1090e+01 │   1.7767e-23 │   1.0704e-38
 6 │   1.7944e+01 │   2.1320e-23 │   1.2845e-38
 7 │   2.9034e+01 │   2.4874e-23 │   1.4986e-38

Tipp: Verwende --save png um die Visualisierung zu speichern.
```

## CMB-Falsifikation

```bash
# Standard-Test (5000 Simulationen)
ig cmb-test

# Mit Reproduzierbarkeit
ig cmb-test --n-sim 5000 --seed 42

# Strengeres Signifikanzniveau
ig cmb-test --alpha 0.01 --n-sim 10000
```

### Beispiel-Ausgabe (`ig cmb-test`)

```
╭─────────────────────────────────────────────────────────────────────╮
│ CMB-Falsifikationstest  (n_sim=5,000, V_RIG=1352.0 km/s,          │
│ v_CMB=369.82 km/s)                                                  │
╰─────────────────────────────────────────────────────────────────────╯

  Parameter             Wert         Einheit / Info
  V_RIG (Modell)        1352.00      km/s
  v_CMB (Planck 2018)    369.82      km/s
  E[v] unter Modell      676.00      km/s (V_RIG/2)
  μ_MC (Mittelwert)      675.83      km/s
  σ_MC                   390.41      km/s
  |μ - v_CMB|            306.01      km/s (0.78σ)
  n_konsistent           1247        von 5,000
  Toleranz                 1.33      km/s (3σ + 1 km/s)
  p-Wert                 0.249400    α = 0.05

Urteil: NICHT FALSIFIZIERT (p=0.2494 ≥ α=0.05)
```

## Interpretation

Das CMB-Falsifikationsmodell nimmt an, dass die beobachtete CMB-Dipolgeschwindigkeit
die projizierte Komponente von V_RIG ist ($v_{\text{obs}} = V_{\text{RIG}} \cdot \cos\theta$,
gleichverteilter Winkel $\theta$). Der p-Wert gibt an, welcher Anteil der
Monte-Carlo-Simulationen in einem Toleranzband um $v_{\text{CMB}}$ liegt.

Ein hoher p-Wert (≥ α = 0.05) bedeutet: Das Modell ist **nicht falsifiziert**
auf dem gewählten Signifikanzniveau – die Hypothese V_RIG ≈ 1352 km/s ist
mit dem CMB-Dipol vereinbar.

## Referenzen

- Planck Collaboration (2018). *Planck 2018 results I – Overview and the cosmological legacy*.
  A&A 641, A1. arXiv:1807.06205.
- Hinshaw et al. (2009). *Five-Year WMAP Observations: Data Processing and Systematic Effects*.
  ApJS 180, 225.
