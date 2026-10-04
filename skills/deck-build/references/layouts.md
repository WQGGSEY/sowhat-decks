# Layouts and the deck spec

A deck spec is one JSON file. `deck-spec.schema.json` (next to this file) is the contract; this page explains it.
The builder validates the spec, measures every text box with per-font width tables, shrinks text inside the allowed range, and reports anything that still does not fit.

## Minimal spec

```json
{
  "spec_version": "1.0",
  "meta": {"title": "Q3 board update", "language": "en", "draft": true, "sample_data": true},
  "slides": [
    {"layout": "cover", "subtitle": "Board meeting", "date": "October 2026"},
    {"layout": "exhibit_takeaways",
     "title": "Region B grew fastest and now drives most of the gap to plan",
     "exhibit": {"type": "bar", "title": "Revenue growth by region, Q3 vs Q2", "unit": "%",
                 "categories": ["Region A", "Region B", "Region C"], "values": [4, 12, 2],
                 "highlight": ["Region B"]},
     "takeaways": ["Region B adds two thirds of new revenue", "Region C is flat for the third quarter"],
     "source": "Sample data"}
  ]
}
```

## Slide anatomy (default 16:9 template, inches)

The slide is 13.333 x 7.5 in. A 12-column grid sits inside 0.5 in side margins with 0.2 in gutters (one column = 0.844 in).

| Zone | Top | Height | What goes there |
|---|---|---|---|
| Tracker | 0.30 | 0.25 | optional `tracker` label, 11 pt, accent color |
| DRAFT sticker | 0.22 | 0.30 | right edge, only when `draft` is on |
| Action title | 0.55 | 1.00 | `title`, 28 pt, shrinks to 24 pt, max 2 lines |
| Body | 1.75 | to footer | layout content on the 12-column grid |
| Footer | bottom 0.45 | grows up | footnotes, then source (10 pt), page number right |

With a user template the zones come from the template: the title zone is the template's title placeholder, the body runs from under the title to above the template's footer placeholders, and the grid is rebuilt inside that width.

## Type sizes (hard floors)

| Text | Default | Floor | Font |
|---|---|---|---|
| Action title | 28 pt | 24 pt, max 2 lines | heading font (theme major) |
| Cover title | 40 pt | 28 pt | heading font |
| Section title | 36 pt | 28 pt | heading font |
| Body, bullets, table cells, chart labels | 16 pt | 12 pt | body font (theme minor) |
| Exhibit title (what + units) | 14 pt bold | 12 pt | body font |
| Source, footnotes, page number, tracker | 10 pt | 10 pt | body font |

Default theme: headings Georgia, body Arial (both ship with Windows, macOS and PowerPoint). East Asian theme font: Malgun Gothic for Korean, Yu Gothic for Japanese. One accent color (default `#1F5AA6`), text near-black, greys for everything else.

## Recommended text lengths

Hard caps are in the schema. These are the lengths that fit comfortably; the builder measures the real text and flags overflow.

| Field | English | Korean / Japanese |
|---|---|---|
| Action title | 60-100 chars (10-16 words) | 25-50 chars |
| Bullet | <= 120 chars | <= 60 chars |
| Column / pillar heading | <= 35 chars | <= 16 chars |
| Exhibit title | <= 70 chars | <= 35 chars |
| Category label | <= 18 chars | <= 9 chars |

## The 12 layouts

Every layout except `cover` and `section` needs an action title: one sentence that states the so-what ("Region B drives two thirds of growth"), not a topic ("Regional growth").
Every slide accepts `id`, `notes` (speaker notes), `draft`, `ghost`. Content slides also accept `tracker`, `source`, `footnotes` (max 3), `sample_data`.

### 1. `cover`
Fields: `title` (<=100, default `meta.title`), `subtitle` (<=160), `date`, `author` (default `meta.author` / `meta.organization`).
Look: title 40 pt bottom-left on cols 1-9, accent rule above it, subtitle 18 pt grey, date and author 14 pt.

### 2. `executive_summary`
Fields: `title`, `points` (2-5). A point is a string or `{headline (<=120), detail (<=240)}`.
Look: numbered rows across cols 1-12; number in accent, headline bold 18 pt, detail 14 pt grey. Rows share the body height equally.

### 3. `section`
Fields: `title` (<=80), `number` (optional, e.g. 2 or "B"), `subtitle` (<=160).
Look: large accent number on cols 1-2, title 36 pt on cols 3-12, vertically centred.

### 4. `exhibit`
Fields: `title`, `exhibit` (see below), `source` (required).
Look: exhibit title row then the exhibit across cols 1-12.

### 5. `exhibit_takeaways`
Fields: `title`, `exhibit`, `takeaways` (1-4, <=160 each), `takeaways_heading` (default "So what" / 시사점 / 示唆), `source` (required).
Look: exhibit on cols 1-8, takeaways panel on cols 9-12 with a thin accent rule on top.

### 6. `two_column`
Fields: `title`, `left` and `right`: `{heading (<=50), bullets (1-5, <=160), highlight (bool)}`.
Look: two halves of 6 columns, heading 18 pt bold with a rule under it, bullets 16 pt. `highlight: true` puts the heading in the accent color (the preferred option).

### 7. `pillars`
Fields: `title`, `pillars` (3-4): `{heading (<=40), body (<=220) or bullets (<=4, <=100)}`, `numbered` (default true).
Look: equal columns (4 x 3 cols or 3 x 4 cols), number in accent, heading bold, text below.

