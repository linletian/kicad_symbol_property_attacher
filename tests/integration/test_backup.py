import pathlib as pl
from click.testing import CliRunner

from src.cli.main import kicad_sym_prop
from src.lib import parser

FIXTURES = pl.Path("tests/fixtures/kicad_v9")


def test_in_place_creates_backup_and_updates_file(tmp_path: pl.Path):
    runner = CliRunner()
    # copy fixture to temp to avoid modifying original
    src = FIXTURES / "official-basic-no-prop-SzlcscCode.kicad_sym"
    local = tmp_path / "lib.kicad_sym"
    local.write_text(src.read_text("utf-8"), encoding="utf-8")
    backup_suffix = ".bak"
    report = tmp_path / "report.md"
    result = runner.invoke(
        kicad_sym_prop,
        [
            "attach",
            "--input",
            str(local),
            "--property-name",
            "SzlcscCode",
            "--in-place",
            "--backup-suffix",
            backup_suffix,
            "--report",
            str(report),
        ],
    )
    assert result.exit_code == 0, result.output
    # backup exists
    backup = local.with_suffix(local.suffix + backup_suffix)
    assert backup.exists()
    # input updated contains property
    sx = parser.load_s_expr(local)
    sym_sx, _ = parser.iter_symbols(sx)[0]
    assert parser.has_property(sym_sx, "SzlcscCode")
    assert report.exists()


def test_output_and_in_place_mutually_exclusive(tmp_path: pl.Path):
    runner = CliRunner()
    src = FIXTURES / "official-basic-no-prop-SzlcscCode.kicad_sym"
    out_file = tmp_path / "out.kicad_sym"
    result = runner.invoke(
        kicad_sym_prop,
        [
            "attach",
            "--input",
            str(src),
            "--property-name",
            "SzlcscCode",
            "--output",
            str(out_file),
            "--in-place",
        ],
    )
    assert result.exit_code != 0