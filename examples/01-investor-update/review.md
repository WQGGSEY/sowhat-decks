# Deck review: deck.pptx

Automatic checks by deck-review on 2026-10-04 (`review.py run deck.pptx --no-fix --no-render`; deck-build had already rendered every slide to `preview/`). Story scores, so-what lines and the rubric review were filled in by the agent with `skills/deck-review/references/rubric.md` after looking at each rendered slide.

- **Slides:** 13
- **Issues:** 0 high, 0 medium, 5 low
- **Mechanical score:** 9.8/10 (mean of slides; story score is the agent's)

## Top 5 fixes

1. **[low] Text or exhibits collide** — slide 5 (#1, #2, #3). Move or resize so nothing sits on top of text.
2. **[low] Edges that almost line up** — slide 5 (#4). Snap them to a shared edge.
3. **[low] Titles that may be topic labels (heuristic; confirm by reading)** — slide 13 (#5). Rewrite each as one sentence that states what the slide proves (see Rewritten titles).

Agent re-rank: no storyline, evidence or readability problem was found, so the list above stays as polish only. All 5 findings are low severity and are explained (and overruled) in the rubric review below. Nothing needs to change before this deck is shown.

## Title read-through

Read only the titles, top to bottom. Do they tell the whole story? The claim/label verdicts are rule-based guesses; the agent's reading is in the rubric review below.

| Slide | Title | Verdict |
|---|---|---|
| 1 | Duolingo FY2025 investor update | cover |
| 2 | Duolingo is trading 2026 bookings growth for user growth, so judge 2026 by DAUs | claim |
| 3 | Revenue grew 39% to $1.04B in 2025, the first year above $1B | claim |
| 4 | Operating margin rose from 8.4% to 13.1%, and adjusted EBITDA margin reached 29.5% | claim |
| 5 | A one-time $257M tax benefit makes up most of 2025's $414M net income | claim |
| 6 | User growth slowed in 2025: DAUs grew 30% after 51%, and MAUs 14% after 32% | claim |
| 7 | Engagement still deepened: 40% of monthly users now open the app daily, up from 35% | claim |
| 8 | Paid subscribers grew 28% to 12.2M, slower than the 43% of a year earlier | claim |
| 9 | 2026 guidance cuts bookings growth to 10-12% by giving up over $50M of bookings to grow free users | claim |
| 10 | Margins step down in 2026: gross margin to about 69% on AI costs, adjusted EBITDA margin to 25% | claim |
| 11 | $360M of free cash flow and $1.04B in cash can fund the user bet and a $400M buyback | claim |
| 12 | Judge 2026 by whether DAU growth re-accelerates above 2025's 30%, not by bookings growth | claim |
| 13 | Key figures FY2023-FY2025 | **label?** (3 words, no verb) |

As one paragraph: Duolingo FY2025 investor update. Duolingo is trading 2026 bookings growth for user growth, so judge 2026 by DAUs. Revenue grew 39% to $1.04B in 2025, the first year above $1B. Operating margin rose from 8.4% to 13.1%, and adjusted EBITDA margin reached 29.5%. A one-time $257M tax benefit makes up most of 2025's $414M net income. User growth slowed in 2025: DAUs grew 30% after 51%, and MAUs 14% after 32%. Engagement still deepened: 40% of monthly users now open the app daily, up from 35%. Paid subscribers grew 28% to 12.2M, slower than the 43% of a year earlier. 2026 guidance cuts bookings growth to 10-12% by giving up over $50M of bookings to grow free users. Margins step down in 2026: gross margin to about 69% on AI costs, adjusted EBITDA margin to 25%. $360M of free cash flow and $1.04B in cash can fund the user bet and a $400M buyback. Judge 2026 by whether DAU growth re-accelerates above 2025's 30%, not by bookings growth. Key figures FY2023-FY2025.

## Rewritten titles

Proposed by the agent from the slide's own content. No number was added that the deck does not contain.

| Slide | Current | Proposed |
|---|---|---|
| 13 | Key figures FY2023-FY2025 | Keep the label: appendix slides may use one (rubric pass 1). A claim version would be "Revenue nearly doubled from FY2023 to FY2025 while users kept growing". |

## Slide by slide

| Slide | Title | Mechanical (0-10) | Story (0-10) | Issues |
|---|---|---|---|---|
| 1 | Duolingo FY2025 investor update | 10.0 | — | — |
| 2 | Duolingo is trading 2026 bookings growth for user growth, s… | 10.0 | 10 | — |
| 3 | Revenue grew 39% to $1.04B in 2025, the first year above $1B | 10.0 | 9 | — |
| 4 | Operating margin rose from 8.4% to 13.1%, and adjusted EBIT… | 10.0 | 9 | — |
| 5 | A one-time $257M tax benefit makes up most of 2025's $414M … | 8.0 | 10 | #1, #2, #3, #4 |
| 6 | User growth slowed in 2025: DAUs grew 30% after 51%, and MA… | 10.0 | 9 | — |
| 7 | Engagement still deepened: 40% of monthly users now open th… | 10.0 | 9 | — |
| 8 | Paid subscribers grew 28% to 12.2M, slower than the 43% of … | 10.0 | 9 | — |
| 9 | 2026 guidance cuts bookings growth to 10-12% by giving up o… | 10.0 | 10 | — |
| 10 | Margins step down in 2026: gross margin to about 69% on AI … | 10.0 | 9 | — |
| 11 | $360M of free cash flow and $1.04B in cash can fund the use… | 10.0 | 9 | — |
| 12 | Judge 2026 by whether DAU growth re-accelerates above 2025'… | 10.0 | 10 | — |
| 13 | Key figures FY2023-FY2025 | 9.5 | 7 | #5 |

### Slide 1: Duolingo FY2025 investor update

- No automatic findings.
- **So what:** Names the company, the period and the status of the deck (illustration from public filings, not affiliated, not investment advice).

### Slide 2: Duolingo is trading 2026 bookings growth for user growth, so judge 2026 by DAUs

- No automatic findings.
- **So what:** The whole answer on one page: a strong 2025, slowing users, a deliberate 2026 trade, and the cash to fund it. Each point carries its number.

### Slide 3: Revenue grew 39% to $1.04B in 2025, the first year above $1B

- No automatic findings.
- **So what:** The business has real scale. The highlighted FY2025 bar shows $1,038M and the source line gives the growth formula.

### Slide 4: Operating margin rose from 8.4% to 13.1%, and adjusted EBITDA margin reached 29.5%

- No automatic findings.
- **So what:** Profitability improved on both measures; both lines are on the chart and the non-GAAP measure is labelled.

### Slide 5: A one-time $257M tax benefit makes up most of 2025's $414M net income

- **#1 [low] overlap**: Text "sw:label" sits on top of chart "sw:chart". Fix: Fine if it is a deliberate label; otherwise move it clear.
- **#2 [low] overlap**: Text "sw:label" sits on top of chart "sw:chart". Fix: Fine if it is a deliberate label; otherwise move it clear.
- **#3 [low] overlap**: Text "sw:label" sits on top of chart "sw:chart". Fix: Fine if it is a deliberate label; otherwise move it clear.
- **#4 [low] misaligned**: "sw:label" is 0.08 in off the left edge of "sw:title". Fix: Snap it to the same edge.
- **So what:** Most of 2025's net income will not repeat. The stacked bar splits $414M into $257M one-time and $157M rest; the subtraction is disclosed.

### Slide 6: User growth slowed in 2025: DAUs grew 30% after 51%, and MAUs 14% after 32%

- No automatic findings.
- **So what:** The complication: all three user metrics slowed, and DAUs fell most. The slope chart shows every number in the title.

### Slide 7: Engagement still deepened: 40% of monthly users now open the app daily, up from 35%

- No automatic findings.
- **So what:** A counterweight: engagement deepened. Both ratios are on the chart and the formula is in the source line.

### Slide 8: Paid subscribers grew 28% to 12.2M, slower than the 43% of a year earlier

- No automatic findings.
- **So what:** Subscribers still grew, but more slowly. The chart shows 9.5M and 12.2M; the growth rates in the title come from the letters cited.

### Slide 9: 2026 guidance cuts bookings growth to 10-12% by giving up over $50M of bookings to grow free users

- No automatic findings.
- **So what:** The slowdown in 2026 is chosen, not suffered: the bar shows the 11% guidance midpoint and the takeaways give the $50M cost. The footnote says it is guidance.

### Slide 10: Margins step down in 2026: gross margin to about 69% on AI costs, adjusted EBITDA margin to 25%

- No automatic findings.
- **So what:** Margins fall on purpose too. Gross margin is on the chart; the 25% adjusted EBITDA guidance is in the takeaways rather than the exhibit (minor).

### Slide 11: $360M of free cash flow and $1.04B in cash can fund the user bet and a $400M buyback

- No automatic findings.
- **So what:** The bet is affordable. Cash, buyback and free cash flow are on the chart; the comparison with the over-$50M bet is in the speaker notes rather than on the slide (minor).

### Slide 12: Judge 2026 by whether DAU growth re-accelerates above 2025's 30%, not by bookings growth

- No automatic findings.
- **So what:** Turns the argument into three things to track each quarter, with the baseline for each.

### Slide 13: Key figures FY2023-FY2025

- **#5 [low] title_not_claim**: Title "Key figures FY2023-FY2025" may be a topic label (3 words, no verb). This is a heuristic guess; confirm it with the title-only read in the rubric; in the appendix a label is acceptable, a claim is better. Fix: Rewrite as a claim: subject + verb + so-what, e.g. what changed, by how much, and why it matters.
- **So what:** Back-up table for every financial and user figure used in the deck; n/a marks what the material did not cover.

## Rubric review

Audience and purpose (from the brief): investors who know the headline numbers; how to read the 2026 guidance and what to track.

**Title read-through (pass 1).** Governing message heard: *after a profitable $1B year, Duolingo is trading 2026 bookings growth and margin for faster user growth, which cash flow can fund, so judge 2026 by DAU growth.*

| # | Question | Result | Why |
|---|---|---|---|
| 1 | Governing message from the titles alone | Pass | Slide 2 states it; slides 3-12 rebuild it |
| 2 | Every content title a full-sentence claim | Pass | Only the cover and the appendix use labels |
| 3 | Each title follows from the one before | Pass | Results (3-5), the turn (6-8), the plan (9-10), affordability (11), what to watch (12) |
| 4 | Each key argument appears in order | Pass | Four arguments, four groups of slides |
| 5 | Nothing said twice | Pass | Slides 2 and 12 share "judge by DAUs" at two levels: summary and concrete metric |
| 6 | Ends on what the reader must do | Pass | Slide 12 lists three metrics, each with a baseline |
| 7 | Every number in a title is backed on its slide | Pass | Each title number is on the exhibit, in the takeaways or in the source formula |

**Across slides (pass 3).** No duplication. Answer first. The deck has no slide on 2026 results because the brief limits the material to the FY2025 filings; slide 12 makes that explicit by giving the baselines to compare each 2026 letter against.

**Evidence (pass 4).** Every figure comes from the FY2025 Form 10-K (SEC XBRL) or the Q4 FY2025 and Q4 FY2024 shareholder letters, all on SEC EDGAR (see `SOURCES.md`). Derived figures (growth rates, margins, ratios, the $157M remainder) show their formula on the slide or in the speaker notes. Adjusted EBITDA and free cash flow are labelled non-GAAP; 2026 figures are labelled guidance.

**[DATA NEEDED] and placeholders:** none. The storyline had one open request (2026 quarterly DAU growth). It is outside the material the brief allows, so the final deck states what to track instead of leaving a placeholder.

**Low findings overruled (all 5):**
- `overlap` and one label `misaligned` on slide 5: the series names are deliberate labels beside the stacked bar.
- `title_not_claim` on slide 13: appendix label, allowed.

**Verdict:** ready. Mechanical: 0 high, 0 medium. Story: mean 9.2 over the 12 content slides.
