import pathlib as pl

from src.lib.report import write_markdown_report


class DummyStats:
    def __init__(self):
        self.symbols_processed = 3
        self.properties_added = 2
        self.properties_skipped = 1
        self.skipped_symbols = ["U1"]


def test_write_markdown_report(tmp_path: pl.Path):
    report_path = tmp_path / "report.md"
    write_markdown_report(
        report_path=report_path,
        input_path="input.kicad_sym",
        output_path="output.kicad_sym",
        stats=DummyStats(),
        errors=[],
        warnings=["Minor format deviation"],
    )
    assert report_path.exists()
    content = report_path.read_text("utf-8")
    assert "Attachment Report" in content
    assert "Warnings" in content or "WARNING" in content
