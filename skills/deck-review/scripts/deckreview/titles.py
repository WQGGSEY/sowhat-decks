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
    "canceled", "praised", "closed", "helps",
    "makes", "takes", "brings", "sees", "says", "tells", "leaves", "finds", "builds",
    "gains", "hits", "misses", "beats", "outruns", "overtakes", "contributes",
    "represents", "generates", "produces", "drove", "absorbs", "erodes", "offsets",
    "eclipses", "doubles", "triples", "halves", "narrows", "widens", "tops",
    "decides", "determines", "dictates", "shapes", "predicts", "signals",
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

# -s forms that are usually plural nouns in titles ("Key accounts", "Price
# changes since 2024"): a verb only when a determiner, number, particle or
# comparative follows ("accounts for 60%", "changes the timeline").
NOUNY_S = {"accounts", "needs", "offers", "supports", "changes", "plans", "uses", "costs",
           "returns", "moves", "shifts"}
VERB_CUE = {
    "the", "a", "an", "our", "its", "their", "his", "her", "my", "your", "this", "these",
    "those", "us", "them", "it", "every", "each", "all", "most", "no", "both", "some",
    "half", "twice", "up", "down", "out", "off", "back", "ahead", "behind", "more", "less",
    "faster", "slower", "higher", "lower", "only", "nearly", "almost", "about",
}
VERB_CUE |= {"two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
             "several", "many", "few", "fewer"}
PHRASAL_NEXT = {"accounts": "for", "needs": "to", "offers": "to"}
# After a singular subject ("The plan needs ...", "Growth needs ...") an -s form
# is a verb unless what follows marks a heading: a preposition such as by/since
# ("Hiring needs by team", "Price changes since 2024") or a heading noun
# ("Customer needs analysis").
NOT_AFTER_NOUNY = {
    "by", "since", "for", "in", "on", "at", "across", "per", "of", "from", "with",
    "between", "among", "during", "after", "before", "under", "over", "within", "vs",
    "vs.", "versus", "and", "or", "&", "nor", "plus",
}
HEADING_NOUNS = {
    "analysis", "overview", "review", "summary", "assessment", "research", "survey",
    "breakdown", "map", "matrix", "mapping", "framework", "list", "table", "chart",
    "roadmap", "timeline", "profile", "segmentation", "update", "status", "report",
    "dashboard", "scorecard", "inventory", "audit",
}
# Plurals used as modifiers ("Sales plan", "Operations review"): a following base
# word is a verb only with a verb cue after it ("Sales grow 20%").
MODIFIER_PLURALS = {
    "sales", "operations", "logistics", "analytics", "economics", "metrics", "earnings",
    "savings", "goods", "services", "systems", "materials", "resources", "relations",
    "payments", "claims", "communications", "finances", "news", "series",
}

# Base forms that count only right after a subject ("Most customers sit ..."),
# never as a first-word imperative ("Fill rate by warehouse" is a label).
BASE_AFTER_SUBJECT = {
    "sit", "cluster", "fill", "stand", "wait", "lag", "hover", "struggle", "outnumber",
    "outpace", "outperform", "spike", "slip", "stall", "account", "tend", "remain", "rise",
    "fall", "scale", "converge", "dominate", "trail", "peak", "rebound", "recover", "stay",
    "sell", "serve", "earn", "generate", "represent", "contribute", "favor", "favour",
    "value", "trust", "ignore", "skip", "abandon", "adopt", "renew", "upgrade", "downgrade",
    "spend", "pay", "buy", "leave", "join", "return", "complain", "ask", "expect", "like",
    "love", "hate", "dislike", "rate", "rank", "score", "share", "face", "lack", "own",
    "turn", "finish", "block", "bring", "meet", "cost", "price", "change",
}
ADVERBS = {"still", "now", "already", "also", "only", "often", "never", "always", "even",
           "just", "again", "mostly", "rarely", "seldom", "generally", "usually",
           "typically", "increasingly", "consistently", "clearly", "steadily", "quickly",
           "slowly", "largely", "mainly", "strongly", "actually", "really"}
