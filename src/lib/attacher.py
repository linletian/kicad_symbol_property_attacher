"""
Attach property to all Symbols in a `.kicad_sym` file.
Skips when the property already exists (any value). Generates stats and can
write in-place with backup or to a new file.
"""

from __future__ import annotations

import dataclasses as _dc
import pathlib as _pl

from . import io as _io
from . import parser
from .report import ReportOptions, write_markdown_report


@_dc.dataclass
class AttachStats:
    symbols_processed: int = 0
    properties_added: int = 0
    properties_skipped: int = 0
    skipped_symbols: list[str] = _dc.field(default_factory=list)
    added_symbols: list[str] = _dc.field(default_factory=list)


def attach_property_to_file(
    input_path: _pl.Path,
    prop_names: list[str],
    prop_value: str,
    *,
    output_path: _pl.Path | None = None,
    in_place: bool = False,
    backup_suffix: str = ".bak",
    dry_run: bool = False,
    encoding: str = "utf-8",
    report_options: ReportOptions | None = None,
) -> AttachStats:
    lib = parser.load_s_expr(input_path, encoding=encoding)
    stats = AttachStats()
    # Map symbol name -> list of property names to add
    to_add: dict[str, list[str]] = {}

    for sym_sx, _idx in parser.iter_symbols(lib):
        stats.symbols_processed += 1
        name = parser.symbol_name(sym_sx)
        props_to_add: list[str] = []
        for pn in prop_names:
            if parser.has_property(sym_sx, pn):
                stats.properties_skipped += 1
                stats.skipped_symbols.append(name or "<unnamed>")
            else:
                parser.add_property(sym_sx, pn, prop_value)
                stats.properties_added += 1
                stats.added_symbols.append(name or "<unnamed>")
                props_to_add.append(pn)
        if name and props_to_add:
            to_add[name] = props_to_add

    # Write output if not dry-run
    if not dry_run:
        # 新规范：在保存前，始终对 input 文件在同目录下做原始备份；备份不覆盖，使用递增编号。
        _io.make_numbered_backup(input_path, base_suffix=".orig")
        # 输出路径：若未显式提供 --output，则默认与输入同路径同文件名。
        target = output_path or input_path
        original = _io.read_text(input_path, encoding=encoding)
        newline = "\r\n" if "\r\n" in original else "\n"
        updated = _insert_properties_textual_multi(
            original_text=original,
            additions=[(sn, pn, prop_value) for sn, pns in to_add.items() for pn in pns],
            newline=newline,
        )
        _io.write_text(target, updated, encoding=encoding)

    # Report
    if report_options is not None:
        write_markdown_report(
            report_path=report_options.report_path,
            input_path=str(input_path),
            output_path=str(output_path or input_path),
            stats=stats,
            errors=[],
            warnings=[],
        )

    return stats


def _insert_properties_textual_multi(  # noqa: PLR0915
    *,
    original_text: str,
    additions: list[tuple[str, str, str]],  # (symbol_name, prop_name, prop_value)
    newline: str,
) -> str:
    """Insert multiple property blocks into the original text.

    Each addition is a tuple of (symbol_name, prop_name, prop_value). For each symbol occurrence,
    append a full multi-line KiCAD-validated property block before the closing parenthesis.
    Preserves formatting by deriving indentation from the block.
    """

    def find_all_symbol_starts(text: str, name: str) -> list[int]:
        pattern = f"(symbol \"{name}\""
        starts: list[int] = []
        pos = 0
        while True:
            idx = text.find(pattern, pos)
            if idx == -1:
                break
            # back up to the leading '(' of this symbol form
            paren_idx = text.rfind("(", 0, idx + 1)
            if paren_idx != -1:
                starts.append(paren_idx)
            pos = idx + len(pattern)
        return starts

    def find_matching_paren(text: str, start_idx: int) -> int:
        depth = 0
        in_str = False
        i = start_idx
        while i < len(text):
            ch = text[i]
            if ch == '"':
                # toggle string state if not escaped
                esc = i > 0 and text[i - 1] == "\\"
                if not esc:
                    in_str = not in_str
            elif not in_str:
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if depth == 0:
                        return i
            i += 1
        return -1

    def indent_for_block(text: str, start_idx: int, end_idx: int) -> str:
        # Try to reuse indent from an existing property line within the block
        block = text[start_idx:end_idx]
        for line in block.splitlines():
            ls = line.lstrip()
            if ls.startswith("(property "):
                return line[: len(line) - len(ls)]
        # Fallback: use indent of the closing line
        # Find start of closing line
        line_start = text.rfind("\n", start_idx, end_idx)
        if line_start == -1:
            return "  "  # default two spaces
        # indent equals the whitespace prefix of the closing line
        j = line_start + 1
        indent = ""
        while j < len(text) and text[j] in (" ", "\t"):
            indent += text[j]
            j += 1
        return indent or "  "

    out = original_text
    for name, prop_name, prop_value in additions:
        search_pos = 0
        while True:
            starts = find_all_symbol_starts(out[search_pos:], name)
            if not starts:
                break
            # adjust to absolute positions
            start_idx = search_pos + starts[0]
            end_idx = find_matching_paren(out, start_idx)
            if end_idx == -1:
                # malformed; skip this occurrence
                search_pos = start_idx + 1
                continue
            indent = indent_for_block(out, start_idx, end_idx)
            # Build a full property block per KiCAD-checked template (official-prop-template.txt)
            # We preserve indentation by nesting subsequent lines with two extra spaces.
            ind2 = indent + ("  " if indent else "  ")
            ind3 = ind2 + "  "
            ind4 = ind3 + "  "
            block = (
                f"{indent}(property \"{prop_name}\" \"{prop_value}\"{newline}"
                f"{ind2}(at 0 0 0){newline}"
                f"{ind2}(effects{newline}"
                f"{ind3}(font{newline}"
                f"{ind4}(size 1.27 1.27){newline}"
                f"{ind3}){newline}"
                f"{ind3}(hide yes){newline}"
                f"{ind2}){newline}"
                f"{indent}){newline}"
            )
            # insert just before the closing paren, respecting line structure
            out = out[:end_idx] + block + out[end_idx:]
            # advance search position past the inserted content to avoid infinite loop
            search_pos = end_idx + len(block) + 1
    return out
