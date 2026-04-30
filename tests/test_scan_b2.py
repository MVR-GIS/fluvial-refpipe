from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import pytest

from refpipe.cli.commands.scan import scan


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        return list(r)


def _expected_sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def test_scan_writes_manifest_with_expected_columns_and_sha(tmp_path: Path) -> None:
    runs_root = tmp_path / "runs"
    source_root = tmp_path / "incoming"
    source_root.mkdir(parents=True, exist_ok=True)

    pdf_bytes = b"%PDF-1.4\nhello\n%%EOF\n"
    pdf_path = source_root / "a.pdf"
    pdf_path.write_bytes(pdf_bytes)

    config_path = tmp_path / "config.yml"
    _write_text(
        config_path,
        "\n".join(
            [
                "paths:",
                f'  library_pdfs: "C:/workspace/_refpipe_dev/library_pdfs"',
                f'  quarantine_pdfs: "C:/workspace/_refpipe_dev/quarantine_pdfs"',
                f'  state_root: "C:/workspace/_refpipe_dev/state"',
                f'  runs_root: "{runs_root.as_posix()}"',
                "scan:",
                "  source_roots:",
                f'    - "{source_root.as_posix()}"',
                "thresholds:",
                "  candidate_threshold: 0.30",
                "  ingest_threshold: 0.65",
                "",
            ]
        ),
    )

    # Execute scan (creates a run folder under runs_root)
    scan(config=str(config_path))

    # Find the run folder created
    run_dirs = [p for p in runs_root.iterdir() if p.is_dir()]
    assert len(run_dirs) == 1
    run_dir = run_dirs[0]

    manifest_path = run_dir / "manifest.csv"
    assert manifest_path.exists()

    rows = _read_manifest(manifest_path)
    assert len(rows) == 1

    row = rows[0]
    assert set(row.keys()) == {
        "run_id",
        "collected_at_utc",
        "document_sha256",
        "document_id",
        "last_observed_path",
    }

    sha = _expected_sha256(pdf_bytes)
    assert row["document_sha256"] == sha
    assert row["document_id"] == f"sha256:{sha}"
    assert row["last_observed_path"].endswith("a.pdf")


def test_scan_manifest_order_is_deterministic(tmp_path: Path) -> None:
    runs_root = tmp_path / "runs"
    source_root = tmp_path / "incoming"
    source_root.mkdir(parents=True, exist_ok=True)

    # Deliberately create out-of-order names
    (source_root / "b.pdf").write_bytes(b"bbb")
    (source_root / "a.pdf").write_bytes(b"aaa")

    config_path = tmp_path / "config.yml"
    _write_text(
        config_path,
        "\n".join(
            [
                "paths:",
                f'  library_pdfs: "C:/workspace/_refpipe_dev/library_pdfs"',
                f'  quarantine_pdfs: "C:/workspace/_refpipe_dev/quarantine_pdfs"',
                f'  state_root: "C:/workspace/_refpipe_dev/state"',
                f'  runs_root: "{runs_root.as_posix()}"',
                "scan:",
                "  source_roots:",
                f'    - "{source_root.as_posix()}"',
                "",
            ]
        ),
    )

    scan(config=str(config_path))

    run_dirs = [p for p in runs_root.iterdir() if p.is_dir()]
    assert len(run_dirs) == 1
    run_dir = run_dirs[0]

    rows = _read_manifest(run_dir / "manifest.csv")
    assert [Path(r["last_observed_path"]).name for r in rows] == ["a.pdf", "b.pdf"]
