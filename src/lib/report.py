"""
Markdown report generation for attachment runs.
Highlights errors/warnings and lists skipped Symbols.
"""

from __future__ import annotations

import dataclasses as _dc
import pathlib as _pl
from typing import Iterable


@_dc.dataclass
class ReportOptions:
    report_path: _pl.Path


def write_markdown_report(
    *,
    report_path: _pl.Path,
    input_path: str,
    output_path: str,
    stats,
    errors: Iterable[str],
    warnings: Iterable[str],
) -> None:
    lines: list[str] = []
    lines.append(f"# Attachment Report\n")
    lines.append(f"**Input**: `{input_path}`  ")
    lines.append(f"**Output**: `{output_path}`\n")
    lines.append("\n## Summary\n")
    lines.append(f"- Processed: **{stats.symbols_processed}**")
    lines.append(f"- Added: **{stats.properties_added}**")
    lines.append(f"- Skipped: **{stats.properties_skipped}**\n")

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
    if stats.skipped_symbols:
        for name in stats.skipped_symbols:
            lines.append(f"- `{name}`")
    else:
        lines.append("- None\n")

    report_path.write_text("\n".join(lines), encoding="utf-8")
