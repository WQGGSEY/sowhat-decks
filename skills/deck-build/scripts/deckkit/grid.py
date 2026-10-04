"""Boxes in EMU and a 12-column grid."""
from __future__ import annotations

from dataclasses import dataclass, replace

EMU_PER_INCH = 914400
EMU_PER_PT = 12700


def inch(v: float) -> int:
    return int(round(v * EMU_PER_INCH))


def pt(v: float) -> int:
    return int(round(v * EMU_PER_PT))


def to_pt(emu: int) -> float:
    return emu / EMU_PER_PT


@dataclass(frozen=True)
class Box:
    x: int
    y: int
    w: int
    h: int

    @property
    def right(self) -> int:
        return self.x + self.w

    @property
    def bottom(self) -> int:
        return self.y + self.h

    def moved(self, **kw) -> "Box":
        return replace(self, **kw)

    def inset(self, left: int = 0, top: int = 0, right: int = 0, bottom: int = 0) -> "Box":
        return Box(self.x + left, self.y + top, max(0, self.w - left - right), max(0, self.h - top - bottom))

    def take_top(self, h: int, gap: int = 0) -> tuple["Box", "Box"]:
        """Split into a top strip of height h and the rest below it (after gap)."""
        h = min(h, self.h)
        return Box(self.x, self.y, self.w, h), Box(self.x, self.y + h + gap, self.w, max(0, self.h - h - gap))

    def rows(self, n: int, gap: int = 0) -> list["Box"]:
        each = (self.h - gap * (n - 1)) // n
        return [Box(self.x, self.y + i * (each + gap), self.w, each) for i in range(n)]

    def cols(self, n: int, gap: int = 0) -> list["Box"]:
        each = (self.w - gap * (n - 1)) // n
        return [Box(self.x + i * (each + gap), self.y, each, self.h) for i in range(n)]

    def inside(self, outer: "Box", tolerance: int = 0) -> bool:
        return (self.x >= outer.x - tolerance and self.y >= outer.y - tolerance
                and self.right <= outer.right + tolerance and self.bottom <= outer.bottom + tolerance)


@dataclass(frozen=True)
class Grid:
    """12 columns with gutters across a body box. Columns are numbered 1..12."""
    body: Box
    cols: int = 12
    gutter: int = inch(0.2)

    @property
    def col_w(self) -> float:
        return (self.body.w - self.gutter * (self.cols - 1)) / self.cols

    def x(self, col: int) -> int:
        return self.body.x + int(round((col - 1) * (self.col_w + self.gutter)))

    def width(self, span: int) -> int:
        return int(round(span * self.col_w + (span - 1) * self.gutter))

    def span(self, start: int, span: int, y: int | None = None, h: int | None = None) -> Box:
        """Box over columns start..start+span-1, full body height unless y/h given."""
        if start < 1 or start + span - 1 > self.cols:
            raise ValueError(f"columns {start}..{start + span - 1} are outside the {self.cols}-column grid")
        return Box(self.x(start), self.body.y if y is None else y, self.width(span), self.body.h if h is None else h)

    def equal(self, n: int, start: int = 1, span: int | None = None) -> list[Box]:
        """n equal boxes across the given columns, separated by the gutter."""
        area = self.span(start, span or self.cols)
        each = (area.w - self.gutter * (n - 1)) / n
        return [Box(int(round(area.x + i * (each + self.gutter))), area.y, int(each), area.h) for i in range(n)]
