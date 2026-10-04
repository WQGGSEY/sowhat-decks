---
name: deck-storyline
description: Plans an answer-first storyline for a business presentation before any slide is designed. Turns a purpose, audience, decision and raw material (notes, data, documents) into one governing message, SCQA, 3-5 non-overlapping key arguments, and a full-sentence action title per slide with the evidence and exhibit it needs, marks missing evidence as [DATA NEEDED], runs the "read only the titles" test, and writes storyline.md plus a title-only ghost deck spec that deck-build renders to .pptx. Use when the user asks for a storyline, deck outline, presentation structure, slide titles, executive summary, board update, investor update, QBR, pitch, recommendation or market-entry deck, or asks "what should my slides say" or "how should I structure this deck" (also 스토리라인, 장표 구성, 발표 목차, ストーリーライン, 構成案).
---

# deck-storyline

Decide what the deck argues before deciding what it looks like. The output is a
storyline a senior reader would accept from the titles alone, with every claim tied
to evidence or to an explicit gap.

Part of SoWhat Decks: `deck-storyline` → `deck-build` (+ `deck-exhibits`) → `deck-review`.

## Inputs (the brief)

| Field | Ask or infer |
|---|---|
| Purpose | What must this deck achieve? |
| Audience | Who reads it, what do they know, what do they care about? |
| Decision | What should they decide or do? Phrase it as a question. |
| Raw material | Notes, data files, documents, links the user provides |
| Constraints | Length, date, language (en/ko/ja), template, real vs sample data |

If the decision is unknown, ask once — it drives everything. For anything else
missing, make a reasonable assumption and write it under `Assumptions:` in the brief.

## Outputs

1. `storyline.md` — from [templates/storyline.md](templates/storyline.md). Keep its
   headings and `- Field:` labels; the script reads them.
2. `ghost.json` — a title-only ghost deck spec for deck-build (spec 1.0; every
   content slide uses the `ghost` layout).
3. Optional: `ghost.pptx` / PDF / PNGs rendered by deck-build.

## Workflow

Copy this checklist and tick it off:

```
- [ ] 1 Brief written (purpose, audience, decision, assumptions)
- [ ] 2 Evidence ledger built; every fact tagged; gaps marked [DATA NEEDED]
- [ ] 3 Governing message: one sentence that answers the decision
- [ ] 4 SCQA written; Answer = governing message
- [ ] 5 3-5 key arguments; split and overlap/gap check recorded
- [ ] 6 Slide plan: action title + role + layout + exhibit + evidence + gaps per slide
- [ ] 7 Title-only test recorded with PASS/FAIL per check
- [ ] 8 Ghost deck spec written (and rendered, if deck-build is available)
```

**1. Brief.** Fill section 0 of the template. Restate the decision as the
audience would ask it.

**2. Evidence first.** Read all raw material. List every usable fact in the evidence
ledger with unit, period and tag (`SRC n`, `USER`, `CALC`, `SAMPLE`, `ASSUMPTION`,
`HYPOTHESIS`). Write formulas for derived numbers and recheck the arithmetic.
Anything the story needs but the material lacks becomes
`[DATA NEEDED: what, unit, period, from where; owner]`.
See [references/evidence.md](references/evidence.md).

**3. Governing message.** One sentence, under ~30 words, that answers the decision
question and contains the so-what. If you cannot write it, the analysis is not
done: state a hypothesis and mark it `[HYPOTHESIS]`.
See [references/answer-first.md](references/answer-first.md).

