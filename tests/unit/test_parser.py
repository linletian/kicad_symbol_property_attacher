import pathlib as pl

from src.lib import parser

FIXTURES = pl.Path("tests/fixtures/kicad_v9")


def test_load_and_iter_symbols_basic():
    path = FIXTURES / "official-basic-no-prop-SzlcscCode.kicad_sym"
    sx = parser.load_s_expr(path)
    symbols = parser.iter_symbols(sx)
    assert isinstance(symbols, list)
    # Expect at least one symbol in official fixture
    assert len(symbols) >= 1


def test_has_property_absent_then_add():
    path = FIXTURES / "official-basic-no-prop-SzlcscCode.kicad_sym"
    sx = parser.load_s_expr(path)
    symbols = parser.iter_symbols(sx)
    sym_sx, _ = symbols[0]
    assert not parser.has_property(sym_sx, "SzlcscCode")
    parser.add_property(sym_sx, "SzlcscCode", "")
    assert parser.has_property(sym_sx, "SzlcscCode")


def test_dump_s_expr_returns_string():
    path = FIXTURES / "official-basic-no-prop-SzlcscCode.kicad_sym"
    sx = parser.load_s_expr(path)
    out = parser.dump_s_expr(sx)
    assert isinstance(out, str)
