"""
CLI entrypoint for KiCAD Symbol Property Batch Attacher.

Provides commands to attach a specified property to all Symbols in a
`.kicad_sym` file without overwriting existing properties. Generates
Markdown report with highlighted errors/warnings and skipped Symbols.
"""

from __future__ import annotations

import datetime as _dt
import pathlib as _pl
import sys
from typing import Optional

import click

from ..lib.attacher import attach_property_to_file
from ..lib.report import ReportOptions


@click.group()
def kicad_sym_prop() -> None:
    """KiCAD symbol property tools (no GUI)."""


@kicad_sym_prop.command("attach")
@click.option("--input", "input_path", type=click.Path(path_type=_pl.Path), required=True)
@click.option("--property-name", "prop_name", type=str, required=True)
@click.option("--property-value", "prop_value", type=str, default="")
@click.option("--output", "output_path", type=click.Path(path_type=_pl.Path), default=None)
@click.option("--in-place", "in_place", is_flag=True, default=False)
@click.option("--backup-suffix", "backup_suffix", type=str, default=".bak")
@click.option("--dry-run", "dry_run", is_flag=True, default=False)
@click.option("--report", "report_path", type=click.Path(path_type=_pl.Path), default=None)
@click.option("--encoding", "encoding", type=str, default="utf-8")
def attach(
    input_path: _pl.Path,
    prop_name: str,
    prop_value: str,
    output_path: Optional[_pl.Path],
    in_place: bool,
    backup_suffix: str,
    dry_run: bool,
    report_path: Optional[_pl.Path],
    encoding: str,
) -> None:
    """
    Attach property to all Symbols. Skips existing same-name properties regardless of value.
    Produces Markdown report with summary and highlighted errors/warnings.
    """

    if output_path and in_place:
        click.echo("Error: --output and --in-place are mutually exclusive", err=True)
        sys.exit(1)

    # Default report path next to target file with timestamp
    if report_path is None:
        ts = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        base = (output_path or input_path).with_suffix("")
        report_path = base.parent / f"{base.name}.{ts}.report.md"

    ropts = ReportOptions(report_path=report_path)

    try:
        stats = attach_property_to_file(
            input_path=input_path,
            output_path=output_path,
            in_place=in_place,
            backup_suffix=backup_suffix,
            prop_name=prop_name,
            prop_value=prop_value,
            dry_run=dry_run,
            encoding=encoding,
            report_options=ropts,
        )
    except Exception as exc:  # noqa: BLE001
        click.echo(f"Error: {exc}", err=True)
        sys.exit(2)

    # Success
    click.echo(
        f"Processed={stats.symbols_processed} added={stats.properties_added} skipped={stats.properties_skipped}"
    )


def main() -> None:  # Entry point for console_scripts
    kicad_sym_prop()


if __name__ == "__main__":
    main()
