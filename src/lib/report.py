"""
Markdown report generation for attachment runs.
Highlights errors/warnings and lists skipped Symbols.
"""

from __future__ import annotations

import dataclasses as _dc
import datetime as _dt
import pathlib as _pl
from collections.abc import Iterable
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .attacher import AttachStats


@_dc.dataclass
class ReportOptions:
    report_path: _pl.Path


def write_markdown_report(
    *,
    report_path: _pl.Path,
    input_path: str,
    output_path: str,
    stats: AttachStats | None,
    errors: Iterable[str],
    warnings: Iterable[str],
) -> None:
    lines: list[str] = []
    ts = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append("# Attachment Report\n")
    lines.append(f"**Input**: `{input_path}`  ")
    lines.append(f"**Output**: `{output_path}`\n")
    lines.append(f"**Timestamp**: `{ts}`\n")
    lines.append("\n## Summary\n")
    if stats is not None:
        lines.append(f"- Processed: **{getattr(stats, 'symbols_processed', 0)}**")
        lines.append(f"- Added: **{getattr(stats, 'properties_added', 0)}**")
        lines.append(f"- Skipped: **{getattr(stats, 'properties_skipped', 0)}**\n")
    else:
        lines.append("- Processed: **0**")
        lines.append("- Added: **0**")
        lines.append("- Skipped: **0**\n")

    lines.append("## Errors\n")
    if errors:
        for e in errors:
            lines.append(f"- ❌ **ERROR**: {e}")
    else:
        lines.append("- None\n")

    lines.append("## Warnings\n")
    if warnings:
        for w in warnings:
            lines.append(f"- ⚠️ **WARNING**: {w}")
    else:
        lines.append("- None\n")

    lines.append("## Skipped Symbols (already had property)\n")
    if stats is not None and stats.skipped_symbols:
        for name in stats.skipped_symbols:
            lines.append(f"- `{name}`")
    else:
        lines.append("- None\n")

    report_path.write_text("\n".join(lines), encoding="utf-8")