PRONOUN_SUBJECTS = {"we", "they", "you", "i"}


def _subject_before(words, i):
    """True if a subject (pronoun or plural noun) ends right before words[i],
    skipping adverbs ("Older customers still prefer")."""
    j = i - 1
    while j >= 0 and words[j] in ADVERBS:
        j -= 1
    if j < 0:
        return False
    p = words[j]
    if p in SUBJECTS or p in PRONOUN_SUBJECTS:
        return True
    if p in ("that", "who", "which") and j > 0:
        # "Accounts that finish onboarding ... churn at ..." is a sentence only
        # because a main verb follows; "Clinics that adopt early" is a segment name.
        return _plural(words[j - 1]) and _later_verb(words, i)
    return _plural(p)


def _later_verb(words, i):
    """A verb candidate after position i that does not follow a determiner."""
    for k in range(i + 1, len(words)):
        w = words[k]
        if words[k - 1] in DETERMINERS:
            continue
        if w in AUX or w in STRONG or w in BASE or w in BASE_AFTER_SUBJECT or w in WEAK_S:
            return True
    return False


TIME_WORDS = {"year", "quarter", "month", "week", "season", "half", "fiscal", "spring",
              "summer", "fall", "autumn", "winter"}


def _verb_cue(w, after=""):
    """A word that shows the word before it is a verb. "this/next/last" before a
    time word ("Product changes this quarter") is a time phrase, not an object."""
    if w in ("this", "next", "last") and after in TIME_WORDS:
        return False
    return w in VERB_CUE or bool(re.fullmatch(r"[$€£¥]?\d[\d.,]*\s?[%x]?", w or "-"))


def _plural(p):
    return (len(p) > 2 and p.endswith("s") and not p.endswith(("ss", "us", "is", "'s"))
            and p not in DETERMINERS)


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
KO_YO_NOUNS = ("개요", "수요", "필요", "중요")
KO_PREDICATE_NOUNS = ("증가", "감소", "성장", "하락", "상승", "확대", "축소", "개선", "악화",
                      "필요", "가능", "회복", "둔화", "급증", "급감", "돌파", "달성", "초과",
                      "미달", "유지", "전환", "앞섬", "뒤처짐")
