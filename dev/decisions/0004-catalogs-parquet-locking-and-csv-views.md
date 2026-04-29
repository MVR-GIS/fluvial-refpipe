---
id: "0004"
title: "Store catalogs as Parquet with file locking; publish CSV views"
date: "2026-04-29"
status: "accepted"
repo: "MVR-GIS/fluvial-refpipe"
tags:
  - "catalogs"
  - "parquet"
  - "locking"
  - "audit"
supersedes: []
superseded_by: ""
related_commits: []
---

# ADR 0004: Store catalogs as Parquet with file locking; publish CSV views

## Context
Catalogs must persist across runs, support scale, and be robust to interruptions. Even with a single primary operator, network drives and future concurrency motivate defensive writes.

Stakeholders also need human-readable snapshots for review.

## Decision
- Durable catalogs MUST be stored as **Parquet**.
- Updates MUST use:
  - a filesystem lock (e.g., `state/catalogs/.lock`), and
  - write-then-atomic-rename semantics where feasible.
- After any catalog update, publish CSV views:
  - `pdf_catalog_latest.csv`
  - `curated_latest.csv`
  - `quarantine_latest.csv`

## Rationale
- Parquet provides stable typing and better performance than CSV for large catalogs.
- Locking + atomic writes reduce risk of partial/corrupt state.
- CSV views make review and ad hoc analysis easy without special tooling.

## Consequences
### Positive
- Scales better than CSV-only catalogs.
- Safer updates on network drives.
- Reviewers can inspect latest state via CSV.

### Negative / tradeoffs
- Requires `pyarrow` and careful I/O implementation.
- “Atomic rename” semantics can vary by filesystem; must be tested on `R:/`.

### Follow-ups
- Specify catalog schemas in `dev/40_schemas.md`.
- Implement lock stale detection and logging.
- Implement “publish views” as a callable stage/command.

## Alternatives considered
- CSV-only: rejected (typing issues, scale, corruption risk).
- SQLite: possible alternative, deferred (adds DB semantics; may be harder on shared drive).

## Links
- Design: `dev/10_design.md#catalogs-state-and-update-safety`