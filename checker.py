# checker.py – checks the student's answer with code, not with the model.
#
# Two steps:
#   1. CONTENT: are the words right? (we ignore capitals and punctuation here,
#      and treat "I'm" and "I am" as the same)
#   2. FORM: if the words are right, are the capitals, the end punctuation and
#      the apostrophes right too? (only when the teacher has "strict" switched on)
# If the words are not right, we decide if it is a small SPELLING slip (freindly)
# or a real mistake (like / likes, is / are), which William then explains.
import re

END = (".", "?", "!")
WORD = re.compile(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*|['’][a-z]+")

# ---- contractions: "I'm" = "I am", "don't" = "do not" -------------------------
NOT_FORMS = {"can't": ["can", "not"], "cannot": ["can", "not"], "won't": ["will", "not"]}
PRONOUN_IS = {"he", "she", "it", "that", "what", "there", "where", "who", "here", "how"}
SHORT = {"'m": ["am"], "'re": ["are"], "'s": ["is"], "'ll": ["will"], "'ve": ["have"], "'d": ["would"]}
# the same words written without the apostrophe (a form mistake, not a content mistake)
NO_APOSTROPHE = {
    "im": "I'm", "dont": "don't", "doesnt": "doesn't", "didnt": "didn't", "isnt": "isn't", "arent": "aren't",
    "wasnt": "wasn't", "werent": "weren't", "havent": "haven't", "hasnt": "hasn't", "shouldnt": "shouldn't",
    "mustnt": "mustn't", "couldnt": "couldn't", "wouldnt": "wouldn't", "cant": "can't", "wont": "won't",
    "youre": "you're", "theyre": "they're", "thats": "that's", "whats": "what's", "theres": "there's",
    "ive": "I've", "youve": "you've", "weve": "we've", "theyve": "they've", "youll": "you'll",
    "theyll": "they'll", "hes": "he's", "shes": "she's",
}
# British and American spellings both count
SAME = {"color": "colour", "favorite": "favourite", "yogurt": "yoghurt", "traveled": "travelled",
        "center": "centre", "mom": "mum", "gray": "grey", "theater": "theatre", "meter": "metre"}
NUMBERS = {str(i): w for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
    "sixteen seventeen eighteen nineteen twenty".split())}


def expand(token):
    """One lower-case word -> the words it really means: "don't" -> ["do", "not"]."""
    if token in NOT_FORMS:
        return NOT_FORMS[token]
    if token in SHORT:
        return SHORT[token]
    if token == "let's":
        return ["let", "us"]
    if token.endswith("n't"):
        return [token[:-3], "not"]
    for end, full in (("'m", "am"), ("'re", "are"), ("'ll", "will"), ("'ve", "have"), ("'d", "would")):
        if token.endswith(end):
            return [token[: -len(end)], full]
    if token.endswith("'s") and token[:-2] in PRONOUN_IS:
        return [token[:-2], "is"]
    return [token]


def content(text):
    """The words of an answer, without capitals, punctuation or contractions.
    Returns (words, contractions the student wrote without an apostrophe)."""
    text = text.replace("’", "'").replace("‘", "'").replace("`", "'").lower()
    text = re.sub(r"\b(he|she|it|who|what|there|that)'s got\b", r"\1 has got", text)
    words, missing = [], []
    for token in WORD.findall(text):
        if token in NO_APOSTROPHE:
            missing.append(NO_APOSTROPHE[token])
            token = NO_APOSTROPHE[token].lower()
        for w in expand(token):
            w = SAME.get(w, NUMBERS.get(w, w))
            words.append(w.replace("-", ""))      # t-shirt = tshirt, but we note it below
    return words, missing


# ---- spelling or grammar? ------------------------------------------------------
GROUPS = [{"am", "is", "are", "was", "were", "be"}, {"a", "an", "the"}, {"do", "does", "did"},
          {"have", "has", "had"}, {"this", "that", "these", "those"}, {"much", "many"}, {"some", "any"},
          {"in", "on", "at"}, {"i", "me", "my", "mine"}, {"he", "him", "his"}, {"she", "her", "hers"},
          {"we", "us", "our", "ours"}, {"they", "them", "their", "theirs"}, {"you", "your", "yours"},
          {"it", "its"}, {"more", "most"}, {"than", "then", "as"}, {"must", "should", "can", "will"},
          {"always", "usually", "often", "sometimes", "never"}]


def lev(a, b):
    """How many letters must change to turn a into b."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def stems(w):
    """bigger -> {(bigger, ''), (big, 'er'), (bigg, 'er'), ...}"""
    out = {(w, "")}
    for end in ("iest", "ier", "ies", "ied", "est", "ing", "er", "ed", "es", "ly", "s", "d"):
        if w.endswith(end) and len(w) - len(end) >= 2:
            base = w[: -len(end)]
            out |= {(base, end), (base + "e", end), (base + "y", end)}
            if len(base) > 2 and base[-1] == base[-2]:
                out.add((base[:-1], end))
    return out


def grammar_slip(a, b):
    """like/likes, big/biggest, is/are: the same word in another form = a grammar mistake."""
    if any(a in g and b in g for g in GROUPS):
        return True
    return any(s1 == s2 and e1 != e2 for s1, e1 in stems(a) for s2, e2 in stems(b))


def spelling_slip(a, b):
    if grammar_slip(a, b):
        return False
    limit = 1 if len(b) <= 4 else 2 if len(b) <= 8 else 3
    return 0 < lev(a, b) <= limit


# ---- form: capitals, end punctuation, apostrophes ----------------------------------
def form_issues(answer, target, sentence, blank_at_start=False):
    """What is wrong with the capitals and punctuation, when the words themselves are right."""
    issues, notes = [], []
    a = answer.strip()
    target_words = WORD.findall(target)
    answer_words = WORD.findall(a)

    first = next((c for c in a if c.isalpha()), "")
    target_first = next((c for c in target if c.isalpha()), "")
    if (sentence or blank_at_start) and target_first.isupper() and first.islower():
        issues.append({"code": "start_capital"})
    if any(w == "i" or w.startswith(("i'", "i’")) for w in answer_words):
        issues.append({"code": "i_capital"})
    # names, countries, months, TV ... : every capital letter in the answer key must be there
    lowered = {w.lower(): w for w in answer_words}
    start = 1 if sentence or blank_at_start else 0   # the first word was checked above
    for w in target_words[start:]:
        if w[0].isupper() and w not in ("I",) and not w.startswith("I'"):
            written = lowered.get(w.lower())
            if written and written != w and not (written[0].isupper() and not w.isupper()):
                issues.append({"code": "acronym" if w.isupper() and len(w) > 1 else "proper_capital", "w": w})

    if sentence:
        t_end = target.rstrip()[-1] if target.rstrip().endswith(END) else ""
        a_end = a[-1] if a.endswith(END) else ""
        if t_end == "?" and a_end != "?":
            issues.append({"code": "end_question" if not a_end else "is_question"})
        elif t_end in (".", "!") and not a_end:
            issues.append({"code": "end_dot"})
        elif t_end in (".", "!") and a_end == "?":
            issues.append({"code": "not_question"})
        # commas and punctuation inside the answer: a gentle note, not a mistake
        inner_t = len(re.findall(r"[,.?!]", target.rstrip()[:-1]))
        inner_a = len(re.findall(r"[,.?!]", a[:-1] if a_end else a))
        if inner_a < inner_t:
            notes.append({"code": "inner_punct", "a": target})
    return issues, notes


# ---- the main function ------------------------------------------------------------
def strip_hint(q):
    """'I ___ swim. (moku)' -> 'I ___ swim.'"""
    return q.rsplit(" (", 1)[0] if q.endswith(")") else q


def fill_in(q, answer):
    return strip_hint(q).replace("___", answer, 1)


def expected(item):
    """The correct answer to show the student (a whole sentence for fill-in-the-blank)."""
    if item["type"] == "fill":
        return fill_in(item["q"], item["a"][0])
    return item["a"][0]


def check(item, answer, strict=True):
    """Returns {"result": right | form | spelling | wrong, "expected", "issues", "notes", "word"}."""
    answer = (answer or "").strip()
    out = {"result": "wrong", "expected": expected(item), "issues": [], "notes": [], "word": ""}
    if not answer:
        return out

    # What do we compare with?  (target text, is it a whole sentence?, was the blank at the start?)
    targets = []
    if item["type"] == "fill":
        sentence = strip_hint(item["q"])
        at_start = sentence.startswith("___")
        whole = len(content(answer)[0]) >= max(3, len(content(sentence.replace("___", ""))[0]))
        for a in item["a"]:
            if whole:
                targets.append((fill_in(item["q"], a), True, False, a))
            else:
                targets.append((a, False, at_start, a))
    else:
        for a in item["a"] + item.get("also", []):
            targets.append((a, a.rstrip().endswith(END), False, a))

    words, missing = content(answer)

    # 1. CONTENT: same words as one of the answers?
    for target, sentence, at_start, key in targets:
        if words == content(target)[0]:
            issues, notes = form_issues(answer, target, sentence, at_start) if strict else ([], [])
            if strict and missing:
                issues.append({"code": "apostrophe", "w": ", ".join(dict.fromkeys(missing))})
            if strict and "-" in target and "-" not in answer:      # T-shirt written as tshirt
                notes.append({"code": "hyphen", "a": target})
            if key in item.get("also", []):
                notes.append({"code": "also_right", "a": item["a"][0]})
            out.update(result="form" if issues else "right", issues=issues, notes=notes)
            if not issues and item["type"] == "fill" and not sentence:
                out["expected"] = fill_in(item["q"], key)
            return out

    # 2. Not the same words: a spelling slip, or a real mistake?
    for target, *_ in targets:
        t_words = content(target)[0]
        if len(words) == len(t_words):
            diff = [(a, b) for a, b in zip(words, t_words) if a != b]
            if 0 < len(diff) <= 2 and all(spelling_slip(a, b) for a, b in diff):
                original = {w.lower().replace("-", ""): w for w in WORD.findall(target)}
                out.update(result="spelling", word=", ".join(original.get(b, b) for _, b in diff))
                return out
        if "".join(words) == "".join(t_words):          # "ice hockey" written as "icehockey"
            out.update(result="spelling", word=target)
            return out
    return out
