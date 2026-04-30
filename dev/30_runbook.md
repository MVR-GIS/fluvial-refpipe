# fluvial-refpipe - Runbook

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

### A1/A2/A3 — pytest smoke tests

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
- These tests ensure `refpipe --help` and each planned subcommand `--help` succeeds and provides stable help text.

---

## CLI structure (Milestone A2)

The CLI is implemented as a structured package:

- App registration (Typer `app`):
  - `src/refpipe/cli/app.py`
- Command stubs (one file per command):
  - `src/refpipe/cli/commands/`

Planned commands (A2) are registered and must have working help pages:
- `scan`
- `process`
- `copy`
- `rescore-quarantine`
- `parse`
- `chunk`
- `export`
- `refpipe <command> --help` works for all planned commands
- `pytest -q` => `8 passed` (CLI help smoke tests) 

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
   - In the active env, try: `python -m refpipe.cli.app --help`
   - If that works but `refpipe` does not, re-check shell activation and `pip install -e .` output.

---

## Configuration (Milestone B1)

The pipeline is configured by a YAML file passed via `--config`.

### File locations (repo convention)

- Example (tracked): `config/config.example.yml`
- Operator config (NOT tracked): `config/config.yml` (gitignored)

Create your operator config:

```powershell
# from repo root
copy config/config.example.yml config/config.yml
```

Edit `config/config.yml` and set:

- `paths.*` to your shared-drive or local dev paths (see local dev mode below)
- `scan.source_roots` to one or more folders containing PDFs to scan

### Validate configuration (recommended before any run)

Config validation is strict and happens before command execution.

```powershell
conda activate analysis
python -m pip install -e .

# Validate via Python (fast, explicit)
python -c "from refpipe.config import RefpipeConfig; RefpipeConfig.from_yaml('config/config.yml'); print('config ok')"

# Optional: run the test gate
pytest -q
```

### Local dev mode (when VPN/shared drives are unavailable)

When VPN access to `R:/...` is patchy, you can run the pipeline against **local folders** while developing.

Recommended local layout (outside git artifacts, safe to delete):

- `C:/workspace/_refpipe_dev/library_pdfs/`
- `C:/workspace/_refpipe_dev/quarantine_pdfs/`
- `C:/workspace/_refpipe_dev/state/`
- `C:/workspace/_refpipe_dev/runs/`

Example local dev config:

```yaml
paths:
  library_pdfs: "C:/workspace/_refpipe_dev/library_pdfs"
  quarantine_pdfs: "C:/workspace/_refpipe_dev/quarantine_pdfs"
  state_root: "C:/workspace/_refpipe_dev/state"
  runs_root: "C:/workspace/_refpipe_dev/runs"
scan:
  source_roots:
    - "C:/workspace/_refpipe_dev/incoming_pdfs"
thresholds:
  candidate_threshold: 0.30
  ingest_threshold: 0.65
```

Notes:
- Local dev mode is intended for testing pipeline mechanics and output formats.
- Do not commit local paths in `config/config.yml` (it is intentionally untracked).
- The production/shared-drive paths remain the canonical defaults shown in `config/config.example.yml`.

---

## Scan (Milestone B2)

The `scan` command discovers PDFs in `scan.source_roots`, computes sha256 identities, and writes a per-run manifest.

### Run scan

From repo root:

    conda activate analysis
    python -m pip install -e .
    refpipe scan --config config/config.yml

Expected:
- A new run folder is created under `paths.runs_root`:
  - `<runs_root>/<run_id>/manifest.csv`
- The command prints the manifest path, observed PDF count, and `run_id`.

### Manifest contents

`manifest.csv` includes:
- `run_id`
- `collected_at_utc`
- `document_sha256`
- `document_id` (`sha256:<hex>`)
- `last_observed_path`

Notes:
- B2 writes run artifacts only; durable catalogs and locks are added later (Milestone C).




## Recent progress log (from dev/05_plan.md)
 
- 2026-04-30: A1 completed locally:
  - `mamba env update -f environment.yml --prune` (no changes)
  - `python -m pip install -e .` succeeded
  - `refpipe --help` succeeded (Typer app shows planned commands)
  - `pytest -q` => passing

- 2026-04-30: A2 completed locally:
  - CLI refactored into structured package:
    - `src/refpipe/cli/app.py`
    - `src/refpipe/cli/commands/*.py`
  - `refpipe <command> --help` works for all planned commands
  - `pytest -q` => `8 passed` (CLI help smoke tests)

- 2026-04-30: A3 completed locally:
  - Pytest configuration added to `pyproject.toml`:
    - `[tool.pytest.ini_options]` with `testpaths=["tests"]` and `addopts="-q"`
  - Import smoke test added (`test_import_refpipe`)

- 2026-04-30: B1 completed (config model + example config):
  - Config model implemented: `src/refpipe/config.py` (`RefpipeConfig.from_yaml`)
  - Example config added: `config/config.example.yml` (copy to `config/config.yml`)
  - Validation behavior:
    - strict schema validation (Pydantic)
    - Windows absolute drive paths required (no relative paths)
    - thresholds defaults: candidate=0.30, ingest=0.65; requires ingest >= candidate
