"""
S-expression parser helpers for KiCAD `.kicad_sym` files.

Uses `sexpdata` for MVP to parse and serialize while aiming for round-trip
integrity. This module abstracts reading/writing and basic navigation
to locate `symbol` and `property` forms.
"""

from __future__ import annotations

import pathlib as _pl
from typing import Any, cast

import sexpdata


def load_s_expr(path: _pl.Path, encoding: str = "utf-8") -> Any:
    with path.open("r", encoding=encoding) as f:
        text = f.read()
    return sexpdata.loads(text)


def dump_s_expr(sx: Any) -> str:
    return cast(str, sexpdata.dumps(sx))


def iter_symbols(library_sx: Any) -> list[tuple[Any, int]]:
    """Return list of (symbol_sx, index) for all `(symbol ...)` forms in library.

    The library root is expected as `(kicad_symbol_lib ... (symbol ...) ...)`.
    """
    if not isinstance(library_sx, list) or not library_sx:
        return []
    out: list[tuple[Any, int]] = []
    for i, node in enumerate(library_sx):
        if isinstance(node, list) and node and node[0] == sexpdata.Symbol("symbol"):
            out.append((node, i))
    return out


def symbol_name(symbol_sx: Any) -> str:
    """Get symbol name from `(symbol "Name" ...)`."""
    if (
        isinstance(symbol_sx, list)
        and len(symbol_sx) >= 2
        and isinstance(symbol_sx[1], str)
    ):
        return symbol_sx[1]
    return ""


def has_property(symbol_sx: Any, prop_name: str) -> bool:
    for node in symbol_sx:
        if (
            isinstance(node, list)
            and node
            and node[0] == sexpdata.Symbol("property")
            and len(node) >= 3
            and isinstance(node[1], str)
            and node[1] == prop_name
        ):
            return True
    return False


def add_property(symbol_sx: Any, prop_name: str, prop_value: str) -> None:
    """Append a simple `(property "Name" "Value")` form to the symbol."""
    symbol_sx.append([sexpdata.Symbol("property"), prop_name, prop_value])
