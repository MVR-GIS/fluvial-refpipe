---
id: "0007"
title: "Hybrid chunking with separate references corpus"
date: "2026-04-29"
status: "accepted"
repo: "MVR-GIS/fluvial-refpipe"
tags:
  - "chunking"
  - "tei"
  - "rag"
  - "references"
supersedes: []
superseded_by: ""
related_commits: []
---

# ADR 0007: Hybrid chunking with separate references corpus

## Context
Downstream embedding/RAG requires chunks that are:
- semantically coherent,
- traceable back to page/element spans,
- constrained by size/token limits,
- robust to imperfect parsing.

References sections are often noisy and should be queryable separately.

## Decision
- Use a hybrid chunking approach:
  1) structure-first segmentation (TEI/headings) into coherent segments
  2) fallback heading-based segmentation if TEI is partial/missing
  3) element-level semantic chunking to enforce chunk sizing while preserving traceability
- Export two corpora:
  - `chunks_main.jsonl`
  - `chunks_references.jsonl`

## Rationale
- Structure-first improves coherence versus naive fixed-window chunking.
- Semantic chunking improves relevance while obeying size constraints.
- Separating references reduces noise for typical queries while retaining provenance.

## Consequences
### Positive
- Higher-quality chunks for retrieval.
- Strong auditability (element/page span lineage).
- Cleaner “main narrative” corpus.

### Negative / tradeoffs
- More complex implementation and more parameters to version.
- Requires careful metadata propagation from parse → chunk.

### Follow-ups
- Define chunk schema and required lineage fields in `dev/40_schemas.md`.
- Define deterministic chunk IDs and parameter hashing.

## Alternatives considered
- Fixed-size sliding windows: rejected (breaks coherence; weak traceability).
- Semantic-only chunking without structure: rejected (more brittle; less deterministic).

## Links
- Design: `dev/10_design.md#chunking-design-hybrid-option`