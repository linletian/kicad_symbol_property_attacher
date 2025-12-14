# KiCAD Symbol Property Batch Attacher

![CI](https://github.com/linletian/kicad_symbol_property_attacher/actions/workflows/ci.yml/badge.svg)

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

## Environments

### Option A: Virtual Environment (recommended)
- Pros: dependency isolation, reproducibility, no sudo, easy cleanup.
- Install:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install click==8.1.7 sexpdata==0.0.3
```
- Use:
```bash
src/.venv/bin/python -m src.cli.main attach \
	--input path/to/lib.kicad_sym \
	--property-name SzlcscCode
```
- Uninstall (cleanup):
```bash
deactivate || true
rm -rf .venv
```

### Option B: System Environment (alternative)
- Pros: no venv needed. Cons: risk of global version conflicts; may require sudo.
- Install:
```bash
python3 -m pip install click==8.1.7 sexpdata==0.0.3
```
- Use:
```bash
python3 -m src.cli.main attach \
	--input path/to/lib.kicad_sym \
	--property-name SzlcscCode
```
- Uninstall (global):
```bash
python3 -m pip uninstall -y click sexpdata
```

## Install as CLI (optional)
You can install the package and use the `kicad-sym-prop` command provided by entry points:
```bash
# In venv
pip install .
kicad-sym-prop attach --input path/to/lib.kicad_sym --property-name SzlcscCode

# Or system env (beware global effects)
python3 -m pip install .
kicad-sym-prop attach --input path/to/lib.kicad_sym --property-name SzlcscCode
```

Note for users in Mainland China: if network to default PyPI is unstable, consider using a trusted domestic mirror temporarily during installation (e.g. Tsinghua Tuna). Example in venv:
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple \
	--trusted-host pypi.tuna.tsinghua.edu.cn \
	.
```
Then run:
```bash
kicad-sym-prop attach --input path/to/lib.kicad_sym --property-name SzlcscCode
```

Tip: if build isolation pulls dependencies from PyPI and fails due to SSL/cert restrictions, you can disable isolation during local install:
```bash
pip install --no-build-isolation .
```

## Usage
```bash
# Output to new file (explicit)
kicad-sym-prop attach \
	--input path/to/lib.kicad_sym \
	--property-name SzlcscCode \
	# --property-value is optional; defaults to empty string
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

### Multiple Properties
You can add multiple properties in one run by repeating `--property-name`. The `--property-value` applies to all provided property names and is optional (default empty string).

```bash
kicad-sym-prop attach \
	--input path/to/lib.kicad_sym \
	--property-name SzlcscCode \
	--property-name SzlcscPriceRef \
	--property-name SzlcscLink \
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
- When `--report` is omitted, a timestamped Markdown report is generated next to the target file by default.
- See `specs/001-kicad-symbol-property/` for full spec, plan, tasks.

## Release
- Current: `v0.1.3` — CLI entry fix; README EN/CN install notes (mirror + no-build-isolation); validation complete.
- Previous: `v0.1.0` — US1/US2/US3 complete; quality gates (ruff, black, mypy, pytest) green on macOS
- Changelog: see `CHANGELOG.md`

## Dependencies
See `docs/dependencies.md` for pinned versions and LTS notes.

## License
GPL-3.0. See `LICENSE`.

## Hardware Adjustment
N/A (software-only). See `docs/hardware-adjustment.md`.
