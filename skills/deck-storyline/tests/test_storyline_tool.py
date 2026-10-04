"""Tests for deck-storyline/scripts/storyline_tool.py (stdlib only; deck-build validator used when present)."""
import json
import pathlib
import sys

import pytest

SKILL = pathlib.Path(__file__).resolve().parents[1]
REPO = SKILL.parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

import storyline_tool as st  # noqa: E402

EXAMPLES = sorted((REPO / "examples" / "storyline-tests").glob("0*/storyline.md"))


def _slide(title, role="evidence", evidence="E1", gaps="none"):
    return st.Slide(num=3, title=title, fields={"role": role, "evidence": evidence, "gaps": gaps})


def _levels(issues):
    return [lvl for lvl, _ in issues]


def _write(tmp_path, text):
    p = tmp_path / "storyline.md"
    p.write_text(text, encoding="utf-8")
    return p


MINI = """# Storyline: Test deck

## 0. Brief
- Purpose: get a decision
- Audience: board
- Decision: Approve the plan?
- Deck type: board update
- Date: 2026-10-04
- Language: en
- Data status: sample

## 1. Governing message
> Approve the plan because churn fell and cash lasts two years.

## 2. SCQA
- Situation: We have a plan.
- Complication: Churn changed.
- Question: Approve?
- Answer: Approve the plan because churn fell and cash lasts two years.

## 3. Key arguments
- Split: results / risk / ask
- Order: importance

1. Churn fell by half after the onboarding fix — answers: "Is it working?"
2. Cash lasts two years at the current burn — answers: "Can we afford it?"
3. The plan needs one decision today — answers: "What do you need?"

## 4. Slide plan

### 1. Test deck
- Role: cover
- Layout: cover
- Evidence: none
- Gaps: none

### 2. Approve the plan because churn fell and cash lasts two years
- Role: summary
- Argument: 0
- Layout: executive_summary
- Evidence: E1, E2
- Gaps: none

### 3. Churn fell by half after the onboarding fix
- Role: evidence
- Argument: 1
- Layout: exhibit
- Exhibit: bar — churn by month
- Evidence: E1
- Gaps: none

### 4. Cash lasts two years at the current burn
- Role: evidence
- Argument: 2
- Layout: exhibit
- Exhibit: table — cash, burn
- Evidence: E2
- Gaps: [DATA NEEDED: Q4 burn forecast, $k/month, from Finance; owner: CFO]

### 5. We ask the board to approve the plan today
- Role: next-steps
- Argument: 3
- Layout: recommendations
- Evidence: E1
- Gaps: none

## 5. Title-only test
Overall: PASS — test

## 6. Evidence ledger
| ID | Fact | Tag | Source / formula | Slides |
|---|---|---|---|---|
| E1 | Churn 4% -> 2% | SAMPLE | metrics.csv | 3 |
| E2 | Runway 24 months | CALC | 12,000 / 500 = 24 | 4 |

## 7. Open data requests
- [DATA NEEDED: Q4 burn forecast, $k/month, from Finance; owner: CFO] — slide 4

## 8. Sources
1. Sample data, metrics.csv.
"""


# --------------------------------------------------------------------- title lint

@pytest.mark.parametrize("title", ["Market overview", "Financial summary", "Next steps", "Risks"])
def test_topic_labels_are_errors(title):
    assert "error" in _levels(st.lint_title(_slide(title), 10))


def test_question_title_is_error():
    assert "error" in _levels(st.lint_title(_slide("Why is churn rising so fast this year?"), 10))


def test_claim_title_passes():
    assert st.lint_title(_slide("SMB churn doubled in Q3 because new accounts never finish setup"), 10) == []


def test_noun_phrase_without_verb_warns():
    issues = st.lint_title(_slide("Customer churn analysis by segment and region"), 10)
    assert "warn" in _levels(issues)


def test_number_without_evidence_is_error():
    issues = st.lint_title(_slide("Revenue grew 41% to $748M last year", evidence="none"), 10)
    assert any("number" in m for _, m in issues if _ == "error") or "error" in _levels(issues)


def test_years_and_quarters_are_not_number_claims():
    assert not st._has_number_claim("Churn rose in Q3 2026 and FY2025")
    assert st._has_number_claim("Churn rose to 3.1% in Q3")


def test_data_needed_in_title_warns_not_errors():
    issues = st.lint_title(_slide("Payback fell to [DATA NEEDED: months] after the price change", evidence="none"), 10)
    assert _levels(issues) == ["warn"]


def test_too_long_title_is_error():
    long = "Revenue grew " + "and margins improved strongly across every segment " * 4
    assert "error" in _levels(st.lint_title(_slide(long), 10))


def test_hedges_warn():
    issues = st.lint_title(_slide("The new feature could possibly help retention a lot"), 10)
    assert any("hedging" in m for _, m in issues)


