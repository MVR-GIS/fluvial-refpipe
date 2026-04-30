# fluvial-refpipe — Design (Architecture + Operating Model)

Last updated: 2026-04-30  
Project repo: `MVR-GIS/fluvial-refpipe`  
Primary operator: single-operator expected (but design tolerates future concurrency)

## Document map (where to look)
This document is the **stable architecture overview** (what is true).

- Architecture decisions (why): `dev/decisions/*.md` (ADRs; YAML front-matter; append-only)
- Operational procedures (how): `dev/30_runbook.md`
- Concrete schemas (exact fields/types): `dev/40_schemas.md`
- Chat governance: `dev/instructions/CHAT_INSTRUCTIONS.md`
- Working notes / scratchpad: `dev/02_dev.md`

## Purpose / Problem Statement
Build a reproducible pipeline to:
1) discover PDFs across multiple source roots that evolve over time,
2) deduplicate and track them by content identity,
3) extract bibliographic metadata and full text,
4) classify items into curated vs quarantine,
5) chunk extracted text for downstream embedding/RAG,
6) export results to Gemini JSONL and Foundry Parquet,
while preserving a strong audit trail.

The pipeline is designed for incremental adoption: start lightweight, then harden as usage grows.

---

## ADR index (authoritative “why”)
These decisions are treated as stable contracts at a point in time. They can change as requirements evolve—when they do, create a new ADR and mark the prior one as `superseded` (don’t rewrite history).

ADRs (linkable index):
- ADR-0001: [SHA256 document identity](decisions/0001-sha256-identity.md)
- ADR-0002: [Paths as observations + `last_observed_path`](decisions/0002-paths-as-observations.md)
- ADR-0003: [Separate code (Git) from data/state (agency filesystem)](decisions/0003-separate-code-from-data-storage.md)
- ADR-0004: [Catalogs: Parquet + file locking + publish CSV views](decisions/0004-catalogs-parquet-locking-and-csv-views.md)
- ADR-0005: [Policy 1 thresholds and copy/quarantine/skip actions](decisions/0005-policy1-copy-quarantine-skip-thresholds.md)
- ADR-0006: [OpenAlex enrichment policy (DOI-first; title-search only for scholarly; stale refresh)](decisions/0006-openalex-enrichment-policy.md)
- ADR-0007: [Hybrid chunking + separate references corpus](decisions/0007-hybrid-chunking-and-separate-references-corpus.md)
- ADR-0008: [Conda-first env + pip editable installs](decisions/0008-conda-first-plus-pip-editable.md)
- ADR-0009: [Windows/Positron supported terminal: PowerShell](decisions/0009-windows-terminal-support.md)

---

## Non-negotiable principles (invariants)

### 1) Identity is content-based (SHA256)
- **Document identity = SHA256 hash of PDF bytes**.
- `document_id` format: `sha256:<hex>`.
- File paths are **not identities**; they are unstable observations.

### 2) Paths are treated as observations
- Maintain an append-only history table: `pdf_path_observations`.
- Provide a single convenience field for humans: `last_observed_path`.
- Never rely on any “original path” for joins; always join via sha256.

### 3) Separation of concerns: code vs data
- Git repo stores: code, docs, config templates, schemas, and tiny test fixtures only.
- Agency filesystem stores: PDFs, catalogs/state, caches, run artifacts.

---

## Storage layout on agency filesystem (source-of-truth for data)

Root: `R:/FluvialGeomorph/references/`

- `library_pdfs/`  
  Curated PDFs, named by sha256: `<sha256>.pdf`

- `quarantine_pdfs/`  
  Quarantine PDFs, named by sha256: `<sha256>.pdf`

- `state/`  
  Durable state shared across runs:
  - `state/catalogs/` (Parquet + CSV views)
  - `state/caches/` (GROBID TEI cache, OpenAlex cache, etc.)

- `runs/`  
  Per-run artifacts written under `runs/<run_id>/...`:
  - inventories, manifests, logs, parse outputs, chunks, exports, state update staging

---

## Catalogs (state) and update safety

### Parquet is the durable format
- Catalogs are stored as Parquet for scalability and reliable typing.
- Human-readable CSV views are published after updates.

