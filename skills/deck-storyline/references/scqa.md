# SCQA: the opening that earns attention

SCQA is a four-part opening that gets the reader from "what we both already know" to
"the answer" in a few sentences. It is the spine of the executive summary and the
first two or three slides.

- **Situation** — the stable, agreed context. Nothing the reader would dispute.
- **Complication** — what changed, or the tension in the situation, that makes a
  decision necessary now.
- **Question** — the question the complication raises in the reader's mind.
  Usually it is the decision question from the brief.
- **Answer** — the governing message.

The point of S and C is not background for its own sake. They exist so that when the
reader reaches the answer, they already feel the question it answers.

## Contents

1. Writing each part
2. Order variants
3. Examples by deck type
4. Where SCQA goes in the deck
5. Failures and fixes

---

## 1. Writing each part

**Situation (1–2 sentences)**
- State facts the audience already accepts. If they would argue with it, it is not
  situation; it belongs in the complication or the arguments.
- Keep it short. Readers skim this part; every extra sentence delays the answer.
- Good: "We sell analytics software to SMB and mid-market teams; ARR grew steadily
  through the first half."
- Bad: "Founded in 2019, the company has a mission to democratize data…" (history,
  not the context for this decision).

**Complication (1–2 sentences)**
- Something changed, something is at risk, or something is newly possible.
- It must be specific enough that the decision follows from it. "Things are
  challenging" is not a complication. "SMB logo churn doubled in Q3" is.
- Good complications: a threat, an opportunity, a gap between plan and actual, a
  new constraint, a choice that can no longer be put off.

**Question (1 sentence, often implicit)**
- Phrase it the way the reader would ask it: "What should we do about it?", "Which
  market first?", "Do we still hit the plan?"
- If the question you write is not the decision in the brief, one of S, C or the
  brief is wrong. Fix that before going on.
- In the deck you often leave Q unstated; the reader asks it in their head. In
  storyline.md always write it down.

**Answer (1 sentence)**
- The governing message. See `answer-first.md`.

## 2. Order variants

The full order (S → C → Q → A) builds tension and suits readers who need context
first. For senior or busy readers, lead with the answer:

| Variant | Order | Use when |
|---|---|---|
| Standard | S → C → (Q) → A | Reader needs to be brought into the problem; new audience |
| Answer-first | A → S → C | Reader knows the context; boards, executives, investors who asked for the update |
| Concern-first | C → S → A | The complication is urgent and the reader already feels it |
| Question-first | Q → S → C → A | The reader asked a specific question; you are replying to it |

Answer-first is the default for this skill. The title of the executive summary is
always the answer, whatever order the body text uses.

## 3. Examples by deck type

The board example uses sample data; the investor and market-entry examples are
condensed from the worked examples in `examples/storyline-tests/` (public sources
cited there). The business-case and status examples are illustrative.

**Board update (sample data)**
- S: The board approved a plan of $12.0M ARR by year end, and new bookings have beaten
  plan every quarter this year.
- C: SMB churn more than doubled since Q1; if the trend continues, year-end ARR lands
  about $230k below plan.
- Q: Will we hit plan, and what should the board approve now?
- A: Not fully; approve moving two Q4 sales hires to onboarding, which recovers about a
  third of the gap this year and removes the cause for 2027.

**Investor update (public company, annual results)**
- S: Investors backed the company to keep growing users and turn that growth into
  profit; in 2025 it passed $1B in revenue with wider margins.
- C: User growth slowed sharply, and 2026 guidance cuts bookings growth to 10-12% and
  the adjusted EBITDA margin to 25%.
- Q: Is the 2026 slowdown a warning sign or a choice, and how should we judge it?
- A: A stated choice to give up near-term bookings and margin for user growth, funded
  by strong cash flow, so judge 2026 by whether daily-user growth re-accelerates.

**Market entry**
- S: Our app is profitable at home and we can fund one new-market launch team in the
  next 12 months.
- C: The four candidate markets differ widely in online audience, income and growth,
  and we can only launch one.
- Q: Which market first?
- A: Indonesia, the largest online market even after adjusting for income, confirmed
  by a six-week paid test before the full budget is committed.

**Business case (illustrative)**
- S: Support handles a steady monthly ticket volume with a fixed team.
- C: Volume grows every month while hiring is frozen.
- Q: How do we keep response times without new hires?
- A: Fund a self-serve help center and triage bot, sized to deflect the repeat
  how-to questions that make up [DATA NEEDED: share of repeat tickets, from the
  helpdesk export].

**Project status (illustrative)**
- S: The billing migration is in month four of six.
- C: Data validation found mismatched invoices, and the vendor cannot fix them before
  the cutover date.
- Q: Do we keep the date?
- A: Move cutover by three weeks; a later date costs less than billing errors at
  this rate.

## 4. Where SCQA goes in the deck

| Slide | What it carries |
|---|---|
| Executive summary (slide 2) | Title = A. Body = S and C in one or two lines each, then the key arguments as bullets |
| Optional context slide | When C needs a chart to be believed (e.g., the churn curve), give it its own slide with an action title stating the complication |
| Closing slide | Restate A as the decision or next steps; the reader leaves on the answer |

In storyline.md, write SCQA as four labeled lines. The ghost deck puts A in the
executive summary title and S + C in its body.

## 5. Failures and fixes

| Failure | Example | Fix |
|---|---|---|
| Situation that argues | "Our product is the best in the market" | Move to arguments with evidence, or cut |
| Complication with no tension | "We have several options" | Name what forces a choice now: deadline, budget, threat |
| Question nobody asked | "How can we leverage synergies?" | Use the reader's words and the brief's decision |
| Answer that restates the question | "We need to decide on a market" | Give the choice: "Enter Indonesia first" |
| SCQA longer than the deck | Five paragraphs of context | One or two sentences per part; details go to slides |
| C and A disconnected | C is about churn, A is about a new product | A must resolve C; otherwise rewrite one of them |
