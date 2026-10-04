# Chart style rules

Each rule exists to make the reader see the title's point in under five seconds.

| Rule | Why | How the builder applies it |
|---|---|---|
| Direct labels instead of a legend | A legend makes the eye travel back and forth | Bars: value at the bar end. Lines: "Series value" at the last point. Stacked: series names beside the last column, values inside segments |
| One accent color | Color is the strongest pointer; one pointer per slide | Theme accent 1 on the highlighted bar / series / row / quadrant / step; everything else grey |
| Units in the exhibit title | Labels stay short; the unit is read once | `title` + `unit` -> "Revenue by region, $M" |
| Exhibit title says what, the slide title says so what | The two titles do different jobs | 14 pt bold exhibit title above the chart; action title in the title placeholder |
| No chart junk | Gridlines, borders, 3D and shadows add ink without information | No border, no 3D, no shadow; bars have no value axis or gridlines; lines keep light gridlines for scale |
| Labels 12 pt or larger | Read from the back of a room and on a laptop | All chart text is set to 12 pt |
| Sort rankings, keep time in order | Order is information | `"sort": "desc"` for rankings; time categories untouched |
| Bars start at zero | Bar length encodes value | Value axis minimum is 0 (or the most negative value) |
| Gaps stay gaps | A missing value is not zero | `null` values are left blank; say why in a footnote |
| Source under every exhibit | Credibility, and the reviewer will ask | Slide `source` is required on exhibit slides |
| Native, editable objects | The user must be able to update the numbers | python-pptx chart objects with an embedded workbook; tables and diagrams are PowerPoint shapes |

## Colors

| Use | Color |
|---|---|
| Highlight | accent (default `#1F5AA6`, or the template's accent 1) |
| Other bars | `#B7BEC7` |
| Other series (lines, stacked) | `#5A6472`, `#737D8A`, `#8C95A1`, `#B7BEC7`, `#D5DAE0` in that order |
| Text on dark fills | white; on light greys ink `#1E2329` |
| Highlighted table cells, quadrant | accent mixed 86% with white |

## Per exhibit

**Bar.** Horizontal for rankings and long names, vertical for time. Gap between bars about one bar width (wider when there are few bars). Value labels outside the end; the highlighted label is bold in the accent. Negative values extend left/down from zero.

**Line.** 2.5 pt accent line for the highlighted series, 1.75 pt greys for the rest, no markers. End labels "Name value"; labels that would collide are spaced apart. Value axis on the left with light gridlines; it may start above zero when the change is the point.

**Stacked bar.** Columns with white separators, values centred in segments that are tall and wide enough (small segments stay unlabelled rather than overlap), totals above columns, series names right of the last column in the series color. Highlight one series, normally the bottom one so its growth reads from a common baseline.

**100% stacked bar.** Same, with shares (0%) and no totals.

**Highlight table.** "No Style, No Grid" table, bold header on an ink rule, grey hairlines between rows, numbers right-aligned, highlighted cells in accent tint and bold.

**2x2 matrix.** Four grey quadrants with names top-left inside each, axes with arrows and low/high labels, items as dots with labels; highlighted quadrant in accent tint, highlighted dots in the accent.

**Process.** Chevrons in a row, label centred in each, detail text below; the highlighted step is filled with the accent and white text. Each chevron and its label are grouped so they move together.

## Rendering differences

PowerPoint, Keynote and LibreOffice draw charts slightly differently (label positions, font metrics). The builder fixes the plot area and axis ranges so labels land in the same places, and it writes `invertIfNegative = 0` on bars so LibreOffice keeps negative values negative. Always check the PNG preview, and open the `.pptx` in PowerPoint before sending when possible.
