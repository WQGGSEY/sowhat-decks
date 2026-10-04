# Design system (default template)

The default look is restrained and grid-disciplined: type and whitespace do the work, one accent color marks the point of each slide, everything else is ink or grey. With a user template, the template's fonts and accent replace these; the grid, sizes and rules stay.

## Color

| Token | Hex | Used for |
|---|---|---|
| Ink | `#1E2329` | titles, body text, table text |
| Ink 2 | `#5A6472` | secondary text, source line, axis labels, labels of non-highlighted series |
| Accent | `#1F5AA6` | the one thing that matters: highlighted bar/series/row, numbers in lists, takeaway rule, tracker |
| Grey 1 | `#8C95A1` | second-level data series |
| Grey 2 | `#B7BEC7` | non-highlighted bars and data |
| Grey 3 | `#D5DAE0` | rules and dividers |
| Grey 4 | `#F2F4F6` | light fills (quadrants, process steps) |
| Accent tint | accent mixed 86% with white | highlighted table rows, highlighted quadrant |

Rules: one accent per slide's message. Never use a second hue to "decorate". Red/green status colors are not part of the system: say "Off track" in words and highlight it with the accent.
Change the accent for the default template with `"theme": {"accent": "#0F6E6E"}`.

## Type

| Role | Font | Size | Floor |
|---|---|---|---|
| Action title | Georgia (theme heading) | 28 pt | 24 pt, max 2 lines |
| Cover title | Georgia | 40 pt | 28 pt |
| Section title | Georgia | 36 pt | 28 pt |
| Quote | Georgia | 28 pt | 20 pt |
| Body, bullets, table cells | Arial (theme body) | 16 pt | 12 pt |
| Lead line in a list (bold) | Arial | 18 pt | 12 pt |
| Exhibit title (what + unit) | Arial bold | 14 pt | 12 pt |
| Chart labels | Arial | 12 pt | 12 pt |
| Source, footnotes, page number, tracker | Arial | 10-11 pt | 10 pt |
| Numbers in lists, section numbers | Arial bold, accent | same as the line they lead | |

Why these two fonts: both ship with Windows, macOS and every PowerPoint, and LibreOffice has metric-compatible substitutes, so line breaks match across machines. Georgia gives action titles an editorial voice; Arial keeps dense body text and charts neutral. Calibri and Aptos were rejected (missing on many Macs and in LibreOffice, so previews would differ), Verdana and Tahoma (too wide or too tight for dense slides).

East Asian theme font: Malgun Gothic for Korean, Yu Gothic for Japanese. Latin characters inside Korean or Japanese text still use Georgia/Arial.

Note: Georgia draws old-style figures (numbers sit on the x-height). That is intended in titles. If a user's brand needs lining figures in titles, use their template.

## Grid and spacing (16:9, 13.333 x 7.5 in)

- Side margins 0.5 in. 12 columns, 0.2 in gutters, one column = 0.844 in.
- Tracker 0.30 in from the top, title box 0.55-1.55 in, body from 1.75 in down to the footer.
- Footer: source line and footnotes sit on the bottom edge (bottom 7.2 in), page number bottom-right on the same baseline.
- Common splits: 6 + 6 (two columns), 4 + 4 + 4 or 3 + 3 + 3 + 3 (pillars), 8 + 4 (exhibit + takeaways), 1 + 11 (numbered rows).
- Like elements share one size: if one pillar's text must shrink to 14 pt, all pillars use 14 pt.
- Content starts at the top of the body area on every slide; whitespace below is fine.

## Building a slide by hand (no-code mode)

Use this when working inside PowerPoint (Claude for PowerPoint) or advising in chat.

1. **Title**: put the action title in the title placeholder. One sentence, 10-16 words, says the so-what. Read all titles in order before building bodies.
2. **Layout**: Title Only for content slides. Do not use the content placeholder for charts; insert the chart or table on the grid.
3. **Grid**: View > Guides. Margins 0.5 in; for 6 + 6 columns the split is at 6.67 in. Align every element's left edge to a column.
4. **Exhibit title**: a 14 pt bold line above the chart: what is shown and the unit ("Revenue by region, 2025, $M").
5. **Chart**: Insert > Chart (native). Delete the legend, gridlines and value axis for bars; add data labels; grey `#B7BEC7` for all bars, accent for the one the title talks about. Details in `deck-exhibits`.
6. **Text**: 16 pt body, never below 12 pt. If it does not fit, cut words or move them to the speaker notes.
7. **Footer**: a 10 pt source line at the bottom left ("Source: ..."), slide number bottom right. Mark illustrative numbers "Sample data". Mark unknown ones `[DATA NEEDED]`.
8. **Draft**: while numbers are not final, put a small "DRAFT" box top right.
9. **Check**: nothing touches the slide edge, nothing overlaps, every chart has a source, one accent per slide.
