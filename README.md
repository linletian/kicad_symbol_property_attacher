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
# Output to new file
kicad-sym-prop attach -i path/to/lib.kicad_sym -n SzlcscCode -o path/to/lib.out.kicad_sym --report path/to/lib.out.report.md

# In-place with backup
kicad-sym-prop attach -i path/to/lib.kicad_sym -n SzlcscCode --in-place --backup-suffix .bak --report path/to/lib.kicad_sym.report.md

# Dry-run
kicad-sym-prop attach -i path/to/lib.kicad_sym -n SzlcscCode --dry-run --report path/to/lib.kicad_sym.report.md
```

## Notes
- KiCAD v9.x should load outputs without warnings/errors.
- Encoding: UTF-8. Line endings preserved consistently.
- See `specs/001-kicad-symbol-property/` for full spec, plan, tasks.
