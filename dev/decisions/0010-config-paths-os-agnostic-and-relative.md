---
id: "0010"
title: "Allow OS-agnostic paths in operator config (relative paths allowed; resolved relative to config file)"
date: "2026-04-30"
status: "accepted"
repo: "MVR-GIS/fluvial-refpipe"
tags:
  - "config"
  - "developer-experience"
  - "portability"
  - "contract"
supersedes: []
superseded_by: ""
related_commits: []
---

# ADR 0010: Allow OS-agnostic paths in operator config (relative paths allowed; resolved relative to config file)

## Context

Early versions of the operator config required Windows absolute drive paths (e.g., `R:/...`, `C:/...`) and disallowed relative paths.

During Milestone B2 (scan + manifest writing), we needed to add durable automated tests. The Windows-drive-only requirement made it difficult to use ephemeral test directories and prevented writing OS-agnostic code and tests.

## Decision

The operator YAML config passed via `--config` will accept:
- absolute paths (Windows or POSIX), and
- relative paths.

Relative paths MUST be resolved relative to the directory containing the config file.

YAML remains literal-only (no env-var interpolation).

## Rationale

- Enables OS-agnostic development and future CI portability.
- Enables clean tests using temporary directories without special drive-path workarounds.
- Preserves reproducibility by using a deterministic resolution rule (relative-to-config-file).

## Consequences

### Positive
- Better developer experience; fewer environment-specific constraints.
- Tests can use `tmp_path`-style directories naturally.

### Negative / tradeoffs
- Operators must understand relative-path resolution semantics.
- Some configs may become less explicit if overusing relative paths (mitigated by documentation and examples).

## Follow-ups
- Update `dev/40_schemas.md` to reflect OS-agnostic / relative path semantics.
- Update `dev/30_runbook.md` to document the resolution rule and provide examples.
- Update `src/refpipe/config.py` validation accordingly.