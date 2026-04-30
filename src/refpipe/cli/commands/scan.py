from __future__ import annotations

import typer


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
