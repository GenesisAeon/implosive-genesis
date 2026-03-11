# CLI Reference

The `ig` command is the central entry point for Implosive Genesis.

---

## `ig scaffold`

Create a new project from a template.

```
Usage: ig scaffold [OPTIONS] PROJECT_NAME

Arguments:
  PROJECT_NAME  Name of the new project (kebab-case recommended)

Options:
  -t, --template TEXT       Template (default: minimal)
  -o, --output-dir PATH     Parent directory for the new project
  --author TEXT             Author name
  --description TEXT        Short project description
  --python-version TEXT     Minimum Python version (e.g. 3.11)
  --dry-run                 Preview without writing files
```

**Examples**

```bash
# Minimal project in the current directory
ig scaffold my-lib

# Genesis preset with a custom author
ig scaffold my-physics-tool --template genesis --author "Ada Lovelace"

# Preview (no files written)
ig scaffold my-lib --dry-run

# Create in a specific directory
ig scaffold my-lib --output-dir ~/projects
```

---

## `ig list-templates`

List all available templates with descriptions.

```bash
ig list-templates
```

---

## `ig validate`

Validate a project directory against Implosive Genesis best practices.

```
Usage: ig validate [PATH]

Arguments:
  PATH  Project directory to validate [default: current directory]
```

Checks performed:

| Check | Severity |
|-------|----------|
| `pyproject.toml` present | **Error** |
| `src/` layout present | Warning |
| `tests/` directory present | Warning |
| `.github/workflows/` present | Warning |
| `README.md` present | Warning |
| `.gitignore` present | Warning |

```bash
# Validate current directory
ig validate

# Validate a specific project
ig validate path/to/my-project
```

---

## `ig version`

Show the installed version.

```bash
ig version
```
