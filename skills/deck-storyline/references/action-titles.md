# Action titles

An action title is the sentence at the top of a slide that states what the slide
proves. The reader should get the point from the title alone; the body is the proof.
Read in order, the titles of a deck tell its whole story.

Numbers in the examples below are illustrative, to show the form only.

## Contents

1. Rules
2. The so-what ladder
3. Length limits
4. Bad → good examples (by failure type)
5. Examples by deck type
6. Korean and Japanese examples
7. Slides that do not need an action title
8. Titles with missing data
9. The title-only test
10. Rewrite procedure

---

## 1. Rules

1. **A full sentence with a verb, stating a claim.** "Churn" is a label. "SMB churn
   doubled in Q3" is a claim.
2. **The takeaway, not the topic.** Ask "so what?" of the chart until you reach the
   point the reader must accept.
3. **One message per slide.** If the title needs "and" to join two unrelated claims,
   split the slide.
4. **Specific.** Name the subject, the direction, the size and the period when known:
   who/what, up/down/bigger/smaller, by how much, compared to what, when.
5. **Supported by the body.** Every number and every comparison in the title must
   be visible on the slide (chart, table, or source note). If the data is missing,
   the title says so with `[DATA NEEDED: …]` (section 8).
6. **Short enough to read in one glance.** Two lines at most at the template's
   title size, which is at least 24 pt in deck-build (section 3).
7. **Plain words, active voice.** Name the actor. No internal codenames, no
   unexplained acronyms, no filler ("It is important to note that…").
8. **Calibrated, not hedged.** State uncertainty once and precisely ("likely",
   "if X holds", "early data suggests"), never as a stack ("may potentially help").
9. **Consistent across the deck.** Same tense for the same kind of slide (past for
   results, present for current state, imperative or "should" for recommendations),
   same names for the same things, same units.
10. **No question titles** in a decision deck. The reader came for answers. (A
    question is fine on a section divider when the next slides answer it.)

## 2. The so-what ladder

Each rung adds meaning. Choose the rung that fits the slide's job: evidence slides
usually sit at rung 3; summary and recommendation slides at rung 4.

| Rung | What it adds | Example |
|---|---|---|
| 0. Topic | Nothing | Q3 revenue |
| 1. Fact | The number | Q3 revenue was $4.2M |
| 2. Comparison | Against plan, prior period, peer | Q3 revenue was $4.2M, 6% above plan |
| 3. Cause or meaning | Why, or what it shows | Mid-market expansion drove a 6% revenue beat in Q3 |
| 4. Implication / action | What to do | Mid-market expansion drove Q3's 6% beat, so we should double the expansion team |

Never stop at rung 0. Rung 1 is acceptable only on a pure data slide in an appendix.

## 3. Length limits

Two lines at the title size is the hard limit; one line is better.

| Language | Target | Hard cap |
|---|---|---|
| English | 10–16 words, 60–100 characters | 20 words, 120 characters |
| Korean | 25–50 characters | 60 characters |
| Japanese | 25–50 characters | 60 characters |

The exact limit depends on the template's title box and font. `deck-build` measures
the real fit; `deck-review` flags titles over two lines. If a title is too long, cut
the clause that the chart already shows, not the claim.

## 4. Bad → good examples

### 4.1 Topic labels

| Bad | Good |
|---|---|
| Market overview | Indonesia has more internet users than Vietnam and Thailand combined |
| Financial summary | Revenue grew 41% while the company turned its first full-year profit |
| Competitive landscape | Two incumbents hold most of the market, but neither offers a free tier |
| Customer feedback | Customers praise setup speed but cancel over missing integrations |
| Team | We have hired the three leaders the plan needs; only the CFO role is open |
| Roadmap | We will ship the three features that block mid-market deals before Q2 |
| Pricing analysis | A usage-based tier would recover the 30% of trials lost at the paywall |
| Risks | The largest risk is a single cloud vendor, and a second region removes most of it |
| Next steps | We need three decisions today: budget shift, hiring freeze exception, launch date |
| Unit economics | Each new customer pays back its acquisition cost in 11 months, down from 16 |

### 4.2 Facts with no implication

| Bad | Good |
|---|---|
| Revenue was $120M in FY2025 | Revenue reached $120M in FY2025, up 41%, the fastest growth in three years |
| NPS is 42 | NPS of 42 puts us ahead of the two closest competitors we benchmark |
| We have 1,200 customers | Customer count grew 30%, but most of the growth is in the lowest-paying tier |
| Churn was 3.1% in September | Monthly churn rose to 3.1%, the highest in six quarters, driven by SMB |
| Indonesia has 283M people | Indonesia's 206M internet users are 2.4 times Vietnam's, the largest online audience in the shortlist |

