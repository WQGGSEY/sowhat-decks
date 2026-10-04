# 02 Market entry: which Southeast Asian market first?

A 13-slide recommendation for a language-learning app choosing between Indonesia, Vietnam, the Philippines and Thailand. **The company is hypothetical.** Every market statistic is World Bank data, cited on each slide.

| File | What it is |
|---|---|
| [brief.md](brief.md) | Purpose, audience, decision, allowed material |
| [inputs/](inputs/) | World Bank WDI extract (2015-2025) and source notes |
| [storyline.md](storyline.md) | Governing message, SCQA, key arguments, slide plan, evidence ledger (deck-storyline). Section 9 lists what changed while building |
| [deck.json](deck.json) | The deck spec deck-build reads |
| [deck.pptx](deck.pptx) · [deck.pdf](deck.pdf) | The deck. Charts are native PowerPoint charts |
| [preview/](preview/) | Slide images (rendered with LibreOffice, scaled to 960 px) |
| [review.md](review.md) | deck-review report: 0 high, 0 medium, 1 low (explained) |
| [SOURCES.md](SOURCES.md) | Indicator codes, API URLs and every formula |

**Titles only:** Launch in Indonesia first, and let a six-week paid test confirm it before full spend. Indonesia has 206M internet users, 2.4 times Vietnam's and over 3 times Thailand's. ... Adjusted for income, Indonesia's online market is at least twice that of any other candidate. Vietnam is the best backup: the fastest-growing economy, but under half Indonesia's online audience. ... We cannot yet say if we can win: app spending, competition and acquisition cost are unknown. ... Approve the paid test now, and launch in Indonesia if acquisition cost meets our payback target.

The deck does not guess what public statistics cannot show (willingness to pay, competition, acquisition cost). It names those gaps and proposes a test to close them.

## How it was made

Claude Code agents built this example during development, following the skills in this repo: one fetched the World Bank data and wrote the storyline, another wrote `deck.json`, built it, looked at every slide, reworked two exhibits (see `storyline.md` section 9) and ran the review. The prompts below restate what each step was asked to do, in the form you would type them. Rerunning them gives a similar deck, not the same words.

> Use deck-storyline to recommend which market our app should launch first, from examples/02-market-entry/brief.md and the World Bank data in examples/02-market-entry/inputs/. The company is hypothetical; cite every statistic and mark what public data cannot answer.

> Use deck-build and deck-exhibits to turn examples/02-market-entry/storyline.md into deck.json and build it in examples/02-market-entry/. Look at every preview image and fix what looks wrong. Then run deck-review on deck.pptx and fix anything high or medium.

Commands, from the repository root:

```bash
python3 skills/deck-storyline/scripts/storyline_tool.py check examples/02-market-entry/storyline.md
python3 skills/deck-build/scripts/build.py examples/02-market-entry/deck.json -o examples/02-market-entry
python3 skills/deck-review/scripts/review.py run examples/02-market-entry/deck.pptx --no-fix --no-render
```

Previews are scaled from 1600 px to 960 px. `review.md` is the review report with the agent's rubric sections filled in.
