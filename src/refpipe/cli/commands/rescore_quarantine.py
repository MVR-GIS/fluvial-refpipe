from __future__ import annotations

import typer


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
