from __future__ import annotations

import pathlib as pl
import shutil
from typing import Optional


def read_text(path: pl.Path, encoding: str = "utf-8") -> str:
    return path.read_text(encoding=encoding)


def write_text(path: pl.Path, text: str, encoding: str = "utf-8") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding=encoding)


def make_backup(path: pl.Path, suffix: str = ".bak") -> pl.Path:
    backup = path.with_suffix(path.suffix + suffix)
    if path.exists():
        # Copy instead of rename to preserve the original file for subsequent reads.
        # This avoids "No such file or directory" errors when backup is created before reading.
        shutil.copy2(path, backup)
    return backup


def make_numbered_backup(path: pl.Path, base_suffix: str = ".orig") -> pl.Path:
    """Create a numbered backup copy next to the input file without overwriting.

    Examples (for input `foo.kicad_sym`):
    - `foo.kicad_sym.orig` if available, else
    - `foo.kicad_sym.orig.1`, `foo.kicad_sym.orig.2`, ...
    """
    candidate = path.with_name(path.name + base_suffix)
    if not candidate.exists():
        shutil.copy2(path, candidate)
        return candidate
    n = 1
    while True:
        numbered = path.with_name(f"{path.name}{base_suffix}.{n}")
        if not numbered.exists():
            shutil.copy2(path, numbered)
            return numbered
        n += 1
