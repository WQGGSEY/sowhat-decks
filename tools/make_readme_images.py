"""Build the README images in docs/img/ from the rendered example slides.

    python3 tools/make_readme_images.py

Needs Pillow (a development tool only; the skills do not use it). Every image is
made from files in examples/, so it shows real output, nothing drawn by hand:

- hero.png               six slides from the three example decks
- review-before-after.png  the same slide in the draft (with deck-review's boxes) and rebuilt
- before-after-titles.png  the draft's titles next to the rebuilt deck's titles
- demo.gif               draft -> review -> titles -> rebuilt slides -> review result
"""
from __future__ import annotations

import pathlib
import re

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
EX = ROOT / "examples"
OUT = ROOT / "docs" / "img"
INK, GREY, LINE, ACCENT, RED, BG = (31, 41, 55), (100, 110, 125), (210, 214, 220), (31, 90, 166), (196, 48, 43), (255, 255, 255)
FONT_DIRS = ["/System/Library/Fonts/Supplemental", "/Library/Fonts", "C:/Windows/Fonts",
             "/usr/share/fonts/truetype/msttcorefonts", "/usr/share/fonts/truetype/dejavu"]


def font(size: int, bold: bool = False, serif: bool = False):
    names = (["Georgia Bold.ttf", "georgiab.ttf"] if bold else ["Georgia.ttf", "georgia.ttf"]) if serif else \
        (["Arial Bold.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"] if bold else ["Arial.ttf", "arial.ttf", "DejaVuSans.ttf"])
    for d in FONT_DIRS:
        for n in names:
            p = pathlib.Path(d) / n
            if p.is_file():
                return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def slide(path: pathlib.Path, width: int) -> Image.Image:
    im = Image.open(path).convert("RGB")
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def framed(im: Image.Image) -> Image.Image:
    out = Image.new("RGB", (im.width + 2, im.height + 2), LINE)
    out.paste(im, (1, 1))
    return out


def save_png(im: Image.Image, path: pathlib.Path, colors: int = 128) -> None:
    im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(path, optimize=True)
    print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size // 1024} KB)")


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line] if line else lines


def titles_from(storyline: pathlib.Path) -> list[str]:
    return re.findall(r"^### \d+\. (.+)$", storyline.read_text(encoding="utf-8"), re.M)


