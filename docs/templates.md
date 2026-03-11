# Templates

Implosive Genesis ships with two built-in templates. Custom templates can be added with a single Python file.

---

## `minimal`

**The default.** A clean, modern Python project with everything you need.

```bash
ig scaffold my-lib
ig scaffold my-lib --template minimal
```

### Generated Files

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

### Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `name` | *(required)* | Project name |
| `description` | `"A Python project"` | Short description |
| `author` | `"Your Name"` | Author name |
| `python_version` | `"3.11"` | Minimum Python version |

---

## `genesis`

An extension of `minimal` – adds a `domains.yaml` for domain/metric configuration and an entropy-table bridge module.

```bash
ig scaffold my-physics-tool --template genesis
```

### Additional Files

```
my-physics-tool/
├── domains.yaml           ← domain/metric configuration
├── config/
│   └── entropy.yaml       ← entropy-table bridge configuration
└── src/
    └── my_physics_tool/
        ├── __init__.py
        └── bridge.py      ← entropy-table export function
```

### Additional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `metrics` | `"crep"` | Default metric abbreviation |

---

## Adding a Custom Template

1. Create file `src/implosive_genesis/templates/my_template.py`:

```python
TEMPLATE = {
    "name": "my_template",
    "description": "My custom template",
    "variables": ["name", "description", "author", "python_version"],
    "defaults": {
        "description": "A Python project",
        "author": "Your Name",
        "python_version": "3.11",
    },
    "files": {
        "README.md": "# ${name}\n\n${description}\n",
        "pyproject.toml": "...",
        # keys = relative paths, values = template strings
        # ${variable} for substitution
        # $$ for a literal dollar sign
    },
}
```

2. Register it in `src/implosive_genesis/templates/__init__.py`:

```python
from .my_template import TEMPLATE as MY_TEMPLATE

REGISTRY: dict[str, dict] = {
    "minimal": MINIMAL_TEMPLATE,
    "genesis": GENESIS_TEMPLATE,
    "my_template": MY_TEMPLATE,  # ← add here
}
```

`ig list-templates` will show the new template immediately.
