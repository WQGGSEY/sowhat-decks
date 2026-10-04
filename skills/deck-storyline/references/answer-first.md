# Answer-first structure

A decision deck exists to move one reader to one decision. The fastest way to do
that is to state the answer first and then prove it, top-down. This file covers how
to find the answer (the governing message), how to break it into 3–5 key arguments
that do not overlap and leave nothing out, and how to order everything underneath.

## Contents

1. The shape: one message, a few arguments, evidence underneath
2. Writing the governing message
3. Choosing the key arguments
4. The overlap-and-gap test (MECE)
5. Ordering arguments and slides
6. Deck types and what "the answer" means for each
7. Common failures and fixes
8. Worked example

---

## 1. The shape

```
                Governing message (1 sentence)
               /            |              \
     Key argument 1   Key argument 2   Key argument 3      (3–5, each a claim)
        /    \            /    \            /    \
   slide   slide     slide   slide     slide   slide        (action titles)
     |       |         |       |         |       |
  evidence evidence  evidence ...                           (data, facts, quotes)
```

Three rules hold the shape together:

- **Each level summarizes the level below.** The governing message is what you get
  when you compress the key arguments. A key argument is what you get when you
  compress its slides. If a slide does not support its argument, it moves or goes.
- **Each level answers the question the level above raises.** A reader who hears the
  governing message asks "why?" or "how?" or "what makes you sure?". The key
  arguments answer exactly that question, and nothing else.
- **Items in one group are the same kind of thing.** All reasons, or all steps, or all
  options, or all segments. Not two reasons and a timeline.

## 2. Writing the governing message

The governing message is the one sentence you would say if the meeting were cut to
thirty seconds. It answers the decision question directly.

**Procedure**

1. Write the decision question in the reader's words: "Which market should we
   launch first?", "Are we on track for the plan, and what do you need from us?"
2. Write the answer as one sentence that a yes/no or a choice could be read from.
3. Add the single most important reason or condition ("because …", "if …").
4. Cut until it is under ~30 words (English) or ~60 characters per line in CJK.

**Tests**

| Test | Pass looks like |
|---|---|
| Answers the question | A reader can say what you want them to decide |
| Could be disagreed with | Someone could reasonably argue the opposite |
| Says "so what" | Contains an implication, not only a fact |
| Stands alone | Makes sense to someone who has not seen the data |
| Matches the evidence | Every word in it is supported by at least one slide |

**Weak → strong** (numbers in examples are illustrative, to show the form only)

| Weak (topic or fact) | Strong (answer) |
|---|---|
| Q3 business review | Q3 revenue beat plan by 6%, but SMB churn will erase that gain by Q1 unless we fund onboarding now |
| Market entry options in Southeast Asia | Launch in Indonesia first: it has the largest online audience of the four markets, even after adjusting for income |
| Our results this year | We grew revenue 41% while turning profitable, and we will keep investing in AI features rather than buy back stock |
| Customer research findings | Mid-market buyers drop out at security review, so a SOC 2 report is worth more than the next three features |

If you cannot write the governing message yet, you do not have a storyline yet. Go
back to the raw material and look for what changed, what is surprising, or what
must be decided. Draft a hypothesis anyway and mark it `[HYPOTHESIS]` — a wrong
answer stated clearly is easier to fix than a vague one.

## 3. Choosing the key arguments

Key arguments are the 3–5 claims that, if the reader accepts all of them, force the
governing message. Two ways to build them:

**Grouping (inductive):** several parallel reasons or findings that each point to the
same conclusion.
- "Launch in Indonesia first" ← (1) biggest reachable audience, (2) still the biggest
  after adjusting for income, (3) the runner-up is clearly smaller, (4) the open
  questions can be tested cheaply.
- Use this for most business decks. It is robust: if one argument falls, the others
  still stand.

**Chain (deductive):** a sequence where each step leads to the next.
- "Fund onboarding now" ← (1) growth now depends on keeping SMB accounts, (2) SMB
  accounts churn in the first 90 days, (3) the churn is caused by failed setup,
  (4) therefore an onboarding team fixes the binding constraint.
- Use it when the reader needs to follow a cause. It is fragile: if one link breaks,
  the conclusion falls. Keep chains short (3–4 links) and put the strongest evidence
  on the weakest link.

**Phrasing:** every key argument is itself a full-sentence claim, not a label.
"Market size" is a label. "Indonesia has the most internet users of the four
candidates" is a claim.

**How many:** three is the default. Five is the ceiling. If you have seven, two of
them are the same thing, or some are evidence for others. Merge or demote.

## 4. The overlap-and-gap test (MECE)

"Mutually exclusive, collectively exhaustive" means the arguments do not overlap
and, together, cover everything the reader needs to accept the answer.

**Overlap check (mutually exclusive)**
- For each pair of arguments, ask: could the same slide sit under both? If yes, they
  overlap. Redraw the line between them.
