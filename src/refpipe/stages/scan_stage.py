from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from refpipe.config import RefpipeConfig


@dataclass(frozen=True)
class PdfObservation:
    document_sha256: str
    document_id: str
    last_observed_path: str


@dataclass(frozen=True)
class ScanResult:
    run_id: str
    run_dir: Path
    manifest_path: Path
    pdf_count: int
    collected_at_utc: datetime


def iter_pdf_paths(source_roots: list[str]) -> list[Path]:
    pdfs: list[Path] = []
    for root in source_roots:
        root_path = Path(root)
        if not root_path.exists():
            raise FileNotFoundError(f"scan.source_roots entry does not exist: {root_path}")
        if not root_path.is_dir():
            raise NotADirectoryError(f"scan.source_roots entry is not a directory: {root_path}")

        for p in root_path.rglob("*.pdf"):
            if p.is_file():
                pdfs.append(p)

    # Deterministic order for stable manifests
    return sorted(pdfs, key=lambda x: str(x).lower())


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def build_run_id(collected_at_utc: datetime) -> str:
    # Compact, sortable, Windows-safe
    return collected_at_utc.strftime("%Y%m%dT%H%M%SZ")


def run_scan(cfg: RefpipeConfig) -> ScanResult:
    """
    Scan configured source_roots for PDFs and compute sha256 identities.

    Outputs
    -------
    - Writes run artifacts under `<runs_root>/<run_id>/`:
      - `manifest.csv`

    Notes
    -----
    - This is the Milestone B2 implementation: it does NOT update shared catalogs yet.
    - Deterministic manifest ordering is enforced by sorting observed paths.
    """
    collected_at_utc = datetime.now(timezone.utc)
    run_id = build_run_id(collected_at_utc)

    runs_root = Path(cfg.paths.runs_root)
    run_dir = runs_root / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    manifest_path = run_dir / "manifest.csv"

    pdf_paths = iter_pdf_paths(cfg.scan.source_roots)
    observations: list[PdfObservation] = []

    for pdf_path in pdf_paths:
        sha = sha256_file(pdf_path)
        observations.append(
            PdfObservation(
                document_sha256=sha,
                document_id=f"sha256:{sha}",
                last_observed_path=str(pdf_path),
            )
        )

    with manifest_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "run_id",
                "collected_at_utc",
                "document_sha256",
                "document_id",
                "last_observed_path",
            ],
        )
        w.writeheader()
        for obs in observations:
            w.writerow(
                {
                    "run_id": run_id,
                    "collected_at_utc": collected_at_utc.isoformat(),
                    "document_sha256": obs.document_sha256,
                    "document_id": obs.document_id,
                    "last_observed_path": obs.last_observed_path,
                }
            )

    return ScanResult(
        run_id=run_id,
        run_dir=run_dir,
        manifest_path=manifest_path,
        pdf_count=len(observations),
        collected_at_utc=collected_at_utc,
    )
