# Deck review: deck.pptx

Automatic checks by deck-review on 2026-10-04 (`review.py run deck.pptx --no-fix --no-render`; deck-build had already rendered every slide to `preview/`). Story scores, so-what lines and the rubric review were filled in by the agent with `skills/deck-review/references/rubric.md` after looking at each rendered slide.

- **Slides:** 13
- **Issues:** 0 high, 0 medium, 9 low
- **Mechanical score:** 9.7/10 (mean of slides; story score is the agent's)

## Top 5 fixes

1. **[low] Text or exhibits collide** — slide 4 (#1, #2, #3, #4, #5, #6, …). Move or resize so nothing sits on top of text.
2. **[low] Edges that almost line up** — slide 4 (#8). Snap them to a shared edge.
3. **[low] Titles that may be topic labels (heuristic; confirm by reading)** — slide 12 (#9). Rewrite each as one sentence that states what the slide proves (see Rewritten titles).

Agent re-rank: no storyline, evidence or readability problem was found, so the list above stays as polish only. All 9 findings are low severity and are explained (and overruled) in the rubric review below.

## Title read-through

Read only the titles, top to bottom. Do they tell the whole story? The claim/label verdicts are rule-based guesses; the agent's reading is in the rubric review below.

| Slide | Title | Verdict |
|---|---|---|
| 1 | Which Southeast Asian market first? | cover |
| 2 | Launch in Indonesia first, and let a six-week paid test confirm it before full spend | claim |
| 3 | Indonesia has 206M internet users, 2.4 times Vietnam's and over 3 times Thailand's | claim |
| 4 | Indonesia also added the most users since 2019 (+76M) and still has 77M people offline | claim |
| 5 | Income per person in Indonesia matches Vietnam's and trails only Thailand's | claim |
| 6 | Adjusted for income, Indonesia's online market is at least twice that of any other candidate | claim |
| 7 | Vietnam is the best backup: the fastest-growing economy, but under half Indonesia's online audience | claim |
| 8 | Thailand is small and slow-growing, and the Philippines has the lowest income of the four | claim |
| 9 | We cannot yet say if we can win: app spending, competition and acquisition cost are unknown | claim |
| 10 | A six-week paid test in Indonesia and Vietnam answers those questions before full spend | claim |
| 11 | Approve the paid test now, and launch in Indonesia if acquisition cost meets our payback target | claim |
| 12 | Indicator table for the four markets, latest World Bank data | **label?** (no verb found; reads like a topic) |
| 13 | The Philippines' internet-use rate fell 10.6 points in 2024, so treat its online count with caution | claim |

As one paragraph: Which Southeast Asian market first?. Launch in Indonesia first, and let a six-week paid test confirm it before full spend. Indonesia has 206M internet users, 2.4 times Vietnam's and over 3 times Thailand's. Indonesia also added the most users since 2019 (+76M) and still has 77M people offline. Income per person in Indonesia matches Vietnam's and trails only Thailand's. Adjusted for income, Indonesia's online market is at least twice that of any other candidate. Vietnam is the best backup: the fastest-growing economy, but under half Indonesia's online audience. Thailand is small and slow-growing, and the Philippines has the lowest income of the four. We cannot yet say if we can win: app spending, competition and acquisition cost are unknown. A six-week paid test in Indonesia and Vietnam answers those questions before full spend. Approve the paid test now, and launch in Indonesia if acquisition cost meets our payback target. Indicator table for the four markets, latest World Bank data. The Philippines' internet-use rate fell 10.6 points in 2024, so treat its online count with caution.

## Rewritten titles

Proposed by the agent from the slide's own content. No number was added that the deck does not contain.

| Slide | Current | Proposed |
|---|---|---|
| 12 | Indicator table for the four markets, latest World Bank data | Keep the label: appendix slides may use one (rubric pass 1). A claim version would be "Working-age share and mobile subscriptions barely separate the four markets". |

## Slide by slide

| Slide | Title | Mechanical (0-10) | Story (0-10) | Issues |
|---|---|---|---|---|
| 1 | Which Southeast Asian market first? | 10.0 | — | — |
| 2 | Launch in Indonesia first, and let a six-week paid test con… | 10.0 | 10 | — |
| 3 | Indonesia has 206M internet users, 2.4 times Vietnam's and … | 10.0 | 9 | — |
| 4 | Indonesia also added the most users since 2019 (+76M) and s… | 6.0 | 9 | #1, #2, #3, #4, #5, #6, #7, #8 |
| 5 | Income per person in Indonesia matches Vietnam's and trails… | 10.0 | 9 | — |
| 6 | Adjusted for income, Indonesia's online market is at least … | 10.0 | 10 | — |
| 7 | Vietnam is the best backup: the fastest-growing economy, bu… | 10.0 | 9 | — |
| 8 | Thailand is small and slow-growing, and the Philippines has… | 10.0 | 9 | — |
| 9 | We cannot yet say if we can win: app spending, competition … | 10.0 | 9 | — |
| 10 | A six-week paid test in Indonesia and Vietnam answers those… | 10.0 | 8 | — |
| 11 | Approve the paid test now, and launch in Indonesia if acqui… | 10.0 | 10 | — |
| 12 | Indicator table for the four markets, latest World Bank data | 9.5 | 7 | #9 |
| 13 | The Philippines' internet-use rate fell 10.6 points in 2024… | 10.0 | 10 | — |

### Slide 1: Which Southeast Asian market first?

- No automatic findings.
- **So what:** States the question and, on the cover, that the company is hypothetical and the statistics are World Bank data.

### Slide 2: Launch in Indonesia first, and let a six-week paid test confirm it before full spend

- No automatic findings.
- **So what:** The answer and its condition on one page: Indonesia first, confirmed by a six-week paid test.

### Slide 3: Indonesia has 206M internet users, 2.4 times Vietnam's and over 3 times Thailand's

- No automatic findings.
- **So what:** Indonesia is by far the largest reachable audience; the bar shows every number in the title and the formula is in the source line.

### Slide 4: Indonesia also added the most users since 2019 (+76M) and still has 77M people offline

- **#1 [low] overlap**: Text "sw:label" sits on top of chart "sw:chart". Fix: Fine if it is a deliberate label; otherwise move it clear.
- **#2 [low] overlap**: Text "sw:label" sits on top of chart "sw:chart". Fix: Fine if it is a deliberate label; otherwise move it clear.
- **#3 [low] overlap**: Text "sw:label" sits on top of chart "sw:chart". Fix: Fine if it is a deliberate label; otherwise move it clear.
- **#4 [low] overlap**: Text "sw:label" sits on top of chart "sw:chart". Fix: Fine if it is a deliberate label; otherwise move it clear.
- **#5 [low] overlap**: Text "sw:label" sits on top of chart "sw:chart". Fix: Fine if it is a deliberate label; otherwise move it clear.
- **#6 [low] overlap**: Text "sw:label" sits on top of chart "sw:chart". Fix: Fine if it is a deliberate label; otherwise move it clear.
- **#7 [low] overlap**: Text "sw:label" sits on top of chart "sw:chart". Fix: Fine if it is a deliberate label; otherwise move it clear.
- **#8 [low] misaligned**: "sw:label" is 0.08 in off the left edge of "sw:title". Fix: Snap it to the same edge.
- **So what:** Indonesia's audience is still growing fastest, with the largest offline pool; the highlighted segment shows the +76M.

### Slide 5: Income per person in Indonesia matches Vietnam's and trails only Thailand's

- No automatic findings.
- **So what:** Income does not rule Indonesia out: it matches Vietnam and trails only Thailand. Both years are on the slide.

### Slide 6: Adjusted for income, Indonesia's online market is at least twice that of any other candidate

- No automatic findings.
- **So what:** Even after income, Indonesia leads by at least 2x; the proxy and its assumption are stated on the slide.

### Slide 7: Vietnam is the best backup: the fastest-growing economy, but under half Indonesia's online audience

- No automatic findings.
- **So what:** Why Vietnam is second, not first: fastest growth on the chart, smaller audience in the takeaways.

### Slide 8: Thailand is small and slow-growing, and the Philippines has the lowest income of the four

- No automatic findings.
- **So what:** Why not the other two, with one sourced fact per bullet.

### Slide 9: We cannot yet say if we can win: app spending, competition and acquisition cost are unknown

- No automatic findings.
- **So what:** Names what public statistics cannot answer and how each gap gets closed. No guessed numbers.

### Slide 10: A six-week paid test in Indonesia and Vietnam answers those questions before full spend

- No automatic findings.
- **So what:** The test that closes those gaps; it is a proposal, so the slide is evidence of a plan rather than of a result.

### Slide 11: Approve the paid test now, and launch in Indonesia if acquisition cost meets our payback target

- No automatic findings.
- **So what:** The decision: approve the test now, with owners, timing and the go/no-go rule.

### Slide 12: Indicator table for the four markets, latest World Bank data

- **#9 [low] title_not_claim**: Title "Indicator table for the four markets, latest World Bank data" may be a topic label (no verb found; reads like a topic). This is a heuristic guess; confirm it with the title-only read in the rubric; in the appendix a label is acceptable, a claim is better. Fix: Rewrite as a claim: subject + verb + so-what, e.g. what changed, by how much, and why it matters.
- **So what:** Back-up table, including the two indicators that do not separate the markets.

### Slide 13: The Philippines' internet-use rate fell 10.6 points in 2024, so treat its online count with caution

- No automatic findings.
- **So what:** A data-quality caveat that a careful reader would raise, with the check that it does not change the ranking.

## Rubric review

Audience and purpose (from the brief): CEO and CFO of a hypothetical app company with budget for one new-market launch; which market first.

**Title read-through (pass 1).** Governing message heard: *launch in Indonesia first because it is the largest online market even after adjusting for income, but let a six-week paid test confirm we can win before committing the full budget.*

| # | Question | Result | Why |
|---|---|---|---|
| 1 | Governing message from the titles alone | Pass | Slide 2 states the choice and the condition |
| 2 | Every content title a full-sentence claim | Pass | Cover is a question; slide 12 is an appendix label |
| 3 | Each title follows from the one before | Pass | Size, growth, income, size x income, why not Vietnam, why not the others, what we do not know, how we find out, decide |
| 4 | Each key argument appears in order | Pass | Reach (3-4), ability to pay (5-6), alternatives (7-8), ability to win (9-10) |
| 5 | Nothing said twice | Pass | Slides 2 and 11 both mention the test: answer vs decision rule |
| 6 | Ends on what the reader must do | Pass | Slide 11: four actions with owners and timing |
| 7 | Every number in a title is backed on its slide | Pass | All title numbers are on the exhibits or in the takeaways |

**Across slides (pass 3).** No duplication. Answer first. The recommendation is conditional by design, and slides 9-11 cover cost, risk and timing of the test.

**Evidence (pass 4).** Every market figure is World Bank WDI (indicator codes on each slide, URLs in `SOURCES.md`). Derived figures show their formula. The income-adjusted proxy is labelled as a ranking device with its assumption. Company facts (budget, team) are hypothetical and appear only in the brief and the speaker notes.

**[DATA NEEDED] and placeholders:** none in the deck. The storyline listed eight open requests (app spending, competitors, payment methods, rules, budgets, acquisition cost, payback target, the Philippines series break). The deck does not need any of those numbers to make its argument, so it states them as unknowns with an owner and a way to find out (slides 9-11, 13) instead of leaving placeholders.

**Low findings overruled (all 9):**
- `overlap` and one label `misaligned` on slide 4: the series names are deliberate labels beside the stacked bars.
- `title_not_claim` on slide 12: appendix label, allowed.

**Verdict:** ready. Mechanical: 0 high, 0 medium. Story: mean 9.1 over the 12 content slides.
