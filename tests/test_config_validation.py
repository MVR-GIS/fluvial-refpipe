from __future__ import annotations

from pathlib import Path

import pytest

from refpipe.config import RefpipeConfig


def test_config_example_validates(tmp_path: Path) -> None:
    # minimal valid config yaml
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


def test_paths_allow_relative_and_resolve_relative_to_config_dir(tmp_path: Path) -> None:
    # Layout:
    #   tmp_path/
    #     cfg/config.yml
    #     data/incoming_pdfs/a.pdf
    #     out/{library_pdfs, quarantine_pdfs, state, runs}
    cfg_dir = tmp_path / "cfg"
    data_dir = tmp_path / "data" / "incoming_pdfs"
    out_dir = tmp_path / "out"

    cfg_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    (data_dir / "a.pdf").write_bytes(b"%PDF-1.4\nhello\n%%EOF\n")

    cfg_path = cfg_dir / "config.yml"
    cfg_path.write_text(
        """
paths:
  library_pdfs: "../out/library_pdfs"
  quarantine_pdfs: "../out/quarantine_pdfs"
  state_root: "../out/state"
  runs_root: "../out/runs"
scan:
  source_roots:
    - "../data/incoming_pdfs"
""".lstrip(),
        encoding="utf-8",
    )

    cfg = RefpipeConfig.from_yaml(cfg_path)

    assert Path(cfg.paths.library_pdfs) == (cfg_dir / "../out/library_pdfs").resolve()
    assert Path(cfg.paths.quarantine_pdfs) == (cfg_dir / "../out/quarantine_pdfs").resolve()
    assert Path(cfg.paths.state_root) == (cfg_dir / "../out/state").resolve()
    assert Path(cfg.paths.runs_root) == (cfg_dir / "../out/runs").resolve()

    assert [Path(p) for p in cfg.scan.source_roots] == [(cfg_dir / "../data/incoming_pdfs").resolve()]


def test_absolute_paths_are_preserved(tmp_path: Path) -> None:
    # Use tmp_path absolute paths; render with forward slashes to keep YAML parsing simple on Windows.
    runs_root = (tmp_path / "runs_abs").resolve().as_posix()
    incoming = (tmp_path / "incoming_abs").resolve().as_posix()
    (tmp_path / "incoming_abs").mkdir(parents=True, exist_ok=True)

    library = (tmp_path / "library").resolve().as_posix()
    quarantine = (tmp_path / "quarantine").resolve().as_posix()
    state = (tmp_path / "state").resolve().as_posix()

    cfg = tmp_path / "config.yml"
    cfg.write_text(
        "\n".join(
            [
                "paths:",
                f'  library_pdfs: "{library}"',
                f'  quarantine_pdfs: "{quarantine}"',
                f'  state_root: "{state}"',
                f'  runs_root: "{runs_root}"',
                "scan:",
                "  source_roots:",
                f'    - "{incoming}"',
                "",
            ]
        ),
        encoding="utf-8",
    )

    parsed = RefpipeConfig.from_yaml(cfg)
    assert Path(parsed.paths.runs_root) == Path(runs_root)
    assert [Path(p) for p in parsed.scan.source_roots] == [Path(incoming)]


def test_missing_config_file_raises_file_not_found(tmp_path: Path) -> None:
    missing = tmp_path / "nope.yml"
    with pytest.raises(FileNotFoundError, match="Config file not found"):
        _ = RefpipeConfig.from_yaml(missing)