- Typical overlap: "Customers love the product" and "Retention is strong" — retention
  is evidence of the first. Merge or make one about a different dimension.

**Gap check (collectively exhaustive)**
- Ask the reader's hardest question: "What would make this answer wrong?" Each
  credible objection must be answered by some argument.
- Use a known complete split when one exists:
  - money: revenue vs cost; price × volume
  - customers: acquire, keep, expand
  - time: past, present, future
  - market choice: attractiveness vs our ability to win vs cost/risk of entry
  - plan: what, who, when, how much
  - business health: growth, efficiency, risk
- If no complete split exists, list the objections the audience will raise and make
  sure each one is covered.

**Write the test down.** In storyline.md, record one line per check: the split you
used, and which objection each argument answers. Reviewers look for it.

## 5. Ordering

Order key arguments by one principle and say which:

| Principle | Use when | Example |
|---|---|---|
| Importance | Recommendations, parallel reasons | Strongest reason first |
| Time | Updates, plans, histories | What happened → where we are → what's next |
| Structure | Breakdowns of a whole | Acquire → keep → expand |
| Logic chain | Deductive arguments | Cause → effect → action |

Inside an argument, order slides the same way: the claim slide first, then the
supporting slides. End the deck with what the reader must do or decide.

The executive summary slide (slide 2 in most decks) restates the governing message
as its title and lists the key arguments as its body. If the summary slide is all a
busy reader sees, they should still get the answer.

## 6. Deck types

| Deck type | Decision question | Governing message form | Typical key-argument split |
|---|---|---|---|
| Recommendation | "What should we do?" | "Do X, because Y" | Why act → why this option → how → risks |
| Board update | "Are we on track, and what do you need?" | "We are [ahead/behind] on [plan] because [driver]; we need [decision]" | Results → drivers → outlook → asks |
| Investor update | "Is this still a good bet?" | "We [did X] and [proved Y], so [outlook]" | Growth → efficiency → strategy → outlook |
| Market entry | "Should we enter, where, and how?" | "Enter [market] first via [mode]" | Attractiveness → ability to win → entry cost/risk → plan |
| Business case | "Should we fund this?" | "Invest [amount] in X to get [return] by [date]" | Problem cost → solution → return → risk |
| Status / steering | "Is the project OK, and what is blocked?" | "On track for [milestone], except [blocker] needing [decision]" | Progress → issues → decisions needed |
| Post-mortem | "What went wrong, and what changes?" | "[Event] happened because [cause]; [change] prevents a repeat" | What happened → why → what changes |

An "information only" deck still has an answer: what the reader should believe or
remember after reading it. If even that is missing, consider sending a memo instead.

## 7. Common failures

| Failure | Symptom | Fix |
|---|---|---|
| Topic deck | Titles are nouns: "Market", "Competition", "Financials" | Ask "so what?" of each section until you get a claim |
| Buried answer | The recommendation appears on the last slide | Move it to slide 2 and the opening of the summary |
| Story of the work | Slides follow the order you did the analysis | Reorder by the reader's question, not your process |
| Kitchen sink | 8+ key arguments, every finding gets a slide | Keep the arguments that change the decision; move the rest to the appendix |
| Overlapping arguments | Same evidence used twice | Redraw boundaries using a complete split (section 4) |
| Missing objection | The obvious "but what about …?" has no slide | Add an argument or a risk slide answering it |
| Unsupported top | The governing message contains a number no slide shows | Add the evidence or soften the claim |
| Hedged answer | "We could consider possibly exploring…" | Commit, then state the condition: "Do X if Y holds" |

## 8. Worked example

This is a condensed version of `examples/storyline-tests/02-market-entry` in the
SoWhat Decks repository (hypothetical company, real World Bank statistics).

**Brief:** Head of growth at a subscription language-learning app, deciding which of
four Southeast Asian markets to launch first. Audience: CEO and CFO. Material: public
population, internet-use and income statistics; no internal test data yet.

**Governing message:** "Launch in Indonesia first: it has 2.4 times Vietnam's online
audience at similar income per person, but a six-week paid test should confirm we
can win before the full budget is committed."

**Key arguments (split: reach / value after income / best alternative / ability to
win):**
1. Indonesia is the largest reachable market (internet users × population data).
2. Adjusted for income, it is still at least twice any other candidate.
3. Vietnam is the best backup: fastest-growing economy, but under half the audience.
4. Whether we can win is unproven: [DATA NEEDED: app spending, competitor map,
   cost per paying subscriber, payment methods, local rules].

**What the method caught:** a first draft favoured Vietnam because its economy grows
fastest. The evidence ledger showed Indonesia added four times as many internet
users since 2019 and stays far ahead after the income adjustment, so the answer
changed. Argument 4 has no public evidence at all; instead of filling it with a
guessed acquisition cost, the storyline turns it into a test and a decision rule.
