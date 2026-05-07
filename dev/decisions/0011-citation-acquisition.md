---
id: "0011"
title: "Citation acquisition: open/legal-only sources; resolver order; provenance logging"
date: "2026-05-07"
status: "proposed"
repo: "MVR-GIS/fluvial-refpipe"
tags:
  - "acquire"
  - "policy"
  - "provenance"
  - "open-access"
supersedes: []
superseded_by: ""
related_commits: []
---

# ADR 0011: Citation acquisition: open/legal-only sources; resolver order; provenance logging

## Context
A new use case requires starting from a list of citation reference strings (e.g., copied from a References section) and retrieving full-text (or best-available) PDFs for downstream TEI extraction, chunking, and export.

This introduces external network interactions and potential ambiguity (wrong matches, paywalls, non-PDF landing pages). The pipeline must remain auditable and avoid polluting curated storage.

## Decision
1) Add an upstream pipeline stage `acquire` that:
- accepts a citations text file (one citation per line),
- performs best-effort resolution and download,
- writes only run-local artifacts under `runs/<run_id>/...`,
- requires an explicit `scan` of `runs/<run_id>/acquired_pdfs/` to enter the normal pipeline (SHA256 identity boundary).

2) Allowed sources policy (initial):
- Only open/legal sources are permitted for automated download (`open_access_only`).

3) Resolver order (initial; additive later):
- Extract DOI from citation text if present.
- Use OpenAlex DOI lookup when DOI is present.
- Use OpenAlex title-search when DOI is absent, with conservative matching thresholds.
- Download only when the chosen URL appears to be a PDF and passes policy gates.

4) Provenance logging (required):
- Record attempted resolvers, selected match rationale/confidence, URLs attempted, HTTP status, content-type checks, timestamps, and outcomes.

## Rationale
- Keeps acquisition auditable and separate from ingestion QA (Policy 1).
- Preserves core invariants: document identity remains SHA256 of PDF bytes.
- Allows future extension to institutional access methods without redesigning downstream stages.

## Consequences
### Positive
- Supports citation-first workflows while reusing the existing pipeline.
- Clear audit trail for downloads and failures.
- Avoids silent writes into curated/quarantine libraries.

### Negative / tradeoffs
- Acquisition may fail frequently for paywalled material under the open-only policy.
- Requires careful matching to avoid wrong-PDF downloads.
- Adds new operator steps (per-run acquisition scan config).

## Alternatives considered
- Integrate acquisition into `scan`: rejected (blurs responsibilities; makes scan network-touching).
- Treat citations as first-class documents without PDFs: rejected (conflicts with SHA256-of-PDF identity model).

## Follow-ups
- Define the minimum viable citation normalization and matching algorithm.
- Define which OpenAlex fields/links qualify as open/legal downloadable sources.
- Add tests and fixtures for representative citation formats.
