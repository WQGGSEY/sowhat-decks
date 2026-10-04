# Evidence: what counts, how to label it, how to mark gaps

A storyline is only as strong as the evidence under each title. This file defines
what counts as support, how to tag every fact with where it came from, and how to
mark what is missing. The one rule that overrides everything else:

> **Never invent a number.** Not a plausible one, not a rounded one, not a
> "placeholder" that looks real. If you do not have it, write `[DATA NEEDED: …]`.

This includes numbers you "remember" from training data. A figure recalled from
memory is not a source. Either fetch and cite it, or mark it as needed.

## Contents

1. What counts as support
2. Evidence tags
3. The evidence ledger
4. Marking gaps
5. Numbers: hygiene rules
6. Sample data
7. How strong is strong enough
8. Checks before hand-off

---

## 1. What counts as support

| Type | Counts when | Example |
|---|---|---|
| Sourced data | The source is named, dated and findable (URL, file, report and page) | "Revenue $748.0M, FY2024, Form 10-K, income statement" |
| User-provided data | It came in the brief or files the user gave you; cite the file | "ARR by month, `inputs/metrics.csv`" |
| Calculation | Inputs are themselves supported and the formula is written down | "Growth = 748.0 / 531.1 − 1 = 40.8%" |
| Direct quote | Verbatim, attributed, with context | Customer interview #4, 2026-08-12 |
| Documented fact | A rule, price list, policy or event with a source | Published price page, retrieved date |
| Labeled sample data | Clearly marked "Sample data" on every slide that uses it | Demo board deck |
| Labeled assumption | Stated as an assumption, with its basis, and shown as such on the slide | "Assumes 3% monthly churn (Q3 actual)" |

**Does not count**

- Numbers recalled from memory or "general knowledge" without a source.
- Adjectives in place of measures: "strong growth", "significant demand".
- A source that does not say what you claim (check the exact metric, unit, period).
- Another slide in the same deck that has no source itself.
- An AI-generated summary of a document you have not opened.
- Survey results without sample size and who was asked.

## 2. Evidence tags

Tag every fact in storyline.md. Tags travel with the fact into the slide notes and
the source line.

| Tag | Meaning | Required details |
|---|---|---|
| `[SRC n]` | Sourced; n points to the Sources list | Publisher, title, URL or file, date retrieved, page/table |
| `[USER]` | Given by the user | File name or "brief" |
| `[CALC]` | Derived | Formula and the tags of its inputs |
| `[SAMPLE]` | Sample data, not real | Must also appear as "Sample data" on the slide |
| `[ASSUMPTION]` | A stated assumption | Basis, and which slides depend on it |
| `[HYPOTHESIS]` | A claim to test, no evidence yet | What evidence would confirm or kill it |
| `[DATA NEEDED: …]` | Missing | What, why, likely source, owner if known |

## 3. The evidence ledger

Before writing slides, build a ledger. One row per fact you might use:

| ID | Fact (with unit and period) | Tag | Source / formula | Used on slide |
|---|---|---|---|---|
| E1 | Revenue FY2024: $748.0M | SRC 1 | 10-K FY2024, income statement | 3 |
| E2 | Revenue FY2023: $531.1M | SRC 1 | same | 3 |
| E3 | Revenue growth FY2024: 40.8% | CALC | E1 / E2 − 1 | 1, 3 |
| E4 | Cost per paying subscriber in Indonesia | DATA NEEDED | Run a six-week paid test | 5 |

(Rows are illustrative.)

Then map the ledger onto the slide plan. Any slide with no row is unsupported. Any
row with no slide is unused — drop it or move it to the appendix.

## 4. Marking gaps

Write gaps so that someone can go and fill them:

```
[DATA NEEDED: Q3 logo churn by segment (SMB, mid-market), monthly %, from billing export; owner: RevOps]
```

Format: `[DATA NEEDED: <what> (<breakdown>), <unit>, <period>, from <likely source>; owner: <who>]`.
Keep what you know; mark only what you do not.

Where gaps go:

- **In storyline.md**: on the slide's Evidence and Gaps lines, and in the
  "Open data requests" list at the end.
- **In the ghost deck**: in the slide body placeholder, so the gap is visible
  when the deck is opened.
- **In a title**: only if the claim's number is missing. Prefer a title that states
  what you can prove, and put the gap in the body.

A storyline with gaps is normal and useful. It is a work plan. A storyline with
invented numbers is worse than none.

## 5. Numbers: hygiene rules

1. **Unit, period, scope** on every number: "$748.0M revenue, FY2024 (Jan–Dec),
   consolidated".
2. **Same metric, same definition.** Do not compare GAAP revenue with bookings, or
   calendar year with fiscal year, without saying so.
3. **Comparison base stated.** "Up 41%" — versus what? Prior year, plan, peer?
4. **Show the formula** for every derived number in the ledger. Check sums: parts
   must add to the total (or say why not, e.g., rounding).
5. **Round consistently** and only after calculating. Keep one decimal for
   percentages under 10%, none above, unless precision matters.
6. **Do not extrapolate silently.** A forecast is an assumption; tag it and show the
   method.
7. **Latest vs as-of.** Statistics have a reference year. Write it: "internet users,
   % of population, 2023 (latest available)".
8. **Currency and inflation.** Say nominal or real, and which currency. Convert with a
   cited rate and date.
9. **Percent vs percentage points.** Margin from 20% to 22% is +2 points, not +10%.
10. **Copy numbers exactly** from the source first; round in a later step.

## 6. Sample data

Sample data is allowed for demos, templates and tests. Rules:

- Tag every sample fact `[SAMPLE]` in the ledger.
- Put "Sample data" on every slide that uses it (source line or sticker), and on the
  cover.
- Do not mix sample and real data on one slide.
- Make sample data internally consistent (totals add up, rates match counts), so the
  storyline method can be tested honestly.

## 7. How strong is strong enough

Match evidence strength to the weight a claim carries.

| Claim role | Minimum evidence |
|---|---|
| Governing message | Every key argument supported; at least one quantitative anchor |
| Key argument | Two independent pieces of support, or one decisive one |
| Slide title | The exhibit on that slide proves it |
| Recommendation | Expected effect sized (even roughly, with stated assumptions) plus main risk |
| "Largest / fastest / first" claims | A comparison set and a source covering all members |

If evidence is weaker than the claim, either soften the claim ("early data
suggests") or mark the gap. Do not strengthen the words to cover weak data.

## 8. Checks before hand-off

- [ ] Every number in every title appears in the ledger with a tag.
- [ ] No `[SRC n]` without a matching entry in Sources (URL or file, date).
- [ ] Every `[CALC]` shows its formula; the arithmetic is rechecked.
- [ ] Every sample fact is tagged and the deck carries "Sample data" labels.
- [ ] Every `[DATA NEEDED]` says what, where from, and who.
- [ ] "Largest / fastest / only" claims have a full comparison set.
- [ ] Nothing in the deck came from memory alone.
