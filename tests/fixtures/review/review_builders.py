"""Deck builders for deck-review tests.

Builds small .pptx files with python-pptx so tests never depend on binary
fixtures. Two decks carry 10 deliberately seeded defects (SEEDED_DEFECTS);
one clean deck is the false-positive guard.

Run directly to write the decks somewhere you can open them:

    python tests/fixtures/review/review_builders.py out/review-fixtures
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Emu, Inches, Pt

WIDE_W = Inches(13.333)
WIDE_H = Inches(7.5)
ACCENT = RGBColor(0x1F, 0x5A, 0xA6)
GRAY = RGBColor(0x59, 0x59, 0x59)

LAYOUT_TITLE = 0
LAYOUT_TITLE_ONLY = 5
LAYOUT_BLANK = 6


# ---------------------------------------------------------------- primitives


def new_deck(wide: bool = True) -> Presentation:
    prs = Presentation()
    if wide:
        prs.slide_width = WIDE_W
        prs.slide_height = WIDE_H
    return prs


def add_cover(prs, title: str, subtitle: str = "October 2026"):
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_TITLE])
    slide.shapes.title.text = title
    slide.shapes.title.left, slide.shapes.title.top = Inches(0.6), Inches(2.4)
    slide.shapes.title.width, slide.shapes.title.height = Inches(12.1), Inches(1.4)
    sub = slide.placeholders[1]
    sub.text = subtitle
    sub.left, sub.top, sub.width, sub.height = Inches(0.6), Inches(4.0), Inches(12.1), Inches(0.8)
    return slide


def add_titled_slide(prs, title: str, size: int = 28):
    """Title-only layout with the title placed for a 16:9 slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_TITLE_ONLY])
    t = slide.shapes.title
    t.left, t.top, t.width, t.height = Inches(0.6), Inches(0.4), Inches(12.1), Inches(1.1)
    t.text = title
    for p in t.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(size)
    return slide


def add_text(slide, text, left, top, width, height, size=14, font=None,
             color=None, bold=None, name=None):
    """Add a word-wrapped text box. `text` may be a list of paragraphs."""
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    if name:
        box.name = name
    tf = box.text_frame
    tf.word_wrap = True
    paras = text if isinstance(text, list) else [text]
    for i, ptxt in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        run = p.add_run()
        run.text = ptxt
        run.font.size = Pt(size)
        if font:
            run.font.name = font
        if color is not None:
            run.font.color.rgb = color
        if bold is not None:
            run.font.bold = bold
    return box


def add_source(slide, text="Source: Company financials, FY2025 (sample data)", top=6.85):
    return add_text(slide, text, 0.6, top, 12.1, 0.35, size=10, color=GRAY, name="Source")


def add_bar_chart(slide, left=0.6, top=1.7, width=8.0, height=4.8, single_color=True):
    data = CategoryChartData()
    data.categories = ["Q1", "Q2", "Q3", "Q4"]
    data.add_series("Revenue ($M)", (3.1, 3.4, 4.2, 4.6))
    gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(left), Inches(top),
                                Inches(width), Inches(height), data)
    chart = gf.chart
    chart.has_legend = False
    if single_color:
        fill = chart.plots[0].series[0].format.fill
        fill.solid()
        fill.fore_color.rgb = ACCENT
    return gf


def add_table(slide, rows, left=0.6, top=1.7, width=8.0, row_h=0.45, size=12):
    n_rows, n_cols = len(rows), len(rows[0])
    gf = slide.shapes.add_table(n_rows, n_cols, Inches(left), Inches(top), Inches(width),
                                Inches(row_h * n_rows))
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = gf.table.cell(r, c)
            cell.text = str(val)
            for p in cell.text_frame.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(size)
    return gf


def chart_png_bytes(width=900, height=560) -> bytes:
    """A bar chart drawn as a flat image, the way a pasted matplotlib/Excel chart looks."""
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (width, height), "white")
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = 80, 40, width - 40, height - 70
    d.line([(x0, y0), (x0, y1)], fill=(40, 40, 40), width=3)  # y axis
    d.line([(x0, y1), (x1, y1)], fill=(40, 40, 40), width=3)  # x axis
    for gy in range(y0, y1, 80):  # light gridlines
        d.line([(x0 + 3, gy), (x1, gy)], fill=(220, 220, 220), width=1)
    values = [0.45, 0.6, 0.8, 0.95, 0.7]
    bw = (x1 - x0) // (len(values) * 2)
    for i, v in enumerate(values):
        bx = x0 + bw // 2 + i * bw * 2
        d.rectangle([bx, y1 - int(v * (y1 - y0)), bx + bw, y1 - 2], fill=(31, 90, 166))
        d.text((bx + 4, y1 + 10), f"Y{i + 1}", fill=(40, 40, 40))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def photo_png_bytes(width=600, height=400) -> bytes:
    """A noisy many-colored image that should NOT look like a chart."""
    import random

    from PIL import Image

    rnd = random.Random(7)
    img = Image.new("RGB", (width, height))
    px = img.load()
    for y in range(height):
        for x in range(width):
            px[x, y] = (rnd.randrange(256), (x * 3 + rnd.randrange(60)) % 256,
                        (y * 2 + rnd.randrange(60)) % 256)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ---------------------------------------------------------------- seeded decks

