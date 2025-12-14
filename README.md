# KiCAD Symbol Property Batch Attacher

A CLI tool to batch-add a specified Property to all Symbols in KiCAD v9.x `.kicad_sym` libraries while preserving S-expression validity. Cross-platform, with Markdown reports and safe update workflows.

## Features
- Add property to Symbols that lack it; never overwrite existing same-name properties
- Skip differing value without duplication
- Output to new file or in-place with backup
- Dry-run preview with stats and report
- Markdown report with highlighted errors/warnings and skipped symbols

## Install (dev)
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install click==8.1.* sexpdata==0.0.3 pytest==8.* pytest-cov==5.* ruff==0.6.* black==24.* mypy==1.11.*
```

## Usage
```bash
# Output to new file (explicit)
kicad-sym-prop attach \
	--input path/to/lib.kicad_sym \
	--property-name SzlcscCode \
	--output path/to/lib.out.kicad_sym \
	--report path/to/lib.out.report.md

# Default output: write back to input (no --output)
# An original backup is created next to input using incremental naming: .orig, .orig.1, ...
kicad-sym-prop attach \
	--input path/to/lib.kicad_sym \
	--property-name SzlcscCode \
	--report path/to/lib.kicad_sym.report.md

# Dry-run (no writes, report still generated)
kicad-sym-prop attach \
	--input path/to/lib.kicad_sym \
	--property-name SzlcscCode \
	--dry-run \
	--report path/to/lib.kicad_sym.report.md
```

### Property Block Format (KiCAD-validated)
The tool inserts a full multi-line Property block compatible with KiCAD checks, preserving indentation and line endings:

```text
(property "SzlcscCode" ""
	(at 0 0 0)
	(effects
		(font
			(size 1.27 1.27)
		)
		(hide yes)
	)
)
```

## Report Example
```markdown
# Attachment Report
**Input**: `tests/fixtures/kicad_v9/official-basic-no-prop-SzlcscCode.kicad_sym`  
**Output**: `out/basic-added.kicad_sym`
**Timestamp**: `2025-12-13 10:08:42`

## Summary
- Processed: **117**
- Added: **116**
- Skipped: **1**

## Errors
- None

## Warnings
- None

## Skipped Symbols (already had property)
- `X1224WRS-02-LPV01`
```

## Failure Path Example
When input is invalid S-expression or no write permission, the CLI returns non-zero and still writes a Markdown report:
```text
Error: Failed to parse S-expression: unexpected token near line 42
```
The report will contain the errors list and zero stats.

## Notes
- KiCAD v9.x should load outputs without warnings/errors.
- Encoding: UTF-8. Line endings preserved consistently.
- When `--output` is omitted, output defaults to input path; an original backup is created next to input using incremental names (`.orig`, `.orig.1`, ...).
- See `specs/001-kicad-symbol-property/` for full spec, plan, tasks.

## Release
- Current: `v0.1.0` — US1/US2/US3 complete; quality gates (ruff, black, mypy, pytest) green on macOS
- Changelog: see `CHANGELOG.md`

## Dependencies
See `docs/dependencies.md` for pinned versions and LTS notes.

## Hardware Adjustment
N/A (software-only). See `docs/hardware-adjustment.md`.
