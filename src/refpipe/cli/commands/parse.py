from __future__ import annotations
from refpipe.config import RefpipeConfig

import typer


def parse(config: str = typer.Option(..., "--config", help="Path to config YAML.")) -> None:
    """
    Parse curated PDFs (default) into unstructured elements.jsonl.
    """
    _ = RefpipeConfig.from_yaml(config)
    raise NotImplementedError
