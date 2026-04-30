from __future__ import annotations

import typer


def export(config: str = typer.Option(..., "--config", help="Path to config YAML.")) -> None:
    """
    Export chunk corpora to Gemini JSONL and Foundry Parquet.
    """
    raise NotImplementedError
