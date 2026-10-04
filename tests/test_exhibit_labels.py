"""Chart labels land where a reader can read them (issues #14 and #15).

Geometry is read back from the chart XML: the fixed inner plot area, the axis range
and the values give where each bar ends; the label must fit inside the plot, so it
cannot reach the category labels drawn outside it.
"""
import pytest
from pptx.oxml.ns import qn

from deckkit import text_fit
from deckkit.build import build_deck
from deckkit.numbers import fmt_number

LABEL_PT = 12


def deck(exhibit, layout="exhibit"):
    slide = {"layout": layout, "title": "Margin turned positive and kept rising", "exhibit": exhibit, "source": "Sample data"}
    if layout == "exhibit_takeaways":
        slide["takeaways"] = ["Margin rose every year"]
    return {"spec_version": "1.0", "meta": {"title": "Labels"}, "slides": [slide]}


def chart_of(prs):
    return next(sh for sh in prs.slides[0].shapes if sh.has_chart)


def plot_geometry(frame):
    space = frame.chart._chartSpace
    ml = space.find(".//" + qn("c:plotArea")).find(qn("c:layout")).find(qn("c:manualLayout"))
    assert ml is not None, "bar charts need a fixed inner plot area"
    get = lambda tag: float(ml.find(qn(f"c:{tag}")).get("val"))  # noqa: E731
    scaling = space.find(".//" + qn("c:valAx")).find(qn("c:scaling"))
    lo, hi = (float(scaling.find(qn(f"c:{t}")).get("val")) for t in ("min", "max"))
    w, h = frame.width / 12700, frame.height / 12700
    return get("x") * w, get("y") * h, get("w") * w, get("h") * h, lo, hi


@pytest.mark.parametrize("orientation", ["vertical", "horizontal"])
@pytest.mark.parametrize("values", [[-2.5, 8.4, 13.1], [-13.1, 2.5, 8.4], [-3, -8, -1], [4, 12, 2]])
@pytest.mark.parametrize("layout", ["exhibit", "exhibit_takeaways"])
def test_bar_value_labels_stay_inside_the_plot(orientation, values, layout):
    ex = {"type": "bar", "title": "Operating margin", "unit": "%", "number_format": "0.0", "orientation": orientation,
          "categories": ["FY2023", "FY2024", "FY2025"], "values": values, "highlight": ["FY2025"]}
    frame = chart_of(build_deck(deck(ex, layout))[0])
    px, py, pw, ph, lo, hi = plot_geometry(frame)
    for v in values:
        label_w = text_fit.text_width(fmt_number(v, "0.0"), "Arial", LABEL_PT, bold=True) * text_fit.SAFETY
        if orientation == "vertical":
            end = py + ph * (hi - v) / (hi - lo)
            label = (end, end + LABEL_PT * 1.2 + 2) if v < 0 else (end - LABEL_PT * 1.2 - 2, end)
            assert py - 0.5 <= label[0] and label[1] <= py + ph + 0.5, (v, label, (py, py + ph))
        else:
            end = px + pw * (v - lo) / (hi - lo)
            label = (end - label_w - 3, end) if v < 0 else (end, end + label_w + 3)
            assert px - 0.5 <= label[0] and label[1] <= px + pw + 0.5, (v, label, (px, px + pw))


def _end_labels(frame):
    out = []
    for ser in frame.chart.plots[0].series:
        dlbls = ser._element.find(qn("c:dLbls"))
        for dlbl in (dlbls.findall(qn("c:dLbl")) if dlbls is not None else []):
            rich = dlbl.find(qn("c:tx")).find(qn("c:rich"))
            paras = ["".join(t.text or "" for t in p.iter(qn("a:t"))) for p in rich.findall(qn("a:p"))]
            out.append((ser.name, paras, rich.find(qn("a:bodyPr")).get("wrap")))
    return out


@pytest.mark.parametrize("name", ["Operating margin", "EBITDA margin, adjusted basis", "Revenue growth, year on year"])
def test_line_end_label_never_breaks_inside_the_value(name):
    ex = {"type": "line", "title": "Margins", "unit": "%", "number_format": "0.0", "categories": ["FY2023", "FY2024", "FY2025"],
          "series": [{"name": name, "values": [-2.5, 8.4, 13.1]}, {"name": "Gross margin", "values": [70.1, 72.4, 72.9]}],
          "highlight": name}
    frame = chart_of(build_deck(deck(ex, "exhibit_takeaways"))[0])
    for series, paras, wrap in _end_labels(frame):
        assert wrap == "none", "end labels must not be re-wrapped by the renderer"
        value = paras[-1].split(" ")[-1]
        assert value in ("13.1", "72.9")  # the whole value sits in one paragraph
        reserved = frame.width / 12700 * 0.45
        for p in paras:  # every line fits the space kept free right of the plot
            assert text_fit.text_width(p, "Arial", LABEL_PT, bold=True) <= reserved, p


def test_short_line_labels_stay_on_one_line():
    ex = {"type": "line", "title": "Users", "unit": "thousands", "categories": ["Q1", "Q2"],
          "series": [{"name": "Active", "values": [10, 12]}]}
    frame = chart_of(build_deck(deck(ex))[0])
    assert [paras for _, paras, _ in _end_labels(frame)] == [["Active 12"]]
