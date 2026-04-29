---
id: "0002"
title: "Treat file paths as observations, not identifiers"
date: "2026-04-29"
status: "accepted"
repo: "MVR-GIS/fluvial-refpipe"
tags:
  - "provenance"
  - "catalogs"
  - "audit"
supersedes: []
superseded_by: ""
related_commits: []
---

# ADR 0002: Treat file paths as observations, not identifiers

## Context
PDFs originate in multiple directories and may move/rename over time. Operators still need to see “where it came from” for review and debugging, but using paths as keys breaks reproducibility.

## Decision
- The system MUST record file paths as **observations** only.
- Maintain an append-only table/log of observations: `pdf_path_observations`.
- Provide a single convenience field `last_observed_path` for human use.
- No stable join/key MUST depend on a path string.

## Rationale
This preserves provenance information without allowing unstable filesystem state to corrupt identity or joins.

## Consequences
### Positive
- Stable joins and caches (SHA256).
- Human-debuggable provenance remains available.
- Supports incremental scanning and moving/renaming files.

### Negative / tradeoffs
- Requires maintaining an additional history table.
- UI/reporting must be clear that paths are “best known last location” not truth.

### Follow-ups
- Define observation fields: observed_at, root_id/source_root, raw_path, file size, mtime (optional).
- Define how `last_observed_path` is derived (max observed_at).

## Alternatives considered
- Store only a single “original path”: rejected (becomes wrong; loses provenance).
- Canonicalize paths and treat as keys: rejected (still unstable).

## Links
- Design: `dev/10_design.md#non-negotiable-principles-invariants`