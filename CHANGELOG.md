# Changelog

All notable changes to this project will be documented in this file.

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

### Fixed
- Governance/spec cleanup: removed template residue, merged duplicate FR-003, added non-technical overview/scope/traceability
- Updated `ruff.toml` to new `[lint]` section; addressed lints and typing issues

### Notes
- Quality gates passed: `ruff`, `black`, `mypy`, `pytest` all green on macOS
- Dependencies pinned to LTS-appropriate versions; installed via Tsinghua mirror due to SSL constraints
