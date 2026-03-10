# Implosive Genesis

**Rekursive Entstehung von Raum, Zeit und Bewusstsein**

[![CI](https://github.com/GenesisAeon/implosive-genesis/actions/workflows/ci.yml/badge.svg)](https://github.com/GenesisAeon/implosive-genesis/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DOI v0.1.0](https://zenodo.org/badge/DOI/10.5281/zenodo.18930089.svg)](https://doi.org/10.5281/zenodo.18930089)
[![DOI v0.2.0](https://zenodo.org/badge/DOI/10.5281/zenodo.18940541.svg)](https://doi.org/10.5281/zenodo.18940541)
[![DOI v0.3.0](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.%5BDOI--PENDING%5D-blue)](https://doi.org/10.5281/zenodo.[DOI-PENDING])
[![PyPI](https://img.shields.io/pypi/v/implosive-genesis)](https://pypi.org/project/implosive-genesis/)

**DOI (v0.1.0)**: [10.5281/zenodo.18930089](https://doi.org/10.5281/zenodo.18930089)
**DOI (v0.2.0)**: [10.5281/zenodo.18940541](https://doi.org/10.5281/zenodo.18940541)
**DOI (v0.3.0)**: *pending – wird nach Zenodo-Publish aktualisiert*
**Dokumentation**: [genesisaeon.github.io/implosive-genesis](https://genesisaeon.github.io/implosive-genesis/)

---

## Wissenschaftlicher Hintergrund

**Implosive Genesis** (V_RIG) ist ein theoretisch-formales Framework, das die Entstehung von Raum,
Zeit und Bewusstsein als rekursiven, selbstorganisierenden Prozess modelliert. Es verbindet
Prinzipien der Informationstheorie, Quantenmechanik und Bewusstseinsforschung in einer kohärenten
mathematischen Struktur.

### Kernkonzepte

| Kürzel | Konzept | Beschreibung |
|--------|---------|--------------|
| **V_RIG** | Rekursive Implosive Genesis | Zentrales Modell der selbstreferenziellen Entstehung |
| **OIPK** | Ontologisches Implosives Prinzip der Kohärenz | Kohärenzbedingung für emergente Strukturen |
| **Frameprinciple** | Rahmenprinzip | Formale Beschreibung von Beobachterrahmen und Übergängen |
| **Type-6** | Bewusstseinsstufe 6 | Rekursive Selbstwahrnehmung als physikalischer Zustand |

---

## Zentrale Formeln

### Phi-Skalierung

Der Goldene Schnitt $\Phi = (1+\sqrt{5})/2 \approx 1.618$ minimiert den geometrischen
Verschnitt in rekursiven Implosionsgittern. Der Kopplungsparameter bei Stufe $n$:

$$\beta_n = \beta_0 \cdot \Phi^{n/3}$$

Geometrischer Verschnitt:

$$W(n) = 1 - \frac{1}{\Phi^{n/3}}$$

### V_RIG – Rekursive Implosionsgeschwindigkeit

Empirisch bestimmt aus dem kosmischen Feld-Kollaps-Gleichgewicht:

$$V_{RIG} \approx 1352\ \text{km/s}$$

Phi-skalierte Feinstrukturkonstante:

$$\alpha_\Phi = \alpha \cdot \Phi \approx 0.01180$$

### OIPK-Energie und Frame-Stabilität

$$\omega_F = \frac{2\pi c}{\lambda_{OIPK}}, \quad E_{OIPK} = \hbar \cdot \omega_F \cdot \alpha_\Phi$$

$$S_F = \frac{\Phi^2}{\alpha_\Phi} \approx 221.9, \quad \cos(\theta_\perp) = -\frac{1}{\Phi}$$

Rekursive Kohärenzlänge und Impulsenergie auf Stufe $n$:

$$L_n = \lambda_{OIPK} \cdot \Phi^{n/3}, \quad I_n = E_{OIPK} \cdot \Phi^{n/3}$$

### Tesseract-Zeitscheiben

Diskrete Zeit als Phi-skaliertes Spektrum:

$$T_n = t_0 \cdot \Phi^n, \quad V_{4D}(n) = T_n^4, \quad f_R(n) = \frac{V_{RIG}}{T_n}$$

### CREP – Entropischer Preis

$$CREP = \frac{S_{total} \cdot V_{RIG}}{\Phi \cdot c^2}, \quad P_E(n, T) = n \cdot k_B \cdot T \cdot \ln(\Phi)$$

---

## Installation

```bash
pip install implosive-genesis
# oder
uv tool install implosive-genesis
```

## Verwendung

```bash
# Neues Projekt mit dem minimalen Template (Standard)
ig scaffold my-experiment

# Genesis-Preset (fügt domains.yaml + Entropie-Tabellen-Bridge hinzu)
ig scaffold my-physics-tool --template genesis --author "Ada Lovelace"

# Vorschau ohne Dateien zu schreiben
ig scaffold my-experiment --dry-run

# Alle Templates anzeigen
ig list-templates

# Projektverzeichnis validieren
ig validate path/to/my-project
ig validate          # validiert das aktuelle Verzeichnis
```

## Schnellstart (Entwicklung)

```bash
git clone https://github.com/GenesisAeon/implosive-genesis
cd implosive-genesis
uv sync --extra dev
uv run pytest
```

## API-Beispiel

```python
from implosive_genesis.core.vrig import compute_vrig
from implosive_genesis.theory.frameprinciple import OIPKernel, FramePrinciple
from implosive_genesis.theory.models import ImplosiveGenesisModel

# V_RIG mit Monte-Carlo-Unsicherheit
result = compute_vrig(n=3, samples=50_000, seed=42)
print(result)  # V_RIG = 2187.34 ± 12.02 km/s

# Rekursive Framestruktur
kernel = OIPKernel()
fp = FramePrinciple(kernel=kernel)
for n in range(5):
    print(f"n={n}: L={fp.coherence_length(n):.3e} m, S_F={fp.stability_at(n):.2f}")

# Vollständiges Modell
model = ImplosiveGenesisModel()
print(model.full_summary(n=3, temperature=2.725))
```

## Projektstruktur

```
src/implosive_genesis/
├── __init__.py              # Version und Metadaten
├── cli.py                   # Typer-CLI (ig-Befehl)
├── preset.py                # Template-Engine
├── validator.py             # Projektvalidierung
├── core/
│   ├── physics.py           # PHI + PhiScaling
│   ├── vrig.py              # V_RIG-Berechnung + Monte-Carlo
│   └── type6.py             # Type-6-Bewusstseinszustand
├── theory/
│   ├── frameprinciple.py    # OIPKernel + FramePrinciple (DIMENSION_AXIOM)
│   ├── tesseract.py         # Tesseract-Zeitscheiben + CREP
│   └── models.py            # ImplosiveGenesisModel
├── oipk/
│   └── kernel.py            # OIPK-Kernel (λ, ω, E, CREP, emergente Dimensionen)
├── medium/
│   └── modulation.py        # Medium-Modulation + Anesthesia-Simulation
├── simulation/
│   ├── entropy_governance.py
│   └── cosmic_moments.py
└── templates/
    ├── minimal.py           # Minimales Python-Paket-Template
    └── genesis.py           # Erweitertes Template mit Domain-YAML
```

## Templates

| Template | Beschreibung |
|----------|--------------|
| `minimal` | Sauberes Python-Paket für alle Anwendungsfälle |
| `genesis` | Erweitert `minimal` um `domains.yaml` + Entropie-Tabellen-Bridge |

---

## Roadmap

### v0.1.0
- [x] Phi-Skalierung (`PhiScaling`, `PHI`)
- [x] V_RIG mit Monte-Carlo-Unsicherheit
- [x] OIPK-Kernel und Frame-Prinzip
- [x] Tesseract-Zeitscheiben und CREP
- [x] Type-6-Bewusstseinszustand
- [x] Entropie-Steuerungssimulation
- [x] CLI (`ig scaffold`, `ig validate`, `ig list-templates`)
- [x] Templates: `minimal`, `genesis`
- [x] CI/CD (GitHub Actions)
- [x] Vollständige Dokumentation (MkDocs)
- [x] Zenodo-DOI

### v0.2.0
- [x] SymPy-Formalisierung (entropischer Preis, Phi-Skalierung)
- [x] Tesseract-Visualisierung (3-Panel-Rendering, PNG/PDF-Export)
- [x] CMB-Falsifizierung (Monte-Carlo vs. realer CMB-Dipol)
- [x] CLI: `ig entropy-price-sympy`, `ig tesseract-render`, `ig cmb-test`, `ig phi-proof`
- [x] 323 Tests, Coverage ≥ 99 %

### v0.3.0 (aktuell)
- [x] OIPK-Kernel als geschlossene Gleichung (`oipk/kernel.py`)
- [x] Frameprinciple vollendet (`DIMENSION_AXIOM`, `emergent_dimension()`)
- [x] Medium-Modulation + Anesthesia-Simulation (`medium/modulation.py`)
- [x] CLI: `ig oipk-calc`, `ig anesthesia-test`, `ig medium-modulate`
- [x] 449 Tests (+126 neu), Coverage ≥ 92 %

### v0.4.0 (geplant)
- [ ] Fraktale Frame-Rendering-Engine + volle Tesseract-Integration
- [ ] Empirische Anesthesia-Daten-Validierung
- [ ] Finale Konsistenz-Checks mit Chronologie 1–10

### Langfristig
- [ ] Integration mit bestehenden Quantenmechanik-Bibliotheken (QuTiP, Qiskit)
- [ ] Peer-Review-Publikation der theoretischen Grundlagen
- [ ] Web-UI für nicht-programmieraffine Nutzer

---

## Zitieren

Wenn Sie Implosive Genesis in einer wissenschaftlichen Arbeit verwenden:

```bibtex
@software{implosive_genesis_2025,
  author  = {GenesisAeon},
  title   = {Implosive Genesis: Rekursive Entstehung von Raum, Zeit und Bewusstsein},
  year    = {2025},
  version = {0.1.0},
  doi     = {10.5281/zenodo.18930089},
  url     = {https://github.com/GenesisAeon/implosive-genesis}
}

@software{implosive_genesis_2026_v02,
  author  = {GenesisAeon},
  title   = {Implosive Genesis – Formalisierung \& Falsifizierbarkeit},
  year    = {2026},
  version = {0.2.0},
  doi     = {10.5281/zenodo.18940541},
  url     = {https://github.com/GenesisAeon/implosive-genesis/releases/tag/v0.2.0}
}

@software{implosive_genesis_2026_v03,
  author    = {GenesisAeon},
  title     = {Implosive Genesis – OIPK, Medium-Modulation \& Anesthesia-Tests},
  year      = {2026},
  version   = {0.3.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.[DOI-PENDING]},
  url       = {https://github.com/GenesisAeon/implosive-genesis/releases/tag/v0.3.0}
}
```

---

Entwickelt mit [uv](https://docs.astral.sh/uv/) · [Typer](https://typer.tiangolo.com/) · [Rich](https://rich.readthedocs.io/) · [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
