# Phase 0 Research: KiCAD Symbol Property Batch Attacher

**Branch**: `001-kicad-symbol-property`  
**Date**: 2025-12-13  
**Spec**: `specs/001-kicad-symbol-property/spec.md`

## Objectives

Resolve unknowns and select best practices for:
- S-expression parsing strategy suitable for KiCAD `.kicad_sym` v9.x
- CLI ergonomics and cross-platform behavior
- Markdown report content and highlighting conventions
- Performance expectations and I/O patterns (in-place with backup vs output file)
- Dependency versions and quality tooling alignment

## Findings & Decisions

### 1) Parser choice for S-expression
- Decision: Use `sexpdata==0.0.3` for initial MVP; validate with representative `.kicad_sym` samples. If limitations are found, consider `lark` or `pyparsing` with a small grammar for KiCAD subset.
- Rationale: `sexpdata` is lightweight, focused on S-expr, minimizes bespoke grammar work.
- Alternatives considered:
  - `lark`: Powerful, but requires grammar maintenance; heavier learning curve.
  - `pyparsing`: Flexible; similar trade-offs to `lark` for grammar upkeep.

### 2) Property attach semantics
- Decision: Do not overwrite existing properties of the same name. If the same-name property exists but with different value, skip modification and do not add duplicates.
- Rationale: Preserves original data and avoids ambiguity in KiCAD ingestion.
- Alternatives considered: Overwrite or duplicate entries (rejected due to risk of data loss or schema confusion).

### 3) CLI design
- Decision: Use `click==8.1.*` for a clean, cross-platform CLI with options:
  - `--property-name <str>` (required)
  - `--property-value <str>` (optional, default "")
  - `--output <path>` OR `--in-place` (mutually exclusive)
  - `--dry-run` (show stats only)
  - `--report <path>` (optional; default to timestamped Markdown alongside output)
- Rationale: Widely adopted library with good ergonomics and testing support.
- Alternatives considered: `argparse` (standard, minimal), `typer` (nice DX but adds dependency).

### 4) Markdown report format
- Decision: Structure sections with clear highlighting:
  - Title + timestamp + input/output paths
  - Summary metrics (processed, added, skipped, duration)
  - Errors (highlighted with bold/emojis/badges)
  - Warnings (highlighted similarly)
  - Skipped Symbols (list of names/IDs)
- Rationale: Quick triage; human-readable; aligns with spec requirements for emphasis.
- Alternatives considered: JSON report (machine-friendly) in addition—can be added later.

### 5) Performance & I/O
- Decision: Read entire file into memory for MVP; optimize only if needed. Use safe write with backup for `--in-place`.
- Rationale: Simplicity; `.kicad_sym` sizes typically manageable; spec targets ≤10MB.
- Alternatives considered: Streaming parser—added complexity; will revisit if performance issues occur.

### 6) Quality tooling
- Decision: Enforce `ruff`, `black`, `mypy (strict where feasible)`, `pytest` + `pytest-cov` per constitution.
- Rationale: Code quality and maintainability.
- Alternatives considered: `pylint` (heavier), omitting type checks (rejected).

## Open Questions (tracked)
- Need sample `.kicad_sym` variations to validate parser robustness.
- Confirm exact KiCAD property node names/placement in v9.x (expected: standard `property` forms).

## Research Tasks Completion

- Decision: Python 3.11, `click 8.1.*`, `sexpdata 0.0.3` primary; `rich 13.*` optional.
- Rationale: Stable, cross-platform, LTS-priority; low friction for CLI and parsing.
- Alternatives: Grammar-based parsers if `sexpdata` shows gaps.

## Next Steps

- Phase 1: Produce `data-model.md` (Symbol/Property structure), `contracts/` (CLI contract or OpenAPI-like docs for future API), and `quickstart.md` (usage examples).
- Update agent context via `.specify/scripts/bash/update-agent-context.sh copilot`.