### 4.3 Vague

| Bad | Good |
|---|---|
| Performance improved significantly | Page load time fell from 3.2s to 1.1s after the CDN switch |
| Several challenges remain | Two issues block launch: payment-provider approval and a missing translation |
| The market is attractive | The market is large (12M target users) and still growing 15% a year |
| There are opportunities to optimize costs | Moving logs to cold storage cuts cloud cost by $40k a month |
| Results were mixed | Enterprise beat plan by 12% while SMB missed by 9% |

### 4.4 Too long or two messages

| Bad | Good |
|---|---|
| Revenue grew 41% and we also launched in five new countries while hiring 200 people and improving gross margin by 2 points | Revenue grew 41% while gross margin improved 2 points (split hiring and launches into their own slides) |
| Our analysis of the three candidate markets across seven criteria shows that, on balance and with some caveats regarding data quality, Market A is the most attractive | Market A scores highest on five of seven criteria |
| Customer support tickets increased and the response time also got worse, which led to more churn among enterprise accounts in Q3 | Slower support responses drove Q3 enterprise churn |

### 4.5 Hedged or weak verbs

| Bad | Good |
|---|---|
| We might potentially want to consider exploring a partnership | Partner with a local distributor to enter in six months instead of eighteen |
| The new feature could possibly help with retention | Users who adopt the new feature churn half as often in their first 90 days |
| There may be some correlation between onboarding and churn | Accounts that finish onboarding in week one churn at a third of the rate |
| It seems that pricing is an issue | Price is the top cancellation reason, cited by 41% of churned accounts |

### 4.6 Claims the slide cannot support

| Bad | Good |
|---|---|
| We will dominate the market by 2028 | We can reach 5% share by 2028 if the CAC test holds (chart shows the path) |
| Customers love the product | 82% of surveyed customers would be "very disappointed" without the product |
| Indonesia is the best market (chart shows only population) | Indonesia has the largest population of the four candidates (other slides prove the rest) |
| Competitors are falling behind | Our release cadence is twice that of the two main competitors over the last year |

### 4.7 Questions and teasers

| Bad | Good |
|---|---|
| Why is churn rising? | Churn is rising because new SMB accounts never finish setup |
| What should we do next? | Fund an onboarding team for two quarters, then decide on expansion |
| The surprising truth about our pipeline | Half of the pipeline value sits in five deals that have stalled for 60+ days |

### 4.8 Jargon, codenames, passive voice

| Bad | Good |
|---|---|
| Project Falcon KPIs trending green | The billing migration is on schedule and under budget |
| NRR delta driven by cohort mix shift | Net revenue retention fell because new customers are smaller and expand less |
| Mistakes were made in the forecast | The forecast missed because it assumed last year's renewal rate |
| A decision on headcount is required | The board needs to approve two hires before the Q4 plan can start |

## 5. Examples by deck type

The board, investor and market-entry chains are condensed from
`examples/storyline-tests/` (board: sample data; investor and market entry: public,
cited data). The business-case chain is illustrative.

**Board update (sample data)**
1. Q3 beat plan, but SMB churn puts year-end ARR $230k short; we propose moving two hires to onboarding
2. New ARR beat plan by 21% in Q3, the third straight quarter above plan
3. SMB churned ARR more than doubled since Q1 and now offsets a third of new bookings
4. Most SMB accounts that churned in Q3 never finished setup in their first 30 days
5. Shifting two Q4 sales hires to onboarding saves $110k a year and recovers about $82k of Q4 ARR
6. We ask the board to approve the swap and a revised year-end forecast of $11.85M

**Investor update (public company, FY2025)**
1. The company is trading 2026 bookings growth for user growth, so judge 2026 by daily users
2. Revenue grew 39% to $1.04B in 2025, the first year above $1B
3. User growth slowed in 2025: DAUs grew 30% after 51%, and MAUs 14% after 32%
4. 2026 guidance cuts bookings growth to 10-12% by giving up over $50M of bookings to grow free users
5. $360M of free cash flow and $1.04B in cash can fund the user bet and a $400M buyback
6. Judge 2026 by whether DAU growth re-accelerates above 2025's 30%, not by bookings growth

**Market entry**
1. Launch in Indonesia first, and let a six-week paid test confirm it before full spend
2. Indonesia has 206M internet users, 2.4 times Vietnam's and over 3 times Thailand's
3. Adjusted for income, Indonesia's online market is at least twice that of any other candidate
4. Vietnam is the best backup: the fastest-growing economy, but under half Indonesia's online audience
5. We cannot yet say if we can win: app spending, competition and acquisition cost are unknown
6. Approve the paid test now, and launch in Indonesia if acquisition cost meets our payback target

