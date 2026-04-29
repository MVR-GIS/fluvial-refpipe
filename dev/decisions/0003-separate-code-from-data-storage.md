---
id: "0003"
title: "Separate code (Git) from data/state (agency filesystem)"
date: "2026-04-29"
status: "accepted"
repo: "MVR-GIS/fluvial-refpipe"
tags:
  - "operations"
  - "storage"
  - "reproducibility"
supersedes: []
superseded_by: ""
related_commits: []
---

# ADR 0003: Separate code (Git) from data/state (agency filesystem)

## Context
The pipeline produces large artifacts (PDF corpora, TEI, parse elements, chunks, exports) and relies on durable state catalogs. Storing these in Git would be impractical and would undermine reviewability.

## Decision
- Git repository MUST store: code, docs, config templates, schemas, tiny test fixtures only.
- Agency filesystem MUST store: PDFs, durable state catalogs, caches, and run artifacts.
- Default root for operational data is `R:/FluvialGeomorph/references/` (configurable).

## Rationale
- Keeps Git history clean and reviewable.
- Allows large files and iterative artifacts without bloating the repo.
- Aligns with audit and operations needs on Windows network drives.

## Consequences
### Positive
- Lightweight repo; faster clones; clearer code review.
- State and runs can scale independently of Git.

### Negative / tradeoffs
- Requires careful path configuration and documentation.
- Sharing “state” requires filesystem access, not git clone alone.

### Follow-ups
- Provide `config.example.yml` with explicit root paths and explanation.
- Add runbook guidance for initializing the data root.

## Alternatives considered
- Store state in Git LFS: rejected (still heavy; adds operational complexity).
- Store everything under repo directory: rejected (too large; brittle on Windows paths).

## Links
- Design: `dev/10_design.md#storage-layout-on-agency-filesystem-source-of-truth-for-data`