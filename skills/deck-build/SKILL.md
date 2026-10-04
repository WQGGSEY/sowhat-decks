---
name: deck-build
description: Builds an editable, answer-first PowerPoint deck (.pptx) from a storyline, notes or data - 12 consulting-style layouts on a 12-column grid, native charts, the user's own .pptx/.potx template, source footnotes, page numbers, a DRAFT sticker and speaker notes - then renders a PDF/PNG preview to check it. Use when the user asks for a deck, slides, a presentation, a board update, an investor update, a pitch deck, a QBR or a PowerPoint/.pptx file, or wants a storyline or ghost deck turned into real slides.
---

# deck-build

Turn a storyline into an editable `.pptx` whose titles carry the argument. Every slide states its so-what in the title; the body proves it.

## Quick start (script mode)

```bash
python3 -m pip install --user python-pptx pypdfium2  # python-pptx builds; pypdfium2 only makes PNG previews
python3 scripts/build.py deck.json -o out/            # out/deck.pptx, build-report.json, deck.pdf, preview/*.png
python3 scripts/build.py deck.json --template brand.potx -o out/   # on the user's template
```

`deck.json` is a deck spec: see [references/layouts.md](references/layouts.md) and the contract [references/deck-spec.schema.json](references/deck-spec.schema.json).

```json
{"spec_version": "1.0",
 "meta": {"title": "Q3 board update", "language": "en", "draft": true, "sample_data": true},
 "slides": [
   {"layout": "cover", "subtitle": "Board meeting", "date": "October 2026"},
   {"layout": "exhibit_takeaways",
    "title": "Region B grew fastest and now drives most of the gap to plan",
    "exhibit": {"type": "bar", "title": "Revenue growth by region, Q3 vs Q2", "unit": "%",
                "categories": ["Region A", "Region B", "Region C"], "values": [4, 12, 2], "highlight": ["Region B"]},
    "takeaways": ["Region B adds two thirds of new revenue"],
    "source": "Sample data"}]}
```

Works with Python 3.9 or newer (the `python3` that ships with macOS is fine). PDF/PNG previews need LibreOffice (optional). Without it the build still writes the `.pptx` and says the preview was skipped. Nothing is ever installed or downloaded by the scripts.

## Workflow

Copy this checklist and tick it off:

- [ ] 1. **Storyline first.** One governing message, then one message per slide. If there is no storyline yet, use the `deck-storyline` skill (it writes a ghost deck spec this skill builds) or write the action titles first and read them in order: they must tell the story alone.
- [ ] 2. **Pick a layout per slide** with the table below.
- [ ] 3. **Write the spec.** Titles are full sentences (10-16 words, max 2 lines). Every number comes from the user's material or a cited public source. Unknown numbers stay `null` in charts and `[DATA NEEDED]` in text. Illustrative numbers must say `Sample data`.
- [ ] 4. **Validate:** `python3 scripts/build.py deck.json --check-only`. Fix every message (they name the slide and field).
- [ ] 5. **Build** and read the console summary and `build-report.json`. Any `overflow` means text did not fit at the minimum size: shorten it or split the slide. Never lower the type floors.
- [ ] 6. **Look at every `preview/slide-NN.png`.** Check the title reads as the slide's conclusion, the highlighted element matches the title, nothing collides, nothing is cut off.
- [ ] 7. Hand over `deck.pptx` (editable, charts open their data in PowerPoint) plus the PDF. Use the `deck-review` skill for a full rubric review.

## Pick the layout

| The slide needs to... | Layout |
|---|---|
| open the deck | `cover` |
| give the whole answer on one page | `executive_summary` (2-5 points) |
| start a part of the story | `section` |
| prove one message with one chart or table | `exhibit` |
| prove it and spell out the implications | `exhibit_takeaways` (exhibit left, 1-4 takeaways right) |
| compare two options or before/after | `two_column` |
| show 3-4 parallel moves, causes or principles | `pillars` |
| show exact figures across several dimensions | `table` |
| show a sequence over time | `timeline` |
| let a customer or expert make the point | `quote` |
| ask for a decision or assign next steps | `recommendations` |
| hold back-up material | `appendix` |
| sketch the story before the evidence exists | `ghost` (or `"mode": "ghost"`) |

For which chart to use inside an exhibit, follow the `deck-exhibits` skill (bar, line, stacked bar, highlight table, 2x2 matrix, process).

## Rules the build enforces

- Action title on every content slide: at most 2 lines at 24 pt or more (starts at 28 pt, shrinks to 24).
- Body text, table cells and chart labels 12 pt or more; source, footnotes and page numbers 10 pt or more.
- Nothing placed outside the slide; text measured before it is placed, overflow reported.
- Exhibit slides need a `source`. `meta.sample_data: true` stamps "Sample data" on every slide.
- One accent color for the point of the slide; everything else ink or grey. Two fonts (headings Georgia, body Arial by default) plus the East Asian theme font for `ko` / `ja`.
- Charts are native PowerPoint charts with direct labels, never pictures.

## The user's template

Pass `--template brand.pptx` (or `.potx`), or set `"template": {"path": "brand.potx"}` in the spec. The deck uses the template's slide size, theme fonts and colors, its title-slide, section and title-only layouts, its title placeholder position and its slide-number placeholder. Sample slides inside the template are dropped. Override the layout choice with `"template": {"layout_map": {"content": "Title Only"}}`. Details and limits: [references/templates.md](references/templates.md).

`python3 scripts/build.py --export-template default.pptx` writes the built-in template (also in `assets/default-template.pptx`) for users who want to start from it.

## Languages

Set `meta.language` to `en`, `ko` or `ja`. This sets the East Asian theme font (Malgun Gothic / Yu Gothic), run language tags, and the built-in labels (Source / 출처 / 出所, DRAFT / 초안 / ドラフト). Korean and Japanese titles fit about half as many characters per line as English: keep them to 25-50 characters.

## No-code mode (chat, Claude for PowerPoint)

Designed for chat and the Claude for PowerPoint sidebar; not yet tested in Claude for PowerPoint.

When you cannot run scripts, apply the same rules by hand inside PowerPoint or in your answer:

1. Write the action titles first and check they read as a story.
2. Use the user's template layouts: Title Only for content slides, Title Slide for the cover, Section Header for dividers.
3. Place content on the 12-column grid, keep one accent color, keep text at or above the type floors above, and add a source line and slide numbers.
4. Build charts as native PowerPoint charts styled per `deck-exhibits`.
5. Mark unknown numbers `[DATA NEEDED]` and illustrative ones "Sample data".

Grid, sizes, colors and a step-by-step manual checklist: [references/design-system.md](references/design-system.md).

## Troubleshooting

| Message | Fix |
|---|---|
| `slides[3].title: 131 characters, max 120` | Shorten the title; it should be one sentence. |
| `overflow: slide 5 body at 12pt` | Cut words, move detail to speaker notes or the appendix, or split the slide. |
| `LibreOffice not found` | The `.pptx` is fine. Install LibreOffice for previews or set `SOFFICE=/path/to/soffice`. |
| `template has no layout named ...` | Use one of the names the error lists in `layout_map`. |
| Korean or Japanese text in the wrong font | Set `meta.language`; with a user template, set its theme East Asian font in PowerPoint (Design > Variants > Fonts). |
