<!--
Sync Impact Report
- Version change: (none) → 1.0.0
- Modified principles: Template placeholders → Concrete Python project governance
- Added sections: Dependencies & Hardware Guidance integrated within principles
- Removed sections: None
- Templates requiring updates:
  ✅ .specify/templates/plan-template.md (Constitution Check aligns conceptually; no changes required)
  ✅ .specify/templates/spec-template.md (No conflicting constraints detected)
  ✅ .specify/templates/tasks-template.md (Task grouping remains compatible)
  ⚠ Pending: Repository README.md, CHANGELOG.md, PLAN docs—must follow Governance update on each commit
- Deferred TODOs:
  - TODO(RATIFICATION_DATE): Original adoption date not known; set once confirmed
-->

# Kicad Symbol Property Attacher Constitution

## Core Principles

### I. Code Quality First (NON-NEGOTIABLE)
All Python source MUST meet strict quality standards:
- Linting: Enforce `flake8`/`ruff` with zero errors before merge.
- Formatting: Use `black` with repository-wide configuration.
- Type safety: Apply `mypy` with `strict` where feasible; public APIs MUST be typed.
- Structure: Keep modules small, cohesive, and single-responsibility.
- Performance: Avoid premature optimization; profile hotspots before changes.

Rationale: High code quality reduces defects, eases maintenance, and improves
collaboration across contributors.

### II. Complete English Documentation in Code
All functions, methods, classes, and modules MUST have complete English docstrings
and comments that explain intent, inputs, outputs, side effects, and error cases.
- Docstrings: Follow Google or NumPy style consistently; include examples where apt.
- Annotations: Every parameter and return value SHOULD have type hints.
- Comments: Explain non-obvious logic; avoid redundant or outdated comments.
- API docs: Auto-generate from docstrings when publishing releases.

Rationale: Clear, English documentation enables global collaboration and ensures
the codebase remains accessible and maintainable.

### III. Test Standards and Discipline
Testing is mandatory and layered:
- Unit tests: Cover core logic with `pytest`; target ≥85% coverage on critical paths.
- Integration tests: Validate CLI flows and file I/O behaviors.
- Hardware-adjustment tests: Include configuration validation and simulated run checks.
- Test-first: Write failing tests before implementing significant features.
- CI gates: All tests MUST pass in CI; flaky tests are prohibited.

Rationale: Reliable tests provide safety for refactoring and accelerate confident releases.

### IV. Hardware Adjustment Guidance
Provide a detailed, versioned guidance document under `docs/hardware-adjustment.md`:
- Environment setup: OS, drivers, required tools, calibration procedures.
- Step-by-step adjustments: Parameters, expected ranges, and verification steps.
- Safety notes: Explicit warnings for operations that can damage hardware.
- Traceability: Link guidance steps to code/config versions and test cases.

Rationale: Hardware-related changes require precise instructions to ensure reproducibility
and safe operation across environments.

### V. Release Documentation & Git Hygiene
Before each commit to `main` or a release branch:
- Update `README.md`, `CHANGELOG.md`, and plan/spec/task docs with any behavior changes.
- Tagging: Create annotated git tags for releases (`vMAJOR.MINOR.PATCH`).
- SemVer: Respect semantic versioning for public CLI/API changes.
- Commit messages: Use conventional commits; reference related docs and tests.

Rationale: Up-to-date documentation and disciplined versioning improve user trust and
developer productivity.

### VI. Dependencies Policy (LTS First)
Third-party components MUST prioritize LTS versions; if unavailable, use the latest stable.
- Document all dependencies with exact versions in `requirements.txt` / `pyproject.toml`.
- Maintain `docs/dependencies.md` listing components and versions, with upgrade notes.
- Security: Monitor advisories; patch vulnerable dependencies promptly.
- Reproducibility: Use lock files (`pip-tools`/`uv`) to pin transitive versions.

Rationale: Stable dependencies reduce integration risk and improve reproducibility.

## Additional Constraints

Security, Performance, and CLI Standards:
- Security: Validate inputs, sanitize file paths, avoid unsafe eval/exec.
- Performance: Document expected scales; profile before optimizing; cache where justified.
- CLI: Provide consistent text I/O; errors to stderr; support JSON and human-readable outputs.

## Development Workflow

Quality Gates and Reviews:
- Pull Requests MUST pass lint, format, type-check, and full test suite.
- Reviews verify adherence to principles and documentation completeness.
- Any hardware-impacting change MUST update `docs/hardware-adjustment.md` and related tests.
- Constitution compliance is a required review checklist item.

## Governance

This Constitution supersedes other practices. Amendments require:
- Documentation of proposed changes with rationale and impact assessment.
- Version bump per semantic rules; migration plan for breaking changes.
- Compliance review added to PRs; CI checks updated if gates change.

All PRs and reviews MUST verify compliance with these principles. Complexity MUST be
justified in writing. Refer to runtime guidance documents (README, quickstart, hardware
guidance) during development.

**Version**: 1.0.0 | **Ratified**: 2025-12-13 | **Last Amended**: 2025-12-13
