# deck-storyline tests

Three real tasks run through the `deck-storyline` skill, plus one negative control.
Each folder holds the inputs, the `storyline.md` the skill produced, the ghost deck
spec (`ghost.json`), and the ghost deck rendered by `deck-build`
(`render/ghost.pptx`, `render/ghost.pdf`, `render/preview/slide-NN.png`).

| Test | Task | Data | Slides | `check` | Title-only test | Open data requests |
|---|---|---|---|---|---|---|
| [01-investor-update](01-investor-update/) | Investor update on Duolingo's FY2025 results and 2026 plan | Public: FY2025 Form 10-K (SEC XBRL API) and Q4 FY2025 / Q4 FY2024 shareholder letters | 13 | PASS, 0 warnings | **PASS** (7/7) | 1 |
| [02-market-entry](02-market-entry/) | Which Southeast Asian market a language-learning app should launch first | Public: World Bank WDI (population, internet use, GDP per capita PPP, GDP growth); company is hypothetical | 13 | PASS, 0 warnings | **PASS** (7/7) | 8 |
| [03-board-update-sample](03-board-update-sample/) | Q3 board update for a SaaS company with a churn problem | **Sample data** (invented, labelled on every slide) | 14 | PASS, 0 warnings | **PASS** (7/7) | 1 (2 mentions) |
| [control-topic-titles](control-topic-titles/) | Test 03 with every action title replaced by a topic label | Sample data | 14 | FAIL, 8 errors + 3 warnings | **FAIL** (2/7, both trivial) | — |

## Title-only test results

**01 Investor update — PASS.** Titles alone say: revenue passed $1B with wider
margins; most of the net income is a one-time tax benefit; user growth slowed sharply;
2026 guidance deliberately gives up bookings growth and margin for users; cash can
fund it; judge 2026 by DAU growth. The turn from "strong year" to "slowing users" is
explicit (slide 6), and slide 9's title ties the guidance cut to user growth, so the
plan does not appear from nowhere. Limit: whether the bet is working needs 2026
quarterly data, which the brief excluded — marked `[DATA NEEDED]` on the last slide.

**02 Market entry — PASS.** Titles alone give the choice (Indonesia), why (largest
online audience, still largest after adjusting for income), why not the others
(Vietnam smaller though faster-growing; Thailand small and slow; Philippines lowest
income), what is unknown, and the decision rule. The recommendation is conditional
by design: public statistics cannot show willingness to pay, competition or
acquisition cost, so those are eight explicit data requests and a six-week paid
test, not guessed numbers. Note: an early draft written before fetching the data
favoured Vietnam; the evidence ledger changed the answer.

**03 Board update (sample data) — PASS.** Titles alone say: Q3 beat plan; churn is
eating the beat and puts year-end ARR $230k short; the cause is SMB accounts that
never finish setup as onboarding load rose; moving two sales hires to onboarding
saves money and recovers about a third of the gap; the 2027 capacity cost is not
yet sized; here are the two approvals we need.

**Control — FAIL, as intended.** Same evidence and order, topic titles
("Bookings performance", "Churn by segment", "Next steps"). The read-out is an
agenda, not a story. `storyline_tool.py titles` flags all 11 content titles
(8 errors, 3 "no verb" warnings) and exits 1; see `control-topic-titles/title-lint.txt`.

## Cross-check with deck-review

`skills/deck-review/scripts/review.py check render/ghost.pptx` on the three ghost decks
reports only expected findings: `data_needed` (high) on every slide that carries a
`[DATA NEEDED]` marker (1, 4 and 2 slides), and `title_not_claim` (low) on the two
appendix slides that use a descriptive label (allowed for appendix slides). The
gaps the storyline marked are therefore visible to the reviewer downstream.

## Number policy

- 01 and 02: every number is either copied from a cited source (URLs and retrieval
  date in each `storyline.md` section 8 and `inputs/source-notes.md`) or derived with
  the formula written in the evidence ledger (`CALC`).
- 01 letter figures (bookings, DAUs, guidance) were read from the SEC-hosted letters
  with a page-reading tool; the figures that also appear in the XBRL data matched.
  Spot-check them against the letters before publishing.
- 03: every number is invented sample data, tagged `SAMPLE` in the ledger; the deck
  carries "Sample data" on every slide.
- 01 is an illustrative example built from public filings. It is not produced by,
  affiliated with, or endorsed by Duolingo, Inc., and it is not investment advice.

## Reproduce

From the repository root:

```bash
T=skills/deck-storyline/scripts/storyline_tool.py
for d in examples/storyline-tests/0*/; do
  python3 $T check  $d/storyline.md
  python3 $T titles $d/storyline.md
  python3 $T ghost  $d/storyline.md -o $d/ghost.json
  python3 skills/deck-build/scripts/build.py $d/ghost.json -o $d/render --name ghost
done
```

Rendering to PDF/PNG needs LibreOffice; the `.pptx` is built without it.
