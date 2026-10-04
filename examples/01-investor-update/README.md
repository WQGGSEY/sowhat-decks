# 01 Investor update: Duolingo FY2025 results and the 2026 plan

A 13-slide investor update built only from a public company's FY2025 Form 10-K and two shareholder letters. Every number is cited on its slide.

Illustrative example, not affiliated with or endorsed by Duolingo, Inc. Not investment advice.

| File | What it is |
|---|---|
| [brief.md](brief.md) | Purpose, audience, decision, allowed material |
| [inputs/](inputs/) | XBRL extract from the 10-K and source notes |
| [storyline.md](storyline.md) | Governing message, SCQA, key arguments, slide plan, evidence ledger (deck-storyline). Section 9 lists what changed while building |
| [deck.json](deck.json) | The deck spec deck-build reads |
| [deck.pptx](deck.pptx) · [deck.pdf](deck.pdf) | The deck. Charts are native PowerPoint charts |
| [preview/](preview/) | Slide images (rendered with LibreOffice, scaled to 960 px) |
| [review.md](review.md) | deck-review report: 0 high, 0 medium, 1 low (explained) |
| [SOURCES.md](SOURCES.md) | Every source with its URL, and every formula |

**Titles only:** Duolingo is trading 2026 bookings growth for user growth, so judge 2026 by DAUs. Revenue grew 39% to $1.04B in 2025, the first year above $1B. Operating margin rose from 8.4% to 13.1%, and adjusted EBITDA margin reached 29.5%. A one-time $257M tax benefit makes up most of 2025's $414M net income. User growth slowed in 2025: DAUs grew 30% after 51%, and MAUs 14% after 32%. ... Judge 2026 by whether DAU growth re-accelerates above 2025's 30%, not by bookings growth.

## How it was made

Claude Code agents built this example during development, following the skills in this repo: one wrote the storyline, another wrote `deck.json`, built it, looked at every slide, reworked five exhibits (see `storyline.md` section 9) and ran the review. The prompts below restate what each step was asked to do, in the form you would type them. Rerunning them gives a similar deck, not the same words.

> Use deck-storyline to plan an investor update from examples/01-investor-update/brief.md and the files in examples/01-investor-update/inputs/. Use only those sources and cite every number.

> Use deck-build and deck-exhibits to turn examples/01-investor-update/storyline.md into deck.json and build it in examples/01-investor-update/. Look at every preview image and fix what looks wrong. Then run deck-review on deck.pptx and fix anything high or medium.

The commands, from the repository root, rebuild the committed files from `deck.json`:

```bash
python3 skills/deck-storyline/scripts/storyline_tool.py check examples/01-investor-update/storyline.md
python3 skills/deck-build/scripts/build.py examples/01-investor-update/deck.json -o examples/01-investor-update
python3 skills/deck-review/scripts/review.py run examples/01-investor-update/deck.pptx --no-fix --no-render
```

The build writes PNG previews 1600 px wide; the committed ones were scaled to 960 px to keep the repository small. The review writes its report to `deck-review/review.md`; `review.md` here is that report with the agent's rubric sections filled in.