**4. SCQA.** Situation (agreed context), Complication (what forces a decision now),
Question (the audience's), Answer (the governing message). Default slide order is
answer-first. See [references/scqa.md](references/scqa.md).

**5. Key arguments.** 3-5 full-sentence claims that, if accepted, force the
governing message. Pick a complete split (e.g. attractiveness / ability to win /
cost and risk; results / drivers / outlook / asks). Record the overlap check and
which objection each argument answers.

**6. Slide plan.** One block per slide, in order: cover → executive summary (title
= governing message, compressed to two lines if needed) → a group of slides per key
argument (claim first, then proof; optionally opened by a `section` slide) →
recommendation or decision/next steps → appendix. For each slide:
- an action title: a full sentence stating the takeaway, 10-16 words
  (Korean/Japanese 25-50 characters), max two lines;
- the deck-build layout and the exhibit (type — measure, breakdown, period);
- evidence IDs from the ledger, and every gap as `[DATA NEEDED: …]`;
- optional `Tracker:` (short section label shown above the title) and, on the
  cover, `Subtitle:`.
See [references/action-titles.md](references/action-titles.md) for rules and
many good/bad examples.

**7. Title-only test.** Read only the titles, in order, as one paragraph. Answer
the seven checks (action-titles.md, section 9): governing message recoverable,
every title a claim, no jumps, each key argument present, nothing repeated, ends on
the ask, every number backed or marked. Record PASS/FAIL with one line of
reasoning each. If it fails, fix titles or order and rerun before going on.

**8. Ghost deck.** Write the ghost spec and, if deck-build is installed, render it.
Open the PNGs and read the titles once more as a reader would.

## Script mode (any agent that can run Python, such as Claude Code)

The helper uses only the Python standard library and makes no network calls.

```bash
S=<path to this skill>/scripts/storyline_tool.py
python3 $S titles storyline.md            # title paragraph + per-title lint
python3 $S check  storyline.md            # structure, evidence links, gaps; exit 1 on errors
python3 $S ghost  storyline.md -o ghost.json
```

Then render with deck-build (see its SKILL.md for options):

```bash
python3 <deck-build>/scripts/build.py ghost.json -o out/ --name ghost
# -> out/ghost.pptx, out/ghost.pdf, out/preview/slide-NN.png (PDF/PNG need LibreOffice)
```

- `titles` cannot judge whether the story holds; it only flags labels, questions,
  length, hedges, numbers without evidence, and near-duplicate titles. You still
  answer the seven checks yourself.
- `ghost` puts the key arguments on the executive summary slide and, on every
  other content slide, the action title plus a dashed box with the planned layout,
  exhibit and evidence (gaps prefixed `[DATA NEEDED]`). `--pure` makes the summary
  title-only too. Data status `sample` turns on the "Sample data" footer.
- Fix every `ERROR` from `check` before handing off. Warnings need a reason.
- When the storyline is accepted, deck-build turns the same slide plan into a full
  spec: keep each title and swap the ghost slide for its planned layout.

## No-code mode (chat, Claude for PowerPoint sidebar)

Same method, no files or scripts. Designed for chat and the Claude for PowerPoint sidebar; not yet tested in Claude for PowerPoint.

- **Plain chat:** reply with the storyline in the template's order: brief,
  governing message, SCQA, key arguments, slide plan (numbered titles, each with
  exhibit, evidence and gaps), the title-only paragraph with the seven checks, and
  the open data requests. Keep `[DATA NEEDED]` markers verbatim.
- **Inside PowerPoint:** create one slide per planned slide using the title-only
  layout. Put the action title in the title placeholder. Put the planned exhibit and
  evidence (including `[DATA NEEDED]` items) in the speaker notes or in a text box
  labelled "Planned exhibit". Put the governing message in the executive summary
  title and the key arguments as its bullets.
- Run the title-only test on the slide titles alone (desktop PowerPoint's Outline
  View shows them; in the sidebar, list the titles in order) and report the seven
  checks in the chat.
- Never type a number into a slide that is not in the user's material or a cited
  source.

## Hard rules

- **Never invent numbers**, including "remembered" figures. Fetch and cite, use the
  user's data, or write `[DATA NEEDED: …]`.
- Sample data is tagged `SAMPLE` in the ledger and labelled "Sample data" in the deck.
- Every content title is a full-sentence claim. Labels like "Market overview" fail.
- One message per slide. The body must prove the title.
- The answer comes first: the executive summary title is the governing message.
- 3-5 key arguments, no overlap, no obvious objection left unanswered.
- End the main deck on the decision, ask or next steps — not "Thank you".

## Example (short)

Brief: board update, SaaS company, decision "approve moving two planned sales hires
to onboarding?" (sample data).

- Governing message: "Q3 beat plan, but rising SMB churn now puts year-end ARR about
  $230k short; moving two planned sales hires to onboarding cuts that gap by about a
  third and fixes the cause."
- Key arguments: (1) new business is healthy and beat plan; (2) SMB churn is now the
  binding constraint; (3) the churn comes from accounts that never finish setup;
  (4) moving two hires to onboarding attacks the cause and costs less.
- Open gap kept visible: `[DATA NEEDED: 2027 new-ARR capacity with 2 vs 4 Q4 AE
  hires, from Sales capacity model; owner: VP Sales]`.
- Title chain ends on: "We ask the board to approve the swap and a revised year-end
  forecast of $11.85M."

Full worked examples with inputs, storyline, ghost spec and rendered decks:
`examples/storyline-tests/` in the SoWhat Decks repository.

## References

- [references/answer-first.md](references/answer-first.md) — governing message, key arguments, overlap/gap test, ordering, deck types
- [references/scqa.md](references/scqa.md) — situation, complication, question, answer; variants and examples
- [references/action-titles.md](references/action-titles.md) — title rules, so-what ladder, length limits, good/bad examples (en/ko/ja), the title-only test
- [references/evidence.md](references/evidence.md) — what counts as support, tags, ledger, gap markers, number hygiene, sample data
- [templates/storyline.md](templates/storyline.md) — the storyline.md template
