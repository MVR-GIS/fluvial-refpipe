from __future__ import annotations

import typer

from .commands.chunk import chunk
from .commands.copy import copy
from .commands.export import export
from .commands.parse import parse
from .commands.process import process
from .commands.rescore_quarantine import rescore_quarantine
from .commands.scan import scan

app = typer.Typer(
    help="Fluvial reference pipeline: scan → extract → enrich → copy/quarantine → parse → chunk → export.",
    no_args_is_help=True,
)

app.command()(scan)
app.command("rescore-quarantine")(rescore_quarantine)
app.command()(process)
app.command()(copy)
app.command()(parse)
app.command()(chunk)
app.command()(export)
