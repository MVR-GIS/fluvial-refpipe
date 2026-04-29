---
id: "0005"
title: "Policy 1 thresholds and copy/quarantine/skip actions"
date: "2026-04-29"
status: "accepted"
repo: "MVR-GIS/fluvial-refpipe"
tags:
  - "policy"
  - "quarantine"
  - "ingestion"
supersedes: []
superseded_by: ""
related_commits: []
---

# ADR 0005: Policy 1 thresholds and copy/quarantine/skip actions

## Context
The system must avoid polluting the curated library with low-quality or irrelevant documents, while still capturing candidates for later review. Operators need a deterministic policy with a quarantine lane.

## Decision
Define Policy 1 thresholds:
- `candidate_threshold = 0.30`
- `ingest_threshold = 0.65`

Actions:
- Curated if `score_ingest >= ingest_threshold` OR allowlisted
- Quarantine if `candidate_threshold <= score_ingest < ingest_threshold`
- Skip otherwise

Additionally:
- Quarantine items MUST still receive TEI extraction + enrichment to support review.

## Rationale
- Provides a deterministic ingestion rule.
- Quarantine supports human-in-the-loop review without blocking the pipeline.
- Enriching quarantine items improves decision quality later.

## Consequences
### Positive
- Limits curated library noise.
- Maintains an evidence-rich quarantine queue.

### Negative / tradeoffs
- Thresholds may require tuning; changes must be versioned and auditable.
- Quarantine processing increases compute/storage.

### Follow-ups
- Define allowlist mechanism (by sha256? DOI? title pattern?).
- Record decision rationale per document (signals) in logs.

## Alternatives considered
- Binary accept/reject: rejected (no quarantine lane).
- Manual review-only: rejected (too slow; doesn’t scale).

## Links
- Design: `dev/10_design.md#policy-1-copy--quarantine--skip`