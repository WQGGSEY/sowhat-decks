"""Is a slide title a claim (a sentence with a verb) or a topic label?

A dictionary-free heuristic for English, Korean and Japanese. It is tuned to
miss few labels; borderline titles go to the rubric review, where the agent
judges them.
"""

from __future__ import annotations

import re

# Titles that may stay labels (cover, agenda, appendix, closing).
EXEMPT = re.compile(
    r"^\s*(agenda|contents|table of contents|appendix|appendices|backup|q\s*&\s*a|"
    r"questions\??|thank you!?|thanks!?|contact( us)?|disclaimer|목차|부록|감사합니다\.?|"
    r"질의\s*응답|q&a|目次|付録|ご清聴ありがとうございました)\s*$", re.IGNORECASE)

# Common topic labels: a title equal to one of these is never a claim.
LABELS = {
    "overview", "market overview", "background", "introduction", "summary",
    "executive summary", "next steps", "conclusion", "conclusions", "recommendation",
    "recommendations", "financials", "financial summary", "team", "timeline", "roadmap",
    "market analysis", "competitive landscape", "competition", "key findings", "findings",
    "results", "methodology", "approach", "objectives", "goals", "risks", "options",
    "discussion", "situation", "context", "problem", "solution", "pricing", "strategy",
    "customer feedback", "market", "products", "status", "update", "kpis", "metrics",
}

AUX = {
    "is", "are", "was", "were", "be", "been", "am", "will", "would", "can", "could",
    "should", "must", "may", "might", "shall", "has", "have", "had", "does", "do", "did",
    "isn't", "aren't", "wasn't", "weren't", "won't", "can't", "cannot", "doesn't",
    "don't", "didn't", "hasn't", "haven't", "shouldn't", "it's", "we're", "they're",
    "there's", "we'll", "we've",
}

# Inflected verb forms that are rarely nouns in a title.
STRONG = {
    "grew", "rose", "fell", "drove", "led", "beat", "won", "lost", "took", "made", "became",
    "came", "went", "gave", "saw", "held", "kept", "overtook", "shrank", "sank", "began",
    "brought", "bought", "sold", "paid", "spent", "met", "outpaced", "outperformed",
    "outperforms", "outpaces", "doubled", "tripled", "halved", "remains", "remained",
    "outweighs", "exceeds", "exceeded", "lags", "lagged", "trails", "trailed",
    "recommends", "proposes", "suggests", "requires", "enables", "delivers", "reached",
    "reaches", "grows", "declined", "increased", "decreased", "improves", "improved",
    "reduces", "reduced", "showed", "shown", "pays", "saves", "beats", "loses",
    "creates", "allows", "lowers", "explains", "indicates", "depends", "relies",
    "fails", "stays", "keeps", "becomes", "gets", "gives", "expands", "accelerates",
    "dominates", "differs", "varies", "justifies", "outgrows", "outsells", "prefers",
    "wants", "spends", "scored", "ranked", "turned", "stood", "churned", "cancelled",
    "canceled", "praised", "closed", "offers", "needs", "helps", "supports",
    "makes", "takes", "brings", "sees", "says", "tells", "leaves", "finds", "builds",
    "gains", "hits", "misses", "beats", "outruns", "overtakes", "accounts", "contributes",
    "represents", "generates", "produces", "drove", "absorbs", "erodes", "offsets",
    "eclipses", "doubles", "triples", "halves", "narrows", "widens", "tops",
}

# Words that often follow a verb, rarely a plural noun: "makes up", "grows above".
FOLLOW = {
    "the", "a", "an", "our", "its", "their", "his", "her", "my", "your", "this", "that",
    "these", "those", "by", "to", "from", "above", "below", "over", "under", "more", "less",
    "most", "all", "every", "each", "no", "only", "about", "nearly", "almost", "at", "as",
    "up", "down", "out", "off", "into", "ahead", "behind", "half", "twice", "faster",
    "slower", "higher", "lower", "further", "much", "us", "them", "it", "well", "again",
    "still", "even", "back", "away",
}

# Ambiguous -s forms (also plural nouns): count only inside a sentence.
WEAK_S = {
    "costs", "means", "works", "holds", "sets", "puts", "runs", "shows", "returns",
    "shifts", "moves", "scores", "ranks", "covers", "limits", "closes", "turns", "stands",
    "wins", "leads", "drives", "falls", "rises", "declines", "increases", "decreases",
    "peaks", "stalls", "slows", "recovers", "rebounds", "matters", "concentrates",
    "launches", "cuts", "changes", "plans", "uses", "raises", "adds", "comes", "goes",
}

