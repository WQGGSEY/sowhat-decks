---
name: deck-exhibits
description: Chooses and builds the right exhibit for each slide message as native, editable PowerPoint objects - bar with a highlighted bar, line with end labels, stacked and 100% stacked bars, highlight table, 2x2 matrix and process chevrons - styled with direct labels, one accent color and units in the title. Use when a deck, slides, a presentation, a board update or a pitch needs a chart, graph, table or diagram, when the user asks which chart to use, or wants PowerPoint charts that look clean and consulting-style.
---

# deck-exhibits

An exhibit proves one message. Choose it from the message, not from the data, and make the eye land on the part the title talks about.

## Quick start

1. Write the slide's message as a sentence: "Region B grew three times faster than the rest".
2. Classify it and pick the exhibit with the table below (full guide: [references/exhibit-chooser.md](references/exhibit-chooser.md)).
3. Put it in a deck spec slide and build (this skill carries its own copy of the builder):

```bash
python3 -m pip install --user python-pptx pypdfium2   # pypdfium2 only for PNG previews
python3 scripts/build.py exhibits.json -o out/      # out/deck.pptx, preview/*.png if LibreOffice is installed
```

```json
{"spec_version": "1.0", "meta": {"title": "Growth", "sample_data": true},
 "slides": [{"layout": "exhibit",
   "title": "Region B grew three times faster than the rest of the business",
   "exhibit": {"type": "bar", "title": "Revenue growth by region, this year vs last year", "unit": "%",
               "categories": ["Region A", "Region B", "Region C"], "values": [3, 12, 2],
               "highlight": ["Region B"], "sort": "desc"},
   "source": "Sample data"}]}
```

Use `"layout": "exhibit_takeaways"` with `"takeaways": [...]` to put 1-4 implications beside the exhibit. If the `deck-build` skill is installed, put the same exhibit objects into the full deck spec there.

## Message type to exhibit

| The message is about... | Example | Exhibit (`type`) |
|---|---|---|
| **Comparison** (ranking, one item vs others) | "Product 4 sells the most" | `bar` horizontal, sorted, highlight the item |
| **Change over time** (trend, few periods) | "Costs fell every year" | `bar` with `"orientation": "vertical"` (up to ~8 periods) |
| **Change over time** (trend, many periods or several series) | "Channel C overtook the others" | `line`, highlight one series |
| **Composition** (parts of a whole, and how the total moves) | "Subscription drives the growth" | `stacked_bar` |
| **Composition** (shares only) | "Online is the largest channel everywhere" | `stacked_bar_100` |
| **Distribution / exact values across dimensions** | "Plan B is the only option that meets all criteria" | `highlight_table` |
| **Relationship / positioning** (two dimensions) | "Two initiatives are high value, low effort" | `matrix_2x2` |
| **Process / sequence** | "The import step is the bottleneck" | `process` |

If the message does not fit one row, the slide probably has two messages: split it.

## Workflow

- [ ] Message sentence written; it becomes the slide's action title.
- [ ] Exhibit chosen from the table; one exhibit per slide (two only if they make one point).
- [ ] Data checked: every number from the user's material or a cited public source; unknown values are `null` (shown as a gap) and listed as `[DATA NEEDED]`; illustrative data says "Sample data".
- [ ] Highlight set on exactly the bar, series, row, quadrant or step the title talks about.
- [ ] Exhibit `title` says what is shown and the unit; `unit` filled in.
- [ ] `source` on the slide.
- [ ] Built and the PNG checked: labels readable, nothing overlapping, highlight matches the title.

## Style rules (summary)

- **Direct labels, no legend.** Bars carry value labels; lines carry an end label "Series value"; stacked bars name each series beside the last column.
- **One accent color** for the highlighted element; all other data in greys.
- **Units in the exhibit title**, not on every label ("Revenue by region, $M").
- **No chart junk**: no gridlines on bars, no value axis when bars are labelled, no 3D, no shadows, no chart border.
- **Labels at 12 pt or more**. Category names short (about 18 characters).
- **Sort** ranking bars; keep time in time order.
- **Start bars at zero.** Lines may start above zero when the change is the message (the axis shows the scale).

Full rules and the reasons: [references/chart-style.md](references/chart-style.md).

## No-code mode (chat, Claude for PowerPoint)

Designed for chat and the Claude for PowerPoint sidebar; not yet tested in Claude for PowerPoint.

Build the same exhibits with PowerPoint's own tools:

1. Insert > Chart and pick the type from the table above (bar = Clustered Bar or Clustered Column, stacked = Stacked Column, 100% = 100% Stacked Column, line = Line).
2. Delete the legend, the chart title (put the exhibit title in a text box above), gridlines and, for bars, the value axis.
3. Add data labels (Outside End for bars, Center for stacked). For lines, label only the last point with the series name and value.
4. Color all data grey (`#B7BEC7`, darker greys for other stacked series) and only the highlighted bar or series in the accent.
5. Tables: Insert > Table, set "No Style, No Grid", bold header with a dark bottom border, hairlines between rows, numbers right-aligned, highlighted row in a light accent tint.
6. 2x2 and process: rectangles and chevrons from Insert > Shapes, grey fills, accent on the one that matters.
7. Add the 10 pt source line under the exhibit.

## Exhibit fields

The full contract is `scripts/deckkit/deck-spec.schema.json` (same file as deck-build's `references/deck-spec.schema.json`). Field-by-field examples for each type: [references/exhibit-chooser.md](references/exhibit-chooser.md#fields).
