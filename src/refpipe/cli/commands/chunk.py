from __future__ import annotations
from refpipe.config import RefpipeConfig

import typer


def chunk(config: str = typer.Option(..., "--config", help="Path to config YAML.")) -> None:
    """
    Hybrid chunking (Option 4): TEI/structure segmentation + element-level semantic chunking.

    References Handling
    -------------------
    Output two corpora by default:
    - chunks_main.jsonl
    - chunks_references.jsonl
    """
    _ = RefpipeConfig.from_yaml(config)
    raise NotImplementedError