# Base forms: verbs after a subject ("we recommend", "customers want") or as an
# imperative first word ("Launch in Vietnam first").
BASE = {
    "launch", "enter", "invest", "partner", "hire", "fund", "approve", "stop", "start",
    "focus", "prioritize", "prioritise", "build", "buy", "sell", "keep", "shift", "move",
    "cut", "cancel", "use", "limit", "close", "cover", "recommend", "propose", "suggest",
    "require", "enable", "deliver", "lead", "want", "prefer", "spend", "praise", "churn",
    "concentrate", "differ", "vary", "outgrow", "outsell", "justify", "outweigh", "hold",
    "need", "grow", "drive", "make", "take", "pay", "save", "beat", "win", "lose",
    "expect", "plan", "reach", "exceed", "double", "cancel", "switch", "choose", "ask",
    "pick", "delay", "defer", "expand", "reduce", "increase", "decrease", "raise",
    "lower", "add", "drop", "keep", "replace", "pause", "accept", "reject", "sign",
    "renew", "restructure", "consolidate", "migrate", "adopt", "test", "pilot", "ship",
    "decide", "agree", "spend", "rely", "depend", "see", "say", "tell", "show", "prove",
    "judge", "measure", "track", "watch", "treat", "assume", "target", "commit", "avoid",
}
SUBJECTS = {"we", "they", "you", "i", "users", "customers", "buyers", "teams", "most",
            "both", "all", "few", "many", "competitors", "incumbents", "people"}
NOUNISH = {"plan", "plans", "timeline", "strategy", "and", "of", "options", "overview",
           "roadmap", "status", "update", "review", "analysis", "results", "metrics",
           "summary", "readiness", "checklist", "budget", "team", "costs", "&"}

DETERMINERS = {
    "the", "a", "an", "our", "its", "their", "his", "her", "my", "your", "this", "that",
    "these", "those", "of", "for", "with", "in", "on", "by", "and", "or", "to", "from",
    "at", "as", "vs", "vs.", "versus", "key", "new", "next",
}
ED_ADJECTIVES = {
    "proposed", "selected", "detailed", "advanced", "limited", "united", "related",
    "based", "integrated", "automated", "targeted", "expected", "estimated", "projected",
    "planned", "combined", "consolidated", "adjusted", "audited", "unaudited",
    "hundred", "seed", "speed", "need", "feed", "shed", "bed", "red",
}

KO_ENDINGS = ("다", "다.", "요", "함", "음", "임", "됨", "짐", "냄", "봄", "옴", "남",
              "줌", "듦", "앎", "삼", "음.", "함.", "됨.")
KO_PREDICATE_NOUNS = ("증가", "감소", "성장", "하락", "상승", "확대", "축소", "개선", "악화",
                      "필요", "가능", "회복", "둔화", "급증", "급감", "돌파", "달성", "초과",
                      "미달", "유지", "전환", "앞섬", "뒤처짐")
JA_ENDINGS = ("る", "た", "だ", "い", "す", "ない", "ある", "した", "です", "ます", "った",
              "える", "げる", "せる", "れる", "ぐ", "む", "ぶ", "つ", "く", "う")

_WORD = re.compile(r"[A-Za-z][A-Za-z'’\-]*")
_TOKEN = re.compile(r"[A-Za-z0-9$€£¥%][\w'’\-.%$]*")
_HANGUL = re.compile(r"[가-힣]")
_KANA = re.compile(r"[぀-ヿ]")
_CJK = re.compile(r"[一-鿿]")


def is_exempt(title: str) -> bool:
    return bool(EXEMPT.match(title or ""))


def classify(title: str) -> dict:
    """Return {"claim": bool, "reason": str} for one title."""
    t = (title or "").strip()
    if not t:
        return {"claim": False, "reason": "empty title"}
    if _HANGUL.search(t):
        return _classify_ko(t)
    if _KANA.search(t) or (_CJK.search(t) and not _WORD.search(t)):
        return _classify_ja(t)
    return _classify_en(t)


