from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator


def _is_windows_drive_path(p: str) -> bool:
    # Accepts e.g. "R:/x" or "R:\\x"
    return len(p) >= 3 and p[1] == ":" and (p[2] == "/" or p[2] == "\\")


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

    @field_validator("library_pdfs", "quarantine_pdfs", "state_root", "runs_root")
    @classmethod
    def _must_be_windows_drive_path(cls, v: str) -> str:
        if not _is_windows_drive_path(v):
            raise ValueError(f"must be a Windows drive path like 'R:/...'; got: {v!r}")
        return v


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
    """

    paths: Paths
    scan: ScanConfig
    thresholds: Thresholds = Field(default_factory=Thresholds)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "RefpipeConfig":
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Config file not found: {p}")
        data: dict[str, Any]
        with p.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        try:
            return cls.model_validate(data)
        except ValidationError as e:
            # Re-raise with context for CLI display
            raise ValueError(f"Invalid config: {p}\n{e}") from e