def test_korean_claim_and_label():
    assert st.lint_title(_slide("인도네시아의 인터넷 이용자는 후보 4개국 중 가장 많다", evidence="E1"), 10) == []
    assert "warn" in _levels(st.lint_title(_slide("인도네시아 시장 현황 및 경쟁 구도 분석"), 10))


def test_japanese_claim():
    assert st.lint_title(_slide("第3四半期の売上は計画を6%上回った", evidence="E1"), 10) == []


def test_cover_and_appendix_are_not_claim_checked():
    assert st.lint_title(_slide("Q3 board update", role="cover"), 10) == []
    assert st.lint_title(_slide("Key figures", role="appendix"), 10) == []


# --------------------------------------------------------------------- parse / check / ghost

def test_parse_mini(tmp_path):
    s = st.parse(_write(tmp_path, MINI))
    assert s.deck_name == "Test deck"
    assert s.governing.startswith("Approve the plan")
    assert len(s.arguments) == 3 and s.arguments[0].startswith("Churn fell by half")
    assert [x.num for x in s.slides] == [1, 2, 3, 4, 5]
    assert set(s.ledger) == {"E1", "E2"}
    assert s.sources == {"1": "Sample data, metrics.csv."}


def test_check_mini_passes(tmp_path, capsys):
    assert st.run_check(st.parse(_write(tmp_path, MINI))) == 0
    assert "[DATA NEEDED]: 1" in capsys.readouterr().out


def test_check_catches_missing_ledger_id(tmp_path):
    bad = MINI.replace("- Evidence: E2\n- Gaps: [DATA", "- Evidence: E9\n- Gaps: [DATA")
    assert st.run_check(st.parse(_write(tmp_path, bad))) == 1


def test_check_catches_unresolved_source(tmp_path):
    bad = MINI.replace("| E1 | Churn 4% -> 2% | SAMPLE |", "| E1 | Churn 4% -> 2% | SRC 7 |")
    assert st.run_check(st.parse(_write(tmp_path, bad))) == 1


def test_template_fails_check():
    assert st.run_check(st.parse(SKILL / "templates" / "storyline.md")) == 1


def test_ghost_spec_shape(tmp_path):
    spec, warnings = st.build_ghost(st.parse(_write(tmp_path, MINI)))
    assert spec["spec_version"] == "1.0" and "mode" not in spec
    assert spec["meta"]["sample_data"] is True and spec["meta"]["draft"] is True
    layouts = [s["layout"] for s in spec["slides"]]
    assert layouts == ["cover", "executive_summary", "ghost", "ghost", "ghost"]
    assert spec["slides"][1]["points"][0].startswith("Churn fell by half")
    gap = spec["slides"][3]["ghost"]["evidence"]
    assert any(e.startswith("[DATA NEEDED]") for e in gap)
    assert warnings == []


def test_ghost_pure_has_no_summary_points(tmp_path):
    spec, _ = st.build_ghost(st.parse(_write(tmp_path, MINI)), pure=True)
    assert spec["mode"] == "ghost"
    assert spec["slides"][1]["layout"] == "ghost"


def test_ghost_never_adds_numbers(tmp_path):
    """Every digit in the ghost spec must already appear in storyline.md."""
    import re
    text = MINI
    spec, _ = st.build_ghost(st.parse(_write(tmp_path, text)))
    spec.pop("spec_version")
    for s in spec["slides"]:
        s.pop("id", None)
        s.pop("number", None)
    for num in re.findall(r"\d[\d,.]*", json.dumps(spec, ensure_ascii=False)):
        assert num.rstrip(".,") in text


def _deckkit_validate():
    scripts = REPO / "skills" / "deck-build" / "scripts"
    if not (scripts / "deckkit" / "spec.py").exists():
        return None
    sys.path.insert(0, str(scripts))
    from deckkit import spec as dk_spec  # type: ignore
    return dk_spec.validate


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.parent.name)
def test_examples_pass_and_ghosts_validate(path, capsys):
    s = st.parse(path)
    assert st.run_check(s) == 0
    spec, _ = st.build_ghost(s)
    validate = _deckkit_validate()
    if validate is None:
        pytest.skip("deck-build not installed next to this skill")
    assert validate(spec) == []


CONTROL = REPO / "examples" / "storyline-tests" / "control-topic-titles" / "storyline.md"


@pytest.mark.skipif(not CONTROL.exists(), reason="negative control not present")
def test_topic_title_control_fails(capsys):
    s = st.parse(CONTROL)
    assert st.run_titles(s) == 1
    flagged = [x for x in s.slides if x.role not in st.NO_CLAIM_ROLES and st.lint_title(x, len(s.slides))]
    claim_slides = [x for x in s.slides if x.role not in st.NO_CLAIM_ROLES]
    assert len(flagged) == len(claim_slides)  # every topic label is caught (error or warning)
