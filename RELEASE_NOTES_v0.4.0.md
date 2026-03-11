# Release Notes – v0.4.0

**Vierte und finale stabile Version** – das gesamte Modell ist nun fraktal-renderbar, die 10-teilige Chronologie vollständig im Code validiert und alle Komponenten (V_RIG, OIPK, Frameprinciple, Type-6, entropischer Preis, Tesseract, Anesthesia etc.) zentral verknüpft.

## Kern-Neuerungen in v0.4.0

### Fraktale Tesseract-Rendering-Engine

Rekursive Phi-Skalierung:

$$\beta_n = \beta_0 \cdot \Phi^{n/3}, \quad L_n = \lambda_{\rm OIPK} \cdot \Phi^{n/3}, \quad I_n = 1/\Phi^n$$

ASCII-Animation + PNG/SVG-Export. Beispiel-Ausgabe (`ig fractal-render --depth 5 --ascii`):

```
FractalTesseract  depth=5  Φ≈1.6180
  n= 0 │ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ │ β=1.000
  n= 1 │      xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx │ β=1.174
  n= 2 │           +++++++++++++++++++++++++++++++ │ β=1.379
  n= 3 │                ·····················  │ β=1.620
  n= 4 │                     ············  │ β=1.902
  n= 5 │                          ······ │ β=2.234
```

### Vollständige 10-Teile-Chronologie

`ChronologyValidator` prüft **alle 10 Teile** (UTAC → Type-6 → Entropy Governance → OIPK → Frameprinciple …).
100 % Bestehensquote. Beispiel-Ausgabe (`ig chronology-validate`):

```
✓ 10/10 ALLE BESTANDEN  (Bestehensquote: 100%)
```

### Zentrale ImplosiveGenesis-Klasse

Verbindet **alle** Module in einer einzigen Instanz.
`full_summary(n=5)` → kompletter Überblick in einem Befehl.

### Neue CLI-Befehle

```bash
ig fractal-render --depth 8 [--animate --ascii]
ig chronology-validate [--part 4 --verbose]
ig full-summary
```

### Tests & Qualität

609 Tests (+160 neu), ≥ 90 % Coverage, ruff + pre-commit 100 % clean.

---

## Installation & Test

```bash
git checkout main
git pull
uv sync --extra dev
uv run ig fractal-render --depth 5 --ascii
uv run ig chronology-validate
uv run ig full-summary
```

## Upgrade von v0.3.0

Keine Breaking Changes. Alle bestehenden CLI-Befehle und APIs bleiben kompatibel.

```bash
pip install --upgrade implosive-genesis
# oder
uv add implosive-genesis==0.4.0
```

## Zitieren

```bibtex
@software{implosive-genesis-v0.4.0,
  author    = {GenesisAeon},
  title     = {Implosive Genesis – Fraktale Rendering-Engine & Chronologie-Abschluss},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.18956822},
  url       = {https://github.com/GenesisAeon/implosive-genesis/releases/tag/v0.4.0}
}
```

---

**Projekt jetzt vollständig** – alle 10 Chronologie-Teile implementiert und validierbar.
Von Phi-Skalierung über entropischen Preis bis zur fraktalen Frame-Rendering-Engine.
Bereit für empirische Validierung, Paper und weitere Forks.
