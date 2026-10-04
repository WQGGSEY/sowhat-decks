# Automatic checks

What `scripts/review.py` measures, the thresholds, and what `fix` may change.
Thresholds live in `DEFAULTS` in `scripts/deckreview/checks.py`.

| Check | Finds | Severity | Auto-fix |
|---|---|---|---|
| `title_missing` | Content slide without a title | medium | no |
| `title_not_claim` | Title reads like a topic label (no verb, common label word, question, ends with ":") | medium; low in the appendix | no (agent rewrites) |
| `title_too_long` | Title over 2 lines at its size, over 20 words, or over 120 characters (60 for Korean/Japanese) | medium | no |
| `title_font_small` | Title under 24 pt | low | no |
| `font_below_floor` | Body under 12 pt; source/note lines, tables, footers and labels under 10 pt; chart text under 10 pt (low) | medium | yes: raises runs to the floor (not chart text) |
| `text_overflow` | Estimated text height over 110% of a fixed box (high over 130%); grow-to-fit boxes that grow 1.5x or more; unwrapped text wider than its box; shrink-to-fit that will shrink text | medium/high | no |
| `off_slide` | Shape partly outside the slide (high; low if only the empty part of a text frame sticks out); entirely outside (low) | high/low | yes, for partly-outside top-level shapes |
| `overlap` | Text on text (high), exhibit on exhibit (medium), text covering a chart or picture (low, may be a deliberate label) | high/medium/low | no |
| `missing_source` | Chart, numeric table or chart-like picture with no "Source:", "Note:", 출처, 出典 or "Sample data" line | medium | yes: adds `Source: [SOURCE NEEDED]` at 10 pt |
| `chart_as_image` | Large picture that looks like a chart: few flat colors, light background, straight axis lines; EMF/WMF metafile; name or alt text says chart/graph/plot | medium | no |
| `data_needed` | `[DATA NEEDED]`, `[SOURCE NEEDED]`, TBD, XX%, $XX, lorem ipsum, "Click to add text", ??? | high | no |
| `empty_placeholder` | Empty placeholders on a slide (one issue per slide) | low | no |
| `dense_slide` | More than 150 words | low | no |
| `misaligned` | Edges 0.03-0.15 in apart (left, top for side-by-side, right for wide shapes); padding inside a container is ignored | low | yes: snaps to the neighbor's edge |
| `font_count` | More than 2 font families in the deck (symbol fonts ignored) | medium | no |
| `accent_colors` | More than 1 accent hue across text, fills, table fills and chart series (grays ignored; tints of one hue count once) | low (2 hues), medium (3+) | no |
| `duplicate_title` | Same or near-same title as an earlier slide | medium | no |
| `title_position` | Title placed differently from most slides | low | no |

## How text fit is estimated

No renderer is needed. Each character's width comes from an Arial width table,
scaled per font (Calibri 0.90, Georgia 1.02, ...); Korean, Japanese and Chinese
characters count one em. Lines wrap word by word; line height is 1.2 x the font
size times the paragraph's line spacing. Font sizes are resolved through run,
paragraph, shape, layout, master and theme styles, including shrink-to-fit
scaling. Expect about +/-10%; the thresholds leave room for that. When a render
is available, confirm overflow findings on the annotated PNG.

## Roles

Each text shape gets a role, which sets its font floor:
- `title`: title placeholder, or the biggest text near the top when a deck has no
  placeholders
- `source`: starts with Source/Note/출처/出典, or a short line low on the slide that
  mentions a source or sample data
- `footer`: footer, date and slide-number placeholders, short text in the bottom 10%
- `label`: short text (6 words or fewer) above the title area, such as a tracker or
  a DRAFT sticker
- `body`: everything else

## What fix never does

- Change words, numbers, chart data, slide order or notes
- Move shapes that sit entirely off the slide (they may be parked on purpose)
- Move shapes inside groups, rotated shapes, or shapes larger than the slide
- Shrink anything
- Overwrite the input file