# (deck key, slide number or None for deck level, check id, description)
SEEDED_DEFECTS = [
    ("flawed1", 2, "title_not_claim", "topic-label title 'Market Overview'"),
    ("flawed1", 3, "font_below_floor", "body text at 9 pt"),
    ("flawed1", 4, "text_overflow", "~150 words in a 4 x 1.2 in box"),
    ("flawed1", 5, "off_slide", "text box runs past the right edge"),
    ("flawed1", 6, "missing_source", "native chart with no source line"),
    ("flawed2", 2, "chart_as_image", "bar chart pasted as a PNG"),
    ("flawed2", 3, "overlap", "two text boxes on top of each other"),
    ("flawed2", 4, "font_count", "four font families in one deck"),
    ("flawed2", 5, "accent_colors", "red, green and orange accents next to blue"),
    ("flawed2", 6, "misaligned", "two boxes whose left edges differ by 0.08 in"),
]

LONG_TEXT = (
    "Our analysis of the three candidate markets looked at population, online "
    "penetration, spending per user, competitive intensity, regulatory hurdles, "
    "payment infrastructure and the availability of local partners. Each market was "
    "scored on a five-point scale for every criterion, and the scores were weighted "
    "by how much each criterion drove revenue in our existing markets. The weighting "
    "came from a regression on twelve quarters of data across four countries. Vietnam "
    "scored highest on five of seven criteria, Indonesia scored highest on market size "
    "but lowest on payments, and Thailand was in the middle on most criteria. The "
    "result held under three alternative weightings that we tested with the regional "
    "teams during the September workshop."
)


def build_flawed_deck_1(path) -> Path:
    prs = new_deck()
    add_cover(prs, "Q3 board update")

    s = add_titled_slide(prs, "Market Overview")  # defect: topic label
    add_text(s, ["Online learning spend grew 14% a year since 2021.",
                 "Two incumbents hold 60% of paying users."], 0.6, 1.7, 12.1, 2.0, size=16)

    s = add_titled_slide(prs, "Mid-market deals closed 20% faster after the pricing change")
    add_text(s, ["Median sales cycle fell from 92 to 74 days.",
                 "Discount requests fell by a third."], 0.6, 1.7, 12.1, 2.0, size=9,
             name="Tiny body")  # defect: 9 pt body

    s = add_titled_slide(prs, "Vietnam scores highest on five of seven criteria")
    add_text(s, LONG_TEXT, 0.6, 1.7, 4.0, 1.2, size=16, name="Overflowing box")  # defect

    s = add_titled_slide(prs, "Two hires in onboarding would cut early churn by a third")
    add_text(s, ["Accounts that finish setup in week one churn at a third of the rate."],
             0.6, 1.7, 6.0, 1.5, size=16)
    add_text(s, ["Onboarding team: 2 FTE"], 10.0, 4.0, 5.0, 1.0, size=16,
             name="Off-slide box")  # defect: right edge at 15 in > 13.33 in

    s = add_titled_slide(prs, "Revenue grew every quarter and reached $4.6M in Q4")
    add_bar_chart(s)  # defect: no source line

    prs.save(str(path))
    return Path(path)


