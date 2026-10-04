# 03 Review before and after: a Q3 board update

A draft board deck with planted problems, the deck-review report on it, and the deck rebuilt with the skills. Same company, same figures: **Sample Co. is fictional and every number is sample data.**

| | Draft (`before/before.pptx`) | Rebuilt (`deck.pptx`) |
|---|---|---|
| deck-review findings | 1 high, 18 medium, 11 low | 0 high, 0 medium, 0 low |
| Mechanical score | 7.5 / 10 | 9.6 / 10 |
| Story score (rubric, mean) | 2.8 / 10 | 9.2 / 10 |
| Verdict | needs a storyline rework | ready |
| Report | [review.md](review.md) | [after-review.md](after-review.md) |
| PDF | [before-review/render/before.pdf](before-review/render/before.pdf) | [deck.pdf](deck.pdf) |

The draft's problems were planted on purpose by [`before/make_before.py`](before/make_before.py): topic-label titles, charts pasted as pictures, 8-11 pt text, no source lines and a "TBD" forecast. It is a constructed test case, not the output of any particular tool.

## Read only the titles

| Draft | Rebuilt |
|---|---|
| Executive summary | Q3 beat plan, but SMB churn puts year-end ARR $230k short; we propose moving two hires to onboarding |
| Bookings performance | New ARR beat plan by 21% in Q3, the third straight quarter above plan |
| Q3 ARR bridge | Ending ARR of $11.05M beat plan by 1.4%, a smaller margin than new ARR because churn rose |
| Churn by segment | SMB churned ARR more than doubled since Q1 and now offsets a third of new bookings |
| Q4 outlook | If the SMB trend continues, year-end ARR lands about $230k below the $12.0M plan |
| Setup status of churned accounts | Most SMB accounts that churned in Q3 never finished setup in their first 30 days |
| Churn by setup status | Accounts that finish setup churn at about a fifth of the rate of those that do not |
| Onboarding capacity | Setup completion fell from 68% to 55% as new accounts per specialist rose 41% |
| Proposal: hiring plan changes | Shifting two Q4 sales hires to onboarding saves $110k a year and recovers about $82k of Q4 ARR |
| Risks | The cost is slower sales capacity in 2027, which Sales has not yet sized |
| Next steps | We ask the board to approve the swap and a revised year-end forecast of $11.85M |
| Cash runway | Cash runway stays near 22 months at the current $650k monthly burn |

## Files

| File | What it is |
|---|---|
| [brief.md](brief.md), [inputs/](inputs/) | The brief and the sample data |
| [before/](before/) | `make_before.py` and the draft it writes, `before.pptx` |
| [before-review/](before-review/) | What deck-review wrote for the draft: `annotated/` (problems boxed), `render/` (PDF and slide images), `before.fixed.pptx` (safe fixes only: text raised to the size floors, `Source: [SOURCE NEEDED]` lines added), `review.json` |
| [review.md](review.md) | The review of the draft, with the agent's rubric pass: re-ranked fixes, rewritten titles, story scores |
| [storyline.md](storyline.md) | The storyline for the rebuilt deck (deck-storyline) |
| [deck.json](deck.json), [deck.pptx](deck.pptx), [deck.pdf](deck.pdf), [preview/](preview/) | The rebuilt deck and its slide images |
| [after-review.md](after-review.md) | The review of the rebuilt deck |
| [SOURCES.md](SOURCES.md) | What the sample data files hold |

## Prompts and commands

Claude Code agents built this example during development, following the skills in this repo. The prompts restate what each step was asked to do, in the form you would type them; rerunning them gives similar but not identical wording. The commands, run from the repository root, produce the committed files.

**1. Make the draft** (no agent; a script plants the problems)

```bash
python3 examples/03-review-before-after/before/make_before.py
```

**2. Review the draft**

> Use deck-review on examples/03-review-before-after/before/before.pptx. Give me the five fixes that matter most.

```bash
python3 skills/deck-review/scripts/review.py run examples/03-review-before-after/before/before.pptx --out examples/03-review-before-after/before-review
```

The script writes `review.md` into `before-review/`; the agent then fills in the rubric sections. The completed report is [review.md](review.md).

**3. Plan the storyline**

> Use deck-storyline to plan a 12-15 slide Q3 board update from examples/03-review-before-after/brief.md and the files in examples/03-review-before-after/inputs/. The decision we need: approve moving two Q4 sales hires to onboarding, and accept a revised year-end ARR forecast. Every number is sample data; say so on every slide.

```bash
python3 skills/deck-storyline/scripts/storyline_tool.py check examples/03-review-before-after/storyline.md
python3 skills/deck-storyline/scripts/storyline_tool.py titles examples/03-review-before-after/storyline.md
```

**4. Build and review the deck**

> Use deck-build and deck-exhibits to turn examples/03-review-before-after/storyline.md into deck.json and build it in examples/03-review-before-after/. Look at every preview image and fix what looks wrong. Then run deck-review on deck.pptx and fix anything high or medium.

```bash
python3 skills/deck-build/scripts/build.py examples/03-review-before-after/deck.json -o examples/03-review-before-after
python3 skills/deck-review/scripts/review.py run examples/03-review-before-after/deck.pptx --no-fix --no-render
```

Images in `preview/` and `before-review/` were scaled from 1600 px to 960 px to keep the repository small.

## What the review did not catch

- deck-review's title check flagged 11 of the 12 label titles; "Setup status of churned accounts" passed the script and was caught in the agent's title-only read.
- The chart-as-picture check looks for dark axis lines. The draft's charts use black axes (an older spreadsheet default); a pasted chart with light grey axes and no "chart" in its name may not be flagged. The title-only read and the missing-source check still apply.