### 8. `table`
Fields: `title`, `table`: `{columns (2-6), rows (1-10 rows of cells), align, number_format, highlight}`. `number_format` takes the chart style (`#,##0`, `0.0`, `0%`) or a Python format spec (`,.1f`).
Look: native PowerPoint table, header row bold on a rule, no vertical lines, numbers right-aligned. `highlight` (rows / cols / cells, 0-based, rows exclude the header) gets a light accent tint and bold text.

### 9. `timeline`
Fields: `title`, `milestones` (2-6): `{when (<=20), label (<=40), detail (<=120), highlight}`.
Look: horizontal line with dots, `when` above in accent or grey, label bold and detail below. Highlighted milestone gets the accent dot.

### 10. `quote`
Fields: `title`, `quote` (<=220), `attribution` (<=80).
Look: quote 28 pt (shrinks to 20 pt) in the heading font on cols 2-11, accent bar to the left, attribution 14 pt grey.

### 11. `recommendations`
Fields: `title`, `items` (1-6): `{action (<=100), detail (<=160), owner (<=30), due (<=20)}`.
Look: numbered rows; action bold, detail grey under it; owner and due columns on the right when any item has them.

### 12. `appendix`
Fields: `title` plus exactly one of `bullets` (<=8), `table`, `exhibit`.
Look: "Appendix" label in the tracker position, then the content like the matching layout.

### Ghost mode (`mode: "ghost"` or `layout: "ghost"`)
A ghost deck is the storyline before the evidence: every slide shows its action title and nothing else except a dashed placeholder box.
- Set `"mode": "ghost"` at the top level to render every slide (except `cover` and `section`) as a ghost.
- Or use `{"layout": "ghost", "title": "...", "ghost": {...}}` per slide. Only `title` is required.
- `ghost` hints: `layout` (the planned final layout), `exhibit` (planned exhibit, e.g. "Bar: revenue by region, 2025, $M"), `evidence` (up to 5 items; tag what you have with `[SRC n]`, `[CALC]` or `[SAMPLE]`, and mark anything not yet sourced `[DATA NEEDED]` or `[DATA NEEDED: what is missing]`).
- The dashed box shows the planned exhibit, then the evidence in two groups: **Evidence** (items without a data-needed tag) and **Still needed** (items with `[DATA NEEDED]` or `[DATA NEEDED: ...]`, any case). A group with no items is left out. Ghost slides get the DRAFT sticker automatically.

Example ghost slide:

```json
{"layout": "ghost",
 "title": "Region B drives two thirds of growth, so the plan should fund it first",
 "ghost": {"layout": "exhibit_takeaways", "exhibit": "Bar: revenue growth by region, Q3 vs Q2, %",
           "evidence": ["Regional revenue Q2 and Q3 from finance", "[DATA NEEDED] Region B pipeline"]}}
```

## Exhibits (field `exhibit`)

All charts are native PowerPoint charts (double-click to edit the data). Full style rules: deck-exhibits `references/chart-style.md`.

| `type` | Required fields | Optional |
|---|---|---|
| `bar` | `title`, `categories` (2-12), `values` | `highlight` (names or indexes), `orientation` (horizontal / vertical), `sort`, `unit`, `number_format` |
| `line` | `title`, `categories` (2-24), `series` (1-4 `{name, values}`) | `highlight` (series name), `unit`, `number_format` |
| `stacked_bar` | `title`, `categories` (1-8), `series` (2-5) | `highlight`, `show_totals`, `unit`, `number_format` |
| `stacked_bar_100` | `title`, `categories` (1-8), `series` (2-5) | `highlight`, `unit`, `number_format` |
| `highlight_table` | `title`, `columns`, `rows` | `highlight`, `align`, `number_format` |
| `matrix_2x2` | `title`, `x_label`, `y_label`, `quadrants` (4: TL, TR, BL, BR) | `x_low`, `x_high`, `y_low`, `y_high`, `items` (`{label, x 0-1, y 0-1, highlight}`), `highlight_quadrant` |
| `process` | `title`, `steps` (2-6 `{label, detail}`) | `highlight` (step index) |

`values` and each series' `values` must have one finite number (or `null`) per category; stacked bars take values of 0 or more. Chart `number_format` is a safe Excel format: optional currency sign, `0` or `#,##0`, up to 6 decimals, optional `%` (`0.0`, `#,##0`, `$#,##0`, `0%`). The exhibit `title` says what is shown and its unit ("Revenue by region, 2025, $M"); if `unit` is given and missing from the title, it is appended.

## Rules the builder enforces

- Spec validates against the schema; series lengths match categories.
- Nothing is placed outside the slide.
- Text is measured; if it does not fit at the floor size it is reported as overflow (`build-report.json`, and exit code 3 with `--strict`).
- Titles: at most 2 lines at >= 24 pt.
- Exhibit slides need a `source`. The line reads `Source: <text>` (`출처: ` in Korean, `出所：` in Japanese); a prefix you wrote yourself (`Source:`, `Sources:`, `출처:`, `出所：`) is kept and never doubled. When `meta.sample_data` or the slide's `sample_data` is true, `Sample data` is always the first item: `Source: Sample data; <text>`, decided by that flag alone, not by words inside your source.
- Numbers are never invented by the builder. Missing values stay `null` (gap in the chart) and should be written `[DATA NEEDED]` in text.