### File-lock protocol for catalog writes
Even if single-operator is expected, we use a lock because it is low-cost and prevents corruption.

- Lock file: `state/catalogs/.lock`
- On update:
  1) write run-local staging updates (`runs/<run_id>/state_updates/...`)
  2) acquire lock
  3) apply updates
  4) write temp + atomic rename
  5) publish CSV views
  6) release lock

### CSV views to publish (after any update)
- `pdf_catalog_latest.csv`
- `curated_latest.csv`
- `quarantine_latest.csv`

---

## Policy 1: copy / quarantine / skip

### Thresholds (current)
- `candidate_threshold = 0.30`
- `ingest_threshold = 0.65`

### Actions
- **curated** if `score_ingest >= ingest_threshold` OR allowlisted
- **quarantine** if `candidate_threshold <= score_ingest < ingest_threshold`
- **skip** otherwise

### Quarantine is not “ignored”
Quarantine items still receive:
- GROBID TEI extraction (cached)
- metadata normalization
- classification signals
- OpenAlex enrichment (with safe refresh policy)

Rationale: quarantine review needs evidence and context.

---

## Enrichment policy (OpenAlex)

### DOI lookup
- If a DOI exists: do OpenAlex DOI lookup for all items.

### Title-search (safer default)
- Use OpenAlex title-search only when `doc_type_guess == scholarly`.
- Rationale: prevent incorrect matches for internal reports, memos, etc.

### Quarantine rescore job
- Scope: **quarantine only**
- Refresh: only if stale/missing
- Default: `max_age_days = 30`

---

## Operator configuration (Milestone B1)

### Contract
- The pipeline is configured via a YAML file provided on the CLI with `--config`.
- Configuration is validated at the CLI boundary (fail fast) before any stage executes.
- YAML is treated as **literal-only** for reproducibility (no env-var interpolation).
- Config fields/types/defaults are authoritative in `dev/40_schemas.md`.

### Repo convention (locations)
- Tracked example config: `config/config.example.yml`
- Operator config (untracked): `config/config.yml` (gitignored)

Rationale:
- keep sensitive/operator-specific paths out of git
- provide a stable, reviewable template and contract in the repo

### Local dev mode (robustness)
When VPN/shared-drive access is patchy, operators may point `paths.*` and `scan.source_roots`
to local folders (e.g., under `C:/workspace/_refpipe_dev/`) to test pipeline mechanics and output
formats without requiring `R:/...` access.

Local dev mode must still preserve the core invariants:
- sha256 identity
- separation of code (git) vs data/state (filesystem)
- deterministic, auditable run artifacts under `runs_root`

---

## Pipeline stages and CLI contract

Planned stages (names may evolve; the stage concepts are required):

- `scan`
  - discover PDFs in configured source roots
  - compute sha256
  - update catalogs/path observations

- `process`
  - TEI extraction via GROBID (cached by sha256)
  - normalize bib metadata
  - classify (doc_type_guess, score_ingest, signals)
  - enrich (OpenAlex per policy)

- `copy`
  - apply Policy 1 actions
  - copy curated to `library_pdfs/`
  - copy quarantine to `quarantine_pdfs/`
  - never overwrite; record “exists” when already present

- `rescore-quarantine`
  - rerun scoring & refresh stale/missing OpenAlex for quarantine items only

- `parse`
  - parse curated PDFs (default) into `elements.jsonl`
  - include `last_observed_path` for human debugging

- `chunk`
  - hybrid chunking (structure-first + semantic chunking)
  - export two corpora: main and references

- `export`
  - Gemini JSONL
  - Foundry Parquet

- `publish-catalog-views`
  - regenerate CSV views from Parquet catalogs (often called automatically)

---

## Parsing outputs (run artifacts)

### `runs/<run_id>/manifest.csv`
Backbone table (tabular) for the run. Includes:
- `run_id`
- `collected_at_utc`
- `document_sha256`
- `document_id`
- `library_pdf_path` (stable sha256-based path if curated/copied)
- `bytes` (optional)
- `modified_time_utc` (optional)
- `tier` (curated/quarantine if included)
- merged `title`, `year`, `doi`, `openalex_id`
- `doc_type_guess`
- `last_observed_path` (human convenience)

