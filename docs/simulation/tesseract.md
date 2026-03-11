# Tesseract Visualisation (v0.2.0)

The **Tesseract Visualisation** renders the 4-dimensional time structure of the
Implosive Genesis framework as an interactive matplotlib figure with three panels:

1. **CREP Heatmap**: $P_E(n, T)$ over recursion levels $n$ and temperature factors
2. **CREP Bar Chart**: CREP values per level (log-scaled)
3. **Log-Phi Scaling**: $\ln(T_n)$ vs. $\ln(\Phi^{n/3})$

## Core Formulae

$$
T_n = t_0 \cdot \Phi^n \qquad \text{(time slice)}
$$

$$
V_{4D}(n) = T_n^4 = t_0^4 \cdot \Phi^{4n} \qquad \text{(4D volume)}
$$

$$
\text{CREP}(n) = \frac{P_E(n,T) \cdot V_{\text{RIG}}}{\Phi \cdot c^2}
$$

$$
P_E(n, T) = n \cdot k_B \cdot T \cdot \ln(\Phi) \qquad \text{(entropic price)}
$$

## Tesseract Time Slices

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

## Frame-Buffer Concept

Each time slice $T_n$ corresponds to a **frame buffer** in the Tesseract structure.
The CREP heatmap shows how the entropic price scales across different
temperature scales (T/2, T, 2T).

## Python API

```python
from implosive_genesis.simulation.tesseract_render import TesseractRenderer, render_tesseract

# Configure renderer
renderer = TesseractRenderer(n_max=7, temperature=2.725)

# ASCII preview (no matplotlib required)
print(renderer.ascii_preview())

# Render figure
fig = renderer.render()

# Save as PNG (300 DPI)
renderer.dpi = 300
saved = renderer.save("tesseract_output.png")
print(f"Saved: {saved}")

# Convenience function
data = render_tesseract(n_max=7, save_path="tesseract.png")
print(data.time_slices)
```

## CLI Usage

```bash
# ASCII preview (fast, no matplotlib)
ig tesseract-render --ascii

# Save as PNG
ig tesseract-render --save png

# Save as PDF with custom n_max
ig tesseract-render --save tesseract.pdf --n-max 10

# Specify a custom file path
ig tesseract-render --save /tmp/my_tesseract.png
```

### Example Output (`--ascii`)

```
╭─────────────────────────────────────────────────────────────────╮
│ Tesseract Visualisation  (n_max=7, T=2.725 K, Φ=1.618034)      │
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

Tip: Use --save png to save the visualisation.
```

## CMB Falsification

```bash
# Default test (5000 simulations)
ig cmb-test

# With reproducibility seed
ig cmb-test --n-sim 5000 --seed 42

# Stricter significance level
ig cmb-test --alpha 0.01 --n-sim 10000
```

### Example Output (`ig cmb-test`)

```
╭─────────────────────────────────────────────────────────────────────╮
│ CMB Falsification Test  (n_sim=5,000, V_RIG=1352.0 km/s,           │
│ v_CMB=369.82 km/s)                                                   │
╰─────────────────────────────────────────────────────────────────────╯

  Parameter             Value        Unit / Info
  V_RIG (model)         1352.00      km/s
  v_CMB (Planck 2018)    369.82      km/s
  E[v] under model       676.00      km/s (V_RIG/2)
  μ_MC (mean)            675.83      km/s
  σ_MC                   390.41      km/s
  |μ - v_CMB|            306.01      km/s (0.78σ)
  n_consistent           1247        of 5,000
  tolerance                1.33      km/s (3σ + 1 km/s)
  p-value                0.249400    α = 0.05

Verdict: NOT FALSIFIED (p=0.2494 ≥ α=0.05)
```

## Interpretation

The CMB falsification model assumes that the observed CMB dipole velocity is the
projected component of V_RIG ($v_{\text{obs}} = V_{\text{RIG}} \cdot \cos\theta$,
uniformly distributed angle $\theta$). The p-value indicates what fraction of the
Monte Carlo simulations falls within a tolerance band around $v_{\text{CMB}}$.

A high p-value (≥ α = 0.05) means: the model is **not falsified** at the chosen
significance level – the hypothesis V_RIG ≈ 1352 km/s is consistent with the
CMB dipole.

## References

- Planck Collaboration (2018). *Planck 2018 results I – Overview and the cosmological legacy*.
  A&A 641, A1. arXiv:1807.06205.
- Hinshaw et al. (2009). *Five-Year WMAP Observations: Data Processing and Systematic Effects*.
  ApJS 180, 225.
