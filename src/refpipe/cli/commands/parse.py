from __future__ import annotations

import typer


def parse(config: str = typer.Option(..., "--config", help="Path to config YAML.")) -> None:
    """
    Parse curated PDFs (default) into unstructured elements.jsonl.
    """
    raise NotImplementedError
