"""Claim vs topic-label judgement on titles (English, Korean, Japanese)."""

import pytest
from deckreview.titles import classify, is_exempt

CLAIMS = [
    "Revenue grew 18% in Q3, driven by mid-market expansion",
    "Mid-market deals closed 20% faster after the pricing change",
    "Vietnam scores highest on five of seven criteria",
    "Two hires in onboarding would cut early churn by a third",
    "Customers cancel over missing integrations, not price",
    "Launch in Vietnam first and reassess Indonesia after six months",
    "A two-phase launch limits the downside to one market's budget",
    "We recommend moving two sales hires to onboarding",
    "Support tickets doubled after the September release",
    "Each new customer pays back its acquisition cost in 11 months, down from 16",
    "NPS of 42 puts us ahead of the two closest competitors we benchmark",
    "Two incumbents hold most of the market, but neither offers a free tier",
    "Enter Vietnam first",
    "Churn is rising because new SMB accounts never finish setup",
    "3분기 매출은 계획을 6% 넘었지만 SMB 이탈이 연말 ARR을 위협한다",
    "주요 경쟁사 두 곳 모두 무료 요금제가 없다",
    "매출 30% 성장",
    "ベトナムの25歳未満のオンライン人口は候補4か国で最も多い",
    "A one-time $257M tax benefit makes up most of 2025's $414M net income",
    "Judge 2026 by whether DAU growth re-accelerates above 2025's 30%, not by bookings growth",
    "Duolingo is trading 2026 bookings growth for user growth, so judge 2026 by DAUs",
]

LABELS = [
    "Market Overview",
    "Customer feedback",
    "Ticket volume",
    "Competitive landscape",
    "Rising costs",
    "Costs and benefits",
    "Product launch timeline",
    "Revenue growth in 2025",
    "Why is churn rising?",
    "Key findings:",
    "Pricing analysis",
    "3분기 실적",
    "비용 절감 방안 검토",
    "市場概要",
    "第3四半期の結果",
    "Key trends in Asian retail markets 2025",
    "성장은 어디서 왔나",
    "내년 성장은 어디서 오는가",
    "왜 이탈이 늘었나?",
    "なぜ解約が増えたのか",
]


@pytest.mark.parametrize("title", CLAIMS)
def test_claims_are_recognised(title):
    assert classify(title)["claim"], classify(title)


@pytest.mark.parametrize("title", LABELS)
def test_topic_labels_are_flagged(title):
    assert not classify(title)["claim"], classify(title)


@pytest.mark.parametrize("title", ["Agenda", "Appendix", "Q&A", "Thank you", "목차", "부록"])
def test_agenda_appendix_and_closing_titles_are_exempt(title):
    assert is_exempt(title)
