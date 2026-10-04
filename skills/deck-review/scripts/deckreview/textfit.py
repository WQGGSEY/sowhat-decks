"""Estimate how much room text needs, without a renderer.

Widths come from a Helvetica/Arial width table (1/1000 em) scaled by a per-font
factor. East Asian characters count as one full em. The result is an estimate
(roughly +/-10%); checks use generous tolerances on top of it.
"""

from __future__ import annotations

import unicodedata

_ARIAL = {
    " ": 278, "!": 278, '"': 355, "#": 556, "$": 556, "%": 889, "&": 667, "'": 191,
    "(": 333, ")": 333, "*": 389, "+": 584, ",": 278, "-": 333, ".": 278, "/": 278,
    ":": 278, ";": 278, "<": 584, "=": 584, ">": 584, "?": 556, "@": 1015,
    "[": 278, "\\": 278, "]": 278, "^": 469, "_": 556, "`": 333, "{": 334, "|": 260,
    "}": 334, "~": 584,
    "A": 667, "B": 667, "C": 722, "D": 722, "E": 667, "F": 611, "G": 778, "H": 722,
    "I": 278, "J": 500, "K": 667, "L": 556, "M": 833, "N": 722, "O": 778, "P": 667,
    "Q": 778, "R": 722, "S": 667, "T": 611, "U": 722, "V": 667, "W": 944, "X": 667,
    "Y": 667, "Z": 611,
    "a": 556, "b": 556, "c": 500, "d": 556, "e": 556, "f": 278, "g": 556, "h": 556,
    "i": 222, "j": 222, "k": 500, "l": 222, "m": 833, "n": 556, "o": 556, "p": 556,
    "q": 556, "r": 333, "s": 500, "t": 278, "u": 556, "v": 500, "w": 722, "x": 500,
    "y": 500, "z": 500,
}
for _d in "0123456789":
    _ARIAL[_d] = 556

# Average width relative to Arial. Unknown fonts use 1.0.
_FONT_FACTOR = [
    ("calibri", 0.90), ("carlito", 0.90), ("aptos", 0.97), ("helvetica", 1.0),
    ("arial narrow", 0.82), ("arial", 1.0), ("liberation sans", 1.0),
    ("times", 0.90), ("liberation serif", 0.90), ("georgia", 1.02), ("cambria", 0.95),
    ("garamond", 0.86), ("verdana", 1.14), ("tahoma", 1.0), ("segoe", 0.98),
    ("trebuchet", 0.98), ("century gothic", 1.10), ("gill sans", 0.92),
    ("franklin gothic", 0.92), ("open sans", 1.04), ("roboto", 0.98), ("lato", 0.95),
    ("inter", 1.04), ("noto sans", 1.03), ("source sans", 0.92), ("montserrat", 1.12),
    ("futura", 1.0), ("avenir", 1.0), ("malgun", 1.0), ("meiryo", 1.03),
]
_MONO = ("courier", "mono", "consolas", "menlo", "monaco")


def is_wide(ch: str) -> bool:
    """True for characters that take a full em (CJK, Hangul, Kana, full-width)."""
    return unicodedata.east_asian_width(ch) in ("W", "F")


def font_factor(font: str | None) -> float:
    name = (font or "").lower()
    for key, factor in _FONT_FACTOR:
        if key in name:
            return factor
    return 1.0


def char_width_pt(ch: str, size_pt: float, font: str | None = None, bold: bool = False) -> float:
    if is_wide(ch):
        return size_pt
    name = (font or "").lower()
    if any(m in name for m in _MONO):
        em = 0.60
    else:
        em = _ARIAL.get(ch, 556) / 1000.0 * font_factor(font)
    if bold:
        em *= 1.06
    return em * size_pt


def _tokens(chars):
    """Split styled chars into wrap tokens: words keep their trailing space; each
    wide (CJK) char is its own token; '\n' is a forced break token."""
    tokens, cur = [], []
    for item in chars:
        ch = item[0]
        if ch == "\n":
            if cur:
                tokens.append(cur)
                cur = []
            tokens.append("\n")
        elif is_wide(ch):
            if cur:
                tokens.append(cur)
                cur = []
            tokens.append([item])
        elif ch in " \t":
            cur.append(item)
            tokens.append(cur)
            cur = []
        else:
            cur.append(item)
    if cur:
        tokens.append(cur)
    return tokens


def measure(chars, avail_w_pt: float, wrap: bool = True):
    """Lay out one paragraph.

    chars: list of (char, size_pt, font, bold).
    Returns dict(lines, max_line_w_pt, widest_token_pt, line_sizes) where
    line_sizes is the largest font size on each line (for line height).
    """
    avail = max(avail_w_pt, 1.0)
    lines = []  # list of [width, max_size]
    cur_w, cur_size = 0.0, 0.0
    widest = 0.0
    started = False

    def width_of(tok, strip_trailing=False):
        items = tok
        if strip_trailing:
            while items and items[-1][0] in " \t":
                items = items[:-1]
        return sum(char_width_pt(c, s, f, b) for c, s, f, b in items)

    for tok in _tokens(chars):
        if tok == "\n":
            lines.append([cur_w, cur_size])
            cur_w, cur_size, started = 0.0, 0.0, False
            continue
        tw = width_of(tok)
        tw_trim = width_of(tok, strip_trailing=True)
        tsize = max((s for _, s, _, _ in tok), default=0.0)
        widest = max(widest, tw_trim)
        if wrap and started and cur_w + tw_trim > avail:
            lines.append([cur_w, cur_size])
            cur_w, cur_size = 0.0, 0.0
        if wrap and tw_trim > avail:
            # A single token wider than the line breaks across lines.
            n_extra = int(tw_trim // avail)
            for _ in range(n_extra):
                lines.append([avail, tsize])
            cur_w = tw_trim - n_extra * avail
        else:
            cur_w += tw
        cur_size = max(cur_size, tsize)
        started = True
    lines.append([cur_w, cur_size])
    # Trailing spaces do not take room at the end of a line.
    max_w = max((w for w, _ in lines), default=0.0)
    return {
        "lines": len(lines),
        "max_line_w_pt": round(max_w, 2),
        "widest_token_pt": round(widest, 2),
        "line_sizes": [s for _, s in lines],
    }