def build_flawed_deck_2(path) -> Path:
    prs = new_deck()
    add_cover(prs, "Market entry recommendation")

    s = add_titled_slide(prs, "Vietnam's online population grew fastest over five years")
    s.shapes.add_picture(io.BytesIO(chart_png_bytes()), Inches(0.6), Inches(1.7),
                         Inches(8.0), Inches(4.8))  # defect: chart as image
    add_source(s, "Source: World Bank WDI (sample data)")

    s = add_titled_slide(prs, "Customers cancel over missing integrations, not price")
    add_text(s, ["41% of churned accounts cited a missing integration."], 0.6, 1.7, 6.0, 1.0,
             size=16, name="Finding A")
    add_text(s, ["Only 12% cited price as the main reason."], 0.9, 1.9, 6.0, 1.0,
             size=16, name="Finding B")  # defect: overlaps Finding A

    s = add_titled_slide(prs, "Three partners can cover payments in all four markets")
    add_text(s, ["Partner A covers Vietnam and Thailand."], 0.6, 1.7, 12.1, 0.6, size=16,
             font="Times New Roman")
    add_text(s, ["Partner B covers Indonesia."], 0.6, 2.5, 12.1, 0.6, size=16,
             font="Courier New")
    add_text(s, ["Partner C covers the Philippines."], 0.6, 3.3, 12.1, 0.6, size=16,
             font="Georgia")  # defect: Calibri + 3 more fonts

    s = add_titled_slide(prs, "Launch in Vietnam first and reassess Indonesia after six months")
    for i, (label, rgb) in enumerate([
        ("Vietnam: launch", RGBColor(0x1F, 0x5A, 0xA6)),
        ("Indonesia: wait", RGBColor(0xD0, 0x21, 0x21)),
        ("Thailand: partner", RGBColor(0x2E, 0xA0, 0x43)),
        ("Philippines: monitor", RGBColor(0xF2, 0x8C, 0x18)),
    ]):  # defect: four accent hues
        box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6 + i * 3.1), Inches(2.0),
                                 Inches(2.8), Inches(1.6))
        box.fill.solid()
        box.fill.fore_color.rgb = rgb
        box.line.fill.background()
        box.text_frame.text = label
        for r in box.text_frame.paragraphs[0].runs:
            r.font.size = Pt(16)
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    s = add_titled_slide(prs, "A two-phase launch limits the downside to one market's budget")
    add_text(s, ["Phase 1: Vietnam, six months, $400k budget."], 0.6, 1.7, 12.1, 0.8, size=16)
    add_text(s, ["Phase 2: Indonesia only if CAC is under $30."], 0.68, 2.8, 12.0, 0.8,
             size=16)  # defect: left edge 0.08 in off

    prs.save(str(path))
    return Path(path)


def build_clean_deck(path) -> Path:
    """A deck that follows the rules. Should produce no high/medium issues."""
    prs = new_deck()
    add_cover(prs, "Q3 board update")

    s = add_titled_slide(prs, "Revenue grew 18% in Q3, driven by mid-market expansion")
    add_text(s, ["Mid-market bookings rose 31% while SMB was flat.",
                 "Average deal size grew from $22k to $27k.",
                 "Net revenue retention held at 112%."], 0.6, 1.7, 12.1, 2.2, size=16)
    add_source(s)

    s = add_titled_slide(prs, "Revenue grew every quarter and reached $4.6M in Q4")
    add_bar_chart(s)
    add_text(s, ["Q4 is 48% above Q1."], 9.0, 1.7, 3.7, 1.0, size=14)
    add_source(s)

    s = add_titled_slide(prs, "Vietnam leads the shortlist on four of five criteria")
    add_table(s, [["Market", "Users (M)", "Growth"],
                  ["Vietnam", "38", "14%"],
                  ["Indonesia", "71", "9%"],
                  ["Thailand", "29", "6%"]], width=12.1)
    add_source(s, "Source: Company analysis of public statistics (sample data)")

    s = add_titled_slide(prs, "We recommend moving two sales hires to onboarding")
    add_text(s, ["Cost-neutral: both roles are already in the plan.",
                 "Decision needed today: approve the shift."], 0.6, 1.7, 12.1, 1.6, size=16)

    prs.save(str(path))
    return Path(path)


def build_plain_default_deck(path) -> Path:
    """A deck the way a hurried person makes it from the stock template (4:3)."""
    prs = Presentation()
    s = prs.slides.add_slide(prs.slide_layouts[LAYOUT_TITLE])
    s.shapes.title.text = "Team offsite"
    s.placeholders[1].text = "Planning for next year"
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = "Agenda"
    s.placeholders[1].text_frame.text = "Where we are"
    for line in ["What we learned", "What we will do next"]:
        s.placeholders[1].text_frame.add_paragraph().text = line
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = "Customer feedback"
    s.placeholders[1].text_frame.text = "Setup is fast"
    s.placeholders[1].text_frame.add_paragraph().text = "Integrations are missing"
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = "Support tickets doubled after the September release"
    s.placeholders[1].text_frame.text = "Most tickets are about the new import flow"
    s = prs.slides.add_slide(prs.slide_layouts[5])
    s.shapes.title.text = "Ticket volume"
    s.shapes.add_picture(io.BytesIO(photo_png_bytes()), Inches(1), Inches(1.8),
                         Inches(6), Inches(4))
    prs.save(str(path))
    return Path(path)


