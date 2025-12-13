# Data Model: KiCAD Symbol Property Batch Attacher

**Branch**: `001-kicad-symbol-property`  
**Date**: 2025-12-13  
**Spec**: `specs/001-kicad-symbol-property/spec.md`

## Entities

### Symbol
- Fields:
  - `name: str` — Symbol identifier
  - `properties: List[Property]` — Attached properties
  - `raw: SExprNode` — Original S-expression subtree for round-trip integrity
- Relationships:
  - Contains multiple `Property`
- Validation:
  - `name` non-empty
  - `properties` entries maintain schema order required by KiCAD

### Property
- Fields:
  - `name: str`
  - `value: str` (may be empty)
  - `flags: Dict[str, Any]` (optional; KiCAD schema-specific attributes)
- Validation:
  - `name` non-empty and UTF-8 safe
  - Avoid duplicates of the same name when attaching

## State Transitions

- Attach Property
  - Precondition: `Symbol` does not have `Property.name`
  - Transition: Append new `Property(name, value)` to `properties` and update `raw`
  - Postcondition: S-expression remains valid; formatting preserved where feasible

- Skip Existing Property
  - Precondition: `Symbol` contains `Property.name` (any value)
  - Transition: No modification
  - Postcondition: Original data intact; report lists skipped `Symbol`

## Notes

- Round-trip integrity: parsing and serialization MUST not alter structure or comments outside intended property addition.
- Schema specifics: KiCAD v9.x `property` nodes are expected; exact placement confirmed during implementation tests.
