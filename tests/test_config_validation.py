from __future__ import annotations

from pathlib import Path

import pytest

from refpipe.config import RefpipeConfig


def test_config_example_validates(tmp_path: Path) -> None:
    # create a minimal valid config yaml in tmp
    cfg = tmp_path / "config.yml"
    cfg.write_text(
        """
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
""".lstrip(),
        encoding="utf-8",
    )
    _ = RefpipeConfig.from_yaml(cfg)


def test_ingest_threshold_must_be_ge_candidate(tmp_path: Path) -> None:
    cfg = tmp_path / "bad.yml"
    cfg.write_text(
        """
paths:
  library_pdfs: "R:/a"
  quarantine_pdfs: "R:/b"
  state_root: "R:/c"
  runs_root: "R:/d"
scan:
  source_roots: ["R:/incoming"]
thresholds:
  candidate_threshold: 0.80
  ingest_threshold: 0.65
""".lstrip(),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="ingest_threshold must be >= candidate_threshold"):
        _ = RefpipeConfig.from_yaml(cfg)


def test_paths_must_be_windows_drive_paths(tmp_path: Path) -> None:
    cfg = tmp_path / "bad_paths.yml"
    cfg.write_text(
        """
paths:
  library_pdfs: "/tmp/library"
  quarantine_pdfs: "R:/q"
  state_root: "R:/s"
  runs_root: "R:/r"
scan:
  source_roots: ["R:/incoming"]
""".lstrip(),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="must be a Windows drive path"):
        _ = RefpipeConfig.from_yaml(cfg)
