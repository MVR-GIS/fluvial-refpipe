# fluvial-refpipe — Overlay Module (Fluvial Reference Pipeline Conventions)

This module captures repo-specific workflow decisions for `MVR-GIS/fluvial-refpipe`.
It is intended to keep future chat sessions consistent and reproducible.

## Non-negotiable design decisions (required)
### Identity & provenance
- Document identity is **SHA256** of PDF bytes.
- File paths are treated as **unstable observations**, not identifiers.
- Maintain append-only `pdf_path_observations` history.
- Provide `last_observed_path` as a human convenience field in outputs.

### Storage separation (required)
- Git repository stores: code, docs, config templates, schemas, tiny test fixtures only.
- Agency filesystem stores: PDFs, state catalogs, caches, run artifacts:
  - `R:/FluvialGeomorph/references/library_pdfs/`
  - `R:/FluvialGeomorph/references/quarantine_pdfs/`
  - `R:/FluvialGeomorph/references/state/`
  - `R:/FluvialGeomorph/references/runs/` (or configured runs_root)

### Copy policy (Policy 1)
- candidate_threshold = 0.30
- ingest_threshold = 0.65
- Actions:
  - curated if score_ingest >= ingest_threshold OR allowlisted
  - quarantine if candidate_threshold <= score_ingest < ingest_threshold
  - skip otherwise
- Quarantine items MUST still get GROBID extraction + enrichment to support decisionmaking.

### Enrichment policy (OpenAlex safer default)
- OpenAlex DOI lookup for all items with a DOI.
- OpenAlex title-search ONLY for likely-scholarly documents (`doc_type_guess == scholarly`).
- Quarantine rescore job:
  - scope = quarantine only
  - refresh OpenAlex if stale/missing (default max_age_days=30)

### Chunking policy
- Hybrid chunking (Option 4):
  - TEI/structure-first segmentation
  - fallback heading-based segmentation
  - element-level semantic chunking with precise element/page span metadata
- References are exported as a separate corpus:
  - `chunks_main.jsonl` and `chunks_references.jsonl`

## Operational robustness (required)
### Incremental updates
- Pipeline must support scanning additional source roots over time (“piecewise updates”).
- Must be idempotent:
  - copying uses `<sha256>.pdf` destinations and never overwrites
  - cached TEI/enrichment reused by sha256 where possible

### Catalog writes must be safe
- Use a simple shared-drive file lock for catalog updates:
  - `state/catalogs/.lock`
  - stale lock override with explicit logging
- Catalogs stored as Parquet for scale.
- Always publish human-view CSVs after any catalog update:
  - `pdf_catalog_latest.csv`
  - `curated_latest.csv`
  - `quarantine_latest.csv`

## CLI contract (required)
Planned commands (names may evolve, but stages must exist):
- scan
- process
- copy
- rescore-quarantine
- parse
- chunk
- export
- publish-catalog-views (often called automatically)

## Evidence & audit trail (required)
- Every run must write:
  - `run-metadata.json` including pipeline version (git commit hash), config snapshot hash, timestamps
  - action logs for copy/quarantine/skip decisions with reasons and thresholds
- Avoid silent behavior changes: if heuristics/config change, record versions/hashes used.

## Interaction style for this repo (required)
- Prefer implementation choices that preserve auditability and reviewer confidence over maximum convenience.
- When asked to “make it simpler,” propose simplifications that do NOT compromise:
  - sha256 identity,
  - quarantining,
  - audit logs,
  - separation of code vs data storage.
  