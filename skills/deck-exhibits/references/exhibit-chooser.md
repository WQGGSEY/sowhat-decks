# Exhibit chooser

Start from the message, not the data. Write the sentence the slide must prove, find its message type below, and use the exhibit listed. Then highlight the element the sentence is about.

## 1. Comparison

The message ranks items or sets one item against the others.

- Use `bar` (horizontal). Sort descending (`"sort": "desc"`) unless the categories have a natural order. Highlight the item named in the title.
- Up to 12 categories. More than that: show the top 8-10 and put the rest in the appendix.
- Long category names are fine (horizontal bars give them room); keep them under ~18 characters if possible.
- Two values per item (this year vs last year)? Show the change as one bar per item (growth %), or use a `highlight_table`.

## 2. Change over time

The message is about a trend, a turning point or a gap opening up.

- Few periods (up to ~8) and one series: `bar` with `"orientation": "vertical"`; highlight the latest or the turning-point period.
- Many periods, or 2-4 series: `line`; highlight the series in the title. End labels name each series, so no legend is needed.
- Do not mix time and ranking: keep periods in time order.

## 3. Composition

The message is about the parts of a whole.

- Parts and the total both matter ("Subscription drives the growth in total revenue"): `stacked_bar`. Totals print above each column (`"show_totals": false` to hide).
- Only the shares matter ("Online is the largest channel in every region"): `stacked_bar_100`. Give raw values or shares; the builder converts to shares.
- 2-5 series, up to 8 columns. Highlight the series in the title; series names sit beside the last column.
- Values must be zero or positive. For changes that go up and down use a `bar` of the change instead.

## 4. Distribution and exact values

The message needs the reader to see exact numbers across several dimensions, or to scan a scorecard.

- Use `highlight_table` (in an exhibit) or the `table` layout. Up to 10 rows and 6 columns.
- Highlight rows, columns or single cells (`{"rows": [1]}`, `{"cols": [2]}`, `{"cells": [[3, 3]]}`; 0-based, header excluded).
- Numbers are right-aligned automatically; set `number_format` to keep decimals consistent: chart style (`"#,##0.0"`) or Python style (`",.1f"`).
- Status columns: write the status in words ("Off track") and highlight the cells; do not color-code red/amber/green.

## 5. Relationship and positioning

The message places items on two dimensions ("high value, low effort").

- Use `matrix_2x2`. Name both axes (`x_label`, `y_label`) and their ends (`x_low`, `x_high`, `y_low`, `y_high`).
- Quadrant names in reading order: top-left, top-right, bottom-left, bottom-right. Highlight the quadrant the title recommends.
- Up to 10 items, positioned 0-1 on each axis. Positions are judgement unless they come from data: say which in the source line.
- A true correlation between two measured variables is a scatter chart (Pro), not a 2x2.

## 6. Process and sequence

The message is about steps, a flow or where a process breaks.

- Use `process`: 2-6 steps, a short label (1-3 words) and an optional one-line detail each. Highlight the step the title is about.
- Dated milestones are a `timeline` layout, not a process.

## Fields

Every exhibit has `type`, `title` (what is shown, with unit) and optional `unit`. Examples:

```json
{"type": "bar", "title": "Units sold per store per week, by product", "unit": "units",
 "categories": ["Product 1", "Product 2", "Product 3"], "values": [42, 88, 35],
 "highlight": ["Product 2"], "sort": "desc", "orientation": "horizontal", "number_format": "0"}
```

```json
{"type": "line", "title": "Share of new customers by channel", "unit": "%",
 "categories": ["Q1", "Q2", "Q3", "Q4"],
 "series": [{"name": "Channel A", "values": [30, 29, 27, 26]}, {"name": "Channel C", "values": [15, 18, 22, 26]}],
 "highlight": "Channel C"}
```

```json
{"type": "stacked_bar", "title": "Revenue by type", "unit": "$M", "categories": ["2024", "2025"],
 "series": [{"name": "Subscription", "values": [37, 48]}, {"name": "Services", "values": [26, 27]}],
 "highlight": "Subscription", "show_totals": true}
```

```json
{"type": "highlight_table", "title": "Options scored against criteria", "unit": "score 1-5",
 "columns": ["Option", "Cost", "Speed", "Total"], "rows": [["Plan A", 3, 2, 5], ["Plan B", 4, 4, 8]],
 "highlight": {"rows": [1]}}
```

```json
{"type": "matrix_2x2", "title": "Initiatives by value and effort", "x_label": "Effort", "y_label": "Value",
 "x_low": "Low", "x_high": "High", "y_low": "Low", "y_high": "High",
 "quadrants": ["Quick wins", "Major projects", "Fill-ins", "Avoid"], "highlight_quadrant": 0,
 "items": [{"label": "Self-serve setup", "x": 0.2, "y": 0.85, "highlight": true}]}
```

```json
{"type": "process", "title": "Customer onboarding, current process",
 "steps": [{"label": "Sign contract"}, {"label": "Import data", "detail": "Slowest step"}, {"label": "Go live"}],
 "highlight": 1}
```

All numbers in these examples are placeholders; real decks use the user's data or cited public sources, and anything illustrative is marked "Sample data".
