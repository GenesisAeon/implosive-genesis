# Templates

Implosive Genesis liefert zwei eingebaute Templates. Eigene Templates lassen sich mit einer einzigen Python-Datei hinzufügen.

---

## `minimal`

**Der Standard.** Ein sauberes, modernes Python-Projekt mit allem Notwendigen.

```bash
ig scaffold my-lib
ig scaffold my-lib --template minimal
```

### Generierte Dateien

```
my-lib/
├── src/
│   └── my_lib/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── pyproject.toml
├── README.md
├── .gitignore
└── .pre-commit-config.yaml
```

### Variablen

| Variable | Standard | Beschreibung |
|----------|---------|--------------|
| `name` | *(Pflichtfeld)* | Projektname |
| `description` | `"A Python project"` | Kurzbeschreibung |
| `author` | `"Your Name"` | Autorenname |
| `python_version` | `"3.11"` | Minimale Python-Version |

---

## `genesis`

Eine Erweiterung von `minimal` – fügt eine `domains.yaml` für Domain/Metrik-Konfiguration und ein Entropietabellen-Bridge-Modul hinzu.

```bash
ig scaffold my-physics-tool --template genesis
```

### Zusätzliche Dateien

```
my-physics-tool/
├── domains.yaml           ← Domain/Metrik-Konfiguration
├── config/
│   └── entropy.yaml       ← Entropietabellen-Bridge-Konfiguration
└── src/
    └── my_physics_tool/
        ├── __init__.py
        └── bridge.py      ← Entropietabellen-Export-Funktion
```

### Zusätzliche Variablen

| Variable | Standard | Beschreibung |
|----------|---------|--------------|
| `metrics` | `"crep"` | Standard-Metrikkürzel |

---

## Eigenes Template hinzufügen

1. Datei `src/implosive_genesis/templates/my_template.py` erstellen:

```python
TEMPLATE = {
    "name": "my_template",
    "description": "Mein eigenes Template",
    "variables": ["name", "description", "author", "python_version"],
    "defaults": {
        "description": "Ein Python-Projekt",
        "author": "Your Name",
        "python_version": "3.11",
    },
    "files": {
        "README.md": "# ${name}\n\n${description}\n",
        "pyproject.toml": "...",
        # Schlüssel = relative Pfade, Werte = Template-Strings
        # ${variable} für Substitution
        # $$ für ein wörtliches Dollarzeichen
    },
}
```

2. In `src/implosive_genesis/templates/__init__.py` registrieren:

```python
from .my_template import TEMPLATE as MY_TEMPLATE

REGISTRY: dict[str, dict] = {
    "minimal": MINIMAL_TEMPLATE,
    "genesis": GENESIS_TEMPLATE,
    "my_template": MY_TEMPLATE,  # ← hier hinzufügen
}
```

`ig list-templates` zeigt das neue Template sofort an.
