"""Answer checking. Forgiving about capitals, punctuation, missing apostrophes
and contractions; strict about the actual grammar point."""
import random
import re

CONTRACTIONS = [
    (r"\bcan't\b", "cannot"), (r"\bcan not\b", "cannot"), (r"\bwon't\b", "will not"),
    (r"\bmustn't\b", "must not"), (r"n't\b", " not"), (r"\bi'm\b", "i am"), (r"'re\b", " are"),
    (r"'ll\b", " will"), (r"'ve\b", " have"),
]

DONT_KNOW = {"nezinau", "nežinau", "?", "??", "nzn", "i don't know", "i dont know", "idk",
             "dont know", "don't know", "praleisti", "skip", "-"}

LETTERS = "abcd"


def norm(s):
    s = (s or "").lower().strip()
    for a, b in (("’", "'"), ("‘", "'"), ("`", "'"), ("´", "'")):
        s = s.replace(a, b)
    s = re.sub(r"[^\w\s']", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    for pat, rep in CONTRACTIONS:
        s = re.sub(pat, rep, s)
    return re.sub(r"\s+", " ", s).strip()


def lev(a, b):
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def prepare(item):
    """Copy an exercise and add what the screen needs (shuffled word order)."""
    it = dict(item)
    if it["type"] == "order":
        words = it["q"].split()
        shuffled = words[:]
        for _ in range(20):
            random.shuffle(shuffled)
            if shuffled != words:
                break
        it["display"] = " / ".join(shuffled)
    return it


def correct_text(it):
    """The full correct answer, nicely written, to show the student."""
    a = it["a"][0]
    if it["type"] == "fill":
        q = it["q"].split(" (")[0] if it["q"].endswith(")") else it["q"]
        i = q.index("___")
        before = q[:i].rstrip()
        if not before or before.endswith((".", "!", "?")):
            a = a[0].upper() + a[1:]
        return q.replace("___", a, 1)
    if it["type"] == "order":
        return a + ("?" if a.split()[0] in ("Do", "Does", "Did", "Can", "Is", "Are", "Have", "Will") else ".")
    if it["type"] == "translate" and it.get("topic", "").endswith("days"):
        return a.capitalize()
    return a


def student_full(it, ans):
    """If the student typed the whole sentence for a fill item, cut the gap out."""
    if it["type"] != "fill":
        return ans
    q = it["q"].split(" (")[0] if it["q"].endswith(")") else it["q"]
    pre, post = q.split("___", 1)
    n, p1, p2 = norm(ans), norm(pre), norm(post)
    if p1 and n.startswith(p1 + " ") and (not p2 or n.endswith(" " + p2)):
        mid = n[len(p1):]
        if p2:
            mid = mid[: len(mid) - len(p2)]
        return mid.strip()
    if not p1 and p2 and n.endswith(" " + p2):
        return n[: len(n) - len(p2)].strip()
    return ans


def check(it, ans):
    """Returns (verdict, tip). verdict: ok | near | wrong | dontknow."""
    raw = (ans or "").strip()
    if norm(raw) in DONT_KNOW or raw.lower() in DONT_KNOW:
        return "dontknow", None

    answers = [norm(a) for a in it["a"]]
    if it["type"] == "choose":
        r = norm(raw).rstrip(")")
        if len(r) == 1 and r in LETTERS[: len(it["opts"])]:
            raw = it["opts"][LETTERS.index(r)]
        elif r.isdigit() and 1 <= int(r) <= len(it["opts"]):
            raw = it["opts"][int(r) - 1]

    raw = student_full(it, raw)
    n = norm(raw)
    if n in answers:
        return "ok", None

    flat = _flat(raw)
    for a in it["a"]:
        if _flat(a) == flat:
            return "ok", f"Nepamiršk apostrofo: {a}"

    if it["type"] in ("fill", "translate", "order"):
        for a in answers:
            limit = 2 if len(a) >= 5 else (1 if len(a) >= 3 else 0)
            # only a spelling slip if it's not just another option/word form
            if 0 < lev(n, a) <= limit and not _is_grammar_slip(n, a):
                return "near", None
    return "wrong", None


def _flat(s):
    s = (s or "").lower().replace("’", "'").replace("'", "")
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s)).strip()


def _stems(w):
    """Possible (stem, ending) splits of a word: bigger -> (big, er), (bigg, er) ..."""
    out = {(w, "")}
    for end in ("est", "ing", "er", "ed", "es", "s", "d"):
        if w.endswith(end) and len(w) - len(end) >= 2:
            base = w[: -len(end)]
            out |= {(base, end), (base + "e", end)}
            if len(base) > 2 and base[-1] == base[-2]:
                out.add((base[:-1], end))
    return out


def _is_grammar_slip(n, a):
    """like/likes, bigger/biggest, run/running are grammar mistakes, not spelling slips
    (same word, different ending). biger/bigger is a spelling slip (same ending)."""
    if {n, a} in ({"is", "as"}, {"an", "a"}, {"was", "were"}):
        return True
    return any(s1 == s2 and e1 != e2 for s1, e1 in _stems(n) for s2, e2 in _stems(a))
