from __future__ import annotations
 
from pathlib import Path
 
import pytest
 
from refpipe.config import RefpipeConfig
from refpipe.stages.acquire_stage import run_acquire
 
 
def _write_config(tmp_path: Path) -> Path:
    runs_root = tmp_path / "runs"
    runs_root.mkdir(parents=True, exist_ok=True)
 
    # Minimal config for acquire: paths must exist/resolve; scan roots can be any existing dir
    incoming = tmp_path / "incoming"
    incoming.mkdir(parents=True, exist_ok=True)
 
    config_path = tmp_path / "config.yml"
    config_path.write_text(
        "\n".join(
            [
                "paths:",
                f'  library_pdfs: "{(tmp_path / "library_pdfs").as_posix()}"',
                f'  quarantine_pdfs: "{(tmp_path / "quarantine_pdfs").as_posix()}"',
                f'  state_root: "{(tmp_path / "state").as_posix()}"',
                f'  runs_root: "{runs_root.as_posix()}"',
                "scan:",
                "  source_roots:",
                f'    - "{incoming.as_posix()}"',
                "",
            ]
        ),
        encoding="utf-8",
    )
 
    # Ensure referenced dirs exist (acquire itself only uses runs_root, but config model validates strings)
    (tmp_path / "library_pdfs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "quarantine_pdfs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "state").mkdir(parents=True, exist_ok=True)
 
    return config_path
 
 
def test_acquire_b25_writes_expected_run_artifacts(tmp_path: Path) -> None:
    config_path = _write_config(tmp_path)
    cfg = RefpipeConfig.from_yaml(config_path)
 
    citations_path = tmp_path / "citations.txt"
    citations_path.write_text(
        "\n".join(
            [
                "Smith, J. (2020). Some paper. Journal of Things, 12(3), 1-10.",
                "",
                "  Doe, A. 2019. Another Paper. Conference on Stuff.  ",
            ]
        ),
        encoding="utf-8",
    )
 
    result = run_acquire(cfg, citations_path=citations_path, run_id="TEST_RUN")
 
    assert result.run_id == "TEST_RUN"
    assert result.run_dir.exists()
 
    # Directory contract
    assert result.acquired_pdfs_dir.exists()
    assert result.acquired_pdfs_dir.is_dir()
 
    # File contract
    assert result.citations_input_path.exists()
    assert result.citation_resolution_path.exists()
    assert result.acquire_manifest_path.exists()
 
    # Content sanity
    citations_lines = result.citations_input_path.read_text(encoding="utf-8").splitlines()
    resolution_lines = result.citation_resolution_path.read_text(encoding="utf-8").splitlines()
 
    # blank line skipped => 2 citations
    assert len(citations_lines) == 2
    assert len(resolution_lines) == 2
 
    manifest_text = result.acquire_manifest_path.read_text(encoding="utf-8")
    assert "citation_id" in manifest_text
    assert "unresolved" in manifest_text
 
    # Ensure we did not accidentally write any PDFs (stub)
    assert list(result.acquired_pdfs_dir.glob("*.pdf")) == []