JA_PREDICATE_NOUNS = ("拡大", "増加", "減少", "成長", "改善", "悪化", "上昇", "低下", "達成",
                      "突破", "縮小", "回復", "鈍化", "急増", "急減", "倍増", "半減")
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
    matches = list(_TOKEN.finditer(t))
    raw = [m.group() for m in matches]
    words = [w.lower().replace("’", "'").rstrip(".,;:") for w in raw]
    # "Market A", "Plan B": a capital letter after a capitalised word is a name,
    # not the article "a".
    names = {i for i in range(1, len(raw)) if len(raw[i]) == 1 and raw[i].isupper()
             and raw[i - 1][:1].isupper()}
    # "Win/loss analysis", "Plan B details", "Churn by cohort": not imperatives.
    no_imperative = bool(matches) and (t[matches[0].end():matches[0].end() + 1] == "/"
                                       or 1 in names or words[-1] in HEADING_NOUNS)
    score = 0.0
    found = []
    n_verbs = 0
    for i, w in enumerate(words):
        if i == 0:
            prev = ""
        elif i - 1 in names:
            prev = "<name>"
        else:
            prev = words[i - 1]
        nxt = words[i + 1] if i + 1 < len(words) else ""
        hit = 0.0
        if w in AUX:
            hit = 2
        elif w in STRONG:
            hit = 2 if (i > 0 or len(words) > 1) else 0
            if prev in ("who", "that", "which") and not _later_verb(words, i):
                hit = 0  # "Customers who churned in Q3": a segment, not a sentence
        elif w in NOUNY_S:
            after = words[i + 2] if i + 2 < len(words) else ""
            singular_subject = (prev and not _plural(prev) and nxt
                                and nxt not in NOT_AFTER_NOUNY and nxt not in HEADING_NOUNS
                                and not re.fullmatch(r"(19|20)\d\d", nxt)
                                and not (nxt in ("this", "next", "last") and after in TIME_WORDS))
            if i > 0 and prev not in DETERMINERS and (
                    _verb_cue(nxt, after)
                    or (PHRASAL_NEXT.get(w) == nxt and re.match(r"[$€£¥]?\d|the$|a$|most$|half$",
                                                                after))
                    or singular_subject):
                hit = 2  # "accounts for 60%", "The plan needs two more engineers"
        elif w in BASE:
            if i == 0 and nxt and nxt not in NOUNISH and len(words) >= 3 \
                    and nxt not in ("by", "per", "vs", "vs.", "versus") and not no_imperative:
                hit = 2  # imperative: "Launch in Vietnam first"
            elif i > 0 and (prev in AUX or _subject_before(words, i)) and (
                    prev not in MODIFIER_PLURALS or _verb_cue(nxt)):
                hit = 2  # "we recommend", "customers (still) want"
        elif w in BASE_AFTER_SUBJECT and i > 0 and nxt not in ("and", "of", "&") \
                and _subject_before(words, i) and (prev not in MODIFIER_PLURALS
                                                   or _verb_cue(nxt)):
            hit = 2  # "Most customers sit in ...", "Competitors cluster at ..."
        elif w in WEAK_S:
            if i > 0 and prev not in DETERMINERS and nxt and nxt not in ("and", "of", "&",
                                                                          "vs", "vs."):
                hit = 1.5
        elif (i > 0 and len(w) > 4 and w.endswith("ed") and w not in ED_ADJECTIVES
              and prev not in DETERMINERS):
            # Past tense right after a subject, with more words after it, is a full
            # verb ("We recommended a ...", "Prices edged up"); a bare trailing
            # participle stays weak ("Lessons learned", "Work completed").
            hit = 2 if nxt and nxt != "by" and _subject_before(words, i) else 1.5
        elif (i > 0 and len(w) > 3 and w.endswith("s") and not w.endswith(("ss", "us", "is",
                                                                            "'s"))
              and prev not in DETERMINERS and
              (nxt in FOLLOW or re.fullmatch(r"[$€£¥]?\d[\d.,]*\s?[%x]|[$€£¥]\d.*", nxt))):
            hit = 1.5  # generic third-person verb: "growth re-accelerates above"
        if hit:
            score += hit
            found.append(w)
            n_verbs += hit >= 1.5
    if words and words[0] in ("how", "why", "where", "who") and (len(words) <= 5 or
                                                                 n_verbs < 2):
        # "How we grew revenue", "Who we are": a heading. "How fast we ship
        # decides renewals" has a second, main verb and stays a claim.
        return {"claim": False, "reason": f"'{words[0]}' heading, not the answer"}
    for i, w in enumerate(words[:-1]):
        if w in ("up", "down") and re.fullmatch(r"[$€£¥]?\d[\d.,]*\s?[%x]?", words[i + 1]) \
                and not re.fullmatch(r"(19|20)\d\d", words[i + 1]):
            score += 1.5  # verbless headline: "Revenue up 20% year on year"
            found.append(f"{w} {words[i + 1]}")
            break
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
    yo_noun = s.endswith(KO_YO_NOUNS)  # 개요, 수요: nouns, not the polite ending 요
    if not yo_noun and (s.endswith(KO_ENDINGS) or
                        s.endswith(tuple(e.rstrip(".") for e in KO_ENDINGS))):
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
    if s.endswith(JA_PREDICATE_NOUNS) and re.search(r"[がは]", s) and len(s) >= 5:
        return {"claim": True, "reason": "noun-ending claim"}
    return {"claim": False, "reason": "ends on a noun; reads like a topic"}


def word_count(title: str) -> int:
    t = title or ""
    if _HANGUL.search(t) or _KANA.search(t) or _CJK.search(t):
        return len(t.split())
    return len(_WORD.findall(t))