**Business case (illustrative)**
1. A $180k self-serve help center keeps response times flat without new hires
2. Ticket volume will outgrow the current team by March at today's growth rate
3. A third of tickets are repeat how-to questions that a help center can answer
4. The investment pays back in seven months on avoided hiring alone

## 6. Korean and Japanese examples

**Korean (한국어)** — use a full sentence ending in a plain declarative form
(`~했다`, `~다`) or a noun-ending claim (`~ 증가`) used consistently across the deck.
Plain declarative is clearer for claims.

| Bad | Good |
|---|---|
| 3분기 실적 | 3분기 매출은 계획을 6% 넘었지만 SMB 이탈이 연말 ARR을 위협한다 |
| 시장 현황 | 인도네시아의 인터넷 이용자는 후보 4개국 중 가장 많다 |
| 고객 이탈 분석 | 이탈한 SMB 고객 대부분은 가입 30일 안에 설정을 끝내지 못했다 |
| 향후 계획 | 영업 인력 2명을 온보딩으로 옮기면 연 11만 달러를 아끼고 4분기 ARR 약 8만 달러를 되찾는다 |
| 경쟁사 비교 | 주요 경쟁사 두 곳 모두 무료 요금제가 없다 |
| 비용 절감 방안 검토 | 로그를 콜드 스토리지로 옮기면 클라우드 비용이 월 4만 달러 줄어든다 |

**Japanese (日本語)** — prefer `~である` / `~した` style, or a consistent `~。`-less
claim style. Avoid ending on a bare noun.

| Bad | Good |
|---|---|
| 市場概要 | インドネシアのインターネット利用者は候補4か国で最も多い |
| 第3四半期の結果 | 第3四半期の売上は計画を6%上回ったが、SMBの解約が年末ARRを脅かしている |
| 今後の進め方 | 営業2名をオンボーディングに移せば年11万ドルを節約し、第4四半期のARRを約8万ドル取り戻せる |

## 7. Slides that do not need an action title

| Slide | Title |
|---|---|
| Cover | Deck name + audience + date. The governing message may appear as a subtitle |
| Agenda | "Agenda" is fine, but listing the key arguments as claims is better |
| Section divider | The key argument of that section, written as a claim |
| Appendix | A claim is still better; a descriptive label is acceptable |
| Thank-you / contact | Avoid. End on the decision or next steps slide instead |

## 8. Titles with missing data

If the claim depends on a number you do not have, keep the claim's shape and mark
the gap. Never fill it with a plausible-looking number.

- "Payback period fell to [DATA NEEDED: CAC payback, months, Q3] after the price change"
- Weak: "Indonesia's language-app spend is [DATA NEEDED: app-store category revenue], larger than Vietnam's"
  → better: state what you can prove now, and put the gap on the slide body:
  "Indonesia has the largest online audience; app-spending data is still missing"

A title containing `[DATA NEEDED]` passes the storyline stage but fails final
review. `deck-review` lists every one.

## 9. The title-only test

Read only the titles, in order, aloud or as a single paragraph. Then answer:

| # | Question | Pass |
|---|---|---|
| 1 | Can you state the governing message after reading only the titles? | It matches the one in storyline.md |
| 2 | Is every title a full-sentence claim (except cover/agenda/appendix)? | No topic labels |
| 3 | Does each title follow from the one before, with no jump the reader cannot make? | No "wait, where did that come from?" |
| 4 | Does each key argument appear, in the planned order? | Each one has at least one title stating it |
| 5 | Is anything said twice? | No two titles make the same claim |
| 6 | Does the deck end on what the reader must decide or do? | Last content title is the ask, decision or next step |
| 7 | Is every number in a title backed by evidence or marked `[DATA NEEDED]`? | No unsourced numbers |

Record the result in storyline.md: the titles as one paragraph, then pass/fail for
each question with one line of reasoning. Overall pass = 1, 2, 3, 6 and 7 pass;
4 and 5 may be warnings if explained.

`scripts/storyline_tool.py titles storyline.md` prints the titles as a paragraph and
flags labels, length and unmarked numbers. It cannot judge whether the story holds;
you do that.

## 10. Rewrite procedure

For each weak title:

1. Look at the exhibit. Say, in one breath, what it shows a busy reader.
2. Climb the so-what ladder one rung (section 2).
3. Name the subject and the comparison. Add the number if you have it.
4. Cut words until it fits two lines. Remove clauses the chart already shows.
5. Check that the body proves it. If it does not, change the title or the body.
6. Read it after the previous title. If the chain breaks, fix the order or add a
   bridging slide.