def hero() -> None:
    picks = [("03-review-before-after", 2), ("01-investor-update", 6), ("02-market-entry", 4),
             ("03-review-before-after", 5), ("02-market-entry", 13), ("03-review-before-after", 12)]
    tile_w, gap = 520, 20
    tiles = [framed(slide(EX / ex / "preview" / f"slide-{n:02d}.png", tile_w)) for ex, n in picks]
    tw, th = tiles[0].size
    im = Image.new("RGB", (3 * tw + 4 * gap, 2 * th + 3 * gap), BG)
    for i, t in enumerate(tiles):
        im.paste(t, (gap + (i % 3) * (tw + gap), gap + (i // 3) * (th + gap)))
    save_png(im, OUT / "hero.png")


def before_after() -> None:
    w, gap, head = 780, 24, 64
    left = framed(slide(EX / "03-review-before-after" / "before-review" / "annotated" / "slide-05.png", w))
    right = framed(slide(EX / "03-review-before-after" / "preview" / "slide-05.png", w))
    im = Image.new("RGB", (2 * left.width + 3 * gap, left.height + head + gap), BG)
    d = ImageDraw.Draw(im)
    d.text((gap, 18), "Draft: label title, chart pasted as a picture, no source", font=font(24, True), fill=RED)
    d.text((2 * gap + left.width, 18), "Rebuilt: the title states the finding; native chart, sourced",
           font=font(24, True), fill=ACCENT)
    im.paste(left, (gap, head))
    im.paste(right, (2 * gap + left.width, head))
    save_png(im, OUT / "review-before-after.png")


def titles_image() -> Image.Image:
    before = titles_from(EX / "storyline-tests" / "control-topic-titles" / "storyline.md")[1:13]
    after = titles_from(EX / "03-review-before-after" / "storyline.md")[1:13]
    w, h, pad, col_l = 1600, 900, 56, 430
    im = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(im)
    d.text((pad, 34), "Read only the titles: the same Q3 board update (sample data)", font=font(34, serif=True), fill=INK)
    d.text((pad, 96), "Draft", font=font(22, True), fill=RED)
    d.text((pad + col_l, 96), "Rebuilt with SoWhat Decks", font=font(22, True), fill=ACCENT)
    d.line([(pad, 130), (w - pad, 130)], fill=INK, width=2)
    y, f_left, f_right = 144, font(21), font(21)
    row_h = (h - y - 40) // len(after)
    for b, a in zip(before, after):
        d.text((pad, y + 6), b, font=f_left, fill=GREY)
        lines = wrap(d, a, f_right, w - 2 * pad - col_l)
        for k, line in enumerate(lines[:2]):
            d.text((pad + col_l, y + 6 + k * 25), line, font=f_right, fill=INK)
        y += row_h
        d.line([(pad, y - 4), (w - pad, y - 4)], fill=LINE, width=1)
    return im


def titles() -> None:
    save_png(titles_image(), OUT / "before-after-titles.png", colors=96)


def card(caption: str, body: Image.Image | None = None, text: list[str] | None = None) -> Image.Image:
    w, h, head = 960, 600, 60
    im = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, head], fill=INK)
    d.text((24, head // 2), caption, font=font(24, True), fill=BG, anchor="lm")
    if body is not None:
        b = slide_im(body, w - 40)
        im.paste(framed(b), (19, head + 10))
    for i, line in enumerate(text or []):
        d.text((40, head + 40 + i * 44), line, font=font(26, serif=True), fill=INK)
    return im


def titles_card(titles: list[str]) -> Image.Image:
    im = card("4  deck-storyline writes titles that make the argument")
    d = ImageDraw.Draw(im)
    f, y = font(24, serif=True), 100
    for t in titles:
        for line in wrap(d, t, f, 900)[:2]:
            d.text((32, y), line, font=f, fill=INK)
            y += 32
        y += 18
    return im


def slide_im(im: Image.Image, width: int) -> Image.Image:
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def demo() -> None:
    e3 = EX / "03-review-before-after"
    frames = [
        card("1  A draft board deck (sample data)", Image.open(e3 / "before-review" / "render" / "slide-05.png").convert("RGB")),
        card("2  deck-review boxes what a reviewer would catch", Image.open(e3 / "before-review" / "annotated" / "slide-05.png").convert("RGB")),
        card("3  Its titles read like an agenda", text=["Executive summary", "Bookings performance", "Q3 ARR bridge",
                                                       "Churn by segment", "Q4 outlook", "Next steps"]),
        titles_card(titles_from(e3 / "storyline.md")[1:6]),
        card("5  deck-build: native charts, a source on every exhibit", Image.open(e3 / "preview" / "slide-05.png").convert("RGB")),
        card("5  deck-build: the deck ends on the decision", Image.open(e3 / "preview" / "slide-12.png").convert("RGB")),
        card("6  deck-review on the rebuilt deck: 0 high, 0 medium",
             text=["Draft:    1 high, 18 medium, 11 low", "Rebuilt:  0 high, 0 medium, 12 low",
                   "", "examples/03-review-before-after"]),
    ]
    pal =[f.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for f in frames]
    path = OUT / "demo.gif"
    pal[0].save(path, save_all=True, append_images=pal[1:], duration=[2200, 2600, 2200, 3200, 2600, 2600, 2600],
                loop=0, optimize=True)
    print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size // 1024} KB)")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    hero()
    before_after()
    titles()
    demo()


if __name__ == "__main__":
    main()
