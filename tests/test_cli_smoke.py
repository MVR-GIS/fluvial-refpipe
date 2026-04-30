from __future__ import annotations

from typer.testing import CliRunner

from refpipe.cli import app


runner = CliRunner()

def test_import_refpipe() -> None:
    import refpipe  # noqa: F401

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

def test_refpipe_process_help_exits_zero() -> None:
    result = runner.invoke(app, ["process", "--help"])
    assert result.exit_code == 0
    assert "--config" in result.stdout

def test_refpipe_copy_help_exits_zero() -> None:
    result = runner.invoke(app, ["copy", "--help"])
    assert result.exit_code == 0
    assert "--config" in result.stdout

def test_refpipe_rescore_quarantine_help_exits_zero() -> None:
    result = runner.invoke(app, ["rescore-quarantine", "--help"])
    assert result.exit_code == 0
    assert "--config" in result.stdout

def test_refpipe_parse_help_exits_zero() -> None:
    result = runner.invoke(app, ["parse", "--help"])
    assert result.exit_code == 0
    assert "--config" in result.stdout

def test_refpipe_chunk_help_exits_zero() -> None:
    result = runner.invoke(app, ["chunk", "--help"])
    assert result.exit_code == 0
    assert "--config" in result.stdout

def test_refpipe_export_help_exits_zero() -> None:
    result = runner.invoke(app, ["export", "--help"])
    assert result.exit_code == 0
    assert "--config" in result.stdout
