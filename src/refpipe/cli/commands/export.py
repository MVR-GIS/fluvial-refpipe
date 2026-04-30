from __future__ import annotations
from refpipe.config import RefpipeConfig

import typer


def export(config: str = typer.Option(..., "--config", help="Path to config YAML.")) -> None:
    """
    Export chunk corpora to Gemini JSONL and Foundry Parquet.
    """
    _ = RefpipeConfig.from_yaml(config)
    raise NotImplementedError
