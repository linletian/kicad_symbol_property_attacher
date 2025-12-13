import pathlib as pl

from src.lib import io


def test_make_backup_and_write(tmp_path: pl.Path):
    f = tmp_path / "file.txt"
    f.write_text("data", encoding="utf-8")
    backup = io.make_backup(f, ".bak")
    assert backup.exists()
    # original path now moved (does not exist), we can write new content
    io.write_text(f, "new", encoding="utf-8")
    assert f.read_text("utf-8") == "new"
