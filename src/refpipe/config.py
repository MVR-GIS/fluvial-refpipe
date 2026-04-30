from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator


class Thresholds(BaseModel):
    candidate_threshold: float = Field(0.30, ge=0.0, le=1.0)
    ingest_threshold: float = Field(0.65, ge=0.0, le=1.0)

    @field_validator("ingest_threshold")
    @classmethod
    def _ingest_ge_candidate(cls, v: float, info):  # type: ignore[no-untyped-def]
        candidate = info.data.get("candidate_threshold")
        if candidate is not None and v < candidate:
            raise ValueError("ingest_threshold must be >= candidate_threshold")
        return v


class Paths(BaseModel):
    # Agency filesystem locations (NOT in git)
    library_pdfs: str
    quarantine_pdfs: str
    state_root: str
    runs_root: str


class ScanConfig(BaseModel):
    source_roots: list[str] = Field(..., min_length=1)

    @field_validator("source_roots")
    @classmethod
    def _nonempty_paths(cls, v: list[str]) -> list[str]:
        for p in v:
            if not p or not isinstance(p, str):
                raise ValueError("source_roots entries must be non-empty strings")
        return v


class RefpipeConfig(BaseModel):
    """
    Operator configuration for fluvial-refpipe.

    This file is intended to be a stable contract:
    - stored outside git for operator-specific values (config/config.yml),
    - example tracked in git (config/config.example.yml),
    - YAML is literal-only (no env interpolation) for reproducibility.

    Path semantics:
    - Paths in this config may be absolute or relative.
    - Relative paths are resolved relative to the directory containing the config file.
    """

    paths: Paths
    scan: ScanConfig
    thresholds: Thresholds = Field(default_factory=Thresholds)

    @staticmethod
    def _resolve_path(base_dir: Path, raw: str) -> str:
        p = Path(raw)
        if p.is_absolute():
            return str(p)
        return str((base_dir / p).resolve())

    @classmethod
    def from_yaml(cls, path: str | Path) -> "RefpipeConfig":
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        data: dict[str, Any]
        with config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        try:
            cfg = cls.model_validate(data)
        except ValidationError as e:
            raise ValueError(f"Invalid config: {config_path}\n{e}") from e

        # Resolve relative paths relative to the config file directory
        base_dir = config_path.parent

        cfg.paths.library_pdfs = cls._resolve_path(base_dir, cfg.paths.library_pdfs)
        cfg.paths.quarantine_pdfs = cls._resolve_path(base_dir, cfg.paths.quarantine_pdfs)
        cfg.paths.state_root = cls._resolve_path(base_dir, cfg.paths.state_root)
        cfg.paths.runs_root = cls._resolve_path(base_dir, cfg.paths.runs_root)

        cfg.scan.source_roots = [cls._resolve_path(base_dir, p) for p in cfg.scan.source_roots]

        return cfg
