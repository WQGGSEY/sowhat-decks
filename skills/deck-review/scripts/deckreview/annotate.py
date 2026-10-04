"""Draw numbered boxes around problems on rendered slide PNGs (needs Pillow)."""

from __future__ import annotations

from pathlib import Path

SEVERITY_COLORS = {"high": (214, 39, 40), "medium": (240, 120, 0), "low": (200, 160, 0)}


def marks_for_slide(issues, slide_index):
    """[(number, issue, bbox)] for every located issue that points at this slide."""
    marks = []
    for n, issue in enumerate(issues, start=1):
        num = issue.get("n", n)
        if issue.get("slide") == slide_index and issue.get("bbox"):
            marks.append((num, issue, issue["bbox"]))
        for loc in issue.get("locations", []) or []:
            if loc.get("slide") == slide_index and loc.get("bbox"):
                marks.append((num, issue, loc["bbox"]))
    return marks


def _font(size):
    from PIL import ImageFont

    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # Pillow < 10.1
        return ImageFont.load_default()


def annotate(pngs: dict, issues: list, deck: dict, out_dir) -> list[Path]:
    """Write annotated copies of the PNGs that have located issues.

    pngs: {slide_index: path to rendered PNG}. Returns the written paths.
    """
    from PIL import Image, ImageDraw

    out_dir = Path(out_dir)
    written = []
    for slide_index in sorted(pngs):
        marks = marks_for_slide(issues, slide_index)
        if not marks:
            continue
        with Image.open(pngs[slide_index]) as src:
            im = src.convert("RGB")
        sx = im.width / deck["slide_width"]
        sy = im.height / deck["slide_height"]
        draw = ImageDraw.Draw(im)
        line = max(2, im.width // 400)
        font = _font(max(12, im.width // 60))
        placed = []
        for num, issue, (x, y, w, h) in marks:
            color = SEVERITY_COLORS.get(issue.get("severity"), SEVERITY_COLORS["low"])
            x0 = min(max(0, round(x * sx)), im.width - 1)
            y0 = min(max(0, round(y * sy)), im.height - 1)
            x1 = min(max(x0 + 1, round((x + w) * sx)), im.width - 1)
            y1 = min(max(y0 + 1, round((y + h) * sy)), im.height - 1)
            draw.rectangle([x0, y0, x1, y1], outline=color, width=line)
            label = f"#{num}"
            tb = draw.textbbox((0, 0), label, font=font)
            tw, th = tb[2] - tb[0] + 8, tb[3] - tb[1] + 6
            lx, ly = x0, y0 - th if y0 - th >= 0 else y0 + line
            while (lx, ly) in placed:  # keep labels on the same corner readable
                lx += tw + 2
            placed.append((lx, ly))
            draw.rectangle([lx, ly, lx + tw, ly + th], fill=color)
            draw.text((lx + 4, ly + 3 - tb[1]), label, fill=(255, 255, 255), font=font)
        out_dir.mkdir(parents=True, exist_ok=True)
        dest = out_dir / Path(pngs[slide_index]).name
        im.save(dest)
        written.append(dest)
    return written
