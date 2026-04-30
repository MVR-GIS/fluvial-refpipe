from __future__ import annotations

from typer.testing import CliRunner

from refpipe.cli import app


runner = CliRunner()


def test_refpipe_help_exits_zero() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    # keep assertions resilient but meaningful
    assert "Fluvial reference pipeline" in result.stdout
    assert "Commands" in result.stdout


def test_refpipe_scan_help_exits_zero() -> None:
    result = runner.invoke(app, ["scan", "--help"])
    assert result.exit_code == 0
    assert "--config" in result.stdout
