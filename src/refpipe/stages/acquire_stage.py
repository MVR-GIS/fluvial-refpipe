from __future__ import annotations
 
import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
 
from refpipe.config import RefpipeConfig
from refpipe.stages.scan_stage import build_run_id
 
 
@dataclass(frozen=True)
class AcquireResult:
    run_id: str
    run_dir: Path
    citations_input_path: Path
    citation_resolution_path: Path
    acquire_manifest_path: Path
    acquired_pdfs_dir: Path
    citation_count: int
    collected_at_utc: datetime
 
 
def _normalize_citation_text(raw: str) -> str:
    """
    Minimal, deterministic normalization for B2.5.
 
    Notes:
    - Keep this conservative; more aggressive normalization can be added later with tests.
    - Goal: stable IDs for trivially equivalent whitespace variants.
    """
    # Strip and collapse internal whitespace to single spaces
    return " ".join(raw.strip().split())
 
 
def _sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
 
 
def run_acquire(
    cfg: RefpipeConfig,
    citations_path: str | Path,
    *,
    run_id: str | None = None,
) -> AcquireResult:
    """
    Acquire PDFs for a list of citation strings (Milestone B2.5 stub).
 
    Contract (B2.5):
    - Writes run-local artifacts only under `<runs_root>/<run_id>/...`.
    - MUST NOT write into `library_pdfs/` or `quarantine_pdfs/`.
    - Network download may be stubbed; initial status is "unresolved".
 
    Artifacts written:
    - `citations_input.jsonl`
    - `citation_resolution.jsonl`
    - `acquire_manifest.csv`
    - `acquired_pdfs/` (directory)
    """
    citations_path = Path(citations_path)
    if not citations_path.exists():
        raise FileNotFoundError(f"Citations file not found: {citations_path}")
    if not citations_path.is_file():
        raise FileNotFoundError(f"Citations path is not a file: {citations_path}")
 
    collected_at_utc = datetime.now(timezone.utc)
    if run_id is None:
        run_id = build_run_id(collected_at_utc)
 
    runs_root = Path(cfg.paths.runs_root)
    run_dir = runs_root / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
 
    acquired_pdfs_dir = run_dir / "acquired_pdfs"
    acquired_pdfs_dir.mkdir(parents=True, exist_ok=False)
 
    citations_input_path = run_dir / "citations_input.jsonl"
    citation_resolution_path = run_dir / "citation_resolution.jsonl"
    acquire_manifest_path = run_dir / "acquire_manifest.csv"
 
    # Read lines and keep original line numbers (1-based)
    raw_lines = citations_path.read_text(encoding="utf-8").splitlines()
 
    citations: list[dict[str, object]] = []
    for idx, raw in enumerate(raw_lines, start=1):
        if not raw.strip():
            continue
 
        normalized = _normalize_citation_text(raw)
        citation_sha = _sha256_text(normalized)
 
        citations.append(
            {
                "run_id": run_id,
                "citation_id": citation_sha,
                "line_number": idx,
                "raw_text": raw,
                "normalized_text": normalized,
                "ingested_at_utc": collected_at_utc.isoformat(),
            }
        )
 
    # Write citations_input.jsonl
    with citations_input_path.open("w", encoding="utf-8", newline="\n") as f:
        for rec in citations:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
 
    # Write citation_resolution.jsonl (stub: unresolved for all)
    with citation_resolution_path.open("w", encoding="utf-8", newline="\n") as f:
        for rec in citations:
            f.write(
                json.dumps(
                    {
                        "run_id": run_id,
                        "citation_id": rec["citation_id"],
                        "final_status": "unresolved",
                        "doi_candidate": None,
                        "openalex_id_candidate": None,
                        "selected_pdf_url": None,
                        "downloaded_path": None,
                        "http_status": None,
                        "content_type": None,
                        "bytes": None,
                        "recorded_at_utc": collected_at_utc.isoformat(),
                        "notes": "B2.5 stub (no resolver/download implemented yet).",
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
 
    # Write acquire_manifest.csv (operator-friendly summary)
    with acquire_manifest_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "run_id",
                "citation_id",
                "line_number",
                "status",
                "selected_pdf_url",
                "downloaded_path",
            ],
        )
        w.writeheader()
        for rec in citations:
            w.writerow(
                {
                    "run_id": run_id,
                    "citation_id": rec["citation_id"],
                    "line_number": rec["line_number"],
                    "status": "unresolved",
                    "selected_pdf_url": "",
                    "downloaded_path": "",
                }
            )
 
    return AcquireResult(
        run_id=run_id,
        run_dir=run_dir,
        citations_input_path=citations_input_path,
        citation_resolution_path=citation_resolution_path,
        acquire_manifest_path=acquire_manifest_path,
        acquired_pdfs_dir=acquired_pdfs_dir,
        citation_count=len(citations),
        collected_at_utc=collected_at_utc,
    )
