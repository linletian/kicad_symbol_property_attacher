import pathlib as pl

from src.lib.attacher import attach_property_to_file

FIXTURES = pl.Path("tests/fixtures/kicad_v9")


def test_attach_dry_run_basic_adds_no_writes(tmp_path: pl.Path):
    path = FIXTURES / "official-basic-no-prop-SzlcscCode.kicad_sym"
    # report path not used in this unit test
    stats = attach_property_to_file(
        input_path=path,
        prop_names=["SzlcscCode"],
        prop_value="",
        output_path=None,
        in_place=False,
        dry_run=True,
        report_options=None,
    )
    assert stats.properties_added > 0
    assert stats.properties_skipped >= 0
    assert len(stats.skipped_symbols) == stats.properties_skipped
    # No output written in dry-run
    assert not (tmp_path / path.name).exists()


def test_attach_dry_run_mixed_skips(tmp_path: pl.Path):
    path = FIXTURES / "official-mixed-some-prop-SzlcscCode.kicad_sym"
    stats = attach_property_to_file(
        input_path=path,
        prop_names=["SzlcscCode"],
        prop_value="",
        dry_run=True,
    )
    # Should have some skipped due to existing property
    assert stats.properties_skipped >= 1
