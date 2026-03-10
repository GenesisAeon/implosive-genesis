# Release Notes – v0.3.0

## v0.3.0 – OIPK, Medium-Modulation & Anesthesia-Tests

**Dritte stabile Version** – Frameprinciple jetzt vollständig implementiert, OIPK als geschlossene
Gleichung, Medium-Modulation und erste Anesthesia-Frame-Buffer-Simulationen. Das Modell ist nun
vollständig falsifizierbar auf Bewusstseins-Ebene.

---

### Kern-Neuerungen

#### Orthogonal Impulse Photon Kernel (OIPK)

Geschlossene Gleichung:

```
CREP = w_buffer / (w_buffer + P_info),  τ ⊥ t
```

Berechnete Größen: `λ_OIPK`, `ω`, `E_OIPK`, `S_F` + emergente Dimensionen `D_n`

Beispiel-Ausgabe (`ig oipk-calc`):

```
λ_OIPK   2.217408e+02  m
E_OIPK   9.483e-32     J
CREP     3.503e-38     kg·m/s
τ ⊥ t    True
n=5      I_n=1.241e-31 D_n=1 emergent
```

#### Frameprinciple vollendet

```python
DIMENSION_AXIOM = "A dimension emerges when information would otherwise collapse."
```

Neue Funktionen: `emergent_dimension()`, `dimension_series()` mit exakter OIPK-Integration.

#### Medium-Modulation & Anesthesia-Tests

Frame-Buffer-Simulation bei Bewusstseinsverlust – Bewusst-Anteil, R_loss, R_rec, Anesthesia-Ereignisse.

Beispiel-Ausgabe (`ig anesthesia-test --duration 300`):

```
Anesthesia-Ereignisse: 1
Bewusst-Anteil : 0.7367  (73.7%)
R_loss         : 0.9179
R_rec          : 0.2176
```

---

### Neue CLI-Befehle

```bash
ig oipk-calc [--lambda 500 --tau]
ig anesthesia-test --duration 300 [--timeline]
ig medium-modulate --t-max 240
```

---

### Tests & Qualität

- **449 Tests** (+126 gegenüber v0.2.0)
- Coverage ≥ 92 %
- ruff + pre-commit 100 % clean

---

### Installation & Test

```bash
git checkout main
git pull
uv sync --extra dev
uv run ig oipk-calc
uv run ig anesthesia-test --duration 300
```

---

### Zitieren

```bibtex
@software{implosive-genesis-v0.3.0,
  author    = {GenesisAeon},
  title     = {Implosive Genesis – OIPK, Medium-Modulation & Anesthesia-Tests},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.[DOI-PENDING]},
  url       = {https://github.com/GenesisAeon/implosive-genesis/releases/tag/v0.3.0}
}
```

> DOI wird nach Zenodo-Publish aktualisiert.

---

### Nächste Schritte (v0.4.0)

- Fraktale Frame-Rendering-Engine + volle Tesseract-Integration
- Empirische Anesthesia-Daten-Validierung
- Finale Konsistenz-Checks mit Chronologie 1–10

---

Aufgebaut auf **v0.2.0** (DOI: [10.5281/zenodo.18940541](https://doi.org/10.5281/zenodo.18940541))
