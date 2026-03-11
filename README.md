# Implosive Genesis

**The Recursive Emergence of Space, Time & Consciousness**
*From informational criticality to fractal frame rendering*

[![CI](https://github.com/GenesisAeon/implosive-genesis/actions/workflows/ci.yml/badge.svg)](https://github.com/GenesisAeon/implosive-genesis/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DOI v0.1.0](https://zenodo.org/badge/DOI/10.5281/zenodo.18930089.svg)](https://doi.org/10.5281/zenodo.18930089)
[![DOI v0.2.0](https://zenodo.org/badge/DOI/10.5281/zenodo.18940541.svg)](https://doi.org/10.5281/zenodo.18940541)
[![DOI v0.3.0](https://zenodo.org/badge/DOI/10.5281/zenodo.18942660.svg)](https://doi.org/10.5281/zenodo.18942660)
[![DOI v0.4.0](https://zenodo.org/badge/DOI/10.5281/zenodo.18956822.svg)](https://doi.org/10.5281/zenodo.18956822)
[![PyPI](https://img.shields.io/pypi/v/implosive-genesis)](https://pypi.org/project/implosive-genesis/)

**DOI (v0.1.0)**: [10.5281/zenodo.18930089](https://doi.org/10.5281/zenodo.18930089)
**DOI (v0.2.0)**: [10.5281/zenodo.18940541](https://doi.org/10.5281/zenodo.18940541)
**DOI (v0.3.0)**: [10.5281/zenodo.18942660](https://doi.org/10.5281/zenodo.18942660)
**DOI (v0.4.0)**: [10.5281/zenodo.18956822](https://doi.org/10.5281/zenodo.18956822)
**Documentation**: [genesisaeon.github.io/implosive-genesis](https://genesisaeon.github.io/implosive-genesis/)

---

## Core Idea

When information density exceeds the critical threshold Θ, dimensions emerge as frame-buffers to
prevent collapse (Frameprinciple). Time arises as the entropic price of the transition
$S \propto A \to S \propto V$.

---

## Scientific Background

**Implosive Genesis** (V_RIG) is a theoretical-formal framework that models the emergence of space,
time, and consciousness as a recursive, self-organising process. It unifies principles from
information theory, quantum mechanics, and consciousness research in a coherent mathematical
structure.

### Key Concepts

| Abbreviation | Concept | Description |
|--------------|---------|-------------|
| **V_RIG** | Recursive Implosive Genesis | Central model of self-referential emergence |
| **OIPK** | Ontological Implosive Principle of Coherence | Coherence condition for emergent structures |
| **Frameprinciple** | Frame Principle | Formal description of observer frames and transitions |
| **Type-6** | Consciousness Level 6 | Recursive self-perception as a physical state |

---

## Core Formulae

### Phi Scaling & Minimal Geometric Waste

The golden ratio $\Phi = (1+\sqrt{5})/2 \approx 1.618$ minimises geometric waste in recursive
implosion lattices. Coupling parameter at level $n$:

$$\beta_n = \beta_0 \cdot \Phi^{n/3}$$

Geometric waste:

$$W(n) = 1 - \frac{1}{\Phi^{n/3}}$$

### V_RIG – Recursive Implosive Velocity

Empirically determined from cosmic field-collapse equilibrium, Monte-Carlo validated against the
CMB dipole:

$$V_{RIG} \approx 1352\ \text{km/s}$$

Phi-scaled fine-structure constant:

$$\alpha_\Phi = \alpha \cdot \Phi \approx 0.01180$$

### OIPK Energy & Frame Stability

$$\omega_F = \frac{2\pi c}{\lambda_{OIPK}}, \quad E_{OIPK} = \hbar \cdot \omega_F \cdot \alpha_\Phi$$

$$S_F = \frac{\Phi^2}{\alpha_\Phi} \approx 221.9, \quad \cos(\theta_\perp) = -\frac{1}{\Phi}$$

Recursive coherence length and impulse energy at level $n$:

$$L_n = \lambda_{OIPK} \cdot \Phi^{n/3}, \quad I_n = E_{OIPK} \cdot \Phi^{n/3}$$

### Tesseract Time-Slices

Discrete time as a Phi-scaled spectrum:

$$T_n = t_0 \cdot \Phi^n, \quad V_{4D}(n) = T_n^4, \quad f_R(n) = \frac{V_{RIG}}{T_n}$$

### CREP – Entropic Price & Time Emergence

$$CREP = \frac{w_{\rm buffer}}{w_{\rm buffer} + P_{\rm info}}, \quad P_E(n, T) = n \cdot k_B \cdot T \cdot \ln(\Phi)$$

Entropic price (SymPy closed form):

$$E_{\rm price} = \int (S_V - S_A)\,dV + k_B T \ln 2 \cdot {\rm bits}$$

---

## What's Implemented (v0.4.0)

- **Phi Scaling & Minimal Geometric Waste** — $\beta_n = \beta_0 \cdot \Phi^{n/3}$
- **Recursive Implosive Velocity** — $v_{\rm RIG} \approx 1352\ \text{km/s}$ (Monte-Carlo validated against CMB dipole)
- **Type-6 Inverted Sigmoid + Cubic Root Jump**
- **Orthogonal Impulse Photon Kernel (OIPK)** — $\tau \perp t$, CREP governance
- **Entropic Price → Time Emergence** — SymPy closed form
- **Tesseract Time-Slices & CREP Governance**
- **Fractal Rendering Engine** (ASCII + PNG/SVG + animation)
- **Full 10-Part Chronology Validator** (100% pass rate)
- **Medium Modulation & Anesthesia Frame-Buffer Tests**

---

## Installation

```bash
pip install implosive-genesis
# or
uv tool install implosive-genesis
```

## Quick Start (Development)

```bash
git clone https://github.com/GenesisAeon/implosive-genesis.git
cd implosive-genesis
uv sync --extra dev
uv run pytest
```

## Key CLI Commands

```bash
# Fractal tesseract visualisation
ig fractal-render --depth 8 --ascii

# Validate 10-part chronology (10/10 check)
ig chronology-validate

# Complete model overview
ig full-summary

# OIPK kernel + emergent dimensions
ig oipk-calc

# Consciousness loss simulation
ig anesthesia-test --duration 300

# Entropic price (SymPy)
ig entropy-price-sympy --steps 10000

# Falsification against real CMB dipole
ig cmb-test --n_sim 5000

# Scaffold a new experiment project
ig scaffold my-experiment

# Scaffold with genesis preset
ig scaffold my-physics-tool --template genesis --author "Ada Lovelace"

# Preview without writing files
ig scaffold my-experiment --dry-run

# List available templates
ig list-templates

# Validate a project directory
ig validate path/to/my-project
ig validate          # validates current directory
```

## API Example

```python
from implosive_genesis.core.vrig import compute_vrig
from implosive_genesis.theory.frameprinciple import OIPKernel, FramePrinciple
from implosive_genesis.theory.models import ImplosiveGenesisModel

# V_RIG with Monte-Carlo uncertainty
result = compute_vrig(n=3, samples=50_000, seed=42)
print(result)  # V_RIG = 2187.34 ± 12.02 km/s

# Recursive frame structure
kernel = OIPKernel()
fp = FramePrinciple(kernel=kernel)
for n in range(5):
    print(f"n={n}: L={fp.coherence_length(n):.3e} m, S_F={fp.stability_at(n):.2f}")

# Full model summary
model = ImplosiveGenesisModel()
print(model.full_summary(n=3, temperature=2.725))
```

## Project Structure

```
src/implosive_genesis/
├── __init__.py              # Version and metadata
├── cli.py                   # Typer CLI (ig command)
├── preset.py                # Template engine
├── validator.py             # Project validation
├── core/
│   ├── physics.py           # PHI + PhiScaling
│   ├── vrig.py              # V_RIG calculation + Monte-Carlo
│   ├── type6.py             # Type-6 consciousness state
│   └── genesis.py           # Central ImplosiveGenesis class
├── theory/
│   ├── frameprinciple.py    # OIPKernel + FramePrinciple (DIMENSION_AXIOM)
│   ├── tesseract.py         # Tesseract time-slices + CREP
│   └── models.py            # ImplosiveGenesisModel
├── oipk/
│   └── kernel.py            # OIPK kernel (λ, ω, E, CREP, emergent dimensions)
├── medium/
│   └── modulation.py        # Medium modulation + anesthesia simulation
├── simulation/
│   ├── entropy_governance.py
│   └── cosmic_moments.py
├── render/
│   └── fractal_tesseract.py # Fractal Phi-scaled rendering engine
├── chronology/              # 10-part chronology validator
└── templates/
    ├── minimal.py           # Minimal Python package template
    └── genesis.py           # Extended template with domain YAML
```

## Templates

| Template | Description |
|----------|-------------|
| `minimal` | Clean Python package for all use cases |
| `genesis` | Extends `minimal` with `domains.yaml` + entropy-table bridge |

---

## Roadmap

### v0.1.0
- [x] Phi scaling (`PhiScaling`, `PHI`)
- [x] V_RIG with Monte-Carlo uncertainty
- [x] OIPK kernel and Frame Principle
- [x] Tesseract time-slices and CREP
- [x] Type-6 consciousness state
- [x] Entropy governance simulation
- [x] CLI (`ig scaffold`, `ig validate`, `ig list-templates`)
- [x] Templates: `minimal`, `genesis`
- [x] CI/CD (GitHub Actions)
- [x] Full documentation (MkDocs)
- [x] Zenodo DOI

### v0.2.0
- [x] SymPy formalisation (entropic price, Phi scaling)
- [x] Tesseract visualisation (3-panel rendering, PNG/PDF export)
- [x] CMB falsification (Monte-Carlo vs. real CMB dipole)
- [x] CLI: `ig entropy-price-sympy`, `ig tesseract-render`, `ig cmb-test`, `ig phi-proof`
- [x] 323 tests, coverage ≥ 99%

### v0.3.0
- [x] OIPK kernel as closed-form equation (`oipk/kernel.py`)
- [x] Frameprinciple completed (`DIMENSION_AXIOM`, `emergent_dimension()`)
- [x] Medium modulation + anesthesia simulation (`medium/modulation.py`)
- [x] CLI: `ig oipk-calc`, `ig anesthesia-test`, `ig medium-modulate`
- [x] 449 tests (+126 new), coverage ≥ 92%

### v0.4.0 (current – final release)
- [x] Fractal Tesseract rendering engine (`render/fractal_tesseract.py`)
  — Recursive Phi scaling: `β_n = β_0 · Φ^(n/3)`, ASCII animation + PNG/SVG export
- [x] Full 10-part chronology (`chronology/`) — 100% pass rate
- [x] Central `ImplosiveGenesis` class (`core/genesis.py`) + `full_summary()`
- [x] CLI: `ig fractal-render`, `ig chronology-validate`, `ig full-summary`
- [x] 609 tests (+160 new), coverage ≥ 90%, ruff + pre-commit 100% clean

### 2026 Roadmap
- [ ] Empirical validation with real anesthesia/EEG data
- [ ] ArXiv preprint + peer-review submission
- [ ] Interactive web demo (Streamlit/Gradio)
- [ ] Python package on PyPI
- [ ] Integration with quantum-mechanics libraries (QuTiP, Qiskit)

---

## Citation

If you use Implosive Genesis in academic work, please cite the relevant version:

```bibtex
@software{implosive_genesis_2025,
  author    = {GenesisAeon},
  title     = {Implosive Genesis: Recursive Emergence of Space, Time and Consciousness},
  year      = {2025},
  version   = {0.1.0},
  doi       = {10.5281/zenodo.18930089},
  url       = {https://github.com/GenesisAeon/implosive-genesis}
}

@software{implosive_genesis_2026_v02,
  author    = {GenesisAeon},
  title     = {Implosive Genesis – Formalisation \& Falsifiability},
  year      = {2026},
  version   = {0.2.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.18940541},
  url       = {https://github.com/GenesisAeon/implosive-genesis/releases/tag/v0.2.0}
}

@software{implosive_genesis_2026_v03,
  author    = {GenesisAeon},
  title     = {Implosive Genesis – OIPK, Medium Modulation \& Anesthesia Tests},
  year      = {2026},
  version   = {0.3.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.18942660},
  url       = {https://github.com/GenesisAeon/implosive-genesis/releases/tag/v0.3.0}
}

@software{implosive_genesis_2026_v04,
  author    = {GenesisAeon},
  title     = {Implosive Genesis – Fractal Rendering Engine \& Chronology Completion},
  year      = {2026},
  version   = {0.4.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.18956822},
  url       = {https://github.com/GenesisAeon/implosive-genesis/releases/tag/v0.4.0}
}
```

---

Built with [uv](https://docs.astral.sh/uv/) · [Typer](https://typer.tiangolo.com/) · [Rich](https://rich.readthedocs.io/) · [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
