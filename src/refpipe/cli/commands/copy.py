from __future__ import annotations
from refpipe.config import RefpipeConfig

import typer


def copy(config: str = typer.Option(..., "--config", help="Path to config YAML.")) -> None:
    """
    Apply Policy 1 (copy / quarantine / skip) and copy PDFs to library/quarantine folders by sha256.

    Idempotency
    -----------
    If destination <sha256>.pdf exists, no re-copy occurs; the action is recorded as 'exists'.
    """
    _ = RefpipeConfig.from_yaml(config)
    raise NotImplementedError
