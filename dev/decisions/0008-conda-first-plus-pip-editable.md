---
id: "0008"
title: "Conda-first environment management with pip editable installs for local package"
date: "2026-04-29"
status: "accepted"
repo: "MVR-GIS/fluvial-refpipe"
tags:
  - "python"
  - "packaging"
  - "conda"
  - "developer-experience"
supersedes: []
superseded_by: ""
related_commits: []
---

# ADR 0008: Conda-first environment management with pip editable installs for local package

## Context
This project targets Windows workstations and will use compiled dependencies (e.g., pyarrow, lxml, ML libs). We need a reproducible environment story that works for analysts and supports a CLI entrypoint.

## Decision
- Use Miniforge + mamba and `environment.yml` as the dependency source of truth.
- Use `pyproject.toml` for packaging metadata and console scripts.
- Install the local package into the conda env using:
  - `python -m pip install -e .`
- `pyproject.toml` MAY omit dependency lists when conda is the source of truth.

## Rationale
- Conda-forge is strong for compiled deps on Windows.
- Pip editable installs provide a standard Python dev loop and CLI entrypoint behavior.
- Separating “deps vs package metadata” keeps internal tooling simple.

## Consequences
### Positive
- Reliable installs on Windows for heavy deps.
- Good developer experience: code changes reflected immediately.
- Standard CLI (`refpipe`) works once installed.

### Negative / tradeoffs
- Developers must understand “pip inside conda” (document in runbook).
- Requires consistent activation of the conda env in terminals.

### Follow-ups
- Document “supported terminal” guidance and common activation errors.
- Add minimal smoke tests verifying imports and CLI help.

## Alternatives considered
- pip/venv only: rejected (Windows compiled deps friction).
- poetry-managed env: rejected for now (adds complexity; not needed for internal tool).

## Links
- Design: `dev/10_design.md#python-project-management-developer-workflow`