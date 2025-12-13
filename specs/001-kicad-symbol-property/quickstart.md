# Quickstart: KiCAD Symbol Property Batch Attacher

**Branch**: `001-kicad-symbol-property`  
**Date**: 2025-12-13  

## Install (development)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install click==8.1.* sexpdata==0.0.3 rich==13.* pytest==8.* pytest-cov==5.* ruff==0.6.* black==24.* mypy==1.11.*
```

## Run

```bash
# Output to new file and report
kicad-sym-prop attach -i path/to/lib.kicad_sym -n Manufacturer -v "ACME" -o path/to/lib.out.kicad_sym --report path/to/lib.out.report.md

# In-place update with backup
kicad-sym-prop attach -i path/to/lib.kicad_sym -n MPN --in-place --backup-suffix .bak --report path/to/lib.kicad_sym.report.md

# Dry-run
kicad-sym-prop attach -i path/to/lib.kicad_sym -n Comment --dry-run
```

## Notes

- KiCAD v9.x must load resulting `.kicad_sym` without warnings/errors.
- Existing same-name properties are never overwritten; differing values are skipped without duplication.
- Markdown report is generated with highlighted errors/warnings and a list of skipped Symbols.
