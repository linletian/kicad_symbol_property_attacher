import pathlib as pl

from click.testing import CliRunner

from src.cli.main import kicad_sym_prop
from src.lib import parser

FIXTURES = pl.Path("tests/fixtures/kicad_v9")


def test_default_output_creates_numbered_original_backup_and_updates_file(tmp_path: pl.Path):
    runner = CliRunner()
    # copy fixture to temp to avoid modifying original
    src = FIXTURES / "official-basic-no-prop-SzlcscCode.kicad_sym"
    local = tmp_path / "lib.kicad_sym"
    local.write_text(src.read_text("utf-8"), encoding="utf-8")
    report = tmp_path / "report.md"
    result = runner.invoke(
        kicad_sym_prop,
        [
            "attach",
            "--input",
            str(local),
            "--property-name",
            "SzlcscCode",
            # omit --output to trigger default write-back to input and numbered original backup
            "--report",
            str(report),
        ],
    )
    assert result.exit_code == 0, result.output
    # original backup exists (.orig or .orig.N)
    primary_orig = local.with_name(local.name + ".orig")
    numbered_orig1 = local.with_name(local.name + ".orig.1")
    assert primary_orig.exists() or numbered_orig1.exists()
    # input updated contains property
    sx = parser.load_s_expr(local)
    sym_sx, _ = parser.iter_symbols(sx)[0]
    assert parser.has_property(sym_sx, "SzlcscCode")
    assert report.exists()


def test_output_and_in_place_can_coexist_and_still_update(tmp_path: pl.Path):
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
    # New spec allows coexistence; expect success and out_file to be written
    assert result.exit_code == 0, result.output
    assert out_file.exists()
