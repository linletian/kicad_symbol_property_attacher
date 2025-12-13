"""
Attach property to all Symbols in a `.kicad_sym` file.
Skips when the property already exists (any value). Generates stats and can
write in-place with backup or to a new file.
"""

from __future__ import annotations

import dataclasses as _dc
import pathlib as _pl
from typing import Optional

from . import parser
from .report import ReportOptions, write_markdown_report


@_dc.dataclass
class AttachStats:
    symbols_processed: int = 0
    properties_added: int = 0
    properties_skipped: int = 0
    skipped_symbols: list[str] = _dc.field(default_factory=list)


def attach_property_to_file(
    input_path: _pl.Path,
    prop_name: str,
    prop_value: str,
    *,
    output_path: Optional[_pl.Path] = None,
    in_place: bool = False,
    backup_suffix: str = ".bak",
    dry_run: bool = False,
    encoding: str = "utf-8",
    report_options: Optional[ReportOptions] = None,
) -> AttachStats:
    lib = parser.load_s_expr(input_path, encoding=encoding)
    stats = AttachStats()

    for sym_sx, _idx in parser.iter_symbols(lib):
        stats.symbols_processed += 1
        name = parser.symbol_name(sym_sx)
        if parser.has_property(sym_sx, prop_name):
            stats.properties_skipped += 1
            stats.skipped_symbols.append(name or "<unnamed>")
            continue
        parser.add_property(sym_sx, prop_name, prop_value)
        stats.properties_added += 1

    # Write output if not dry-run
    if not dry_run:
        target = output_path or input_path
        if in_place and output_path is None:
            backup = input_path.with_suffix(input_path.suffix + backup_suffix)
            if input_path.exists():
                input_path.replace(backup)
            target = input_path
        text = parser.dump_s_expr(lib)
        target.write_text(text, encoding=encoding)

    # Report
    if report_options is not None:
        write_markdown_report(
            report_path=report_options.report_path,
            input_path=str(input_path),
            output_path=str(output_path or input_path),
            stats=stats,
            errors=[],
            warnings=[],
        )

    return stats
