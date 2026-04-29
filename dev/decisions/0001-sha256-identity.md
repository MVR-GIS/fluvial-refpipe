---
id: "0001"
title: "Use SHA256 of PDF bytes as the stable document identity"
date: "2026-04-29"
status: "accepted"
repo: "MVR-GIS/fluvial-refpipe"
tags:
  - "identity"
  - "deduplication"
  - "provenance"
supersedes: []
superseded_by: ""
related_commits: []
---

# ADR 0001: Use SHA256 of PDF bytes as the stable document identity

## Context
The pipeline must ingest PDFs from multiple evolving source roots where:
- paths and filenames change over time,
- duplicates exist across folders,
- incremental scanning will be performed repeatedly,
- reproducibility and auditability are required.

We need a stable identifier that supports deduplication and stable joins across catalogs and run artifacts.

## Decision
- Document identity MUST be computed as **SHA256 hash of the raw PDF bytes**.
- The canonical identifier string MUST be `document_id = "sha256:<hex>"`.
- All joins across catalogs, caches, and run artifacts MUST use SHA256 (not paths).
- Curated/quarantine library storage MUST name PDFs as `<sha256>.pdf`.

## Rationale
- Content hashing provides stable identity independent of filesystem layout.
- SHA256 is widely supported, deterministic, and collision-resistant for this use case.
- Enables idempotent copying, caching, and deduplication.

## Consequences
### Positive
- Robust deduplication across source roots.
- Stable, deterministic identity for caching (GROBID TEI, OpenAlex enrichment).
- Easier audit trail: every output can reference a stable `document_id`.

### Negative / tradeoffs
- Requires reading full PDF bytes (cost proportional to file size).
- Changes to PDF bytes (even metadata changes) create a new identity.

### Follow-ups
- Define where SHA256 is computed (scan stage) and persisted (catalog schema).
- Document byte-reading strategy (streamed hashing) to minimize memory use.

## Alternatives considered
- Path-based identity: rejected (paths unstable, duplicates).
- Filename-based identity: rejected (collisions, instability).
- DOI-based identity: rejected (not all PDFs have DOIs; also DOI may be unknown until later).

## Links
- Design: `dev/10_design.md#non-negotiable-principles-invariants`
