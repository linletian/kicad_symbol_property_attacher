# Changelog

All notable changes to this project will be documented in this file.

## [0.1.2] - 2025-12-14
### Added
- Multi-property attach: Support repeating `--property-name` to add multiple properties in one run; `--property-value` remains optional and applies to all provided names (default empty).

### Changed
- README updated with multi-property usage examples and clarified default report generation when `--report` is omitted.
- Spec updated to reflect repeatable `--property-name` and optional `--property-value` behavior.

### Tests
- Unit and integration tests adjusted to cover multi-property and new defaults; full suite passing.

## [0.1.0] - 2025-12-13
### Added
- Initial feature specification, plan, research, data model, contracts, quickstart
- CLI `attach` command with safe update workflow and report generation
- Parser/attacher/report modules
- I/O helpers and unit/integration test skeletons
- Failure-path report generation with timestamp
- Cross-platform tests (UTF-8, path handling, formatting consistency)
- Project setup files: `.gitignore`, `pyproject.toml`, `ruff.toml`, `mypy.ini`, `.editorconfig`, `pytest.ini`
 - Dry-run mode with full stats/report and zero writes
 - In-place write with backup suffix, and mutual exclusion with `--output`
 - Markdown report listing skipped symbols and errors/warnings; default timestamped path

### Changed
- Output/backup workflow: When `--output` is omitted, default output is the input file itself; before saving, create a non-overwriting numbered original backup next to the input (`.orig`, `.orig.1`, ...).
- Property insertion format: Insert a KiCAD-validated multi-line Property block containing `(at 0 0 0)` and `(effects (font (size 1.27 1.27)) (hide yes))`, preserving indentation and line endings.
- CLI examples and docs: README usage switched to long options (`--input`, `--property-name`), updated examples for default output and incremental backups.
- Spec updates: `specs/001-kicad-symbol-property/spec.md` reflects new default output, numbered backups, and multi-line property block requirements.

### Fixed
- Governance/spec cleanup: removed template residue, merged duplicate FR-003, added non-technical overview/scope/traceability
- Updated `ruff.toml` to new `[lint]` section; addressed lints and typing issues

### Notes
- Quality gates passed: `ruff`, `black`, `mypy`, `pytest` all green on macOS
- Dependencies pinned to LTS-appropriate versions; installed via Tsinghua mirror due to SSL constraints