def _rect(slide, left, top, width, height, rgb, name, text=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top),
                                 Inches(width), Inches(height))
    shp.name = name
    shp.fill.solid()
    shp.fill.fore_color.rgb = rgb
    shp.line.fill.background()
    if text:
        shp.text_frame.text = text
        for r in shp.text_frame.paragraphs[0].runs:
            r.font.size = Pt(12)
    return shp


# Shapes the fix may change in build_drawn_exhibits_deck; everything else is part
# of an exhibit and must keep its exact position and size.
DRAWN_SAFE_SHAPES = {"Off-slide note", "Nudged note", "Margin note", "Tiny note", "Source"}


def build_drawn_exhibits_deck(path) -> Path:
    """Charts drawn with shapes, as another tool would draw them (no sw: names).

    Their positions are data, and near-miss edges are deliberate. Only the three
    free-standing notes in DRAWN_SAFE_SHAPES are safe to fix.
    """
    from pptx.enum.shapes import MSO_CONNECTOR

    prs = new_deck()
    add_cover(prs, "Drawn exhibits")
    light = RGBColor(0xBF, 0xBF, 0xBF)

    # Mekko: column widths are sizes, segment heights are shares, so segment tops
    # differ by a few hundredths of an inch between columns.
    s = add_titled_slide(prs, "Enterprise is the largest segment in every region")
    base = 6.0
    for c, (left, width, shares) in enumerate([(0.6, 3.0, (0.62, 0.38)),
                                               (3.7, 2.4, (0.58, 0.42)),
                                               (6.2, 1.8, (0.55, 0.45))]):
        top = 1.8
        for k, share in enumerate(shares):
            h = 4.2 * share
            _rect(s, left, top, width, h, ACCENT if k == 0 else light, f"Mekko {c}-{k}",
                  text=f"{int(share * 100)}%")
            top += h
        add_text(s, f"Region {c + 1}", left, base + 0.05, width, 0.4, size=12,
                 name=f"Mekko label {c}")
    add_text(s, "Note: widths show revenue.", 8.6, 1.8, 4.1, 0.6, size=12, name="Margin note")
    add_text(s, "Shares are of regional revenue.", 8.7, 2.6, 4.0, 0.6, size=12,
             name="Nudged note")  # left edge 0.1 in off the note above
    add_source(s, "Source: Sample data")

    # Gantt: bars start at their dates and sit a little below each row label.
    s = add_titled_slide(prs, "Go-live holds only if data migration finishes in August")
    for r, (label, start, length) in enumerate([("Design", 0.0, 2.0), ("Build", 1.5, 3.0),
                                                ("Migrate", 3.0, 2.5), ("Train", 4.5, 1.5)]):
        y = 2.0 + r * 0.9
        add_text(s, label, 0.6, y, 2.0, 0.5, size=12, name=f"Row {r}")
        _rect(s, 3.0 + start, y + 0.1, length, 0.4, ACCENT, f"Bar {r}")
    for k in range(7):
        line = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(3.0 + k), Inches(1.9),
                                      Inches(3.0 + k), Inches(5.6))
        line.name = f"Grid {k}"
    add_text(s, "Owner: PMO", 11.0, 6.2, 3.0, 0.5, size=12, name="Off-slide note")
    add_source(s, "Source: Sample data")

    # Native chart with a label placed on it, plus a group and a small note.
    s = add_titled_slide(prs, "Revenue grew every quarter and reached $4.6M in Q4")
    add_bar_chart(s)
    add_text(s, "Record quarter", 6.4, 2.0, 2.0, 0.4, size=12, name="Chart callout")
    grp = s.shapes.add_group_shape()
    grp.name = "Legend group"
    for k in range(3):
        box = grp.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.0), Inches(2.0 + k * 0.5),
                                   Inches(0.3), Inches(0.3))
        box.name = f"Swatch {k}"
    add_text(s, "Q4 includes one large renewal.", 9.0, 4.0, 3.7, 0.8, size=9,
             name="Tiny note")
    add_source(s)

    prs.save(str(path))
    return Path(path)


BUILDERS = {
    "flawed1": build_flawed_deck_1,
    "flawed2": build_flawed_deck_2,
    "clean": build_clean_deck,
    "plain": build_plain_default_deck,
    "drawn": build_drawn_exhibits_deck,
}


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "out/review-fixtures")
    out.mkdir(parents=True, exist_ok=True)
    for key, fn in BUILDERS.items():
        print(fn(out / f"{key}.pptx"))
