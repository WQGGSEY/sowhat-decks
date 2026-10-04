# Examples

| Folder | Deck | Data | Review of the final deck |
|---|---|---|---|
| [01-investor-update](01-investor-update/) | Investor update on a public company's FY2025 results and 2026 plan, 13 slides | FY2025 Form 10-K and two shareholder letters (SEC EDGAR), every number cited | 0 high, 0 medium |
| [02-market-entry](02-market-entry/) | Which Southeast Asian market a language-learning app should launch first, 13 slides | World Bank World Development Indicators, cited. The company is hypothetical | 0 high, 0 medium |
| [03-review-before-after](03-review-before-after/) | A Q3 board update: a draft with planted problems, its review, and the deck rebuilt, 14 slides | Sample data, labelled on every slide | Draft: 1 high, 18 medium, 11 low. Rebuilt: 0 high, 0 medium |
| [storyline-tests](storyline-tests/) | The deck-storyline tests: the three storylines as title-only ghost decks, plus a copy of example 03 with topic titles that fails the title check | Same as above | The ghost decks keep their `[DATA NEEDED]` markers, which deck-review reports |

Every example folder has `brief.md`, `inputs/`, `storyline.md`, `deck.json`, `deck.pptx`, `deck.pdf`, `preview/`, `review.md`, `SOURCES.md` and a `README.md` with the prompts and commands.

## Numbers

Every number is either copied from a cited public source, derived from one with the formula shown on the slide or in `SOURCES.md`, or labelled "Sample data". Example 01 is an illustration built from public filings; it is not affiliated with the company it describes and is not investment advice.

## How they were made

Claude Code agents built these examples during development, following the skills in this repository. Each example's README restates the prompts each step worked from and lists the commands that rebuild the files. Previews are scaled to 960 px wide to keep the repository small.

Rebuild all three decks, then check them (from the repository root; the test runs deck-review's checks on every deck):

```bash
for e in 01-investor-update 02-market-entry 03-review-before-after; do
  python3 skills/deck-build/scripts/build.py examples/$e/deck.json -o examples/$e
done
python3 -m pytest -q tests/test_examples.py
```
