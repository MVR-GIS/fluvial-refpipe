# process-docs — Overlay Module (Process Documentation + ADR Discipline)

This module defines a documentation discipline intended to scale across projects.
It ensures the repository remains reviewable by humans and provides stable context for future AI-assisted development.

---

## Purpose of process documentation (required)

Process documentation exists for two audiences:

1) **Human reviewers / colleagues (QAQC + shared understanding)**
   - Make assumptions, invariants, and tradeoffs explicit.
   - Enable peers to validate outputs and assess correctness.

2) **Future chat sessions / AI-driven development**
   - Provide stable, authoritative context so future sessions can extend functionality without re-deriving prior decisions.
   - Reduce hallucination risk by grounding work in repository docs.

---

## Canonical documentation set under `dev/` (required)

Repositories adopting this module MUST maintain these canonical docs (filenames may be repo-specific, but must be explicit and stable):

1) `dev/10_design.md` — architecture overview (“what is true”)
   - Stable description of architecture, invariants, boundaries, and definitions of done.
   - Links to ADRs instead of duplicating rationale.

2) `dev/decisions/*.md` — ADRs (“why we chose it”)
   - One ADR per significant decision.
   - ADRs MUST include YAML front-matter (id/title/date/status/tags).
   - ADRs are append-only records:
     - Prefer new ADR + mark prior as `superseded` instead of rewriting history.

3) `dev/30_runbook.md` — operations (“how to run it”)
   - Step-by-step operator procedures.
   - Troubleshooting notes for expected environment/platform issues.

4) `dev/40_schemas.md` — schemas (“exact fields/types”)
   - Authoritative field definitions for catalogs and outputs.
   - Must be updated when outputs change.

A repo may also keep scratch notes (e.g., `dev/02_dev.md`), but scratch notes are not authoritative.

---

## Required workflow for future changes (process gate)

When planning or implementing changes, the assistant MUST follow this workflow:

### Step 0 — Identify which docs are in scope
Before proposing changes, classify the work as one or more of:
- architecture change (invariants, boundaries, stage contracts)
- policy change (thresholds, classification rules, enrichment rules)
- schema change (fields/types/nullability/backward compatibility)
- operational change (commands, environment, filesystem layout, run procedures)
- implementation-only change (refactor without behavior change)

Then explicitly state which `dev/` docs will need updates.

### Step 1 — Use ADRs for decision points
If work introduces or modifies any major rule/contract, an ADR is REQUIRED, including (non-exhaustive):
- identity model
- storage layout / durability guarantees / locking
- policy thresholds and triage rules
- external services usage rules
- chunking and export strategy
- environment + packaging workflow
- supported platform/terminal guidance

If an ADR already exists for the topic:
- create a new ADR if the decision changes materially, and mark the prior ADR `superseded`.

### Step 2 — Keep the design doc accurate
- `dev/10_design.md` MUST reflect the current state (“what is true now”).
- It SHOULD link to ADRs for rationale.
- It SHOULD include testable definitions of done / readiness milestones.

### Step 3 — Keep the runbook runnable
For operator-visible changes:
- update `dev/30_runbook.md` with exact commands and expected outputs.
- include troubleshooting notes for known failure modes.

### Step 4 — Keep schemas authoritative
For output changes:
- update `dev/40_schemas.md`
- call out backward compatibility:
  - additive (safe) vs breaking (requires migration notes)

### Step 5 — Always include verification steps
For any proposed change, include:
- local verification commands (tests, smoke runs, CLI help)
- expected artifacts and locations
- new assumptions / prerequisites

---

## Interaction style (required)
- Treat doc updates (design/ADRs/runbook/schemas) as part of “definition of done”.
- Prefer small, reviewable edits.
- Do not silently change behavior without:
  - an ADR (if it is a decision/contract), and
  - updated schemas/runbook where relevant.