# fluvial-refpipe — Project Plan

Last updated: 2026-04-29

Now (max 3):
- [ ] A1 Confirm editable install + CLI help (next)
  - Progress: Worked through establishing a correctly configured Python environment. 
  - Note: `refpipe --help` currently fails unless `typer` is available in the active env; ensure `analysis` is activated in PowerShell
- [ ] A2 Establish CLI app + command stubs
- [ ] A3 Add pytest smoke tests

How to use:
- This is the canonical ordered task list.
- Keep tasks small (1–3 hours).
- Each task has a Definition of Done (DoD) and artifacts.
- When resuming work, read this file + `dev/10_design.md`.
- Convention: under any task, add a single sub-bullet `- Progress:` with a short present-tense clause (optionally ending with `; next: <next step>`), and remove/overwrite that line once the checkbox is checked.

## Milestone A — Packaging + CLI skeleton (from dev/10_design.md)
- [ ] A1: Confirm editable install + CLI help
  - [ ] A1: Confirm editable install + CLI help
  - DoD (PowerShell): `conda activate analysis`; `python -c "import typer, pytest"`; `python -m pip install -e .`; `refpipe --help`
  - Artifacts: terminal transcript; minimal smoke test in `tests/`
- [ ] A2: Establish CLI app + command stubs
  - DoD: `refpipe scan --help` etc. exist for planned commands
  - Artifacts: `src/refpipe/cli.py`
- [ ] A3: Add pytest smoke tests
  - DoD: `pytest -q` passes locally
  - Artifacts: `tests/test_cli_smoke.py`

## Milestone B — First end-to-end “toy run” (single PDF)
- [ ] B1: Define config model + example config
  - DoD: config validates; documented in runbook
  - Artifacts: `src/refpipe/config.py`, `config.example.yml`, runbook update
- [ ] B2: Implement `scan` to build run inventory + compute sha256
  - DoD: writes `runs/<run_id>/manifest.csv` with sha256 + path observation
  - Artifacts: run folder + sample output
- [ ] B3: Implement TEI extraction cache hook (GROBID placeholder ok)
  - DoD: cached TEI exists keyed by sha256 (even if mocked initially)
  - Artifacts: cache folder + code
- [ ] B4: Implement `copy` Policy 1 decisions (curated/quarantine/skip)
  - DoD: copied to `<sha256>.pdf` dest; never overwrites; logs action
  - Artifacts: files in `library_pdfs/` or `quarantine_pdfs/`
- [ ] B5: Implement `parse` to emit `elements.jsonl`
  - DoD: elements include doc IDs + span metadata + last_observed_path
  - Artifacts: `runs/<run_id>/elements.jsonl`
- [ ] B6: Implement `chunk` to emit `chunks_main.jsonl` + `chunks_references.jsonl`
  - DoD: deterministic chunk IDs; lineage fields present
  - Artifacts: chunk files
- [ ] B7: Implement `export` (Gemini JSONL + Foundry Parquet)
  - DoD: exports exist and are loadable
  - Artifacts: export files + minimal validation script

## Milestone C — Durable catalogs + idempotency
- [ ] C1: Define Parquet catalog schemas (pdf catalog, curated, quarantine, observations)
- [ ] C2: Implement catalog lock + atomic write
- [ ] C3: Publish CSV views after updates
- [ ] C4: Incremental scan across multiple source roots

## Milestone D — Quality + hardening
- [ ] D1: Logging and run summary report
- [ ] D2: Add unit tests for hashing, policy thresholds, chunking determinism
- [ ] D3: Performance profiling + large-run considerations
- [ ] D4: Documentation polish (design/runbook/schemas/ADR links complete)
