# Implementation Plan: KiCAD Symbol Property Batch Attacher

**Branch**: `001-kicad-symbol-property` | **Date**: 2025-12-13 | **Spec**: `specs/001-kicad-symbol-property/spec.md`
**Input**: Feature specification from `specs/001-kicad-symbol-property/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Batch-add a specified Property to all Symbols in KiCAD v9.x `.kicad_sym` libraries without overwriting existing properties. Preserve S-expression validity and provide cross-platform CLI (Windows/macOS Intel & Apple silicon/Linux). Produce a Markdown report with execution summary, errors/warnings (highlighted), and a list of skipped Symbols.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11 (LTS/stable across platforms)
**Primary Dependencies**: 
- `click==8.1.*` (CLI)
- `sexpdata==0.0.3` (S-expression parser; confirm viability in research)
- `rich==13.*` (optional terminal output)
**Storage**: N/A (file in/out)
**Testing**: `pytest==8.*`, `pytest-cov==5.*`; linting `ruff==0.6.*`, formatting `black==24.*`, typing `mypy==1.11.*`
**Target Platform**: Windows, macOS (Intel & Apple silicon), Linux
**Project Type**: Single project (CLI tool)
**Performance Goals**: Process ≥95% of ≤10MB `.kicad_sym` files under 5s
**Constraints**: No overwrite of existing same-name properties; S-expression validity; Markdown report generation
**Scale/Scope**: Single CLI with core operation; no GUI

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Gates (must pass):
- Code Quality First: ruff/black/mypy configured; types on public APIs
- Complete English documentation: docstrings for all functions/classes/modules
- Test Standards: pytest unit+integration; ≥85% coverage on critical paths; no flaky tests
- Hardware Adjustment Guidance: N/A (software-only); ensure docs section exists but marked N/A
- Release Docs & Git Hygiene: update README/CHANGELOG/plan/spec/tasks; semantic tags for releases
- Dependencies Policy (LTS First): pin versions; document in `docs/dependencies.md`

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/
├── cli/
│   └── main.py           # entrypoint using click
├── lib/
│   ├── parser.py         # S-expression parsing helpers
│   ├── attacher.py       # core logic: attach property
│   ├── report.py         # Markdown report generator
│   └── io.py             # file read/write, backups, dry-run
└── __init__.py

tests/
├── unit/
│   ├── test_parser.py
│   ├── test_attacher.py
│   └── test_report.py
└── integration/
  └── test_cli_attach.py
```

**Structure Decision**: Single-project CLI layout focusing on clear separation: parsing, business logic (attach), reporting, and I/O.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
| N/A | N/A | N/A |

If `sexpdata` proves insufficient, custom parser complexity must be justified with benchmarks and maintainability analysis.
