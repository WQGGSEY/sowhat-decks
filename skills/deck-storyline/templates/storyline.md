# Storyline: <deck name>

<!--
deck-storyline template v1.
Keep the section headings and the "- Field:" labels exactly as written:
scripts/storyline_tool.py reads them to print the title-only test and to build
the ghost deck spec. Replace every <...>. Delete these comments when done.
-->

## 0. Brief

- Purpose: <what this deck must achieve, one line>
- Audience: <who reads it; what they already know; what they care about>
- Decision: <the decision or action wanted from the audience, phrased as a question>
- Deck type: <recommendation | board update | investor update | market entry | business case | status | other>
- Presenter: <name or role>
- Date: <YYYY-MM-DD>
- Language: <en | ko | ja | ...>
- Length: <n main slides + appendix>
- Data status: <real (sourced) | user-provided | sample | mixed>
- Assumptions: <anything you assumed because the brief did not say; "none">

## 1. Governing message

> <One sentence that answers the decision question. Under ~30 words.>

## 2. SCQA

- Situation: <stable context the audience accepts>
- Complication: <what changed / the tension that forces a decision now>
- Question: <the question the audience now asks — normally the brief's decision>
- Answer: <the governing message, same as section 1>
- Order on slides: <answer-first | standard | concern-first | question-first>

## 3. Key arguments

- Split: <the complete split used, e.g. attractiveness / ability to win / cost & risk>
- Order: <importance | time | structure | logic chain>

1. <Key argument 1 as a full-sentence claim> — answers: "<objection or question it settles>"
2. <Key argument 2> — answers: "<...>"
3. <Key argument 3> — answers: "<...>"

MECE check:
- Overlap: <which pairs you checked and how you separated them>
- Gaps: <the hardest objection and which argument answers it; anything left open>

## 4. Slide plan

<!--
One "### n. <action title>" block per slide, in deck order.
Role: cover | summary | section | evidence | recommendation | next-steps | appendix
Argument: the key-argument number this slide supports (0 = whole deck)
Layout: a deck-build layout name (see deck-build/references/layouts.md)
Exhibit: <exhibit type> — <what it shows: measure, breakdown, period>
Evidence: ledger IDs (E1, E2) with tags, or "none"
Gaps: [DATA NEEDED: ...] or "none"
Optional: Tracker: <short section label above the title>; Subtitle: <cover only>
-->

### 1. <Deck title or governing message for the cover>
- Role: cover
- Argument: 0
- Layout: cover
- Exhibit: none
- Evidence: none
- Gaps: none
- Notes: <subtitle: audience · date · "Draft">

### 2. <Governing message as the executive summary title (shorten to two lines if needed)>
- Role: summary
- Argument: 0
- Layout: executive_summary
- Exhibit: none — S, C and the key arguments as bullets
- Evidence: <IDs>
- Gaps: <none | [DATA NEEDED: ...]>
- Notes: <what the presenter says>

### 3. <Action title: a full-sentence claim>
- Role: evidence
- Argument: 1
- Layout: <exhibit | exhibit_takeaways | table | two_column | pillars | timeline | ...>
- Exhibit: <bar | line | stacked bar | table | 2x2 | process | ...> — <what it shows>
- Evidence: <E1 [SRC 1], E3 [CALC]>
- Gaps: <none | [DATA NEEDED: what, unit, period, from where; owner]>
- Notes: <the one thing the presenter should say>

<!-- ...more slides... end with the recommendation / decision / next steps slide, then appendix -->

## 5. Title-only test

Titles in order, read as one paragraph:

> <Title 1.> <Title 2.> <Title 3.> ...

| # | Check | Result | Reasoning |
|---|---|---|---|
| 1 | Governing message recoverable from titles alone | PASS/FAIL | <one line> |
| 2 | Every content title is a full-sentence claim | PASS/FAIL | <one line> |
| 3 | Each title follows from the previous, no jumps | PASS/FAIL | <one line> |
| 4 | Every key argument appears, in order | PASS/WARN/FAIL | <one line> |
| 5 | No claim repeated | PASS/WARN/FAIL | <one line> |
| 6 | Ends on the decision / ask / next step | PASS/FAIL | <one line> |
| 7 | Every number in a title is in the ledger or marked [DATA NEEDED] | PASS/FAIL | <one line> |

Overall: <PASS | FAIL> — <one line>

## 6. Evidence ledger

| ID | Fact (unit, period, scope) | Tag | Source / formula | Slides |
|---|---|---|---|---|
| E1 | <fact> | SRC 1 | <document, page/table> | <n> |
| E2 | <derived fact> | CALC | <formula using E-IDs> | <n> |

## 7. Open data requests

- [DATA NEEDED: <what, unit, period, from where; owner>] — slide <n>

## 8. Sources

1. <Publisher>, <title>, <URL or file path>, retrieved <YYYY-MM-DD>, <page/table/series>.
