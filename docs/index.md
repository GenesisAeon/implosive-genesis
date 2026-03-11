# Implosive Genesis

**Recursive Origin of Space, Time and Consciousness**

[![CI](https://github.com/GenesisAeon/implosive-genesis/actions/workflows/ci.yml/badge.svg)](https://github.com/GenesisAeon/implosive-genesis/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/GenesisAeon/implosive-genesis/blob/main/LICENSE)
[![DOI v0.1.0](https://zenodo.org/badge/DOI/10.5281/zenodo.18930089.svg)](https://doi.org/10.5281/zenodo.18930089)
[![DOI v0.2.0](https://zenodo.org/badge/DOI/10.5281/zenodo.18940541.svg)](https://doi.org/10.5281/zenodo.18940541)
[![DOI v0.3.0](https://zenodo.org/badge/DOI/10.5281/zenodo.18942660.svg)](https://doi.org/10.5281/zenodo.18942660)
[![DOI v0.4.0](https://zenodo.org/badge/DOI/10.5281/zenodo.18956822.svg)](https://doi.org/10.5281/zenodo.18956822)

**Zenodo DOI**: https://doi.org/10.5281/zenodo.18956822
**Live Docs**: https://genesisaeon.github.io/implosive-genesis/

---

**Implosive Genesis** (V_RIG) is a theoretical-formal framework that models the origin of space,
time and consciousness as a recursive, self-organising process. It unifies principles from
information theory, quantum mechanics and consciousness research in a coherent mathematical
structure.

## Quick Start

```bash
pip install implosive-genesis
# or with uv:
uv tool install implosive-genesis
```

```bash
ig scaffold my-experiment
cd my-experiment && uv sync --dev && uv run pytest
```

## Core Concepts

| Abbreviation | Concept | Description |
|--------------|---------|-------------|
| **V_RIG** | Recursive Implosive Genesis | Central model of self-referential origin |
| **OIPK** | Ontological Implosive Principle of Coherence | Coherence condition for emergent structures |
| **Frameprinciple** | Frame Principle | Formal description of observer frames |
| **Type-6** | Consciousness Level 6 | Recursive self-perception as a physical state |

## Core Formulae

**Phi-Scaling** – coupling parameter at recursion level $n$:

$$\beta_n = \beta_0 \cdot \Phi^{n/3}$$

**V_RIG base velocity** (from cosmic field-collapse equilibrium):

$$V_{RIG} \approx 1352\ \text{km/s}$$

**OIPK Energy**:

$$E_{OIPK} = \hbar \cdot \frac{2\pi c}{\lambda_{OIPK}} \cdot \alpha_\Phi \quad \text{with } \alpha_\Phi = \alpha \cdot \Phi$$

**Frame Stability**:

$$S_F = \frac{\Phi^2}{\alpha_\Phi} \approx 221.9$$

**Entropic Price** (CREP):

$$P_E(n, T) = n \cdot k_B \cdot T \cdot \ln(\Phi)$$

## CLI Commands

| Command | Description |
|---------|-------------|
| `ig scaffold <name>` | Create a new project |
| `ig list-templates` | List available templates |
| `ig validate [path]` | Validate project structure |
| `ig version` | Show version |

## Navigation

- [Theory](theory/frameprinciple.md) – Formal foundations (Frame Principle, OIPK, Tesseract)
- [API Reference](api.md) – Complete module and class documentation
- [Examples](examples.md) – Practical code examples
- [CLI Reference](cli.md) – Command-line reference
- [Templates](templates.md) – Project templates

## Citation

```bibtex
@software{implosive_genesis_2025,
  author  = {GenesisAeon},
  title   = {Implosive Genesis: Recursive Origin of Space, Time and Consciousness},
  year    = {2025},
  version = {0.1.0},
  doi     = {10.5281/zenodo.18956822},
  url     = {https://github.com/GenesisAeon/implosive-genesis}
}
```
