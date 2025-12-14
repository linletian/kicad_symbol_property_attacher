"""
CLI entrypoint for KiCAD Symbol Property Batch Attacher.

Provides commands to attach a specified property to all Symbols in a
`.kicad_sym` file without overwriting existing properties. Generates
Markdown report with highlighted errors/warnings and skipped Symbols.
"""

from __future__ import annotations

import datetime as _dt
import importlib
import pathlib as _pl
import sys

import click

# Support both "python -m src.cli.main" (package under src) and installed package imports
try:
    attacher = importlib.import_module("src.lib.attacher")
    report = importlib.import_module("src.lib.report")
except ImportError:
    attacher = importlib.import_module("lib.attacher")
    report = importlib.import_module("lib.report")

# Bind names once to avoid mypy redefinition across conditional imports
attach_property_to_file = attacher.attach_property_to_file
ReportOptions = report.ReportOptions
write_markdown_report = report.write_markdown_report


@click.group()
def kicad_sym_prop() -> None:
    """KiCAD symbol property tools (no GUI)."""


@kicad_sym_prop.command("attach")
@click.option("--input", "input_path", type=click.Path(path_type=_pl.Path), required=True)
@click.option("--property-name", "prop_names", type=str, multiple=True, required=True)
@click.option("--property-value", "prop_value", type=str, default="")
@click.option("--output", "output_path", type=click.Path(path_type=_pl.Path), default=None)
@click.option("--in-place", "in_place", is_flag=True, default=False)
@click.option("--backup-suffix", "backup_suffix", type=str, default=".bak")
@click.option("--dry-run", "dry_run", is_flag=True, default=False)
@click.option("--report", "report_path", type=click.Path(path_type=_pl.Path), default=None)
@click.option("--encoding", "encoding", type=str, default="utf-8")
def attach(
    input_path: _pl.Path,
    prop_names: tuple[str, ...],
    prop_value: str,
    output_path: _pl.Path | None,
    in_place: bool,
    backup_suffix: str,
    dry_run: bool,
    report_path: _pl.Path | None,
    encoding: str,
) -> None:
    """
    Attach property to all Symbols. Skips existing same-name properties regardless of value.
    Produces Markdown report with summary and highlighted errors/warnings.
    """

    # New spec: --output 可以不提供参数，默认为输入文件路径与文件名。
    # 若同时提供 --in-place，以输入路径为准；保持兼容但不再强制互斥。
    if output_path is None:
        output_path = input_path

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
            in_place=True,  # 始终按新规范备份输入原始文件并写出到输出（默认同输入）
            backup_suffix=backup_suffix,
            prop_names=list(prop_names),
            prop_value=prop_value,
            dry_run=dry_run,
            encoding=encoding,
            report_options=ropts,
        )
    except Exception as exc:  # noqa: BLE001
        # Failure path should still generate a report per SC-005
        from contextlib import suppress

        with suppress(Exception):
            write_markdown_report(
                report_path=ropts.report_path,
                input_path=str(input_path),
                output_path=str(output_path or input_path),
                stats=None,
                errors=[str(exc)],
                warnings=[],
            )
        click.echo(f"Error: {exc}", err=True)
        sys.exit(2)

    # Success
    click.echo(f"Processed={stats.symbols_processed} added={stats.properties_added} skipped={stats.properties_skipped}")


def main() -> None:  # Entry point for console_scripts
    kicad_sym_prop()


if __name__ == "__main__":
    main()
