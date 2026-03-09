# Implosive Genesis

**Rekursive Entstehung von Raum, Zeit und Bewusstsein**

[![CI](https://github.com/GenesisAeon/implosive-genesis/actions/workflows/ci.yml/badge.svg)](https://github.com/GenesisAeon/implosive-genesis/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

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

### Theoretische Basis

Das Modell postuliert, dass Raum und Zeit keine fundamentalen Größen sind, sondern emergente
Phänomene eines tieferliegenden rekursiven Informationsprozesses. Bewusstsein wird dabei nicht
als Epiphänomen, sondern als strukturell notwendige Bedingung für stabile Selbstreferenz
behandelt (Type-6-Zustand).

Die Implosion als geometrisch-dynamisches Prinzip beschreibt den Übergang von disperser
Informationsverteilung zu kohärenter, selbstorganisierter Struktur — analog zur Entstehung
stabiler Materie aus Quantenfluktuationen.

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

## Projektstruktur

```
src/implosive_genesis/
├── __init__.py          # Version und Metadaten
├── cli.py               # Typer-CLI (ig-Befehl)
├── preset.py            # Template-Engine
├── validator.py         # Projektvalidierung
└── templates/
    ├── minimal.py       # Minimales Python-Paket-Template
    └── genesis.py       # Erweitertes Template mit Domain-YAML
```

## Templates

| Template | Beschreibung |
|----------|--------------|
| `minimal` | Sauberes Python-Paket für alle Anwendungsfälle |
| `genesis` | Erweitert `minimal` um `domains.yaml` + Entropie-Tabellen-Bridge |

---

Entwickelt mit [uv](https://docs.astral.sh/uv/) · [Typer](https://typer.tiangolo.com/) · [Rich](https://rich.readthedocs.io/)
