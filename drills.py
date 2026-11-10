# drills.py – makes a round of exercises from the course file.
#
# Exercise types (all checked by checker.py):
#   word       Lithuanian word -> English word            ("katė" -> "cat")
#   phrase     Lithuanian phrase -> English phrase         ("Iš kur tu esi?" -> "Where are you from?")
#   fill       fill in the blank                           ("I ___ swim. (moku)" -> "can")
#   translate  Lithuanian sentence -> English sentence     ("Aš moku šokti." -> "I can dance.")
#   listen     hear English, write it down (dictation)     (the browser reads it aloud)
#   sentence   the student makes their own sentence with the words just practised
#              (the code checks the word is there + capitals/punctuation, William checks the grammar)
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


def word_item(w, index):
    """"How do you say 'katė' in English?" – other English words with the same meaning count too."""
    also = set()
    for part in meaning_parts(w["meaning"]):
        also |= index.get(part, set())
    also.discard(w["text"])
    kind = "phrase" if w["text"].endswith(END) else "word"
    return {"type": kind, "lt": w["meaning"], "a": [w["text"]], "also": sorted(also)}


def grammar_items(lesson, kind):
    return [dict(ex) for g in lesson["grammar"] for ex in g.get("exercises", []) if ex["type"] == kind]


def word_drill(w, item, types):
    """One drill for one word: usually "how do you say …", sometimes a dictation."""
    listen = {"type": "listen", "say": w["text"], "a": [w["text"]]}
    if types.get("listen", True) and (not types.get("word", True) or random.random() < 0.3):
        return listen
    return item if types.get("word", True) else None


def make_round(course, lesson, types, count, extra=None):
    """A round of exercises for one lesson part:
         word, word -> a sentence with them, word, word -> a sentence, ...
         then a few grammar exercises (fill in the gap, translate), then the teacher's focus."""
    index = course.get("_synonyms") or synonym_index(course)   # app.py makes it once at start
    words = [w for w in lesson["words"] if usable(w)]
    single = [w for w in words if not w["text"].endswith(END)]   # words and short phrases
    whole = [w for w in words if w["text"].endswith(END)]        # phrases that are already sentences
    pattern = lesson["grammar"][0]["pattern"] if lesson["grammar"] else ""

    groups = []
    for i in range(0, len(single), 2):
        pair = single[i:i + 2]
        group = [d for d in (word_drill(w, word_item(w, index), types) for w in pair) if d]
        if types.get("sentence", True):
            group.append({"type": "sentence", "words": [w["text"] for w in pair],
                          "meanings": [w["meaning"] for w in pair], "pattern": pattern})
        if group:
            groups.append(group)
    for i in range(0, len(whole), 2):
        group = [d for d in (word_drill(w, word_item(w, index), types) for w in whole[i:i + 2]) if d]
        if group:
            groups.append(group)

    # grammar at the end: 2 fill-in-the-gap + 1 translation, and the teacher's focus exercises
    grammar = []
    if types.get("fill", True):
        grammar += random.sample(grammar_items(lesson, "fill"), min(2, len(grammar_items(lesson, "fill"))))
    if types.get("translate", True):
        grammar += random.sample(grammar_items(lesson, "translate"), min(1, len(grammar_items(lesson, "translate"))))
    grammar += extra or []

    # not more than `count` exercises: drop word groups from the end (always keep at least one)
    while len(groups) > 1 and sum(len(g) for g in groups) + len(grammar) > count:
        groups.pop()
    return [item for g in groups for item in g] + grammar


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
