# Changelog

All notable changes to **Implosive Genesis** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), versioning follows [Semantic Versioning](https://semver.org/).

---

## [0.2.0] – 2026-03-10

**Formalisierung & Falsifizierbarkeit** – exakte mathematische Ableitungen, visuelles Tesseract-Rendering und erste empirische CMB-Falsifizierung.

### Added
- **SymPy-Formalisierung** (`formalization/`)
  - Entropischer Preis exakt abgeleitet: Riemann-Integration + geschlossene Form + Linearitätsbeweis
  - Phi-Skalierung bewiesen: `β_{n+3} = Φ · β_n`, inkl. Lyapunov-Exponent-Stabilität
  - Neues Modul `formalization/entropic_price.py` + `formalization/phi_scaling.py`
- **Tesseract-Visualisierung** (`theory/tesseract.py` erweitert)
  - 3-Panel-Matplotlib-Rendering: CREP-Heatmap, Balkendiagramm, Log-Φ-Skalierung
  - ASCII-Tabelle + PNG/PDF-Export
- **CMB-Falsifizierung** (`simulation/cmb_test.py`)
  - Monte-Carlo-Test: V_RIG = 1352 km/s vs. realer CMB-Dipol (369,82 km/s)
  - p-Wert-Berechnung, σ-Abweichung, Konsistenz-Quote
- **Neue CLI-Befehle**
  - `ig entropy-price-sympy --steps N`
  - `ig tesseract-render --save png`
  - `ig cmb-test --n_sim N`
  - `ig phi-proof`
- **Tests**: 323 Tests (89 neu), Coverage ≥ 99 %, ruff + pre-commit 100 % clean

### Changed
- `theory/tesseract.py`: ASCII-Tabelle deutlich erweitert, Export-Optionen hinzugefügt
- `cli.py`: 4 neue Befehle registriert
- `pyproject.toml`: Version auf `0.2.0` angehoben

### Fixed
- ruff-Lint-Fehler: E501, SIM108, F841, B905, I001 (automatisch behoben)
- Formatierung: 4 Dateien per `ruff format` bereinigt

---

## [0.1.0] – 2026-01-15

**Erste stabile Version** – Kernphysik, CLI, Simulation, Dokumentation und Zenodo-DOI.

### Added
- Kernmodule: `V_RIG`, `OIPK`, `Frameprinciple`, `Tesseract`, `CREP`, `Type-6`
- CLI: `ig scaffold`, `ig validate`, `ig list-templates`, `ig version`, `ig simulate`
- Templates: `minimal`, `genesis`
- Simulation: Entropiesteuerung, kosmische Momente
- 234 Tests, Coverage ≥ 95 %
- MkDocs-Dokumentation unter [genesisaeon.github.io/implosive-genesis](https://genesisaeon.github.io/implosive-genesis/)
- Zenodo DOI: [10.5281/zenodo.15001702](https://doi.org/10.5281/zenodo.15001702)

---

[0.2.0]: https://github.com/GenesisAeon/implosive-genesis/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/GenesisAeon/implosive-genesis/releases/tag/v0.1.0
