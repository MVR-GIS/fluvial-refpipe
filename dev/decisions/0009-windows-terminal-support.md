---
id: "0009"
title: "Supported Windows terminal in Positron is PowerShell (Git Bash may be unstable)"
date: "2026-04-29"
status: "accepted"
repo: "MVR-GIS/fluvial-refpipe"
tags:
  - "windows"
  - "developer-experience"
  - "conda"
supersedes: []
superseded_by: ""
related_commits: []
---

# ADR 0009: Supported Windows terminal in Positron is PowerShell (Git Bash may be unstable)

## Context
During local setup in Positron on Windows, Git Bash exhibited missing Unix utilities (`cygpath`, `sed`, `which`) and conda activation issues, while PowerShell behaved predictably with conda/mamba.

We want a reproducible, low-friction onboarding story.

## Decision
- The supported terminal for running conda/mamba and `refpipe` commands in Positron on Windows is **PowerShell**.
- Git Bash may work on some systems, but is not the primary supported path unless explicitly documented and tested.

## Rationale
PowerShell is the least surprising option for conda activation on Windows workstations and avoids dependency on Git Bash/MSYS utilities being present on PATH.

## Consequences
### Positive
- Fewer environment activation issues.
- More consistent “works for everyone” workflow.

### Negative / tradeoffs
- Some users prefer bash; they may need extra setup.
- Documentation should show PowerShell examples primarily.

### Follow-ups
- Add runbook section: “Windows + Positron: use PowerShell”.
- Provide optional Git Bash notes for advanced users.

## Alternatives considered
- Standardize on Git Bash: rejected (too many integration edge cases).
- Standardize on cmd.exe: possible, but PowerShell offers better UX.

## Links
- Design: `dev/10_design.md#windowspositron-terminal-guidance`