# v0.2.0 – Formalisierung & Falsifizierbarkeit

**Zweite stabile Version** – jetzt mit exakter mathematischer Formalisierung, SymPy-Ableitungen, visueller Tesseract-Simulation und erster empirischer Falsifizierung gegen den realen CMB-Dipol.

## Kern-Neuerungen in v0.2.0

### SymPy-Formalisierung
- Entropischer Preis exakt abgeleitet:

  $$E_{\rm price} = \int (S_V - S_A)\,dV + k_B T \ln 2 \cdot \text{bits}$$

  (Riemann-Integration + geschlossene Form + Linearitätsbeweis)

- Phi-Skalierung bewiesen:

  $$\beta_{n+3} = \Phi \cdot \beta_n, \quad \frac{\beta_{n+1}}{\beta_n} = \Phi^{1/3}$$

  inkl. Lyapunov-Exponent-Stabilität

### Tesseract-Visualisierung
- 3-Panel-Matplotlib-Rendering (CREP-Heatmap, Balkendiagramm, Log-Φ-Skalierung)
- ASCII-Tabelle + PNG/PDF-Export
- Beispiel-Ausgabe:
  ```
  n  │  T_n          │  P_E [J]     │  CREP
  7 │ 2.9034e+01 │ 1.2673e-22 │ 1.1782e-33
  ```

### CMB-Falsifizierung
- Monte-Carlo-Test: $v_{\rm RIG} = 1352$ km/s vs. realer CMB-Dipol (369,82 km/s)
- p-Wert-Berechnung, σ-Abweichung, Konsistenz-Quote

### Neue CLI-Befehle
```bash
ig entropy-price-sympy --steps 10000
ig tesseract-render --save png
ig cmb-test --n_sim 5000
ig phi-proof
```

### Tests & Qualität
- 323 Tests (89 neu), 99 % Coverage
- ruff + pre-commit 100 % clean

---

## Installation & Test

```bash
git checkout main
git pull
uv sync --extra dev
uv run ig entropy-price-sympy --steps 1000
uv run ig tesseract-render --ascii
```

---

## Zitieren

```bibtex
@software{implosive-genesis-v0.2.0,
  author    = {GenesisAeon},
  title     = {Implosive Genesis – Formalisierung & Falsifizierbarkeit},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.[DEIN-NEUER-DOI-HIER]},
  url       = {https://github.com/GenesisAeon/implosive-genesis/releases/tag/v0.2.0}
}
```

---

## Nächste Schritte (v0.3.0)
- Medium-Modulation & Anesthesia-Tests
- Vollständige OIPK-Quantifizierung
- Fraktale Frame-Rendering-Engine

---

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
*DOI wird nach Zenodo-Upload final gesetzt.*

[Dokumentation](https://genesisaeon.github.io/implosive-genesis/) · [Issues](https://github.com/GenesisAeon/implosive-genesis/issues) · [v0.1.0](https://github.com/GenesisAeon/implosive-genesis/releases/tag/v0.1.0)
