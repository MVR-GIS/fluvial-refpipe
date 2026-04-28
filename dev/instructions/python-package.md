# python-package — Overlay Module (Python Package + CLI Development)

## Canonical guidance (required)
- Prefer authoritative references over blogs:
  - Python Packaging User Guide (PyPA): https://packaging.python.org/
  - PEP 517/518/621 (pyproject.toml standards)
  - Conda docs for environment management (when relevant)
- When guidance is version-sensitive, state the assumed versions (Python, conda, key libs).

## Scope & assumptions to confirm (required)
Start by confirming:
1) target repository (owner/repo) and default branch,
2) whether this is an internal-only package vs public distribution,
3) environment model (conda/mamba `environment.yml` vs pip/venv),
4) Python version target (>=3.10 unless specified),
5) whether a CLI is required and its intended user personas (operator vs developer).

Do not infer missing requirements; ask concise clarification questions.

## Project structure (required)
- Prefer `src/` layout for packages:
  - `src/<package_name>/...`
- Keep notebooks and scripts thin; move stable logic into importable modules.
- Keep data/artifacts out of Git unless they are tiny test fixtures.

## Dependency management policy (required)
- In conda-first repos:
  - Prefer conda-forge packages for compiled/heavy deps (pandas/pyarrow/lxml/pytorch/etc.).
  - Allow pip *inside the activated conda env* for:
    1) installing the local package (`pip install -e .`) and
    2) pure-Python deps not available on conda-forge.
- Avoid split-brain dependency specs unless there is a clear reason.
- If using conda as the source of truth, it is acceptable for `pyproject.toml` to omit dependency lists.

## Packaging standard (required)
- Use `pyproject.toml` as the packaging entrypoint.
- Prefer the minimal packaging stack unless requirements demand more:
  - `setuptools` backend is acceptable for internal tooling.
- Provide a console script entrypoint when a CLI is part of the project.
- Ensure `python -m pip install -e .` yields a working CLI command.

## Documentation ecosystem (roxygen/pkgdown analogue) (required)
- Required documentation primitives:
  - NumPy-style docstrings for all public functions/classes
  - Type hints for all public functions/classes
- Recommended site generator (pkgdown analogue):
  - MkDocs + Material + mkdocstrings (Python handler)
- Documentation must be buildable locally (no CI requirement assumed):
  - `mkdocs serve` for live preview
  - `mkdocs build` for a static site output

## Testing & verification gates (required)
- TDD-friendly workflow:
  - prefer local `pytest` runs during development
  - do not assume tests run in CI unless explicitly configured
- Always propose a way to verify changes locally:
  - `pytest -q` for unit tests
  - at minimum: import smoke tests and CLI `--help` checks
- Tests should be deterministic and offline-friendly by default.

## Interaction style (required)
1) Inspect relevant repo files before advising when it improves accuracy (pyproject.toml, environment.yml, src/, docs/).
2) Offer 3–5 feasible options ranked by confidence (alignment with standards + repo conventions + minimal assumptions).
3) Wait for the user to select an option before proceeding.
4) Prefer small, reviewable steps with a clear “definition of done”.
