# Feature Specification: KiCAD Symbol Property Batch Attacher

**Feature Branch**: `001-kicad-symbol-property`  
**Created**: 2025-12-13  
**Status**: Draft  
**Input**: User description: "Design a program to batch-add a specified Property to all Symbols in KiCAD v9.x `.kicad_sym` libraries (S-expression format). Ensure KiCAD v9.x reads the library without compatibility errors. Property name is provided via program argument. If a Symbol already has the same Property, do not overwrite existing data. Cross-platform for Windows, macOS (Intel & Apple silicon), and Linux."

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Batch Attach Property via CLI (Priority: P1)

User executes the CLI to add a specified property name and value to all Symbols in a `.kicad_sym` file, ensuring no overwrite of existing identical property names and preserving S-expression validity.

**Why this priority**: Delivers the core value—eliminates repetitive UI work by batch automation.

**Independent Test**: Run CLI on a sample `.kicad_sym` with mixed Symbols (some with property, some without) and verify output file loads in KiCAD v9.x; properties correctly added where missing; no existing property data overwritten.

**Acceptance Scenarios**:

1. **Given** a `.kicad_sym` file without the target property, **When** run CLI with `--property-name` and `--property-value`, **Then** all Symbols include the new property with provided value.
2. **Given** a `.kicad_sym` file where some Symbols already have the target property, **When** run CLI with same property name, **Then** existing property entries remain unchanged; only missing Symbols receive new property.
3. **Given** any input file, **When** processing completes, **Then** the resulting file is a valid S-expression that KiCAD v9.x can load without warnings/errors.
4. **Given** processing completes, **When** the program exits, **Then** it produces a Markdown report containing: execution summary (symbols processed, added, skipped), error/warning list, and a list of Symbols skipped due to existing property; errors/warnings are highlighted for quick review.

---

### User Story 2 - Cross-Platform Operation (Priority: P2)

User runs the program on Windows, macOS (Intel & Apple silicon), and Linux with consistent behavior and output.

**Why this priority**: Ensures broad usability across KiCAD-supported OSes.

**Independent Test**: Execute the same command and sample file on each OS; verify identical results and validity.

**Acceptance Scenarios**:

1. **Given** the same `.kicad_sym` input and CLI arguments, **When** running on Windows, macOS (Intel/Apple silicon), or Linux, **Then** outputs are consistent and valid for KiCAD v9.x.

---

### User Story 3 - Safe Update Workflow (Priority: P3)

User chooses output location or in-place update with backup handling to prevent data loss.

**Why this priority**: Protects user data and supports flexible workflows.

**Independent Test**: Use `--output` to write to a new file or `--in-place` with automatic backup and verify correctness.

**Acceptance Scenarios**:

1. **Given** an input file and `--output out.kicad_sym`, **When** program runs, **Then** the input remains unchanged and output contains modifications.
2. **Given** `--in-place` mode, **When** program runs, **Then** it creates a backup (e.g., `.bak`) before writing changes; restore possible.

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

- Empty or malformed S-expression: Program MUST fail fast with clear error and no output changes.
- Symbols with multiple properties of same name: Program MUST not collapse or overwrite; preserve all existing entries and only add if truly missing.
- Non-ASCII property names/values: Program MUST handle UTF-8 safely across platforms.
- Large files: Program SHOULD process within reasonable time; stream or chunk as needed.
- Read-only files or permission issues: Program MUST report error without partial writes.
- KiCAD version variance: If v9.x minor versions differ in schema tolerance, program MUST adhere to documented schema and avoid vendor-specific extensions.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST parse `.kicad_sym` files as S-expressions without losing structure or comments.
- **FR-002**: System MUST accept CLI arguments for `--property-name` and `--property-value` (value optional; default empty string allowed).
- **FR-003**: System MUST add the specified property to every `Symbol` that lacks it; MUST NOT overwrite existing property entries of the same name; if a property of the same name exists with a different value, skip modification and do not add a duplicate entry.
- **FR-004**: System MUST produce output that KiCAD v9.x can load without compatibility errors or warnings.
- **FR-005**: System MUST support cross-platform execution on Windows, macOS (Intel & Apple silicon), and Linux.
- **FR-006**: System MUST provide `--output` for writing to a new file and `--in-place` safe update with automatic backup.
- **FR-007**: System MUST validate inputs and report errors clearly (invalid file, invalid S-expression, missing permissions).
- **FR-008**: System SHOULD allow dry-run mode to preview changes (e.g., stats of added properties) without writing.
- **FR-009**: System SHOULD preserve file formatting conventions where possible (line endings, indentation).
- **FR-010**: System MUST log processing summary: symbols processed, properties added, properties skipped (existing), duration.
 - **FR-011**: System MUST generate a Markdown report file capturing the execution summary, explicit error list, explicit warning list, and the full list of skipped Symbols (already had the property).
 - **FR-012**: The Markdown report MUST visually highlight errors and warnings (e.g., headings, emphasis, or badges) to enable fast triage.
 - **FR-013**: The report MUST be saved to a user-accessible path; default naming SHOULD include timestamp and input filename.

Assumptions:
- `.kicad_sym` schema for v9.x follows publicly documented S-expression conventions; property node names and placement are deterministic.
- Property values may be empty; absence of property treated as missing.
- Concurrency not required; single-process CLI sufficient for MVP.

### Key Entities

- **Symbol**: A component symbol definition in `.kicad_sym`; attributes include `name`, `properties[]`.
- **Property**: Name/value pair attached to a `Symbol`; includes `name`, `value`, optional flags depending on KiCAD schema.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 95% of `.kicad_sym` files up to 10MB process in under 5 seconds on typical developer hardware.
- **SC-002**: 100% of output files load in KiCAD v9.x without compatibility errors.
- **SC-003**: 0% overwrite incidents for existing properties of the same name across test corpus.
- **SC-004**: CLI runs successfully on Windows, macOS (Intel & Apple silicon), and Linux with consistent output.
 - **SC-005**: Markdown report is generated for 100% of successful runs; on failure, a report is still produced summarizing partial progress and errors.
 - **SC-006**: Report highlights enable users to identify errors/warnings within 10 seconds (validated via usability check with standard-sized reports).

## Clarifications

### Session 2025-12-13

- Q: How to handle when the property already exists but with a different value? → A: Skip overwrite; do not add duplicate.

Applied updates:
- Edge Cases: Explicitly state non-overwrite behavior for differing values and no duplicate additions.
- Functional Requirements: Clarify FR-003 to skip modification when same property name exists, regardless of value.
