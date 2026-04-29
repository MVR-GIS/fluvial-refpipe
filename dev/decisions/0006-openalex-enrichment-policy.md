---
id: "0006"
title: "OpenAlex enrichment: DOI-first; title-search only for scholarly; stale refresh policy"
date: "2026-04-29"
status: "accepted"
repo: "MVR-GIS/fluvial-refpipe"
tags:
  - "openalex"
  - "enrichment"
  - "metadata"
supersedes: []
superseded_by: ""
related_commits: []
---

# ADR 0006: OpenAlex enrichment: DOI-first; title-search only for scholarly; stale refresh policy

## Context
We want improved bibliographic metadata and deduplication signals, but naive title search can misidentify internal reports or non-scholarly material.

We also need a refresh policy that avoids unnecessary network calls while keeping metadata reasonably current.

## Decision
- If a DOI exists, perform OpenAlex lookup by DOI for all items.
- Perform OpenAlex title-search ONLY when `doc_type_guess == scholarly`.
- Quarantine rescore job:
  - scope is quarantine only
  - refresh OpenAlex only if stale or missing
  - default `max_age_days = 30`

## Rationale
- DOI lookups are higher precision than title search.
- Restricting title search reduces false positives.
- Stale refresh balances stability, cost, and currency.

## Consequences
### Positive
- Better metadata quality where available.
- Fewer bad matches for internal/non-scholarly PDFs.
- Predictable network usage.

### Negative / tradeoffs
- Some scholarly items without DOI may not get enriched unless classified as scholarly.
- Requires defining and versioning `doc_type_guess`.

### Follow-ups
- Define what “stale” means precisely (timestamp field and comparison).
- Cache OpenAlex responses by sha256 and/or OpenAlex ID.

## Alternatives considered
- Always title-search: rejected (false positives).
- Never title-search: rejected (misses enrichments without DOI).

## Links
- Design: `dev/10_design.md#enrichment-policy-openalex`