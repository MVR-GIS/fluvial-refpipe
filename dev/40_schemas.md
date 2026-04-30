# Schemas

This document is authoritative for stable field definitions and operator-facing configuration schemas.

## Operator config schema (Milestone B1)

This section defines the authoritative schema for the operator YAML config passed via `--config`.

Notes:
- YAML is treated as literal-only (no env-var interpolation).
- Paths may be absolute or relative.
- Relative paths are resolved relative to the directory containing the config file.

### Files
- Example (tracked): `config/config.example.yml`
- Operator config (untracked): `config/config.yml` (gitignored)

### YAML shape (top-level)

Top-level keys:
- `paths` (required): filesystem locations for PDFs, shared state, and per-run artifacts
- `scan` (required): scan inputs (source roots)
- `thresholds` (optional): Policy 1 thresholds (defaults apply if omitted)

### `paths` (required)

Type: object

Required keys:
- `paths.library_pdfs` (string): destination directory for curated PDFs (sha256-named)
- `paths.quarantine_pdfs` (string): destination directory for quarantine PDFs (sha256-named)
- `paths.state_root` (string): durable shared state root (catalogs, caches)
- `paths.runs_root` (string): per-run artifact root (per-run subfolders live under this root, e.g., `runs/<run_id>/...`)

Constraints:
- Paths may be absolute (Windows or POSIX) or relative.
- Relative paths are resolved relative to the directory containing the config file.
- Local dev mode is allowed (e.g., under `C:/workspace/_refpipe_dev/...`) when VPN/shared drives are unavailable.

### `scan` (required)

Type: object

Required keys:
- `scan.source_roots` (array of strings; length >= 1): one or more directories to scan for PDFs

Constraints:
- entries must be non-empty strings
- paths may be absolute or relative (relative resolved relative to config file directory)

### `thresholds` (optional)

Type: object

Keys:
- `thresholds.candidate_threshold` (float, default `0.30`, range `[0, 1]`)
- `thresholds.ingest_threshold` (float, default `0.65`, range `[0, 1]`)

Constraints:
- `ingest_threshold >= candidate_threshold`

### Example (shared-drive default)

paths:
  library_pdfs: "R:/FluvialGeomorph/references/library_pdfs"
  quarantine_pdfs: "R:/FluvialGeomorph/references/quarantine_pdfs"
  state_root: "R:/FluvialGeomorph/references/state"
  runs_root: "R:/FluvialGeomorph/references/runs"
scan:
  source_roots:
    - "R:/FluvialGeomorph/references/incoming_pdfs"
thresholds:
  candidate_threshold: 0.30
  ingest_threshold: 0.65

### Example (local dev mode)

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
