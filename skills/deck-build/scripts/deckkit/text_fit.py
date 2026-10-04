"""Estimate text size from per-font width tables and shrink text to fit a box.

No font files and no rendering: widths come from deckkit/widths.py (advance
widths in 1/1000 em). Estimates are deliberately a little pessimistic:
SAFETY widens every measured line, CJK glyphs count as a full em, and Korean
wraps only at spaces.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .widths import CHARS, TABLES

SAFETY = 1.03          # measured width x SAFETY must fit the line
LINE_HEIGHT = 1.2      # line pitch / font size for Latin text ("single" spacing)
LINE_HEIGHT_CJK = 1.3  # East Asian fonts have taller line boxes

_INDEX = {ch: i for i, ch in enumerate(CHARS)}
_TABLES = {name: [int(v) for v in data.split(",")] for name, data in TABLES.items()}
_ALIASES = {
    "calibri": "arial", "calibri light": "arial", "aptos": "arial", "aptos display": "arial",
    "helvetica": "arial", "helvetica neue": "arial", "liberation sans": "arial", "arimo": "arial",
    "segoe ui": "verdana", "cambria": "georgia", "garamond": "times new roman",
    "liberation serif": "times new roman", "book antiqua": "georgia", "palatino linotype": "georgia",
}
_CLOSING = set("、。，．）」』】〕〉》！？：；ー・,.)!?:;")


@lru_cache(maxsize=64)
def _table(font: str, bold: bool) -> list[int]:
    name = (font or "arial").strip().lower()
    name = _ALIASES.get(name, name)
    if name not in _TABLES:
        name = "georgia" if ("serif" in name and "sans" not in name) else "arial"
    return _TABLES.get(f"{name} bold" if bold else name) or _TABLES[name]


def is_hangul(ch: str) -> bool:
    o = ord(ch)
    return 0xAC00 <= o <= 0xD7A3 or 0x1100 <= o <= 0x11FF or 0x3130 <= o <= 0x318F or 0xA960 <= o <= 0xA97F


def is_cjk(ch: str) -> bool:
    o = ord(ch)
    return (0x1100 <= o <= 0x11FF or 0x2E80 <= o <= 0x9FFF or 0xA960 <= o <= 0xA97F
            or 0xAC00 <= o <= 0xD7FF or 0xF900 <= o <= 0xFAFF or 0xFE30 <= o <= 0xFE4F
            or 0xFF00 <= o <= 0xFF60 or 0xFFE0 <= o <= 0xFFE6 or 0x20000 <= o <= 0x3FFFF)


def _breakable_cjk(ch: str) -> bool:
    """Han and kana break between characters. Hangul wraps at spaces (pessimistic)."""
    return is_cjk(ch) and not is_hangul(ch)


def has_cjk(text: str) -> bool:
    return any(is_cjk(ch) for ch in text)


def line_pitch(text: str) -> float:
    """Line height as a multiple of the font size."""
    return LINE_HEIGHT_CJK if has_cjk(text) else LINE_HEIGHT


def _units(text: str, table: list[int]) -> int:
    """Advance width in 1/1000 em."""
    total = 0
    for ch in text:
        i = _INDEX.get(ch)
        if i is not None:
            total += table[i]
        elif 0xFF61 <= ord(ch) <= 0xFF9F:  # half-width katakana
            total += 500
        elif is_cjk(ch):
            total += 1000
        else:
            total += table[_INDEX["n"]]
    return total


def text_width(text: str, font: str = "Arial", size: float = 12, bold: bool = False) -> float:
    """Width of one line of text in points (no wrapping, no safety margin)."""
    return _units(text, _table(font, bold)) * size / 1000.0


def _tokens(text: str) -> list[str]:
    """Split into unbreakable tokens; trailing spaces stay on their token."""
    toks: list[str] = []
    for ch in text:
        if ch == " ":
            if toks:
                toks[-1] += ch
            else:
                toks.append(ch)
        elif ch in _CLOSING and toks and not toks[-1].endswith(" "):
            toks[-1] += ch
        elif (_breakable_cjk(ch) or not toks or toks[-1].endswith(" ")
              or _breakable_cjk(toks[-1][-1])):
            toks.append(ch)
        else:
            toks[-1] += ch
    return toks


def wrap(text: str, font: str = "Arial", size: float = 12, width_pt: float = 100,
         bold: bool = False) -> list[str]:
    """Greedy line breaking like PowerPoint's word wrap. Returns the lines.

    Each token is measured once; a line's width is the running sum (trailing spaces
    do not count at a line end).
    """
    table = _table(font, bold)
    limit = width_pt / SAFETY * 1000.0 / size  # in 1/1000 em
    lines: list[str] = []
    for segment in text.split("\n"):
        line, used = "", 0
        for tok in _tokens(segment):
            core = tok.rstrip(" ")
            core_u = _units(core, table)
            tok_u = core_u + _units(tok[len(core):], table)
            if used + core_u <= limit:
                line, used = line + tok, used + tok_u
                continue
            if line:
                lines.append(line.rstrip())
            line, used = "", 0
            for ch in tok:  # a token wider than the line breaks between characters
                ch_u = _units(ch, table)
                if line and ch != " " and used + ch_u > limit:
                    lines.append(line)
                    line, used = "", 0
                line, used = line + ch, used + ch_u
        lines.append(line.rstrip())
    return lines


@dataclass
class Para:
    """One paragraph. Its size is round(base * scale), but never below min_size."""
    text: str
    bold: bool = False
    scale: float = 1.0
    font: str | None = None
    min_size: float = 0
    space_before: float = 0.0  # in lines of this paragraph's size
    indent: float = 0.0        # left indent in points (bullets)
    size: float | None = None  # fixed size; ignores base and scale

    def size_at(self, base: float) -> float:
        return self.size if self.size is not None else max(self.min_size, round(base * self.scale))


@dataclass
class Fit:
    size: float
    sizes: list[float]
    para_lines: list[int]
    height_pt: float
    overflow: bool

    @property
    def lines(self) -> int:
        return sum(self.para_lines)


def measure(paras: list[Para], base: float, width_pt: float, font: str = "Arial") -> tuple[list[float], list[int], float]:
    """(size, line count) per paragraph and the total height in points at a base size."""
    sizes, counts, height = [], [], 0.0
    for i, p in enumerate(paras):
        s = p.size_at(base)
        n = len(wrap(p.text, p.font or font, s, width_pt - p.indent, p.bold)) if p.text else 1
        height += n * s * line_pitch(p.text) + (p.space_before * s if i else 0)
        sizes.append(s)
        counts.append(n)
    return sizes, counts, height


def fit(paras: list[Para], width_pt: float, height_pt: float, max_size: float, min_size: float,
        font: str = "Arial", max_lines: int | None = None) -> Fit:
    """Largest whole-point base size in [min_size, max_size] whose text fits the box.

    If nothing fits, returns min_size with overflow=True.
    """
    base = max_size
    while True:
        sizes, counts, height = measure(paras, base, width_pt, font)
        ok = height <= height_pt + 0.01 and (max_lines is None or sum(counts) <= max_lines)
        if ok or base - 1 < min_size - 1e-9:
            return Fit(base, sizes, counts, height, not ok)
        base -= 1
