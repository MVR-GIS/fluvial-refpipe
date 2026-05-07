from __future__ import annotations
 
from pathlib import Path
 
import typer
 
from refpipe.config import RefpipeConfig
from refpipe.stages.acquire_stage import run_acquire
 
 
def acquire(
    config: str = typer.Option(..., "--config", help="Path to config YAML."),
    citations: str = typer.Option(
        ...,
        "--citations",
        help="Path to citations text file (one citation per line).",
    ),
) -> None:
    """
    Acquire PDFs for a list of citation strings (planned; Milestone B2.5 stub).
 
    This command writes run-local artifacts under `<runs_root>/<run_id>/...` including:
    - citations_input.jsonl
    - citation_resolution.jsonl
    - acquire_manifest.csv
    - acquired_pdfs/ (directory)
 
    After running `acquire`, the operator MUST explicitly run `scan` against the run-local
    `acquired_pdfs/` folder using an untracked per-run config (see runbook).
    """
    cfg = RefpipeConfig.from_yaml(config)
    result = run_acquire(cfg, citations_path=Path(citations))
    typer.echo(f"run_id: {result.run_id}")
    typer.echo(f"run_dir: {result.run_dir}")
    typer.echo(f"citations: {result.citation_count}")
    typer.echo(f"acquired_pdfs_dir: {result.acquired_pdfs_dir}")
