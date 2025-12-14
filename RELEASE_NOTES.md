# Release Notes

## v0.1.3 (2025-12-14)
- Fix: Console script import path corrected. Packaging configured to find packages under `src/`, and `cli/main.py` supports both source and installed imports.
- Docs: EN/CN README updated with domestic mirror notes and `--no-build-isolation` tip to mitigate SSL/cert issues when installing locally.
- Validation: CLI verified via module run; installation path validated after fix.

## v0.1.0 (2025-12-13)
- Features: CLI attach, parser, attacher, report; dry-run; in-place with backup; cross-platform handling; Markdown reports.
- Quality: ruff/black/mypy/pytest all green.
- Docs: README, CHANGELOG, dependencies, hardware guidance.
- Notes: Dependencies installed via mirror due to SSL; see CHANGELOG for details.
## v0.1.2 (2025-12-14)
- Feature: Multi-property attach via repeatable `--property-name`; `--property-value` optional (default empty) and applied to all provided names.
- Behavior: When `--report` is omitted, a timestamped report is generated next to the target file; when `--output` is omitted, output writes back to input and creates a numbered original backup (`.orig`, `.orig.N`).
- Docs: README usage updated (multi-property, default report), spec updated for repeatable names and optional value.
- Quality: Tests updated and passing.
