import pathlib as pl
from click.testing import CliRunner

from src.cli.main import kicad_sym_prop
from src.lib import parser

FIXTURES = pl.Path("tests/fixtures/kicad_v9")


def test_cli_attach_output_file(tmp_path: pl.Path):
    runner = CliRunner()
    input_file = FIXTURES / "official-basic-no-prop-SzlcscCode.kicad_sym"
    out_file = tmp_path / "out.kicad_sym"
    result = runner.invoke(
        kicad_sym_prop,
        [
            "attach",
            "--input",
            str(input_file),
            "--property-name",
            "SzlcscCode",
            "--property-value",
            "",
            "--output",
            str(out_file),
            "--report",
            str(tmp_path / "report.md"),
        ],
    )
    assert result.exit_code == 0, result.output
    assert out_file.exists()
    sx = parser.load_s_expr(out_file)
    sym_sx, _ = parser.iter_symbols(sx)[0]
    assert parser.has_property(sym_sx, "SzlcscCode")


def test_cli_attach_dry_run_no_write(tmp_path: pl.Path):
    runner = CliRunner()
    input_file = FIXTURES / "official-basic-no-prop-SzlcscCode.kicad_sym"
    out_file = tmp_path / "out.kicad_sym"
    report = tmp_path / "report.md"
    result = runner.invoke(
        kicad_sym_prop,
        [
            "attach",
            "--input",
            str(input_file),
            "--property-name",
            "SzlcscCode",
            "--dry-run",
            "--output",
            str(out_file),
            "--report",
            str(report),
        ],
    )
    assert result.exit_code == 0, result.output
    assert not out_file.exists()
    assert report.exists()


def test_cli_attach_invalid_s_expr_generates_error_report(tmp_path: pl.Path):
    runner = CliRunner()
    bad = tmp_path / "bad.kicad_sym"
    bad.write_text("(kicad_symbol_lib (symbol \"MissingParen\" ", encoding="utf-8")
    report = tmp_path / "bad.report.md"
    result = runner.invoke(
        kicad_sym_prop,
        [
            "attach",
            "--input",
            str(bad),
            "--property-name",
            "SzlcscCode",
            "--report",
            str(report),
        ],
    )
    assert result.exit_code != 0
    assert report.exists()
    content = report.read_text("utf-8")
    assert "ERROR" in content


def test_cli_attach_permission_error_generates_error_report(tmp_path: pl.Path):
    runner = CliRunner()
    input_file = FIXTURES / "official-basic-no-prop-SzlcscCode.kicad_sym"
    # Create a directory with the same name as intended output file to cause write error
    out_file = tmp_path / "conflict.kicad_sym"
    out_file.mkdir(parents=True)
    report = tmp_path / "perm.report.md"
    result = runner.invoke(
        kicad_sym_prop,
        [
            "attach",
            "--input",
            str(input_file),
            "--property-name",
            "SzlcscCode",
            "--output",
            str(out_file),
            "--report",
            str(report),
        ],
    )
    assert result.exit_code != 0
    assert report.exists()
    content = report.read_text("utf-8")
    assert "ERROR" in content
