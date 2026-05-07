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
- `acquire` (optional): citation-to-PDF acquisition settings (used by the `acquire` stage)

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

### `acquire` (optional)

Type: object

Purpose:
- Configure the `acquire` stage, which attempts to retrieve PDFs for a list of citation strings using open/legal sources.

Recommended keys (initial; may expand):
- `acquire.allowed_sources` (string, default `"open_access_only"`): policy gate for which sources/URLs may be downloaded
- `acquire.matching_min_confidence` (float, default `0.80`, range `[0, 1]`): minimum confidence required to auto-select a match for download
- `acquire.timeout_seconds` (int, default `30`, range `>= 1`): HTTP timeout
- `acquire.max_retries` (int, default `2`, range `>= 0`): retry count for transient failures
- `acquire.rate_limit_per_minute` (int, default `30`, range `>= 1`): best-effort client-side throttling
- `acquire.user_agent` (string, optional): explicit User-Agent for requests

Notes:
- `acquire` writes PDFs and logs only under `runs/<run_id>/...` and does not write into curated/quarantine libraries.
- Acquisition runs commonly use an additional untracked config instance (e.g., `config/config.acquire.yml`) for the explicit scan step; the schema is the same, but `scan.source_roots` is set to `runs/<run_id>/acquired_pdfs/`.

---

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
