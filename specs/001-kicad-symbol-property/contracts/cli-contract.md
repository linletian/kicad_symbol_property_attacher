# CLI Contract: KiCAD Symbol Property Batch Attacher

**Branch**: `001-kicad-symbol-property`  
**Date**: 2025-12-13  
**Spec**: `specs/001-kicad-symbol-property/spec.md`

## Command

`kicad-sym-prop attach`

## Arguments & Options

- `--input, -i <path>` (required): Path to `.kicad_sym` file
- `--property-name, -n <str>` (required): Property name to attach
- `--property-value, -v <str>` (optional): Property value (default: empty string)
- `--output, -o <path>` (optional): Output file path (mutually exclusive with `--in-place`)
- `--in-place` (optional): Modify input in place with automatic backup
- `--backup-suffix <str>` (optional): Suffix for backup (default: `.bak`)
- `--dry-run` (optional): Do not write; show stats only
- `--report <path>` (optional): Markdown report path (default: alongside output with timestamp)
- `--encoding <str>` (optional): File encoding (default: `utf-8`)

## Behavior

- Parse input as S-expression; validate structure
- For each Symbol:
  - If `property-name` missing: add `property(name=value)`
  - If exists (any value): skip; do not overwrite or duplicate
- Serialize to output (or in-place after backup)
- Produce Markdown report with summary, errors/warnings (highlighted), skipped-symbol list

## Exit Codes

- `0`: Success
- `1`: Invalid arguments / validation failure
- `2`: Parsing error (malformed S-expression)
- `3`: I/O error (permissions, missing files)

## Examples

```bash
kicad-sym-prop attach -i lib.kicad_sym -n Manufacturer -v "ACME" -o lib.out.kicad_sym --report lib.out.report.md
kicad-sym-prop attach -i lib.kicad_sym -n MPN --in-place --backup-suffix .bak --report lib.kicad_sym.report.md
kicad-sym-prop attach -i lib.kicad_sym -n Comment --dry-run
```
