# Schemas

## Operator config schema (Milestone B1)

This section defines the authoritative schema for the operator YAML config passed via `--config`.

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
- `paths.runs_root` (string): per-run artifact root (`runs/<run_id>/...`)

Constraints:
- **Windows paths only; must be absolute drive paths** like `R:/...` or `C:/...`
- no relative paths
- local dev mode is allowed (e.g., `C:/workspace/_refpipe_dev/...`) when VPN/shared drives are unavailable

### `scan` (required)
Type: object

Required keys:
- `scan.source_roots` (array of strings; length >= 1): one or more directories to scan for PDFs

Constraints:
- entries must be non-empty strings
- Windows absolute drive paths are expected (local or shared drives)

### `thresholds` (optional)
Type: object

Keys:
- `thresholds.candidate_threshold` (float, default `0.30`, range `[0, 1]`)
- `thresholds.ingest_threshold` (float, default `0.65`, range `[0, 1]`)

Constraints:
- `ingest_threshold >= candidate_threshold`

### Example (shared-drive default)
```yaml
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