def _classify_en(t: str) -> dict:
    norm = re.sub(r"[^\w\s&'’-]", "", t.lower()).strip()
    if norm in LABELS:
        return {"claim": False, "reason": "common topic label"}
    if t.endswith("?"):
        return {"claim": False, "reason": "question, not an answer"}
    if t.rstrip().endswith(":"):
        return {"claim": False, "reason": "ends with a colon (a label)"}
    words = [w.lower().replace("’", "'").rstrip(".,;:") for w in _TOKEN.findall(t)]
    score = 0.0
    found = []
    for i, w in enumerate(words):
        prev = words[i - 1] if i else ""
        nxt = words[i + 1] if i + 1 < len(words) else ""
        hit = 0.0
        if w in AUX:
            hit = 2
        elif w in STRONG:
            hit = 2 if (i > 0 or len(words) > 1) else 0
        elif w in BASE:
            if i == 0 and nxt and nxt not in NOUNISH and len(words) >= 3:
                hit = 2  # imperative: "Launch in Vietnam first"
            elif i > 0 and (prev in SUBJECTS or prev in AUX or
                            (prev.endswith("s") and prev not in DETERMINERS
                             and not prev.endswith("ss"))):
                hit = 2  # "we recommend", "customers want"
        elif w in WEAK_S:
            if i > 0 and prev not in DETERMINERS and nxt and nxt not in ("and", "of", "&",
                                                                          "vs", "vs."):
                hit = 1.5
        elif (i > 0 and len(w) > 4 and w.endswith("ed") and w not in ED_ADJECTIVES
              and prev not in DETERMINERS):
            hit = 1.5
        elif (i > 0 and len(w) > 3 and w.endswith("s") and not w.endswith(("ss", "us", "is",
                                                                            "'s"))
              and prev not in DETERMINERS and
              (nxt in FOLLOW or re.fullmatch(r"[$€£¥]?\d[\d.,]*\s?[%x]|[$€£¥]\d.*", nxt))):
            hit = 1.5  # generic third-person verb: "growth re-accelerates above"
        if hit:
            score += hit
            found.append(w)
    if len(words) >= 9:
        score += 1.0  # labels are rarely this long
    elif len(words) >= 7:
        score += 0.5
    if re.search(r"\d", t) and len(words) >= 4:
        score += 0.5
    if score >= 2:
        return {"claim": True, "reason": f"verb: {', '.join(found[:3])}" if found
                else "long sentence"}
    if len(words) <= 3:
        return {"claim": False, "reason": f"{len(words)} words, no verb"}
    return {"claim": False, "reason": "no verb found; reads like a topic"}


KO_QUESTION_WORDS = re.compile(r"어디|무엇|뭐|왜|어떻게|언제|누가|누구|얼마|어느|어떤")
KO_QUESTION_ENDINGS = ("까", "나", "가", "니", "냐", "는가", "을까", "ㄹ까")


def _classify_ko(t: str) -> dict:
    s = t.strip().rstrip(".!。 ")
    if is_exempt(s):
        return {"claim": False, "reason": "label"}
    if s.endswith("?") or (KO_QUESTION_WORDS.search(s) and s.endswith(KO_QUESTION_ENDINGS)):
        return {"claim": False, "reason": "question, not an answer"}
    eojeol = s.split()
    if s.endswith(KO_ENDINGS) or s.endswith(tuple(e.rstrip(".") for e in KO_ENDINGS)):
        return {"claim": True, "reason": "ends with a predicate"}
    if len(eojeol) >= 3 and any(n in s for n in KO_PREDICATE_NOUNS):
        return {"claim": True, "reason": "noun-ending claim"}
    if len(eojeol) >= 3 and re.search(r"\d", s):
        return {"claim": True, "reason": "noun-ending claim with a number"}
    return {"claim": False, "reason": "no predicate; reads like a topic"}


def _classify_ja(t: str) -> dict:
    s = t.strip().rstrip("。.!！ ")
    if s.endswith(("?", "？", "か", "のか")):
        return {"claim": False, "reason": "question, not an answer"}
    if s.endswith(JA_ENDINGS) and len(s) >= 6:
        return {"claim": True, "reason": "ends with a predicate"}
    if len(s) >= 12 and re.search(r"\d", s):
        return {"claim": True, "reason": "claim with a number"}
    return {"claim": False, "reason": "ends on a noun; reads like a topic"}


def word_count(title: str) -> int:
    t = title or ""
    if _HANGUL.search(t) or _KANA.search(t) or _CJK.search(t):
        return len(t.split())
    return len(_WORD.findall(t))
