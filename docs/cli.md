# CLI Reference

Das `ig`-Kommando ist der zentrale Einstiegspunkt für Implosive Genesis.

---

## `ig scaffold`

Neues Projekt aus einem Template erstellen.

```
Usage: ig scaffold [OPTIONS] PROJECT_NAME

Arguments:
  PROJECT_NAME  Name des neuen Projekts (kebab-case empfohlen)

Options:
  -t, --template TEXT       Template (Standard: minimal)
  -o, --output-dir PATH     Elternverzeichnis für das neue Projekt
  --author TEXT             Autorenname
  --description TEXT        Kurze Projektbeschreibung
  --python-version TEXT     Minimale Python-Version (z. B. 3.11)
  --dry-run                 Vorschau ohne Dateien zu schreiben
```

**Beispiele**

```bash
# Minimales Projekt im aktuellen Verzeichnis
ig scaffold my-lib

# Genesis-Preset mit benutzerdefiniertem Autor
ig scaffold my-physics-tool --template genesis --author "Ada Lovelace"

# Vorschau anzeigen (keine Dateien schreiben)
ig scaffold my-lib --dry-run

# In einem bestimmten Verzeichnis erstellen
ig scaffold my-lib --output-dir ~/projects
```

---

## `ig list-templates`

Alle verfügbaren Templates mit Beschreibungen anzeigen.

```bash
ig list-templates
```

---

## `ig validate`

Projektverzeichnis gegen Implosive-Genesis-Best-Practices validieren.

```
Usage: ig validate [PATH]

Arguments:
  PATH  Zu validierendes Projektverzeichnis [Standard: aktuelles Verzeichnis]
```

Durchgeführte Prüfungen:

| Prüfung | Schweregrad |
|---------|-------------|
| `pyproject.toml` vorhanden | **Fehler** |
| `src/`-Layout vorhanden | Warnung |
| `tests/`-Verzeichnis vorhanden | Warnung |
| `.github/workflows/` vorhanden | Warnung |
| `README.md` vorhanden | Warnung |
| `.gitignore` vorhanden | Warnung |

```bash
# Aktuelles Verzeichnis validieren
ig validate

# Bestimmtes Projekt validieren
ig validate path/to/my-project
```

---

## `ig version`

Installierte Version anzeigen.

```bash
ig version
```
