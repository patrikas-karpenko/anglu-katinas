# drills.py – makes a round of exercises from the course file.
#
# Exercise types (all checked by checker.py):
#   word       Lithuanian word -> English word            ("katė" -> "cat")
#   phrase     Lithuanian phrase -> English phrase         ("Iš kur tu esi?" -> "Where are you from?")
#   fill       fill in the blank                           ("I ___ swim. (moku)" -> "can")
#   translate  Lithuanian sentence -> English sentence     ("Aš moku šokti." -> "I can dance.")
#   listen     hear English, write it down (dictation)     (the browser reads it aloud)
import random
import re

END = (".", "?", "!")


def meaning_parts(meaning):
    """'britas, britiškas' -> {'britas', 'britiškas'}  (brackets removed)"""
    meaning = re.sub(r"\s*\(.*?\)", "", meaning)
    return {p.strip().lower() for p in meaning.split(",") if p.strip()}


def synonym_index(course):
    """Lithuanian meaning -> every English word in the course with that meaning.
    So 'gražus' accepts both 'beautiful' and 'pretty'."""
    index = {}
    for lesson in course["lessons"]:
        for w in lesson["words"]:
            for part in meaning_parts(w["meaning"]):
                index.setdefault(part, set()).add(w["text"])
    return index


def usable(w):
    """Leave out open phrases ('Shall we …?') and pairs that don't match ('my – mine' = 'mano')."""
    if "…" in w["text"]:
        return False
    if " – " in w["text"] and " – " not in w["meaning"]:
        return False
    return True


def word_items(course, lesson):
    index = course.get("_synonyms") or synonym_index(course)   # app.py makes it once at start
    items = []
    for w in lesson["words"]:
        if not usable(w):
            continue
        text = w["text"]
        also = set()
        for part in meaning_parts(w["meaning"]):
            also |= index.get(part, set())
        also.discard(text)
        kind = "phrase" if text.endswith(END) else "word"
        items.append({"type": kind, "lt": w["meaning"], "a": [text], "also": sorted(also)})
    return items


def listen_items(lesson):
    items = [{"type": "listen", "say": w["text"], "a": [w["text"]]} for w in lesson["words"] if usable(w)]
    for g in lesson["grammar"]:
        for ex in g["examples"]:
            items.append({"type": "listen", "say": ex["text"], "a": [ex["text"]]})
    return items


def grammar_items(lesson, kind):
    return [dict(ex) for g in lesson["grammar"] for ex in g.get("exercises", []) if ex["type"] == kind]


# how much of a round each type gets (if it is switched on and the lesson has it)
WEIGHTS = {"word": 3.5, "listen": 1.5, "fill": 4, "translate": 3}
ORDER = ["word", "phrase", "listen", "fill", "translate"]   # easy first, harder later


def make_round(course, lesson, types, count, extra=None):
    """A list of `count` exercises for one lesson. `extra` = exercises William made for the teacher's focus."""
    pools = {
        "word": word_items(course, lesson),
        "listen": listen_items(lesson),
        "fill": grammar_items(lesson, "fill"),
        "translate": grammar_items(lesson, "translate"),
    }
    extra = extra or []
    count = max(1, count - len(extra))
    active = [t for t in pools if types.get(t, True) and pools[t]]
    if not active:                                   # the teacher switched everything off
        active = [t for t in pools if pools[t]]

    # share the round between the types
    total = sum(WEIGHTS[t] for t in active)
    quota = {t: int(count * WEIGHTS[t] / total) for t in active}
    for t in active:                                 # hand out what rounding left over
        if sum(quota.values()) >= count:
            break
        quota[t] += 1

    chosen = []
    for t in active:
        pool = pools[t][:]
        random.shuffle(pool)
        chosen += pool[: quota[t]]
    # if some pools were too small, fill up from the others
    left = [i for t in active for i in pools[t] if i not in chosen]
    random.shuffle(left)
    chosen += left[: count - len(chosen)]
    chosen += extra                                  # the teacher's focus exercises
    chosen.sort(key=lambda i: ORDER.index(i["type"]))
    return chosen


# ---- the teacher's focus: William writes extra exercises --------------------------
FOCUS_PROMPT = """Write {n} short English exercises for a Lithuanian child (A1 level) who is practising: {focus}
Use mostly these words: {words}

Return ONLY JSON like this:
{{"items": [
  {{"type": "fill", "q": "My cat ___ brown. (būti)", "a": ["is"]}},
  {{"type": "translate", "lt": "Mano katė yra ruda.", "a": ["My cat is brown."]}}
]}}

Rules:
- About half "fill" and half "translate".
- fill: one English sentence with ___ where ONE or TWO words are missing, then a hint in brackets
  (the base verb or the Lithuanian word). "a" = the missing word(s), and other correct versions.
- translate: a short Lithuanian sentence; "a" = 1 to 3 correct English translations.
- Every sentence starts with a capital letter and ends with . ? or !
- At most 8 words per sentence. Friendly school topics only."""


def valid_focus_item(it):
    """Only keep exercises William wrote correctly – the code must be able to check them."""
    if not isinstance(it, dict) or not isinstance(it.get("a"), list) or not it["a"]:
        return None
    answers = [str(a).strip() for a in it["a"] if str(a).strip()][:3]
    if not answers or any(len(a) > 80 for a in answers):
        return None
    if it.get("type") == "fill":
        q = str(it.get("q", "")).strip()
        sentence = q.rsplit(" (", 1)[0] if q.endswith(")") else q
        if q.count("___") != 1 or not sentence.endswith(END) or any(len(a.split()) > 3 for a in answers):
            return None
        return {"type": "fill", "q": q, "a": answers, "src": "focus"}
    if it.get("type") == "translate":
        lt = str(it.get("lt", "")).strip()
        if not lt or not all(a[:1].isupper() and a.endswith(END) for a in answers):
            return None
        return {"type": "translate", "lt": lt, "a": answers, "src": "focus"}
    return None