### `runs/<run_id>/elements.jsonl`
One record per extracted element, includes:
- identifiers: `run_id`, `document_sha256`, `document_id`
- stable path: `library_pdf_path` (and/or quarantine path depending on scope)
- debugging: `last_observed_path`
- element spans: `element_index`, `page_number` (when available)
- content: `text`
- `unstructured_metadata` as JSON object
- small doc metadata copied down: `title`, `year`, `doi`, `openalex_id`, `doc_type_guess`

Note: exact field names/types are specified in `dev/40_schemas.md`.

---

## Chunking design (Hybrid option)

### Strategy
- **Structure-first segmentation** (TEI / headings) to produce coherent segments.
- Fallback: heading-based segmentation when TEI is missing/partial.
- Then **element-level semantic chunking** to enforce token/size constraints while preserving traceability.

### References are separated
- `chunks_main.jsonl`
- `chunks_references.jsonl`

### Chunk record requirements
Each chunk includes:
- chunk identity: `chunk_id`, `chunk_index`, `chunk_corpus`
- provenance: `document_sha256`, `document_id`, `library_pdf_path`, `last_observed_path`
- lineage: element index span + page min/max
- content: `text`, `char_count`, `approx_token_count`
- audit fields: `run_id`, `chunked_at_utc`, `pipeline_version`, `chunking_params`, flags

---

## Export rules

### Source-of-truth remains JSONL with nested objects
- Keep nested objects in JSONL (no double-encoded JSON strings).

### Foundry Parquet is flattened
- At export time, convert nested objects to JSON strings in Parquet columns:
  - `software_versions_json`, `chunking_params_json`, etc.

Rationale: keep JSONL human/audit friendly; keep Parquet schema stable.

---

## Python project management (developer workflow)

### Environment model
- Environment manager: Miniforge + mamba
- Dependency spec: `environment.yml`
- Model: **one environment per repository**
- Default env name: `analysis`

### Packaging model
- Use `pyproject.toml` for packaging metadata and console scripts.
- Dependencies are managed in `environment.yml` (conda-first).
- Editable install is performed via pip *inside the conda env*:
  - `python -m pip install -e .`

Rationale: conda manages heavy deps; pip provides correct Python packaging + CLI entrypoints.

### Windows/Positron terminal guidance
- Supported: PowerShell terminal in Positron (works reliably with conda activation).
- Git Bash integration may be unstable depending on PATH/utility availability.

### Testing (TDD-first, local)
- Prefer local `pytest` runs during development.
- CI is not assumed to run tests unless explicitly added later.

---

## Reproducible chat instructions
This repo uses reproducible chat instruction modules under:
- `dev/instructions/`

Entrypoint:
- `dev/instructions/CHAT_INSTRUCTIONS.md`

All future chat sessions should specify:
- Target repo: `MVR-GIS/fluvial-refpipe`
- Read and follow the entrypoint + modules in order.

---

## Definition of done (project readiness milestones)

### Milestone A: packaging + CLI skeleton
- `python -m pip install -e .` succeeds inside the `analysis` env
- `refpipe --help` works
- `pytest -q` runs locally

### Milestone B: first end-to-end “toy” run (single PDF)
- `scan` inventories a known PDF and writes `runs/<run_id>/manifest.csv`
- `process` produces cached TEI and normalized metadata
- `copy` places the PDF into the correct sha256 destination
- `parse` emits `elements.jsonl`
- `chunk` emits `chunks_main.jsonl` and `chunks_references.jsonl`
- `export` emits Gemini JSONL and Foundry Parquet

---

## Open questions / deferred decisions
Track items here as they arise:
- [ ] Exact Parquet schemas for catalogs and chunks (field names, types, nullability)
- [ ] Exact scoring model for `score_ingest` (features, weights, versioning)
- [ ] Cache formats and invalidation rules (GROBID, OpenAlex, embeddings)
- [ ] Whether/when to add CI (linting only? tests? docs build?)
