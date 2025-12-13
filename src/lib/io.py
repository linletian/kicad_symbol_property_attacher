from __future__ import annotations

import pathlib as pl


def read_text(path: pl.Path, encoding: str = "utf-8") -> str:
    return path.read_text(encoding=encoding)


def write_text(path: pl.Path, text: str, encoding: str = "utf-8") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding=encoding)


def make_backup(path: pl.Path, suffix: str = ".bak") -> pl.Path:
    backup = path.with_suffix(path.suffix + suffix)
    if path.exists():
        path.replace(backup)
    return backup
