---

description: "Tasks for KiCAD Symbol Property Batch Attacher"
---

# Tasks: KiCAD Symbol Property Batch Attacher

**Input**: Design documents from `specs/001-kicad-symbol-property/`  
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Included per spec request — unit + integration tests.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create Python 3.11 virtual env and base deps in `.venv/`
- [ ] T002 [P] Add `pyproject.toml` with pinned deps (click, sexpdata, pytest, ruff, black, mypy)
- [ ] T003 [P] Add quality configs `ruff.toml`, `mypy.ini`, `.editorconfig` in repo root
- [ ] T004 Initialize source layout per plan in `src/` and `tests/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Configure `pytest` with coverage in `tests/`
- [ ] T006 [P] Add lint/format/type check tasks to CI (local scripts) `tools/` or `Makefile`
- [ ] T007 Implement parser scaffold in `src/lib/parser.py`
- [ ] T008 Implement report scaffold in `src/lib/report.py`
- [ ] T009 Create CLI group/command in `src/cli/main.py`
- [ ] T0IO1 [P] Implement `src/lib/io.py` for file read/write, backup creation, and permission error handling
- [ ] T0IO2 [P] Unit tests for `io.py` in `tests/unit/test_io.py`: read/write, backup naming, permission errors


**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Batch Attach Property via CLI (Priority: P1) 🎯 MVP

**Goal**: CLI adds specified property to all Symbols; skip existing; preserve S-expression; generate Markdown report.

**Independent Test**: Run CLI on mixed sample; verify added vs skipped counts, valid output loads in KiCAD v9.x; report generated with highlights.

### Tests for User Story 1

- [ ] T010 [P] [US1] Unit test parser load/dump in `tests/unit/test_parser.py`
- [ ] T011 [P] [US1] Unit test property detection/add in `tests/unit/test_attacher.py`
- [ ] T012 [P] [US1] Unit test report contents/highlights in `tests/unit/test_report.py`
- [ ] T013 [US1] Integration test CLI attach on `tests/fixtures/kicad_v9/official-basic-no-prop-SzlcscCode.kicad_sym` in `tests/integration/test_cli_attach.py`
- [ ] T014 [US1] Integration test CLI attach on `tests/fixtures/kicad_v9/official-mixed-some-prop-SzlcscCode.kicad_sym` in `tests/integration/test_cli_attach.py`
- [ ] T0DR1 [P] [US1] Dry-run integration test: assert no writes, correct stats/report in `tests/integration/test_cli_attach.py`
- [ ] T0FAIL1 [US1] Invalid S-expression input: expect non-zero exit and Markdown report with highlighted errors
- [ ] T0FAIL2 [US1] No write permission: assert no output file; Markdown report includes errors/warnings list

### Implementation for User Story 1

- [ ] T015 [P] [US1] Implement `attach_property_to_file` in `src/lib/attacher.py`
- [ ] T016 [P] [US1] Finalize parser functions (iterate symbols, has/add property) in `src/lib/parser.py`
- [ ] T017 [US1] Implement CLI `attach` options and default report path in `src/cli/main.py`
- [ ] T018 [US1] Implement Markdown report writer highlighting errors/warnings in `src/lib/report.py`
- [ ] T019 [US1] Add logging/summary output in CLI (processed/added/skipped)
- [ ] T0DR2 [US1] Add `--dry-run` option in `src/cli/main.py` and propagate to core logic
- [ ] T0DR3 [US1] Implement dry-run in `src/lib/attacher.py`: compute stats and generate report without writing files or backups
- Note: `attacher.py` should call `io.py` for actual I/O and backups to keep responsibilities focused.


**Checkpoint**: User Story 1 fully functional and independently testable

---

## Phase 4: User Story 2 - Cross-Platform Operation (Priority: P2)

**Goal**: Consistent CLI behavior across Windows, macOS (Intel & Apple silicon), Linux.

**Independent Test**: Execute same commands on each OS; outputs identical; valid for KiCAD v9.x.

### Tests for User Story 2

- [ ] T020 [P] [US2] Encoding/line-endings tests in `tests/integration/test_cli_cross_platform.py`
- [ ] T021 [P] [US2] Path handling tests (in-place vs output) in `tests/integration/test_cli_cross_platform.py`

### Implementation for User Story 2

- [ ] T022 [P] [US2] Ensure UTF-8 default; document platform notes in `README.md`
- [ ] T023 [US2] Validate identical output hashes for same inputs across platforms (doc-driven)

**Checkpoint**: Cross-platform behavior validated

---

## Phase 5: User Story 3 - Safe Update Workflow (Priority: P3)

**Goal**: `--output` or `--in-place` with automatic backup; no data loss.

**Independent Test**: Verify backup created and restore possible; `--output` keeps input untouched.

### Tests for User Story 3

- [ ] T024 [P] [US3] In-place backup/restore test in `tests/integration/test_backup.py`
- [ ] T025 [P] [US3] Output path behavior test in `tests/integration/test_backup.py`

### Implementation for User Story 3

- [ ] T026 [P] [US3] Implement safe in-place write with backup suffix in `src/lib/attacher.py`
- [ ] T027 [US3] Validate mutual exclusion of `--output` and `--in-place` in `src/cli/main.py`

**Checkpoint**: Safe update workflow complete

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T028 [P] Documentation updates in `README.md`
- [ ] T029 Add `CHANGELOG.md` entries and tag release `v0.1.0`
- [ ] T030 [P] Add `docs/dependencies.md` with versions and notes
- [ ] T031 [P] Add `docs/hardware-adjustment.md` section as N/A (software-only); link from README
- [ ] T032 Security hardening: input validation and error messages
- [ ] T033 Performance pass on large files; note benchmarks in `research.md`
- [ ] T0DR4 [P] Update `README.md` and `contracts/cli-contract.md` with dry-run usage and behavior
- [ ] T0DOC1 [P] Update `README.md` with usage, dry-run, report examples, cross-platform notes
- [ ] T0DOC2 Maintain `CHANGELOG.md` with release `v0.1.0` features and behavior notes
- [ ] T0DOC3 [P] Add `docs/dependencies.md` with versions and LTS notes
- [ ] T0DOC4 [P] Ensure `docs/hardware-adjustment.md` exists (N/A) and linked from README
- [ ] T0REL1 Pre-release gate: lint/format/mypy/pytest all green; docs updated; create annotated git tag `v0.1.0`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Should be independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before CLI wiring
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational completes, user stories can start in parallel
- Tests marked [P] per story can run in parallel
- Parser/Report implementations can proceed independently

---

## Parallel Example: User Story 1

```
# Launch all tests for User Story 1 together:
pytest -q tests/unit/test_parser.py tests/unit/test_attacher.py tests/unit/test_report.py
pytest -q tests/integration/test_cli_attach.py -k "basic or mixed"

# Launch models/helpers together:
# parser.py and report.py can be implemented in parallel
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. STOP and VALIDATE: Test User Story 1 independently (unit + integration)
5. Deploy/demo if ready

### Incremental Delivery

1. Foundation ready → US1 → Test independently → Demo
2. Add US2 → Cross-platform checks → Demo
3. Add US3 → Backup/restore verified → Demo

---

## MVP Scope

- Implement US1 end-to-end with tests and Markdown report.
