from __future__ import annotations

import typer

from refpipe.config import RefpipeConfig
from refpipe.stages.scan_stage import run_scan


def scan(config: str = typer.Option(..., "--config", help="Path to config YAML.")) -> None:
    """
    Scan configured source_roots for PDFs and compute sha256 identities.

    Outputs
    -------
    - Writes run artifacts under `<runs_root>/<run_id>/`:
      - `manifest.csv`

    Notes
    -----
    - This is the Milestone B2 implementation: it does NOT update shared catalogs yet.
    """
    cfg = RefpipeConfig.from_yaml(config)
    result = run_scan(cfg)

    typer.echo(f"Wrote manifest: {result.manifest_path}")
    typer.echo(f"PDFs observed: {result.pdf_count}")
    typer.echo(f"run_id: {result.run_id}")
