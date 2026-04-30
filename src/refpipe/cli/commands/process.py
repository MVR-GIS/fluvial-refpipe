from __future__ import annotations
from refpipe.config import RefpipeConfig

import typer


def process(config: str = typer.Option(..., "--config", help="Path to config YAML.")) -> None:
    """
    For candidate+ items: run GROBID TEI extraction (cached), normalize, classify, and enrich (OpenAlex).

    Outputs
    -------
    - doc_registry (tabular)
    - quarantine review queue
    - cache updates under state/caches/
    """
    _ = RefpipeConfig.from_yaml(config)
    raise NotImplementedError
