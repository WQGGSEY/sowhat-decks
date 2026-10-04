# Deck review: deck.pptx

Automatic checks by deck-review on 2026-10-04: `python3 skills/deck-review/scripts/review.py run examples/03-review-before-after/deck.pptx --no-fix --no-render` (deck-build had already rendered every slide to `preview/`). Story scores, so-what lines and the rubric review were filled in by the agent with `skills/deck-review/references/rubric.md` after looking at each rendered slide. Compare with `review.md`, the review of the draft this deck replaces.

- **Slides:** 14
- **Issues:** 0 high, 0 medium, 6 low
- **Mechanical score:** 9.8/10 (mean of slides; story score is the agent's)

## Top 5 fixes

1. **[low] Text or exhibits collide** — slide 5 (#1, #2, #3, #4, #5). Move or resize so nothing sits on top of text.
2. **[low] Edges that almost line up** — slide 5 (#6). Snap them to a shared edge.

Agent re-rank: no storyline, evidence or readability problem was found, so the list above stays as polish only. All 6 findings are low severity and are explained (and overruled) in the rubric review below.

## Title read-through

Read only the titles, top to bottom. Do they tell the whole story? The claim/label verdicts are rule-based guesses; the agent's reading is in the rubric review below.

| Slide | Title | Verdict |
|---|---|---|
| 1 | Q3 2026 board update | cover |
| 2 | Q3 beat plan, but SMB churn puts year-end ARR $230k short; we propose moving two hires to onboarding | claim |
| 3 | New ARR beat plan by 21% in Q3, the third straight quarter above plan | claim |
| 4 | Ending ARR of $11.05M beat plan by 1.4%, a smaller margin than new ARR because churn rose | claim |
| 5 | SMB churned ARR more than doubled since Q1 and now offsets a third of new bookings | claim |
| 6 | If the SMB trend continues, year-end ARR lands about $230k below the $12.0M plan | claim |
| 7 | Most SMB accounts that churned in Q3 never finished setup in their first 30 days | claim |
| 8 | Accounts that finish setup churn at about a fifth of the rate of those that do not | claim |
| 9 | Setup completion fell from 68% to 55% as new accounts per specialist rose 41% | claim |
| 10 | Shifting two Q4 sales hires to onboarding saves $110k a year and recovers about $82k of Q4 ARR | claim |
| 11 | The cost is slower sales capacity in 2027, which Sales has not yet sized | claim |
| 12 | We ask the board to approve the swap and a revised year-end forecast of $11.85M | claim |
| 13 | Cash runway stays near 22 months at the current $650k monthly burn | claim |
| 14 | Q1-Q3 2026 metrics by quarter | claim |

As one paragraph: Q3 2026 board update. Q3 beat plan, but SMB churn puts year-end ARR $230k short; we propose moving two hires to onboarding. New ARR beat plan by 21% in Q3, the third straight quarter above plan. Ending ARR of $11.05M beat plan by 1.4%, a smaller margin than new ARR because churn rose. SMB churned ARR more than doubled since Q1 and now offsets a third of new bookings. If the SMB trend continues, year-end ARR lands about $230k below the $12.0M plan. Most SMB accounts that churned in Q3 never finished setup in their first 30 days. Accounts that finish setup churn at about a fifth of the rate of those that do not. Setup completion fell from 68% to 55% as new accounts per specialist rose 41%. Shifting two Q4 sales hires to onboarding saves $110k a year and recovers about $82k of Q4 ARR. The cost is slower sales capacity in 2027, which Sales has not yet sized. We ask the board to approve the swap and a revised year-end forecast of $11.85M. Cash runway stays near 22 months at the current $650k monthly burn. Q1-Q3 2026 metrics by quarter.

## Rewritten titles

No title failed the automatic claim and length checks. The agent checked each claim against its slide: every title is specific and supported (see the so-what lines).

## Slide by slide

| Slide | Title | Mechanical (0-10) | Story (0-10) | Issues |
|---|---|---|---|---|
| 1 | Q3 2026 board update | 10.0 | — | — |
| 2 | Q3 beat plan, but SMB churn puts year-end ARR $230k short; … | 10.0 | 10 | — |
| 3 | New ARR beat plan by 21% in Q3, the third straight quarter … | 10.0 | 9 | — |
| 4 | Ending ARR of $11.05M beat plan by 1.4%, a smaller margin t… | 10.0 | 9 | — |
| 5 | SMB churned ARR more than doubled since Q1 and now offsets … | 7.0 | 10 | #1, #2, #3, #4, #5, #6 |
| 6 | If the SMB trend continues, year-end ARR lands about $230k … | 10.0 | 10 | — |
| 7 | Most SMB accounts that churned in Q3 never finished setup i… | 10.0 | 9 | — |
| 8 | Accounts that finish setup churn at about a fifth of the ra… | 10.0 | 9 | — |
| 9 | Setup completion fell from 68% to 55% as new accounts per s… | 10.0 | 9 | — |
| 10 | Shifting two Q4 sales hires to onboarding saves $110k a yea… | 10.0 | 10 | — |
| 11 | The cost is slower sales capacity in 2027, which Sales has … | 10.0 | 9 | — |
| 12 | We ask the board to approve the swap and a revised year-end… | 10.0 | 10 | — |
| 13 | Cash runway stays near 22 months at the current $650k month… | 10.0 | 9 | — |
| 14 | Q1-Q3 2026 metrics by quarter | 10.0 | 7 | — |

### Slide 1: Q3 2026 board update

- No automatic findings.
- **So what:** Cover. States on the slide that the company is fictional and every figure is sample data; every other slide repeats "Sample data" in its source line.

### Slide 2: Q3 beat plan, but SMB churn puts year-end ARR $230k short; we propose moving two hires to onboarding

- No automatic findings.
- **So what:** The answer and the ask on one page: Q3 beat plan, churn puts the year $230k short, the cause, the fix and the two approvals.

### Slide 3: New ARR beat plan by 21% in Q3, the third straight quarter above plan

- No automatic findings.
- **So what:** Demand is not the problem: the Q3 bar shows the 21% beat and the takeaways show all three quarters beat plan.

### Slide 4: Ending ARR of $11.05M beat plan by 1.4%, a smaller margin than new ARR because churn rose

- No automatic findings.
- **So what:** The bridge shows why ending ARR beat plan by less: churned ARR is the highlighted row, $300k to $480k.

### Slide 5: SMB churned ARR more than doubled since Q1 and now offsets a third of new bookings

- **#1 [low] overlap**: Text "sw:label" sits on top of chart "sw:chart". Fix: Fine if it is a deliberate label; otherwise move it clear.
- **#2 [low] overlap**: Text "sw:label" sits on top of chart "sw:chart". Fix: Fine if it is a deliberate label; otherwise move it clear.
- **#3 [low] overlap**: Text "sw:label" sits on top of chart "sw:chart". Fix: Fine if it is a deliberate label; otherwise move it clear.
- **#4 [low] overlap**: Text "sw:label" sits on top of chart "sw:chart". Fix: Fine if it is a deliberate label; otherwise move it clear.
- **#5 [low] overlap**: Text "sw:label" sits on top of chart "sw:chart". Fix: Fine if it is a deliberate label; otherwise move it clear.
- **#6 [low] misaligned**: "sw:label" is 0.08 in off the left edge of "sw:title". Fix: Snap it to the same edge.
- **So what:** SMB is the whole change in churn; the stacked bar shows 170 to 390 and the takeaway gives the one-third share.

### Slide 6: If the SMB trend continues, year-end ARR lands about $230k below the $12.0M plan

- No automatic findings.
- **So what:** Sizes the problem the draft left as TBD, with every assumption in the right-hand column.

### Slide 7: Most SMB accounts that churned in Q3 never finished setup in their first 30 days

- No automatic findings.
- **So what:** The symptom: 44 of 61 churned accounts never finished setup.

### Slide 8: Accounts that finish setup churn at about a fifth of the rate of those that do not

- No automatic findings.
- **So what:** The mechanism: 4% vs 19% churn by setup status.

### Slide 9: Setup completion fell from 68% to 55% as new accounts per specialist rose 41%

- No automatic findings.
- **So what:** The driver: load per specialist up 41% while setup completion fell; both columns are highlighted in the table.

### Slide 10: Shifting two Q4 sales hires to onboarding saves $110k a year and recovers about $82k of Q4 ARR

- No automatic findings.
- **So what:** The fix with its cost and benefit side by side, and the $82k labelled as an estimate with its assumptions.

### Slide 11: The cost is slower sales capacity in 2027, which Sales has not yet sized

- No automatic findings.
- **So what:** The cost of the fix, stated openly, with who sizes it and when.

### Slide 12: We ask the board to approve the swap and a revised year-end forecast of $11.85M

- No automatic findings.
- **So what:** Two decisions for today and one review in January, each with an owner and timing.

### Slide 13: Cash runway stays near 22 months at the current $650k monthly burn

- No automatic findings.
- **So what:** Runway is not the constraint (about 22 months).

### Slide 14: Q1-Q3 2026 metrics by quarter

- No automatic findings.
- **So what:** Back-up table of the quarterly metrics.

## Rubric review

Audience and purpose (from `brief.md`): the board of a fictional SaaS company; two approvals needed.

**Title read-through (pass 1).** Governing message heard: *Q3 beat plan, but rising SMB churn puts year-end ARR about $230k short; moving two Q4 sales hires to onboarding fixes the cause, saves $110k a year and recovers about a third of the gap, and the board is asked to approve it with a revised $11.85M forecast.*

| # | Question | Result | Why |
|---|---|---|---|
| 1 | Governing message from the titles alone | Pass | Slide 2 states it; slides 3-12 rebuild it |
| 2 | Every content title a full-sentence claim | Pass | Cover and slide 14 (appendix) are labels, allowed |
| 3 | Each title follows from the one before | Pass | Beat, smaller beat, churn, gap, symptom, mechanism, driver, fix, cost, ask |
| 4 | Each key argument appears in order | Pass | Results (3-4), constraint (5-6), cause (7-9), fix (10-11) |
| 5 | Nothing said twice | Pass | Slides 2 and 12 carry the ask at two levels |
| 6 | Ends on what the reader must decide | Pass | Slide 12: two approvals today, one review in January |
| 7 | Every number in a title is backed on its slide | Pass | Each title number is on the exhibit, in the takeaways or in the source formula |

**Across slides (pass 3).** No duplication; answer first; the recommendation has its cost (slide 11), benefit (slide 10) and timing (slide 12).

**Evidence (pass 4).** Every figure is sample data from `inputs/` (labelled on every slide). Derived figures show their formula; the projection and the $82k are labelled as estimates with their assumptions.

**[DATA NEEDED] and placeholders:** none. The storyline kept one open item (2027 sales capacity). The board can decide without it, so slides 11 and 12 state it as unsized and assign it to the VP Sales for the January meeting instead of leaving a placeholder.

**Low findings overruled (all 6):** `overlap` plus one label `misaligned` on slide 5 (series names placed beside the stacked bars on purpose).

**Before and after.** Draft (`review.md`): 1 high, 18 medium, 11 low; story mean 2.8; verdict "needs a storyline rework". This deck: 0 high, 0 medium, 6 low; story mean 9.2 over slides 2-14; verdict ready.

**Verdict:** ready.
