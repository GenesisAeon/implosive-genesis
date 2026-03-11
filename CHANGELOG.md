# Changelog

All notable changes to **Implosive Genesis** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), versioning follows [Semantic Versioning](https://semver.org/).

---

## [0.4.0] – 2026-03-10

**Fraktale Rendering-Engine & Chronologie-Abschluss** – vollständige 10-Teile-Chronologie validiert, rekursive Phi-skalierte Tesseract-Rendering-Engine, zentrale ImplosiveGenesis-Klasse als Einstiegspunkt für alle Module.

### Added
- **Fraktale Tesseract-Rendering-Engine** (`render/fractal_tesseract.py`)
  - Rekursive Phi-Skalierung: `β_n = β_0 · Φ^(n/3)`, `L_n = λ_OIPK · Φ^(n/3)`, `I_n = 1/Φ^n`
  - ASCII-Animation + PNG/SVG-Export
  - Neue CLI: `ig fractal-render --depth 8 [--animate --ascii]`
- **Vollständige 10-Teile-Chronologie** (`chronology/`)
  - `ChronologyValidator` prüft alle 10 Teile (UTAC → Type-6 → Entropy Governance → OIPK → Frameprinciple → …)
  - 100 % Bestehensquote
  - Neue CLI: `ig chronology-validate [--part 4 --verbose]`
- **Zentrale ImplosiveGenesis-Klasse** (`core/genesis.py`)
  - Verbindet alle Module in einer einzigen Instanz
  - `full_summary(n=5)` → kompletter Überblick in einem Befehl
  - Neue CLI: `ig full-summary`
- **Tests**: 609 Tests (+160 neu), Coverage ≥ 90 %, ruff + pre-commit 100 % clean

### Changed
- `pyproject.toml`: Version auf `0.4.0` angehoben
- `cli.py`: 3 neue Befehle registriert (`fractal-render`, `chronology-validate`, `full-summary`)

### Fixed
- ruff-Lint: Import-Sortierung, unused imports, E501, B017, E741, F541 bereinigt
- Formatierung: alle geänderten Module per `ruff format` bereinigt

---

## [0.3.0] – 2026-03-10

**OIPK, Medium-Modulation & Anesthesia-Tests** – Frameprinciple vollständig implementiert, OIPK als geschlossene Gleichung, Medium-Modulation und Anesthesia-Frame-Buffer-Simulationen.

### Added
- **Orthogonal Impulse Photon Kernel (OIPK)** (`oipk/kernel.py`)
  - Geschlossene Gleichung: `CREP = w_buffer / (w_buffer + P_info)`, `τ ⊥ t`
  - Berechnung von `λ_OIPK`, `ω`, `E_OIPK`, `S_F` + emergente Dimensionen `D_n`
  - Neue CLI: `ig oipk-calc [--lambda 500 --tau]`
- **Frameprinciple vollendet** (`theory/frameprinciple.py`)
  - `DIMENSION_AXIOM = "A dimension emerges when information would otherwise collapse."`
  - `emergent_dimension()`, `dimension_series()` und exakte OIPK-Integration
- **Medium-Modulation** (`medium/modulation.py`)
  - Frame-Buffer-Simulation mit Bewusstseinsverlust-Modellierung
  - Neue CLI: `ig medium-modulate --t-max 240`
- **Anesthesia-Tests** (`medium/modulation.py`)
  - Bewusst-Anteil, R_loss, R_rec, Anesthesia-Ereignisse
  - Neue CLI: `ig anesthesia-test --duration 300 [--timeline]`
- **Tests**: 449 Tests (+126 neu), Coverage ≥ 92 %, ruff + pre-commit 100 % clean

### Changed
- `pyproject.toml`: Version auf `0.3.0` angehoben
- `theory/frameprinciple.py`: DIMENSION_AXIOM + emergente Dimensionen integriert
- `cli.py`: 3 neue Befehle registriert (`oipk-calc`, `anesthesia-test`, `medium-modulate`)

### Fixed
- ruff-Lint: F401 (unused import in `test_oipk.py`) behoben
- Formatierung: `cli.py`, `modulation.py`, `test_theory.py` per `ruff format` bereinigt

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

[0.4.0]: https://github.com/GenesisAeon/implosive-genesis/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/GenesisAeon/implosive-genesis/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/GenesisAeon/implosive-genesis/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/GenesisAeon/implosive-genesis/releases/tag/v0.1.0
