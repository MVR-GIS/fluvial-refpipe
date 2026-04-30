# fluvial-refpipe ��� Runbook

Last updated: 2026-04-30

## Purpose

This runbook is the operator/developer “how to run it” reference for `MVR-GIS/fluvial-refpipe`.

It covers:
- environment setup,
- installing the package in editable mode,
- verifying the CLI is available,
- running the test gates required by the project plan.

(Implementation details and contracts belong in `dev/10_design.md` and `dev/40_schemas.md`.)

---

## Supported environment (developer workstation)

- OS: Windows (PowerShell examples)
- Environment manager: conda/mamba (conda-forge)
- Canonical environment spec: `environment.yml`
- Python: 3.11 (per `environment.yml`)

> Note: Dependencies are managed via `environment.yml`. `pyproject.toml` intentionally does not enumerate runtime dependencies.

---

## Quick start: create/update environment

From repo root:

```powershell
# Create (first time)
mamba env create -f environment.yml

# Or update (subsequent)
mamba env update -f environment.yml --prune

conda activate analysis
```

---

## Install package (editable) + verify CLI

From repo root (after activating env):

```powershell
# Update environment
mamba env update -f environment.yml --prune
# Activate environment
conda activate analysis
# Install package
python -m pip install -e .
refpipe --help
```

Expected:
- `refpipe --help` prints the top-level CLI help with commands:
  - `scan`
  - `process`
  - `copy`
  - `rescore-quarantine`
  - `parse`
  - `chunk`
  - `export`

---

## Test gate (Milestone A)

### A1 — CLI smoke tests

Run from repo root:

```powershell
conda activate analysis
pytest -q
```

Expected:
- all tests pass
- current minimum baseline: CLI help smoke tests

Notes:
- The repository includes a minimal CLI smoke test file:
  - `tests/test_cli_smoke.py`
- These tests ensure `refpipe --help` and `refpipe scan --help` succeed and provide stable help text.

---

## Troubleshooting

### `refpipe --help` fails (common causes)
1) Wrong environment active
   - Confirm prompt shows `(analysis)`
   - Run: `python -c "import typer; print(typer.__version__)"`

2) Editable install not applied
   - Re-run: `python -m pip install -e .`
   - Confirm: `python -c "import refpipe; import refpipe.cli; print('ok')"`

3) Command not on PATH in the active shell
   - In the active env, try: `python -m refpipe.cli --help`
   - If that works but `refpipe` does not, re-check shell activation and `pip install -e .` output.

---

## Recent progress log (from dev/05_plan.md)

- 2026-04-30: A1 completed locally:
  - `mamba env update -f environment.yml --prune` (no changes)
  - `python -m pip install -e .` succeeded
  - `refpipe --help` succeeded (Typer app shows planned commands)
  - `pytest -q` => `2 passed`
