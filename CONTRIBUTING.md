# Contributing

Thanks for your interest in contributing to Implosive Genesis!

## Getting started

1. Fork and clone the repository.
2. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
   (or `.venv\Scripts\activate` on Windows).
3. Install in editable mode with dev dependencies:
   `uv sync --extra dev` (or `pip install -e ".[dev]"`).
4. Run the test suite: `uv run pytest` (or `pytest`).

## Code style

- Format and lint with `ruff format` and `ruff check`.
- Keep functions documented with docstrings where the existing modules do.
- Run `pre-commit run --all-files` before committing.

## Pull requests

- One logical change per PR.
- Add or update tests for any behavioral change.
- Update `CHANGELOG.md` under an `## [Unreleased]` section.
- Fill out the PR template (`.github/PULL_REQUEST_TEMPLATE.md`).

## Reporting issues

Please use the issue templates in `.github/ISSUE_TEMPLATE/` — they help us
triage bug reports vs. feature requests quickly.

## Scientific claims

This is part of a research framework. If your contribution touches any
scientific model, prediction, or benchmark (e.g. V_RIG, OIPK, Phi-scaling,
CREP values), please:

- Cite the source (paper, dataset, or prior GenesisAeon Zenodo record).
- Clearly mark speculative vs. validated claims.
