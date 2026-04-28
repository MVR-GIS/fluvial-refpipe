"""
Command-line interface (CLI) for fluvial-refpipe.

Design goals
-----------
- Provide a single entrypoint command: `refpipe`
- Keep CLI functions thin wrappers around well-documented library functions
- Make it easy to discover behavior via `--help`
- Keep outputs deterministic and auditable (run_id, config snapshot, metadata)

Notes for R package developers
------------------------------
Think of each CLI command as a small wrapper around a "main" function in R:
- CLI command -> validates config -> calls a pure function -> writes outputs
- Core logic lives in importable modules so it can be unit-tested
"""

from __future__ import annotations

import typer

app = typer.Typer(
    help="Fluvial reference pipeline: scan → extract → enrich → copy/quarantine → parse → chunk → export.",
    no_args_is_help=True,
)

# --- Placeholder commands (implement progressively) ---------------------------

@app.command()
def scan(config: str = typer.Option(..., "--config", help="Path to config YAML.")) -> None:
    """
    Scan configured source_roots for PDFs and update catalogs (sha256 identity).

    Parameters
    ----------
    config:
        Path to the operator configuration YAML file (usually config/config.yml).

    Side Effects
    ------------
    - Writes run artifacts under runs/<run_id>/inventory/
    - Updates shared-drive catalogs under R:/.../state/catalogs/ (with file lock)
    - Regenerates csv views (pdf_catalog_latest.csv, curated_latest.csv, quarantine_latest.csv)
    """
    raise NotImplementedError


@app.command("rescore-quarantine")
def rescore_quarantine(
    config: str = typer.Option(..., "--config", help="Path to config YAML."),
) -> None:
    """
    Re-score quarantine items and refresh OpenAlex if stale/missing.

    This job is intended to be run after:
    - heuristic/pattern updates, or
    - periodically (e.g., monthly) to benefit from OpenAlex improvements.

    Default behavior (as decided in this project):
    - Scope: quarantine only
    - Refresh policy: refresh OpenAlex only if stale (> max_age_days) or missing
    """
    raise NotImplementedError


@app.command()
def process(config: str = typer.Option(..., "--config", help="Path to config YAML.")) -> None:
    """
    For candidate+ items: run GROBID TEI extraction (cached), normalize, classify, and enrich (OpenAlex).

    Outputs
    -------
    - doc_registry (tabular)
    - quarantine review queue
    - cache updates under state/caches/
    """
    raise NotImplementedError


@app.command()
def copy(config: str = typer.Option(..., "--config", help="Path to config YAML.")) -> None:
    """
    Apply Policy 1 (copy / quarantine / skip) and copy PDFs to library/quarantine folders by sha256.

    Idempotency
    -----------
    If destination <sha256>.pdf exists, no re-copy occurs; the action is recorded as 'exists'.
    """
    raise NotImplementedError


@app.command()
def parse(config: str = typer.Option(..., "--config", help="Path to config YAML.")) -> None:
    """
    Parse curated PDFs (default) into unstructured elements.jsonl.
    """
    raise NotImplementedError


@app.command()
def chunk(config: str = typer.Option(..., "--config", help="Path to config YAML.")) -> None:
    """
    Hybrid chunking (Option 4): TEI/structure segmentation + element-level semantic chunking.

    References Handling
    -------------------
    Output two corpora by default:
    - chunks_main.jsonl
    - chunks_references.jsonl
    """
    raise NotImplementedError


@app.command()
def export(config: str = typer.Option(..., "--config", help="Path to config YAML.")) -> None:
    """
    Export chunk corpora to Gemini JSONL and Foundry Parquet.
    """
    raise NotImplementedError
