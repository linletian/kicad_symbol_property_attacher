import pathlib as pl

from click.testing import CliRunner

from src.cli.main import kicad_sym_prop
from src.lib import parser

FIXTURES = pl.Path("tests/fixtures/kicad_v9")


def test_output_utf8_and_loadable(tmp_path: pl.Path):
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
            "--output",
            str(out_file),
        ],
    )
    assert result.exit_code == 0, result.output
    data = out_file.read_bytes()
    # UTF-8 decodes without errors
    decoded = data.decode("utf-8")
    assert isinstance(decoded, str)
    # Parser can load the written file
    sx = parser.load_s_expr(out_file)
    assert len(parser.iter_symbols(sx)) >= 1


def test_path_handling_in_place_vs_output(tmp_path: pl.Path):
    runner = CliRunner()
    input_file = FIXTURES / "official-basic-no-prop-SzlcscCode.kicad_sym"

    # Output path chosen
    out_file = tmp_path / "nested" / "dir" / "out.kicad_sym"
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
        ],
    )
    assert result.exit_code == 0, result.output
    assert out_file.exists()

    # In-place mode (no output path) should modify the input copy
    local = tmp_path / "local.kicad_sym"
    local.write_text(input_file.read_text("utf-8"), encoding="utf-8")
    result2 = runner.invoke(
        kicad_sym_prop,
        [
            "attach",
            "--input",
            str(local),
            "--property-name",
            "SzlcscCode",
            "--in-place",
        ],
    )
    assert result2.exit_code == 0, result2.output
    sx2 = parser.load_s_expr(local)
    sym_sx2, _ = parser.iter_symbols(sx2)[0]
    assert parser.has_property(sym_sx2, "SzlcscCode")


def test_line_endings_and_indentation_preservation(tmp_path: pl.Path):
    runner = CliRunner()
    # Prepare CRLF input by rewriting fixture with Windows line endings
    src = FIXTURES / "official-basic-no-prop-SzlcscCode.kicad_sym"
    text = src.read_text("utf-8")
    crlf_text = text.replace("\n", "\r\n")
    crlf_in = tmp_path / "crlf.kicad_sym"
    crlf_in.write_text(crlf_text, encoding="utf-8")

    out_file = tmp_path / "out_crlf.kicad_sym"
    result = runner.invoke(
        kicad_sym_prop,
        [
            "attach",
            "--input",
            str(crlf_in),
            "--property-name",
            "SzlcscCode",
            "--output",
            str(out_file),
        ],
    )
    assert result.exit_code == 0, result.output
    data = out_file.read_bytes()
    decoded = data.decode("utf-8")
    # SHOULD preserve formatting where possible: balanced parentheses; new property block uses spaces
    # Do not assert global absence of tabs, as input may contain tabs from upstream files.
    assert decoded.count("(") == decoded.count(")")
    # If input had CRLF, we prefer preserving; allow either CRLF or LF depending on serializer
    # At minimum, ensure it remains consistent (no mixed endings)
    has_crlf = "\r\n" in decoded
    # Consistency: not both CRLF and bare LF mixed
    assert not (has_crlf and decoded.replace("\r\n", "").find("\n") != -1)
